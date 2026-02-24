#!/usr/bin/env python3
"""
Script de ejecución del Módulo de Análisis - Seguridad Colombia

Ejecuta análisis de tendencias, concentración y estacionalidad
sobre el dataset maestro de eventos de seguridad.

Uso:
    python 03_run_analysis.py
    python 03_run_analysis.py --anos 2020 2021 2022 2023
    python 03_run_analysis.py --tipo "HOMICIDIO INTENCIONAL"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Asegurar que el proyecto esté en el path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.analysis import (
    load_maestro,
    comparacion_anual,
    tendencia_lineal,
    por_departamento,
    por_tipo_evento,
    indice_gini,
    top_n_concentracion,
    mes_pico,
    patron_mensual,
)


def main() -> int:
    """Punto de entrada."""
    parser = argparse.ArgumentParser(description="Análisis de Seguridad Colombia")
    parser.add_argument("--anos", type=int, nargs="+", help="Filtrar por años (ej: 2020 2021 2022)")
    parser.add_argument("--tipo", type=str, help="Filtrar por tipo de evento")
    parser.add_argument("--output", type=Path, help="Guardar resultados en JSON")
    parser.add_argument("--project-root", type=Path, default=project_root)

    args = parser.parse_args()

    try:
        df = load_maestro(project_root=args.project_root, anos=args.anos, tipo_evento=args.tipo)

        if len(df) == 0:
            print("No hay datos para el análisis con los filtros especificados.")
            return 1

        print(f"\n{'='*60}")
        print("ANÁLISIS DE SEGURIDAD Y VIOLENCIA - COLOMBIA")
        print(f"{'='*60}")
        print(f"Registros analizados: {len(df):,}")
        print(f"Años: {sorted(df['ano'].unique().tolist())}")
        if args.tipo:
            print(f"Tipo de evento: {args.tipo}")
        print()

        # 1. Comparación año a año
        print("--- Comparación año a año ---")
        comp = comparacion_anual(df)
        comp["var_pct_anterior"] = comp["var_pct_anterior"].round(2)
        print(comp.to_string(index=False))
        print()

        # 2. Tendencia lineal
        print("--- Tendencia lineal ---")
        tend = tendencia_lineal(df)
        for k, v in tend.items():
            print(f"  {k}: {v}")
        print()

        # 3. Top 5 departamentos
        print("--- Top 5 departamentos ---")
        deptos = por_departamento(df, top_n=5)
        print(deptos.to_string(index=False))
        print()

        # 4. Top 5 tipos de evento
        print("--- Top 5 tipos de evento ---")
        tipos = por_tipo_evento(df, top_n=5)
        print(tipos.to_string(index=False))
        print()

        # 5. Índice de Gini (concentración)
        print("--- Concentración territorial ---")
        gini = indice_gini(df, nivel="departamento")
        print(f"  Índice Gini (departamentos): {gini:.4f}")
        conc = top_n_concentracion(df, nivel="departamento", top_n=5)
        print("  Top 5 departamentos (% acumulado):")
        print(conc.to_string(index=False))
        print()

        # 6. Mes pico
        print("--- Estacionalidad ---")
        pico = mes_pico(df)
        print(f"  Mes de mayor incidencia: {pico['mes_nombre']} ({pico['pct_del_total']}% del total)")
        print()

        # Guardar resultados si se solicita
        if args.output:
            resultados = {
                "comparacion_anual": comp.fillna(None).to_dict(orient="records"),
                "tendencia": tend,
                "top_departamentos": deptos.fillna(None).to_dict(orient="records"),
                "top_tipos": tipos.fillna(None).to_dict(orient="records"),
                "gini": float(gini),
                "concentracion": conc.fillna(None).to_dict(orient="records"),
                "mes_pico": pico,
            }
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(resultados, f, indent=2, ensure_ascii=False)
            print(f"Resultados guardados en {args.output}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Ejecute primero el ETL: python 02_run_etl.py", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
