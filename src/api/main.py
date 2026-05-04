"""
API FastAPI - Dashboard Seguridad Colombia

Endpoints para consumo del frontend React.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import math
from io import BytesIO

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse

# Proyecto raíz para imports
PROJECT_ROOT = Path(__file__).resolve().parents[2]
import sys
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
from src.config import get_unidad_por_tipo_evento
from src.analysis.partition_catalog import (
    catalog_ready,
    get_dataframe_for_tipo_evento,
    load_catalog,
    tipo_evento_to_file,
)

app = FastAPI(
    title="Análisis Seguridad Colombia",
    description="API para dashboard de seguridad y violencia - Ministerio de Defensa",
    version="1.0.0",
)

_allowed = os.environ.get("ALLOWED_ORIGINS", "*").strip()
if _allowed == "*":
    _cors_origins = ["*"]
else:
    _cors_origins = [o.strip() for o in _allowed.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
def global_exception_handler(request, exc):
    """Devuelve el error en JSON para depuración."""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__},
    )


def _parse_anos(anos: str | None) -> list[int] | None:
    """Convierte parámetro anos (ej. '2020,2021') en lista de int o None."""
    if not anos or not str(anos).strip():
        return None
    parts = [a.strip() for a in str(anos).split(",") if a.strip()]
    if not parts:
        return None
    try:
        return [int(a) for a in parts]
    except ValueError:
        return None


def _df_to_records(df):
    """Convierte DataFrame a list[dict] JSON-serializable (NaN→None, numpy→native)."""
    raw = df.to_dict(orient="records")
    out = []
    for row in raw:
        new_row = {}
        for k, v in row.items():
            if v is not None and hasattr(v, "item") and callable(getattr(v, "item", None)):
                try:
                    v = v.item()
                except (ValueError, AttributeError):
                    pass
            if isinstance(v, float) and math.isnan(v):
                v = None
            new_row[k] = v
        out.append(new_row)
    return out


# Caché del dataset completo para no leer el CSV en cada petición (~7M filas)
_cached_df = None


def _get_cached_full_df():
    """Carga el dataset una vez y lo reutiliza en memoria."""
    global _cached_df
    if _cached_df is None:
        _cached_df = load_maestro(project_root=PROJECT_ROOT)
    return _cached_df


def _get_df(
    anos: list[int] | None = None,
    tipo_evento: str | None = None,
    departamento: str | None = None,
):
    """
    Dataset filtrado. Si existe catalog.json y se pide un tipo_evento, carga solo esa partición
    (rápido). Si no, usa el maestro completo en caché.
    """
    df: pd.DataFrame
    if tipo_evento is not None and catalog_ready(PROJECT_ROOT):
        cat = load_catalog(PROJECT_ROOT)
        if cat and tipo_evento_to_file(cat, tipo_evento):
            try:
                df = get_dataframe_for_tipo_evento(PROJECT_ROOT, tipo_evento)
            except Exception:
                df = _get_cached_full_df()
                df = df[df["tipo_evento"] == tipo_evento]
        else:
            df = _get_cached_full_df()
            df = df[df["tipo_evento"] == tipo_evento]
    else:
        df = _get_cached_full_df()
        if tipo_evento is not None:
            df = df[df["tipo_evento"] == tipo_evento]

    if anos is not None:
        df = df[df["ano"].isin(anos)]
    if departamento is not None:
        mask = (
            df["cod_depto"].astype(str).isin([str(departamento)])
            | df["departamento"].str.upper().str.strip().eq(str(departamento).upper())
        )
        df = df[mask]
    return df.reset_index(drop=True)


@app.get("/")
def root():
    """Health check."""
    return {"status": "ok", "api": "análisis-seguridad-colombia"}


def _health_payload() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": "analisis-seguridad-colombia",
        "version": "1.0.0",
    }


@app.get("/health")
async def health_check():
    """Salud del servicio (Docker healthcheck directo al contenedor API)."""
    return _health_payload()


@app.get("/api/health")
async def api_health_check():
    """Misma respuesta vía prefijo /api (nginx expone /api/* al cliente)."""
    return _health_payload()


@app.get("/api")
def api_root():
    """Raíz de la API (evita 404 al abrir /api en el navegador)."""
    return {"status": "ok", "api": "análisis-seguridad-colombia", "docs": "/api/metadata"}


@app.get("/api/metadata")
def metadata():
    """Metadatos del dataset (años disponibles, tipos de evento, unidades)."""
    cat = load_catalog(PROJECT_ROOT)
    if cat:
        tipos = sorted(t["tipo_evento"] for t in cat.get("tipos", []))
        unidades = {t: get_unidad_por_tipo_evento(t) for t in tipos}
        return {
            "anos_disponibles": cat["anos_disponibles"],
            "tipos_evento": tipos,
            "unidades_tipo_evento": unidades,
            "departamentos": cat["departamentos"],
            "total_registros": cat["total_registros"],
        }
    df = _get_cached_full_df()
    tipos = sorted(df["tipo_evento"].unique().tolist())
    unidades = {t: get_unidad_por_tipo_evento(t) for t in tipos}
    return {
        "anos_disponibles": sorted(df["ano"].unique().astype(int).tolist()),
        "tipos_evento": tipos,
        "unidades_tipo_evento": unidades,
        "departamentos": sorted(df["departamento"].dropna().unique().tolist()),
        "total_registros": int(len(df)),
    }


@app.get("/api/comparacion-anual")
def comparacion_anual_endpoint(
    anos: str | None = Query(None, description="Años separados por coma: 2020,2021,2022"),
    tipo_evento: str | None = Query(None),
    departamento: str | None = Query(None),
):
    """Comparación año a año con variación porcentual."""
    anos_list = _parse_anos(anos)
    df = _get_df(anos=anos_list, tipo_evento=tipo_evento, departamento=departamento)
    if len(df) == 0:
        return {"data": [], "message": "Sin datos para los filtros"}
    res = comparacion_anual(df)
    res["var_pct_anterior"] = res["var_pct_anterior"].round(2)
    return {"data": _df_to_records(res)}


@app.get("/api/tendencia")
def tendencia_endpoint(
    anos: str | None = Query(None),
    tipo_evento: str | None = Query(None),
    departamento: str | None = Query(None),
):
    """Tendencia lineal del período."""
    anos_list = _parse_anos(anos)
    df = _get_df(anos=anos_list, tipo_evento=tipo_evento, departamento=departamento)
    if len(df) == 0:
        return {"message": "Sin datos"}
    return tendencia_lineal(df)


@app.get("/api/departamentos")
def departamentos_endpoint(
    anos: str | None = Query(None),
    tipo_evento: str | None = Query(None),
    top_n: int = Query(15, ge=1, le=50),
):
    """Top departamentos por cantidad de eventos."""
    anos_list = _parse_anos(anos)
    df = _get_df(anos=anos_list, tipo_evento=tipo_evento)
    if len(df) == 0:
        return {"data": []}
    res = por_departamento(df, top_n=top_n)
    return {"data": _df_to_records(res)}


@app.get("/api/tipos-evento")
def tipos_evento_endpoint(
    anos: str | None = Query(None),
    departamento: str | None = Query(None),
    top_n: int = Query(15, ge=1, le=50),
):
    """Top tipos de evento por cantidad. Incluye unidad de medida por tipo."""
    anos_list = _parse_anos(anos)
    df = _get_df(anos=anos_list, departamento=departamento)
    if len(df) == 0:
        return {"data": []}
    res = por_tipo_evento(df, top_n=top_n)
    res["unidad"] = res["tipo_evento"].apply(get_unidad_por_tipo_evento)
    return {"data": _df_to_records(res)}


@app.get("/api/concentracion")
def concentracion_endpoint(
    anos: str | None = Query(None),
    tipo_evento: str | None = Query(None),
    top_n: int = Query(10, ge=1, le=32),
):
    """Índice Gini y concentración por departamento."""
    anos_list = _parse_anos(anos)
    df = _get_df(anos=anos_list, tipo_evento=tipo_evento)
    if len(df) == 0:
        return {"gini": 0, "data": []}
    gini = indice_gini(df, nivel="departamento")
    conc = top_n_concentracion(df, nivel="departamento", top_n=top_n)
    return {
        "gini": round(float(gini), 4),
        "data": _df_to_records(conc),
    }


@app.get("/api/estacionalidad")
def estacionalidad_endpoint(
    anos: str | None = Query(None),
    tipo_evento: str | None = Query(None),
    departamento: str | None = Query(None),
):
    """Patrón mensual y mes pico."""
    anos_list = _parse_anos(anos)
    df = _get_df(anos=anos_list, tipo_evento=tipo_evento, departamento=departamento)
    if len(df) == 0:
        return {"mes_pico": None, "patron_mensual": []}
    pico = mes_pico(df)
    patron = patron_mensual(df, agregar="promedio_anual")
    patron["mes_nombre"] = patron["mes"].apply(
        lambda m: ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"][int(m)-1]
    )
    # Asegurar que 'promedio' sea float nativo para que JSON no devuelva escalares raros
    patron["promedio"] = patron["promedio"].astype(float)
    return {
        "mes_pico": pico,
        "patron_mensual": _df_to_records(patron),
    }


@app.get("/api/serie-temporal")
def serie_temporal_endpoint(
    anos: str | None = Query(None),
    tipo_evento: str | None = Query(None),
    departamento: str | None = Query(None),
    agrupacion: str = Query("ano", description="ano o mes"),
):
    """Serie temporal para gráfico de líneas."""
    anos_list = _parse_anos(anos)
    df = _get_df(anos=anos_list, tipo_evento=tipo_evento, departamento=departamento)
    if len(df) == 0:
        return {"data": []}
    if agrupacion == "mes":
        df = df.copy()
        df["periodo"] = df["ano"].astype(str) + "-" + df["mes"].astype(str).str.zfill(2)
        res = df.groupby("periodo")["cantidad"].sum().reset_index()
        res = res.rename(columns={"cantidad": "total"})
    else:
        res = df.groupby("ano")["cantidad"].sum().reset_index()
        res = res.rename(columns={"ano": "periodo", "cantidad": "total"})
        res["periodo"] = res["periodo"].astype(str)
    return {"data": _df_to_records(res)}


@app.get("/api/exportar")
def exportar_endpoint(
    anos: str | None = Query(None),
    tipo_evento: str | None = Query(None),
    departamento: str | None = Query(None),
    formato: str = Query("csv", description="csv o excel"),
):
    """Exportar datos filtrados como CSV o Excel."""
    anos_list = _parse_anos(anos)
    df = _get_df(anos=anos_list, tipo_evento=tipo_evento, departamento=departamento)
    if len(df) == 0:
        return {"message": "Sin datos para exportar"}

    df = df.head(100_000)  # Límite para exportación

    if formato == "excel":
        try:
            buffer = BytesIO()
            df.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)
            return StreamingResponse(
                buffer,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=eventos_seguridad.xlsx"},
            )
        except ImportError:
            formato = "csv"

    buffer = BytesIO()
    df.to_csv(buffer, index=False, encoding="utf-8-sig")
    buffer.seek(0)
    return StreamingResponse(
        buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=eventos_seguridad.csv"},
    )
