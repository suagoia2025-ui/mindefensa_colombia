"""
Pipeline ETL principal - Orquestación de extracción, transformación y carga.
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

from src.etl.config import load_etl_config
from src.etl.extractors import extract_all_files
from src.etl.loaders import save_etl_log, save_maestro_parquet
from src.etl.transformers import transform_dataframe

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_pipeline(
    project_root: Path | None = None,
    config_path: Path | None = None,
) -> dict[str, Any]:
    """
    Ejecuta el pipeline ETL completo.

    Args:
        project_root: Raíz del proyecto. Si None, usa directorio actual.
        config_path: Ruta a config/etl.yaml. Si None, usa la por defecto.

    Returns:
        Diccionario con resumen de la ejecución
    """
    start_time = datetime.now()

    if project_root is None:
        project_root = Path.cwd()

    config = load_etl_config(config_path)
    input_base = project_root / config["input"]["base_path"]
    output_base = project_root / config["output"]["base_path"]
    maestro_file = output_base / config["output"]["maestro_file"]
    log_file = output_base / config["output"]["log_file"]
    exclude_files = config.get("exclude_files", [])

    if isinstance(exclude_files, list):
        exclude_files = set(exclude_files)

    logger.info("Iniciando pipeline ETL")
    logger.info("Origen: %s", input_base)
    logger.info("Destino: %s", maestro_file)

    if not input_base.exists():
        raise FileNotFoundError(f"Directorio de entrada no existe: {input_base}")

    # Extracción
    logger.info("Fase 1: Extracción")
    extracted = extract_all_files(
        base_path=input_base,
        exclude_files=exclude_files,
        extensions=config["input"].get("extensions", [".xlsx"]),
    )

    if not extracted:
        logger.warning("No se encontraron archivos para procesar")
        return {
            "status": "warning",
            "message": "Sin archivos procesados",
            "files_processed": 0,
            "total_records": 0,
            "duration_seconds": (datetime.now() - start_time).total_seconds(),
        }

    # Transformación
    logger.info("Fase 2: Transformación")
    all_dfs: list[Any] = []
    records_per_file: dict[str, int] = {}

    for tipo_evento, df in extracted:
        try:
            transformed = transform_dataframe(df, config)
            if len(transformed) > 0:
                all_dfs.append(transformed)
                records_per_file[tipo_evento] = len(transformed)
        except Exception as e:
            logger.error("Error transformando %s: %s", tipo_evento, e)

    if not all_dfs:
        logger.error("No quedaron registros válidos después de la transformación")
        return {
            "status": "error",
            "message": "Transformación fallida",
            "files_processed": len(extracted),
            "total_records": 0,
            "duration_seconds": (datetime.now() - start_time).total_seconds(),
        }

    # Consolidación
    logger.info("Fase 3: Consolidación")
    maestro_df = pd.concat(all_dfs, ignore_index=True)

    total_records = len(maestro_df)

    # Carga
    logger.info("Fase 4: Carga")
    output_path = save_maestro_parquet(maestro_df, maestro_file)

    # Log
    duration = (datetime.now() - start_time).total_seconds()
    summary = {
        "timestamp": start_time.isoformat(),
        "status": "success",
        "files_processed": len(all_dfs),
        "total_records": total_records,
        "output_file": str(output_path),
        "duration_seconds": round(duration, 2),
        "records_per_event_type": records_per_file,
    }

    save_etl_log(log_file, summary)
    logger.info("Pipeline completado: %d registros en %s", total_records, output_path)

    return summary
