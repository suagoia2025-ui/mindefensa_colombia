#!/usr/bin/env python3
"""
Script de ejecución del Pipeline ETL - Análisis Seguridad Colombia

Consolida los archivos Excel del Ministerio de Defensa en un dataset maestro
en formato Parquet para análisis de tendencias y comparaciones.

Uso:
    python 02_run_etl.py
    python 02_run_etl.py --config config/etl.yaml
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Asegurar que el proyecto esté en el path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.etl.pipeline import run_pipeline


def main() -> int:
    """Punto de entrada."""
    parser = argparse.ArgumentParser(description="Pipeline ETL - Seguridad Colombia")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Ruta al archivo de configuración (default: config/etl.yaml)",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=project_root,
        help="Directorio raíz del proyecto",
    )

    args = parser.parse_args()

    try:
        summary = run_pipeline(
            project_root=args.project_root,
            config_path=args.config,
        )
        print("\n--- Resumen ETL ---")
        print(f"Estado: {summary.get('status', 'N/A')}")
        print(f"Archivos procesados: {summary.get('files_processed', 0)}")
        print(f"Total registros: {summary.get('total_records', 0):,}")
        print(f"Duración: {summary.get('duration_seconds', 0)} segundos")
        print(f"Archivo salida: {summary.get('output_file', 'N/A')}")
        if summary.get("catalog_file"):
            print(f"Catálogo / particiones: {summary.get('catalog_file')}")

        if summary.get("status") == "error":
            return 1
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
