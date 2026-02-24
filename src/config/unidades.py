"""
Mapeo de unidad de medida por tipo de evento.

Cada tipo de evento tiene una unidad distinta (personas, kg, hectáreas, casos).
Esto permite interpretar correctamente los gráficos del dashboard.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_PROJECT_ROOT = Path(__file__).resolve().parents[2]
_CONFIG_PATH = _PROJECT_ROOT / "config" / "unidades_evento.yaml"

_UNIDADES_CACHE: dict[str, str] | None = None


def _load_unidades() -> dict[str, str]:
    """Carga el mapeo tipo_evento -> unidad desde el YAML."""
    global _UNIDADES_CACHE
    if _UNIDADES_CACHE is not None:
        return _UNIDADES_CACHE

    unidades: dict[str, str] = {}
    if not _CONFIG_PATH.exists():
        _UNIDADES_CACHE = unidades
        return unidades

    with open(_CONFIG_PATH, encoding="utf-8") as f:
        config: dict[str, list[str]] = yaml.safe_load(f) or {}

    for unidad, tipos in config.items():
        if isinstance(tipos, list):
            for t in tipos:
                unidades[str(t).strip().upper()] = unidad

    _UNIDADES_CACHE = unidades
    return unidades


def get_unidad_por_tipo_evento(tipo_evento: str) -> str:
    """
    Devuelve la unidad de medida para un tipo de evento.

    Args:
        tipo_evento: Nombre del tipo de evento (ej. INCAUTACIÓN DE COCAINA)

    Returns:
        Unidad: 'personas', 'peso', 'hectareas', 'casos' o '—' si no está mapeado
    """
    mapeo = _load_unidades()
    return mapeo.get(str(tipo_evento).strip().upper(), "—")


def get_mapping_completo() -> dict[str, str]:
    """Devuelve el mapeo completo tipo_evento -> unidad (para API)."""
    return dict(_load_unidades())


