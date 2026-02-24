"""
Transformadores - Normalización y validación de datos.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)

# Mapeos de columnas origen -> destino
DATE_COLUMNS = ["FECHA_HECHO", "FECHA HECHO"]
VALUE_COLUMNS = ["VICTIMAS", "CANTIDAD", "CASOS", "CAPTURAS", "CANTIDAD "]
GEO_COLUMNS = ["COD_DEPTO", "COD_MUNI", "DEPARTAMENTO", "MUNICIPIO"]


def _find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    """Encuentra la primera columna que existe."""
    for c in candidates:
        if c in df.columns:
            return c
    return None


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas a esquema unificado.

    Genera: fecha, cod_depto, cod_muni, departamento, municipio, cantidad
    """
    result = df.copy()

    # Fecha
    date_col = _find_column(df, DATE_COLUMNS)
    if date_col:
        result["fecha"] = pd.to_datetime(result[date_col], errors="coerce")
    else:
        result["fecha"] = pd.NaT

    # Códigos geográficos
    if "COD_DEPTO" in df.columns:
        result["cod_depto"] = result["COD_DEPTO"].astype(str).str.strip().str.zfill(2)
    if "COD_MUNI" in df.columns:
        result["cod_muni"] = result["COD_MUNI"].astype(str).str.strip().str.zfill(5)

    # Nombres geográficos
    if "DEPARTAMENTO" in df.columns:
        result["departamento"] = result["DEPARTAMENTO"].astype(str).str.strip().str.upper()
    if "MUNICIPIO" in df.columns:
        result["municipio"] = result["MUNICIPIO"].astype(str).str.strip().str.upper()

    # Cantidad/valor
    value_col = _find_column(df, VALUE_COLUMNS)
    if value_col:
        result["cantidad"] = pd.to_numeric(result[value_col], errors="coerce").fillna(1).astype("int32")
    else:
        result["cantidad"] = 1

    # Tipo evento (de columna _tipo_evento si existe)
    if "_tipo_evento" in df.columns:
        result["tipo_evento"] = result["_tipo_evento"]
    else:
        result["tipo_evento"] = "DESCONOCIDO"

    # Archivo origen
    if "_archivo_origen" in df.columns:
        result["archivo_origen"] = result["_archivo_origen"]

    return result


def select_output_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Selecciona solo las columnas del esquema final."""
    output_cols = [
        "fecha",
        "ano",
        "mes",
        "cod_depto",
        "cod_muni",
        "departamento",
        "municipio",
        "tipo_evento",
        "cantidad",
        "archivo_origen",
    ]
    existing = [c for c in output_cols if c in df.columns]
    return df[existing].copy()


def validate_temporal(
    df: pd.DataFrame,
    min_year: int = 1990,
    max_year: int = 2030,
    drop_future: bool = True,
) -> pd.DataFrame:
    """Filtra fechas fuera de rango lógico."""
    if "fecha" not in df.columns or df["fecha"].isna().all():
        return df

    df = df.copy()
    df["ano"] = df["fecha"].dt.year
    df["mes"] = df["fecha"].dt.month

    before = len(df)
    df = df[
        (df["ano"] >= min_year) &
        (df["ano"] <= max_year)
    ]

    if drop_future:
        hoy = datetime.now().year
        df = df[df["ano"] <= hoy]

    removed = before - len(df)
    if removed > 0:
        logger.warning("Eliminadas %d filas por fechas fuera de rango", removed)

    return df


def validate_geographic(df: pd.DataFrame) -> pd.DataFrame:
    """Valida y limpia códigos DIVIPOLA."""
    df = df.copy()

    # COD_DEPTO: 1-2 dígitos
    if "cod_depto" in df.columns:
        mask = df["cod_depto"].str.match(r"^\d{1,2}$", na=False)
        df = df[mask | df["cod_depto"].isna()]

    # COD_MUNI: 4-5 dígitos
    if "cod_muni" in df.columns:
        mask = df["cod_muni"].str.match(r"^\d{4,5}$", na=False)
        df = df[mask | df["cod_muni"].isna()]

    return df


def validate_quantity(df: pd.DataFrame) -> pd.DataFrame:
    """Asegura que cantidad sea positiva."""
    if "cantidad" not in df.columns:
        return df
    df = df.copy()
    df.loc[df["cantidad"] < 1, "cantidad"] = 1
    return df


def drop_invalid_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina filas con datos críticos nulos."""
    required = ["fecha", "cod_depto", "cod_muni", "tipo_evento", "cantidad"]
    existing = [c for c in required if c in df.columns]
    return df.dropna(subset=existing)


def transform_dataframe(
    df: pd.DataFrame,
    config: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """
    Aplica todas las transformaciones al DataFrame.

    Args:
        df: DataFrame extraído
        config: Configuración ETL (opcional)

    Returns:
        DataFrame transformado y validado
    """
    validation = (config or {}).get("validation", {})
    min_year = validation.get("min_year", 1990)
    max_year = validation.get("max_year", 2030)
    drop_future = validation.get("drop_future_dates", True)

    df = normalize_column_names(df)
    df = validate_temporal(df, min_year, max_year, drop_future)
    df = validate_geographic(df)
    df = validate_quantity(df)
    df = drop_invalid_rows(df)
    df = select_output_columns(df)

    return df.reset_index(drop=True)
