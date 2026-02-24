"""
Extractores - Lectura de archivos Excel del Ministerio de Defensa.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


def extract_excel_file(
    file_path: Path,
    tipo_evento: str,
    exclude_sheets: set[str] | None = None,
) -> pd.DataFrame | None:
    """
    Extrae datos de un archivo Excel del Ministerio de Defensa.

    Args:
        file_path: Ruta al archivo .xlsx
        tipo_evento: Nombre del tipo de evento (derivado del nombre del archivo)
        exclude_sheets: Hojas a excluir (ej. metadatos)

    Returns:
        DataFrame con columnas raw o None si no se puede procesar
    """
    if exclude_sheets is None:
        exclude_sheets = set()

    try:
        xl = pd.ExcelFile(file_path)
    except Exception as e:
        logger.error("Error al abrir %s: %s", file_path.name, e)
        return None

    all_dfs: list[pd.DataFrame] = []

    for sheet_name in xl.sheet_names:
        if sheet_name in exclude_sheets:
            continue

        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        except Exception as e:
            logger.warning("Error en hoja %s de %s: %s", sheet_name, file_path.name, e)
            continue

        if df.empty or len(df.columns) < 4:
            continue

        # Verificar que tiene columnas mínimas (fecha, geo, valor)
        has_date = any(
            c in df.columns
            for c in ["FECHA_HECHO", "FECHA HECHO"]
        )
        has_geo = "COD_DEPTO" in df.columns and "COD_MUNI" in df.columns
        has_value = any(
            c in df.columns
            for c in ["VICTIMAS", "CANTIDAD", "CASOS", "CAPTURAS", "CANTIDAD "]
        )

        if not (has_date and has_geo and has_value):
            logger.debug("Hoja %s de %s no tiene estructura esperada", sheet_name, file_path.name)
            continue

        df["_archivo_origen"] = file_path.name
        df["_tipo_evento"] = tipo_evento
        all_dfs.append(df)

    if not all_dfs:
        return None

    return pd.concat(all_dfs, ignore_index=True)


def extract_all_files(
    base_path: Path,
    exclude_files: set[str],
    extensions: list[str] = (".xlsx",),
) -> list[tuple[str, pd.DataFrame]]:
    """
    Extrae todos los archivos Excel de un directorio.

    Args:
        base_path: Directorio base
        exclude_files: Nombres de archivos a excluir
        extensions: Extensiones permitidas

    Returns:
        Lista de (tipo_evento, DataFrame)
    """
    results: list[tuple[str, pd.DataFrame]] = []

    for ext in extensions:
        for file_path in base_path.rglob(f"*{ext}"):
            if file_path.name in exclude_files:
                logger.info("Excluido: %s", file_path.name)
                continue

            # Tipo evento = nombre del archivo sin extensión
            tipo_evento = file_path.stem

            df = extract_excel_file(file_path, tipo_evento)
            if df is not None and len(df) > 0:
                results.append((tipo_evento, df))
                logger.info("Extraído %s: %d registros", file_path.name, len(df))

    return results
