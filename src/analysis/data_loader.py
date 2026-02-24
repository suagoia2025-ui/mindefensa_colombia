"""
Carga del dataset maestro con filtros opcionales.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def _resolve_maestro_path(base_path: str | Path) -> Path:
    """Resuelve la ruta al archivo maestro (Parquet o CSV)."""
    base = Path(base_path)
    if base.suffix:
        # Ya tiene extensión
        if base.exists():
            return base
        alt = base.with_suffix(".csv" if base.suffix == ".parquet" else ".parquet")
        if alt.exists():
            return alt
        return base

    parquet = Path(str(base) + ".parquet")
    csv = Path(str(base) + ".csv")
    if parquet.exists():
        return parquet
    if csv.exists():
        return csv
    return csv  # Default para crear


def load_maestro(
    path: str | Path | None = None,
    project_root: Path | None = None,
    anos: list[int] | None = None,
    departamentos: list[str] | None = None,
    tipo_evento: str | list[str] | None = None,
    mes: int | list[int] | None = None,
) -> pd.DataFrame:
    """
    Carga el dataset maestro con filtros opcionales.

    Args:
        path: Ruta directa al archivo. Si None, usa config.
        project_root: Raíz del proyecto para rutas relativas.
        anos: Filtrar por años (ej. [2020, 2021, 2022]).
        departamentos: Filtrar por códigos o nombres de departamento.
        tipo_evento: Filtrar por tipo(s) de evento.
        mes: Filtrar por mes(es) 1-12.

    Returns:
        DataFrame filtrado con columnas: fecha, ano, mes, cod_depto, cod_muni,
        departamento, municipio, tipo_evento, cantidad, archivo_origen
    """
    if path is None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]
        path = project_root / "data" / "processed" / "eventos_seguridad_maestro"

    file_path = _resolve_maestro_path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset maestro no encontrado: {file_path}")

    if file_path.suffix == ".parquet":
        df = pd.read_parquet(file_path)
    else:
        df = pd.read_csv(file_path)
        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"])

    # Asegurar tipos
    if "ano" in df.columns:
        df["ano"] = df["ano"].astype("int16")
    if "mes" in df.columns:
        df["mes"] = df["mes"].astype("int8")

    # Filtros
    if anos is not None:
        df = df[df["ano"].isin(anos)]
    if departamentos is not None:
        mask = df["cod_depto"].astype(str).isin(str(d) for d in departamentos) | df["departamento"].str.upper().isin(str(d).upper() for d in departamentos)
        df = df[mask]
    if tipo_evento is not None:
        tipos = [tipo_evento] if isinstance(tipo_evento, str) else tipo_evento
        df = df[df["tipo_evento"].isin(tipos)]
    if mes is not None:
        meses = [mes] if isinstance(mes, int) else mes
        df = df[df["mes"].isin(meses)]

    return df.reset_index(drop=True)
