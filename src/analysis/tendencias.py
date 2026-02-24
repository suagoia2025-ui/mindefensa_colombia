"""
Análisis de tendencias y comparaciones año a año.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


def comparacion_anual(
    df: pd.DataFrame,
    grupo_por: str | list[str] | None = None,
) -> pd.DataFrame:
    """
    Comparación año a año: total por año y variación % vs año anterior.

    Args:
        df: Dataset con columnas ano, cantidad
        grupo_por: Columnas adicionales para agrupar (ej. tipo_evento)

    Returns:
        DataFrame con ano, total, var_pct_anterior, y columnas de grupo si aplica
    """
    agg = {"cantidad": "sum"}
    group_cols = ["ano"]
    if grupo_por:
        cols = [grupo_por] if isinstance(grupo_por, str) else grupo_por
        group_cols = cols + ["ano"]

    res = df.groupby(group_cols, dropna=False).agg(agg).reset_index()
    res = res.rename(columns={"cantidad": "total"})

    # Ordenar para calcular variación
    res = res.sort_values(group_cols)

    # Variación vs año anterior
    if grupo_por:
        res["var_pct_anterior"] = res.groupby(cols)["total"].pct_change() * 100
    else:
        res["var_pct_anterior"] = res["total"].pct_change() * 100

    return res


def tendencia_lineal(
    df: pd.DataFrame,
    min_anos: int = 3,
) -> dict[str, Any]:
    """
    Tendencia lineal: dirección y fuerza de la serie temporal.

    Args:
        df: Dataset con columnas ano, cantidad
        min_anos: Mínimo de años para calcular tendencia

    Returns:
        Dict con pendiente, r_cuadrado, direccion, interpretacion
    """
    anual = df.groupby("ano")["cantidad"].sum().reset_index()
    if len(anual) < min_anos:
        return {
            "pendiente": None,
            "r_cuadrado": None,
            "direccion": "insuficientes_datos",
            "interpretacion": f"Se requieren al menos {min_anos} años",
        }

    x = anual["ano"].astype(float).values
    y = anual["cantidad"].values

    # Regresión simple: y = mx + b
    n = len(x)
    x_mean = x.mean()
    y_mean = y.mean()
    ss_xy = ((x - x_mean) * (y - y_mean)).sum()
    ss_xx = ((x - x_mean) ** 2).sum()

    if ss_xx == 0:
        return {"pendiente": 0, "r_cuadrado": 0, "direccion": "estable", "interpretacion": "Sin variación"}

    pendiente = ss_xy / ss_xx
    intercepto = y_mean - pendiente * x_mean
    y_pred = pendiente * x + intercepto
    ss_res = ((y - y_pred) ** 2).sum()
    ss_tot = ((y - y_mean) ** 2).sum()
    r_cuadrado = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

    if pendiente > 0:
        direccion = "ascendente"
        interp = "Tendencia al aumento en el período"
    elif pendiente < 0:
        direccion = "descendente"
        interp = "Tendencia a la disminución en el período"
    else:
        direccion = "estable"
        interp = "Sin tendencia clara"

    return {
        "pendiente": round(float(pendiente), 2),
        "r_cuadrado": round(float(r_cuadrado), 4),
        "direccion": direccion,
        "interpretacion": interp,
        "ano_inicio": int(x.min()),
        "ano_fin": int(x.max()),
    }


def resumen_por_periodo(
    df: pd.DataFrame,
    por_tipo_evento: bool = True,
) -> pd.DataFrame:
    """
    Resumen agregado por año y opcionalmente por tipo de evento.

    Args:
        df: Dataset maestro
        por_tipo_evento: Si True, desagrega por tipo_evento

    Returns:
        DataFrame con totales por año (y tipo_evento si aplica)
    """
    if por_tipo_evento:
        res = df.groupby(["ano", "tipo_evento"])["cantidad"].sum().reset_index()
        res = res.pivot(index="ano", columns="tipo_evento", values="cantidad").fillna(0)
    else:
        res = df.groupby("ano")["cantidad"].sum().to_frame("total")

    return res
