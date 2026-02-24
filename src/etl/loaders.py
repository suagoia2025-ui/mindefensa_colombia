"""
Loaders - Escritura del dataset maestro en Parquet.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def ensure_correct_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Asegura tipos de datos correctos para Parquet."""
    df = df.copy()

    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"]).dt.date

    if "cod_depto" in df.columns:
        df["cod_depto"] = df["cod_depto"].astype("string")

    if "cod_muni" in df.columns:
        df["cod_muni"] = df["cod_muni"].astype("string")

    if "departamento" in df.columns:
        df["departamento"] = df["departamento"].astype("string")

    if "municipio" in df.columns:
        df["municipio"] = df["municipio"].astype("string")

    if "tipo_evento" in df.columns:
        df["tipo_evento"] = df["tipo_evento"].astype("string")

    if "cantidad" in df.columns:
        df["cantidad"] = df["cantidad"].astype("int32")

    if "ano" in df.columns:
        df["ano"] = df["ano"].astype("int16")

    if "mes" in df.columns:
        df["mes"] = df["mes"].astype("int8")

    if "archivo_origen" in df.columns:
        df["archivo_origen"] = df["archivo_origen"].astype("string")

    return df


def _has_parquet_engine() -> bool:
    """Verifica si hay motor Parquet disponible (pyarrow o fastparquet)."""
    try:
        import pyarrow  # noqa: F401
        return True
    except ImportError:
        try:
            import fastparquet  # noqa: F401
            return True
        except ImportError:
            return False


def save_maestro_parquet(
    df: pd.DataFrame,
    output_path: Path,
    partition_by: list[str] | None = None,
    fallback_csv: bool = True,
) -> Path:
    """
    Guarda el dataset maestro en formato Parquet (o CSV si no hay motor).

    Args:
        df: DataFrame consolidado
        output_path: Ruta al archivo .parquet
        partition_by: Columnas para particionar (opcional)
        fallback_csv: Si True, guarda como CSV si Parquet no está disponible

    Returns:
        Ruta del archivo guardado
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = ensure_correct_dtypes(df)

    if _has_parquet_engine():
        if partition_by and all(c in df.columns for c in partition_by):
            output_dir = output_path.with_suffix("")
            df.to_parquet(output_dir, partition_cols=partition_by, index=False)
            logger.info("Guardado particionado en %s", output_dir)
            return output_dir
        else:
            df.to_parquet(output_path, index=False)
            logger.info("Guardado Parquet en %s (%d registros)", output_path, len(df))
            return output_path
    elif fallback_csv:
        csv_path = output_path.with_suffix(".csv")
        df.to_csv(csv_path, index=False, encoding="utf-8")
        logger.warning(
            "PyArrow no instalado. Guardado como CSV en %s. "
            "Instale pyarrow para formato Parquet: pip install pyarrow",
            csv_path,
        )
        return csv_path
    else:
        raise ImportError(
            "Se requiere pyarrow o fastparquet para Parquet. "
            "Instale con: pip install pyarrow"
        )


def save_etl_log(
    log_path: Path,
    summary: dict[str, Any],
) -> None:
    """Guarda log de ejecución del ETL."""
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("ETL Run Log\n")
        f.write("=" * 50 + "\n")
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")
