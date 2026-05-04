#!/usr/bin/env python3
"""
Regenera data/processed/partitions/*.parquet y catalog.json desde el maestro existente.

No ejecuta el ETL completo (útil cuando ya tienes eventos_seguridad_maestro.parquet).

    python scripts/rebuild_partitions.py
    python scripts/rebuild_partitions.py --project-root /ruta/al/proyecto
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.analysis.data_loader import load_maestro  # noqa: E402
from src.etl.loaders import save_partitions_and_catalog  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Particiones por tipo_evento + catalog.json")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=project_root,
        help="Raíz del proyecto",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()

    print("Cargando maestro (puede tardar)...")
    df = load_maestro(project_root=root)
    print(f"Registros: {len(df):,}")

    out = save_partitions_and_catalog(df, root / "data" / "processed")
    if out:
        print(f"OK: {out}")
        return 0
    print("No se generaron particiones (¿pyarrow instalado?)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
