"""
Carga y validación de configuración ETL.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_etl_config(config_path: Path | None = None) -> dict[str, Any]:
    """
    Carga la configuración YAML del ETL.

    Args:
        config_path: Ruta al archivo. Si None, usa config/etl.yaml relativo al proyecto.

    Returns:
        Diccionario con la configuración.
    """
    if config_path is None:
        project_root = Path(__file__).resolve().parents[2]
        config_path = project_root / "config" / "etl.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Configuración no encontrada: {config_path}")

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config.get("etl", config)


def get_column_mappings(config: dict[str, Any]) -> dict[str, list[str]]:
    """Extrae mapeos columna_origen -> columna_destino."""
    mappings = config.get("column_mappings", {})
    result: dict[str, list[str]] = {}
    for target, spec in mappings.items():
        if isinstance(spec, dict) and "source" in spec:
            result[target] = spec["source"]
    return result


def get_excluded_files(config: dict[str, Any]) -> set[str]:
    """Archivos a excluir del procesamiento."""
    return set(config.get("exclude_files", []))
