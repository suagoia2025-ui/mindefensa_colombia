"""
Análisis de patrones estacionales (mensual, trimestral).
"""

from __future__ import annotations

from typing import Any

import pandas as pd

MESES_NOMBRES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def patron_mensual(
    df: pd.DataFrame,
    agregar: str = "promedio_anual",
) -> pd.DataFrame:
    """
    Patrón mensual: promedio anual por mes, total por mes, o media de cantidad por mes.

    Args:
        df: Dataset con columnas ano, mes, cantidad
        agregar: 'promedio_anual' (recomendado), 'total' o 'promedio'
          - promedio_anual: para cada mes, promedio de (total de ese mes por año)
          - total: suma de cantidad por mes en todo el período
          - promedio: media de la columna cantidad por mes (legacy)

    Returns:
        DataFrame con mes, mes_nombre, y columna 'promedio' o 'total'
    """
    if agregar == "promedio_anual":
        # Por año y mes: total de eventos; luego por mes: promedio entre años
        por_ano_mes = df.groupby(["ano", "mes"])["cantidad"].sum().reset_index()
        res = por_ano_mes.groupby("mes")["cantidad"].mean().reset_index()
        res = res.rename(columns={"cantidad": "promedio"})
    elif agregar == "promedio":
        res = df.groupby("mes")["cantidad"].mean().reset_index()
        res = res.rename(columns={"cantidad": "promedio"})
    else:
        res = df.groupby("mes")["cantidad"].sum().reset_index()
        res = res.rename(columns={"cantidad": "total"})
        # Para consistencia con el frontend que espera "promedio", no se usa aquí

    res["mes_nombre"] = res["mes"].map(lambda m: MESES_NOMBRES[int(m) - 1])
    return res.sort_values("mes")


def patron_trimestral(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Patrón trimestral: total por trimestre (1-4).

    Args:
        df: Dataset con columnas mes, cantidad

    Returns:
        DataFrame con trimestre, total
    """
    df = df.copy()
    df["trimestre"] = ((df["mes"] - 1) // 3) + 1

    res = df.groupby("trimestre")["cantidad"].sum().reset_index()
    res = res.rename(columns={"cantidad": "total"})
    return res.sort_values("trimestre")


def mes_pico(
    df: pd.DataFrame,
) -> dict[str, Any]:
    """
    Identifica el mes con mayor incidencia histórica.

    Args:
        df: Dataset con columnas mes, cantidad

    Returns:
        Dict con mes, mes_nombre, total, pct_del_total
    """
    por_mes = df.groupby("mes")["cantidad"].sum()
    total_gral = por_mes.sum()

    if total_gral == 0:
        return {"mes": None, "mes_nombre": None, "total": 0, "pct_del_total": 0}

    mes_pico = por_mes.idxmax()
    total_pico = por_mes.max()

    return {
        "mes": int(mes_pico),
        "mes_nombre": MESES_NOMBRES[int(mes_pico) - 1],
        "total": int(total_pico),
        "pct_del_total": round(100 * total_pico / total_gral, 2),
    }


def estacionalidad_por_tipo(
    df: pd.DataFrame,
    top_tipos: int = 5,
) -> pd.DataFrame:
    """
    Patrón mensual promedio por tipo de evento.

    Args:
        df: Dataset maestro
        top_tipos: Cantidad de tipos de evento a incluir (por volumen)

    Returns:
        DataFrame con tipo_evento, mes, promedio
    """
    top = df.groupby("tipo_evento")["cantidad"].sum().nlargest(top_tipos).index.tolist()
    subset = df[df["tipo_evento"].isin(top)]

    res = (
        subset.groupby(["tipo_evento", "mes"])["cantidad"]
        .mean()
        .reset_index()
    )
    res = res.rename(columns={"cantidad": "promedio"})
    res["mes_nombre"] = res["mes"].map(lambda m: MESES_NOMBRES[int(m) - 1])

    return res
