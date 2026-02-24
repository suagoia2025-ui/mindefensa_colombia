"""
Índices de concentración geográfica.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def indice_gini(
    df: pd.DataFrame,
    nivel: str = "departamento",
) -> float:
    """
    Índice de Gini de concentración territorial.

    0 = distribución uniforme, 1 = máxima concentración.

    Args:
        df: Dataset maestro
        nivel: 'departamento' o 'municipio'

    Returns:
        Índice de Gini (0-1)
    """
    col = "departamento" if nivel == "departamento" else "municipio"
    conteos = df.groupby(col)["cantidad"].sum().sort_values(ascending=True)

    if len(conteos) < 2:
        return 0.0

    n = len(conteos)
    valores = conteos.values
    cumsum = valores.cumsum()
    total = cumsum[-1]

    if total == 0:
        return 0.0

    # Gini = 1 - 2 * área bajo curva de Lorenz
    # Área = sum((2*i - n - 1) * y_i) / (n * total)
    idx = np.arange(1, n + 1)
    gini = (2 * (idx * valores).sum() - (n + 1) * total) / (n * total)
    return max(0.0, min(1.0, float(gini)))


def top_n_concentracion(
    df: pd.DataFrame,
    nivel: str = "departamento",
    top_n: int = 10,
) -> pd.DataFrame:
    """
    Porcentaje acumulado del total por top N territorios.

    Args:
        df: Dataset maestro
        nivel: 'departamento' o 'municipio'
        top_n: Cantidad de territorios a incluir

    Returns:
        DataFrame con territorio, total, pct_total, pct_acumulado
    """
    col = "departamento" if nivel == "departamento" else "municipio"
    res = df.groupby(col)["cantidad"].sum().sort_values(ascending=False).reset_index()
    res = res.rename(columns={"cantidad": "total"})

    total_gral = res["total"].sum()
    if total_gral == 0:
        res["pct_total"] = 0
        res["pct_acumulado"] = 0
        return res.head(top_n)

    res["pct_total"] = (res["total"] / total_gral * 100).round(2)
    res["pct_acumulado"] = res["pct_total"].cumsum().round(2)

    return res.head(top_n)


def ranking_municipios(
    df: pd.DataFrame,
    top_n: int = 50,
) -> pd.DataFrame:
    """
    Municipios con mayor carga de eventos y % acumulado.

    Args:
        df: Dataset maestro
        top_n: Cantidad de municipios

    Returns:
        DataFrame con municipio, departamento, total, pct_acumulado, ranking
    """
    res = (
        df.groupby(["cod_muni", "municipio", "departamento"])
        .agg(total=("cantidad", "sum"))
        .reset_index()
    )
    res = res.sort_values("total", ascending=False).reset_index(drop=True)
    res["ranking"] = range(1, len(res) + 1)

    total_gral = res["total"].sum()
    if total_gral > 0:
        res["pct_total"] = (res["total"] / total_gral * 100).round(2)
        res["pct_acumulado"] = res["pct_total"].cumsum().round(2)

    return res.head(top_n)
