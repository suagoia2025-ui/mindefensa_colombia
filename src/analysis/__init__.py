"""
Módulo de Análisis - Seguridad Colombia

Análisis estadístico: tendencias, comparaciones año a año,
concentración geográfica, patrones estacionales.
"""

from src.analysis.data_loader import load_maestro
from src.analysis.tendencias import comparacion_anual, tendencia_lineal, resumen_por_periodo
from src.analysis.agregaciones import (
    por_departamento,
    por_municipio,
    por_tipo_evento,
    cruze_territorio_evento,
)
from src.analysis.concentracion import indice_gini, top_n_concentracion, ranking_municipios
from src.analysis.estacionalidad import (
    patron_mensual,
    patron_trimestral,
    mes_pico,
    estacionalidad_por_tipo,
)

__all__ = [
    "load_maestro",
    "comparacion_anual",
    "tendencia_lineal",
    "resumen_por_periodo",
    "por_departamento",
    "por_municipio",
    "por_tipo_evento",
    "cruze_territorio_evento",
    "indice_gini",
    "top_n_concentracion",
    "ranking_municipios",
    "patron_mensual",
    "patron_trimestral",
    "mes_pico",
    "estacionalidad_por_tipo",
]
