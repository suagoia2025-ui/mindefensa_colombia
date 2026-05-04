"""
Catálogo y particiones por tipo_evento (indicador) para evitar cargar el maestro completo.

Dominio: cada archivo en data/processed/partitions corresponde a un tipo_evento;
catalog.json lista rutas y estadísticas para /api/metadata sin leer Parquet grande.
"""

from __future__ import annotations

import json
from collections import OrderedDict
from pathlib import Path
from typing import Any

import pandas as pd

CATALOG_FILENAME = "catalog.json"
_MAX_CACHED_INDICADORES = 8

_catalog_cache: dict[str, Any] | None = None
_tipo_df_cache: OrderedDict[str, pd.DataFrame] = OrderedDict()


def _processed_root(project_root: Path) -> Path:
    return project_root / "data" / "processed"


def catalog_path(project_root: Path) -> Path:
    return _processed_root(project_root) / CATALOG_FILENAME


def load_catalog(project_root: Path, *, reload: bool = False) -> dict[str, Any] | None:
    """Lee catalog.json si existe."""
    global _catalog_cache
    path = catalog_path(project_root)
    if not path.exists():
        _catalog_cache = None
        return None
    if _catalog_cache is not None and not reload:
        return _catalog_cache
    with open(path, encoding="utf-8") as fh:
        _catalog_cache = json.load(fh)
    return _catalog_cache


def clear_runtime_caches() -> None:
    """Útil en tests o tras hot-reload."""
    global _catalog_cache
    _catalog_cache = None
    _tipo_df_cache.clear()


def tipo_evento_to_file(catalog: dict[str, Any], tipo_evento: str) -> str | None:
    for entry in catalog.get("tipos", []):
        if entry.get("tipo_evento") == tipo_evento:
            return entry.get("file")
    return None


def _read_partition_parquet(project_root: Path, rel_file: str) -> pd.DataFrame:
    base = _processed_root(project_root)
    fp = (base / rel_file).resolve()
    if not str(fp).startswith(str(base.resolve())):
        raise ValueError("Ruta de partición inválida")
    if not fp.exists():
        raise FileNotFoundError(f"Partición no encontrada: {fp}")
    return pd.read_parquet(fp)


def get_dataframe_for_tipo_evento(project_root: Path, tipo_evento: str) -> pd.DataFrame:
    """
    DataFrame de un solo indicador, con LRU en memoria para pocos tipos a la vez.
    """
    cat = load_catalog(project_root)
    if not cat:
        raise FileNotFoundError("No hay catalog.json; ejecute ETL o scripts/rebuild_partitions.py")

    rel = tipo_evento_to_file(cat, tipo_evento)
    if not rel:
        raise KeyError(f"Indicador no está en el catálogo: {tipo_evento!r}")

    if tipo_evento in _tipo_df_cache:
        _tipo_df_cache.move_to_end(tipo_evento)
        return _tipo_df_cache[tipo_evento]

    df = _read_partition_parquet(project_root, rel)
    _tipo_df_cache[tipo_evento] = df
    while len(_tipo_df_cache) > _MAX_CACHED_INDICADORES:
        _tipo_df_cache.popitem(last=False)

    return df


def catalog_ready(project_root: Path) -> bool:
    return catalog_path(project_root).exists()
