"""
Agregaciones por territorio y tipo de evento.
"""

from __future__ import annotations

import pandas as pd


def por_departamento(
    df: pd.DataFrame,
    top_n: int | None = None,
    incluir_pct: bool = True,
) -> pd.DataFrame:
    """
    Conteo por departamento con ranking.

    Args:
        df: Dataset maestro
        top_n: Limitar a los N primeros (None = todos)
        incluir_pct: Añadir columna % del total

    Returns:
        DataFrame con cod_depto, departamento, total, ranking, pct_total (opcional)
    """
    res = (
        df.groupby(["cod_depto", "departamento"])
        .agg(total=("cantidad", "sum"))
        .reset_index()
    )
    res = res.sort_values("total", ascending=False).reset_index(drop=True)
    res["ranking"] = range(1, len(res) + 1)

    if incluir_pct:
        total_gral = res["total"].sum()
        res["pct_total"] = (res["total"] / total_gral * 100).round(2)

    if top_n is not None:
        res = res.head(top_n)

    return res


def por_municipio(
    df: pd.DataFrame,
    top_n: int | None = 50,
    incluir_depto: bool = True,
) -> pd.DataFrame:
    """
    Conteo por municipio.

    Args:
        df: Dataset maestro
        top_n: Limitar a los N primeros (None = todos)
        incluir_depto: Incluir nombre de departamento

    Returns:
        DataFrame con municipio, cod_muni, total, (departamento), ranking
    """
    cols = ["cod_depto", "departamento", "cod_muni", "municipio"] if incluir_depto else ["cod_muni", "municipio"]

    res = df.groupby(cols)["cantidad"].sum().reset_index()
    res = res.rename(columns={"cantidad": "total"})
    res = res.sort_values("total", ascending=False).reset_index(drop=True)
    res["ranking"] = range(1, len(res) + 1)

    total_gral = res["total"].sum()
    res["pct_total"] = (res["total"] / total_gral * 100).round(2)

    if top_n is not None:
        res = res.head(top_n)

    return res


def por_tipo_evento(
    df: pd.DataFrame,
    top_n: int | None = None,
) -> pd.DataFrame:
    """
    Conteo por tipo de evento (categoría de delito).

    Args:
        df: Dataset maestro
        top_n: Limitar a los N primeros (None = todos)

    Returns:
        DataFrame con tipo_evento, total, pct_total, ranking
    """
    res = df.groupby("tipo_evento")["cantidad"].sum().reset_index()
    res = res.rename(columns={"cantidad": "total"})
    res = res.sort_values("total", ascending=False).reset_index(drop=True)
    res["ranking"] = range(1, len(res) + 1)

    total_gral = res["total"].sum()
    res["pct_total"] = (res["total"] / total_gral * 100).round(2)

    if top_n is not None:
        res = res.head(top_n)

    return res


def cruze_territorio_evento(
    df: pd.DataFrame,
    territorio: str = "departamento",
    top_territorios: int = 15,
    top_eventos: int = 10,
) -> pd.DataFrame:
    """
    Cruce territorio x tipo de evento (pivot).

    Args:
        df: Dataset maestro
        territorio: 'departamento' o 'municipio'
        top_territorios: N territorios con más casos
        top_eventos: N tipos de evento con más casos

    Returns:
        DataFrame pivot con territorios en filas, tipos en columnas
    """
    if territorio == "departamento":
        col_terr = "departamento"
    else:
        col_terr = "municipio"

    # Top territorios y eventos
    top_deptos = df.groupby(col_terr)["cantidad"].sum().nlargest(top_territorios).index.tolist()
    top_eventos_list = df.groupby("tipo_evento")["cantidad"].sum().nlargest(top_eventos).index.tolist()

    subset = df[df[col_terr].isin(top_deptos) & df["tipo_evento"].isin(top_eventos_list)]

    pivot = subset.pivot_table(
        index=col_terr,
        columns="tipo_evento",
        values="cantidad",
        aggfunc="sum",
        fill_value=0,
    )

    return pivot
