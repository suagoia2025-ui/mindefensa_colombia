#!/usr/bin/env python3
"""
Script de Descubrimiento de Datos - Análisis de Seguridad Colombia

Analiza todos los archivos Excel en el proyecto y genera un reporte detallado
con: estructura de columnas, rangos temporales, datos faltantes e inconsistencias.

Fuentes: Ministerio de Defensa, DANE, Policía Nacional, Fiscalía
Autor: Sistema de Análisis de Seguridad Colombia
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import warnings
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Extensiones de archivos Excel soportados
EXCEL_EXTENSIONS = {".xlsx", ".xls"}


@dataclass
class ColumnInfo:
    """Información de una columna."""

    name: str
    dtype: str
    non_null_count: int
    null_count: int
    null_pct: float
    sample_values: list[Any] = field(default_factory=list)


@dataclass
class TemporalRange:
    """Rango temporal de los datos."""

    min_date: str | None
    max_date: str | None
    date_column: str | None
    date_format_issues: list[str] = field(default_factory=list)


@dataclass
class GeographicConsistency:
    """Reporte de consistencia geográfica."""

    unique_departments: list[str]
    unique_municipalities_count: int
    divipola_format_issues: list[str] = field(default_factory=list)
    duplicate_names: list[str] = field(default_factory=list)


@dataclass
class SheetReport:
    """Reporte de una hoja de Excel."""

    sheet_name: str
    rows: int
    columns: int
    column_info: list[dict]
    temporal_range: dict
    geographic_info: dict | None
    missing_data_summary: dict
    value_columns: list[str]
    sample_data: list[dict] = field(default_factory=list)


@dataclass
class FileReport:
    """Reporte completo de un archivo Excel."""

    file_path: str
    file_name: str
    file_size_mb: float
    sheets: list[dict]
    total_rows: int
    success: bool
    error: str | None = None
    processing_time_sec: float = 0.0


@dataclass
class DiscoveryReport:
    """Reporte global del descubrimiento."""

    timestamp: str
    search_path: str
    total_files_found: int
    total_files_processed: int
    total_files_failed: int
    file_reports: list[dict]
    summary: dict
    inconsistencies: list[dict] = field(default_factory=list)


def find_excel_files(
    root_path: Path,
    recursive: bool = True,
    xlsx_only: bool = False,
) -> list[Path]:
    """
    Busca todos los archivos Excel en el directorio especificado.

    Args:
        root_path: Ruta raíz de búsqueda
        recursive: Si True, busca en subdirectorios
        xlsx_only: Si True, solo busca .xlsx (evita depender de xlrd para .xls)

    Returns:
        Lista de rutas a archivos Excel
    """
    excel_files: list[Path] = []
    pattern = "**/*" if recursive else "*"
    exts = {".xlsx"} if xlsx_only else EXCEL_EXTENSIONS

    for ext in exts:
        excel_files.extend(root_path.glob(f"{pattern}{ext}"))

    return sorted(excel_files)


def _detect_date_columns(df: pd.DataFrame) -> list[str]:
    """Identifica columnas que contienen fechas."""
    date_cols: list[str] = []
    for col in df.columns:
        if df[col].dtype == "datetime64[ns]":
            date_cols.append(col)
        elif "fecha" in str(col).lower() or "date" in str(col).lower():
            date_cols.append(col)
        elif df[col].dtype == "object" and df[col].notna().any():
            sample = df[col].dropna().head(100)
            if len(sample) > 0:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore", UserWarning)
                        parsed = pd.to_datetime(sample, errors="coerce")
                    if parsed.notna().mean() > 0.5:
                        date_cols.append(col)
                except (ValueError, TypeError):
                    pass
    return date_cols


def _detect_geographic_columns(df: pd.DataFrame) -> dict[str, str]:
    """Identifica columnas geográficas por nombre."""
    geo_map: dict[str, str] = {}
    col_lower = {c.lower(): c for c in df.columns}
    if "departamento" in col_lower:
        geo_map["departamento"] = col_lower["departamento"]
    if "municipio" in col_lower:
        geo_map["municipio"] = col_lower["municipio"]
    if "cod_depto" in col_lower:
        geo_map["cod_depto"] = col_lower["cod_depto"]
    if "cod_muni" in col_lower:
        geo_map["cod_muni"] = col_lower["cod_muni"]
    return geo_map


def _analyze_temporal_range(df: pd.DataFrame, date_cols: list[str]) -> TemporalRange:
    """Analiza el rango temporal de los datos."""
    min_date = None
    max_date = None
    date_column = None
    issues: list[str] = []

    for col in date_cols:
        serie = df[col]
        if serie.dtype == "datetime64[ns]":
            valid = serie.dropna()
            if len(valid) > 0:
                min_date = str(valid.min().date())
                max_date = str(valid.max().date())
                date_column = col
                break
        else:
            try:
                parsed = pd.to_datetime(serie, errors="coerce")
                valid = parsed.dropna()
                if len(valid) > 0:
                    min_date = str(valid.min().date())
                    max_date = str(valid.max().date())
                    date_column = col
                    if parsed.isna().mean() > 0.1:
                        issues.append(f"Columna '{col}': >10% de fechas no parseables")
                    break
            except Exception as e:
                issues.append(f"Columna '{col}': Error al parsear - {e}")

    return TemporalRange(
        min_date=min_date,
        max_date=max_date,
        date_column=date_column,
        date_format_issues=issues,
    )


def _analyze_geographic_consistency(df: pd.DataFrame, geo_cols: dict) -> GeographicConsistency | None:
    """Analiza consistencia de nombres geográficos."""
    if not geo_cols:
        return None

    deptos: list[str] = []
    munis_count = 0
    divipola_issues: list[str] = []
    duplicates: list[str] = []

    if "departamento" in geo_cols:
        deptos = df[geo_cols["departamento"]].dropna().unique().astype(str).tolist()
        deptos = [d.strip() for d in deptos if d and d != "nan"]

    if "municipio" in geo_cols:
        munis = df[geo_cols["municipio"]].dropna()
        munis_count = munis.nunique()

    # Validación básica DIVIPOLA: COD_DEPTO 2 dígitos, COD_MUNI 5 dígitos
    if "cod_depto" in geo_cols:
        cod_col = geo_cols["cod_depto"]
        if cod_col in df.columns:
            serie = df[cod_col].dropna().astype(str).str.strip()
            matches = serie.str.match(r"^\d{1,2}$", na=False)
            if (~matches).sum() > 0:
                divipola_issues.append("COD_DEPTO: códigos con formato distinto a 1-2 dígitos")

    if "cod_muni" in geo_cols:
        cod_col = geo_cols["cod_muni"]
        if cod_col in df.columns:
            serie = df[cod_col].dropna().astype(str).str.strip()
            matches = serie.str.match(r"^\d{4,5}$", na=False)
            if (~matches).sum() > 0:
                divipola_issues.append("COD_MUNI: códigos con formato distinto a 4-5 dígitos")

    return GeographicConsistency(
        unique_departments=sorted(deptos)[:50],
        unique_municipalities_count=int(munis_count),
        divipola_format_issues=divipola_issues,
        duplicate_names=duplicates,
    )


def _identify_value_columns(df: pd.DataFrame) -> list[str]:
    """Identifica columnas numéricas que representan conteos/cantidades."""
    value_keywords = ["victimas", "cantidad", "casos", "total", "valor", "hectareas"]
    value_cols: list[str] = []
    for col in df.columns:
        col_lower = str(col).lower()
        if any(kw in col_lower for kw in value_keywords):
            value_cols.append(col)
        elif pd.api.types.is_numeric_dtype(df[col]):
            value_cols.append(col)
    return value_cols


def analyze_sheet(df: pd.DataFrame, sheet_name: str, sample_size: int = 5) -> SheetReport:
    """
    Analiza una hoja de Excel y genera su reporte.

    Args:
        df: DataFrame con los datos
        sheet_name: Nombre de la hoja
        sample_size: Cantidad de filas de muestra

    Returns:
        SheetReport con la información analizada
    """
    # Info de columnas
    column_info: list[dict] = []
    for col in df.columns:
        null_count = int(df[col].isna().sum())
        non_null = int(df[col].notna().sum())
        null_pct = round(100 * null_count / len(df), 2) if len(df) > 0 else 0
        sample = df[col].dropna().head(5).tolist()
        column_info.append(
            asdict(
                ColumnInfo(
                    name=col,
                    dtype=str(df[col].dtype),
                    non_null_count=non_null,
                    null_count=null_count,
                    null_pct=null_pct,
                    sample_values=[str(v)[:50] for v in sample],
                )
            )
        )

    # Columnas de fecha
    date_cols = _detect_date_columns(df)
    temporal = _analyze_temporal_range(df, date_cols)

    # Columnas geográficas
    geo_cols = _detect_geographic_columns(df)
    geo_info = _analyze_geographic_consistency(df, geo_cols)

    # Valor/medida
    value_cols = _identify_value_columns(df)

    # Resumen datos faltantes
    missing_summary = {
        "total_rows": len(df),
        "columns_with_nulls": sum(1 for c in column_info if c["null_count"] > 0),
        "columns_fully_null": sum(1 for c in column_info if c["null_count"] == len(df)),
    }

    # Muestra de datos
    sample_data = (
        df.head(sample_size).fillna("").astype(str).to_dict(orient="records")
        if len(df) > 0
        else []
    )

    return SheetReport(
        sheet_name=sheet_name,
        rows=len(df),
        columns=len(df.columns),
        column_info=column_info,
        temporal_range=asdict(temporal),
        geographic_info=asdict(geo_info) if geo_info else None,
        missing_data_summary=missing_summary,
        value_columns=value_cols,
        sample_data=sample_data,
    )


def analyze_excel_file(file_path: Path) -> FileReport:
    """
    Analiza un archivo Excel completo (todas las hojas).

    Args:
        file_path: Ruta al archivo

    Returns:
        FileReport con el análisis completo
    """
    start = datetime.now()
    file_name = file_path.name
    rel_path = str(file_path)

    try:
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
    except OSError:
        file_size_mb = 0.0

    try:
        xl = pd.ExcelFile(file_path)
        sheets_data: list[dict] = []
        total_rows = 0

        for sheet_name in xl.sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                if len(df) == 0 and df.shape[1] == 0:
                    continue
                report = analyze_sheet(df, sheet_name)
                sheets_data.append(asdict(report))
                total_rows += report.rows
            except Exception as e:
                logger.warning("Error en hoja %s de %s: %s", sheet_name, file_name, e)
                sheets_data.append(
                    {
                        "sheet_name": sheet_name,
                        "error": str(e),
                        "rows": 0,
                        "columns": 0,
                    }
                )

        elapsed = (datetime.now() - start).total_seconds()
        return FileReport(
            file_path=rel_path,
            file_name=file_name,
            file_size_mb=round(file_size_mb, 2),
            sheets=sheets_data,
            total_rows=total_rows,
            success=True,
            processing_time_sec=round(elapsed, 2),
        )

    except Exception as e:
        logger.error("Error procesando %s: %s", file_name, e)
        elapsed = (datetime.now() - start).total_seconds()
        return FileReport(
            file_path=rel_path,
            file_name=file_name,
            file_size_mb=round(file_size_mb, 2),
            sheets=[],
            total_rows=0,
            success=False,
            error=str(e),
            processing_time_sec=round(elapsed, 2),
        )


def collect_inconsistencies(reports: list[FileReport]) -> list[dict]:
    """Recopila inconsistencias detectadas en todos los archivos."""
    inconsistencies: list[dict] = []
    all_deptos: set[str] = set()
    all_columns: dict[str, set] = {}

    for report in reports:
        if not report.success:
            inconsistencies.append(
                {"type": "file_error", "file": report.file_name, "error": report.error}
            )
            continue

        for sheet in report.sheets:
            if "error" in sheet:
                continue

            # Inconsistencias de fecha
            tr = sheet.get("temporal_range", {})
            if tr.get("date_format_issues"):
                for issue in tr["date_format_issues"]:
                    inconsistencies.append(
                        {
                            "type": "date_format",
                            "file": report.file_name,
                            "sheet": sheet.get("sheet_name"),
                            "detail": issue,
                        }
                    )

            # Inconsistencias DIVIPOLA
            geo = sheet.get("geographic_info")
            if geo and geo.get("divipola_format_issues"):
                for issue in geo["divipola_format_issues"]:
                    inconsistencies.append(
                        {
                            "type": "divipola_format",
                            "file": report.file_name,
                            "sheet": sheet.get("sheet_name"),
                            "detail": issue,
                        }
                    )

            # Acumular departamentos para detectar variaciones de nombre
            if geo and geo.get("unique_departments"):
                for d in geo["unique_departments"]:
                    all_deptos.add(d)

            # Variación de columnas entre archivos del mismo tipo
            cols = tuple(sorted(c["name"] for c in sheet.get("column_info", [])))
            key = report.file_name[:30]
            if key not in all_columns:
                all_columns[key] = set()
            all_columns[key].add(cols)

    return inconsistencies


def generate_markdown_report(discovery: DiscoveryReport) -> str:
    """Genera el reporte en formato Markdown."""
    lines: list[str] = []
    lines.append("# Reporte de Descubrimiento de Datos")
    lines.append("")
    lines.append(f"**Fecha de generación:** {discovery.timestamp}")
    lines.append(f"**Ruta de búsqueda:** {discovery.search_path}")
    lines.append("")
    lines.append("## Resumen Ejecutivo")
    lines.append("")
    lines.append("| Métrica | Valor |")
    lines.append("|---------|-------|")
    lines.append(f"| Archivos Excel encontrados | {discovery.total_files_found} |")
    lines.append(f"| Archivos procesados exitosamente | {discovery.total_files_processed} |")
    lines.append(f"| Archivos con errores | {discovery.total_files_failed} |")
    lines.append(f"| Total de registros | {discovery.summary.get('total_records', 0):,} |")
    lines.append(f"| Inconsistencias detectadas | {len(discovery.inconsistencies)} |")
    lines.append("")

    if discovery.inconsistencies:
        lines.append("## Inconsistencias Detectadas")
        lines.append("")
        for inc in discovery.inconsistencies[:20]:
            lines.append(f"- **{inc.get('type', 'N/A')}** ({inc.get('file', '')}): {inc.get('detail', inc.get('error', ''))}")
        if len(discovery.inconsistencies) > 20:
            lines.append(f"- ... y {len(discovery.inconsistencies) - 20} más")
        lines.append("")

    lines.append("## Detalle por Archivo")
    lines.append("")

    for report in discovery.file_reports:
        lines.append(f"### {report['file_name']}")
        lines.append("")
        lines.append(f"- **Ruta:** {report['file_path']}")
        lines.append(f"- **Tamaño:** {report['file_size_mb']} MB")
        lines.append(f"- **Estado:** {'✓ OK' if report['success'] else '✗ ERROR'}")
        if report.get("error"):
            lines.append(f"- **Error:** {report['error']}")
        lines.append(f"- **Total filas:** {report['total_rows']:,}")
        lines.append(f"- **Tiempo procesamiento:** {report.get('processing_time_sec', 0)} s")
        lines.append("")

        for sheet in report.get("sheets", []):
            if "error" in sheet:
                lines.append(f"#### Hoja: {sheet.get('sheet_name')} - ERROR: {sheet['error']}")
            else:
                lines.append(f"#### Hoja: {sheet.get('sheet_name')}")
                lines.append(f"- Filas: {sheet.get('rows', 0):,} | Columnas: {sheet.get('columns', 0)}")
                tr = sheet.get("temporal_range", {})
                if tr.get("min_date") and tr.get("max_date"):
                    lines.append(f"- **Rango temporal:** {tr['min_date']} a {tr['max_date']} (col: {tr.get('date_column', 'N/A')})")
                geo = sheet.get("geographic_info")
                if geo:
                    lines.append(f"- **Departamentos únicos:** {len(geo.get('unique_departments', []))}")
                    lines.append(f"- **Municipios únicos:** {geo.get('unique_municipalities_count', 0)}")
                lines.append("")
                lines.append("**Columnas:**")
                for col in sheet.get("column_info", [])[:15]:
                    lines.append(f"- `{col['name']}` ({col['dtype']}) - Nulos: {col['null_pct']}%")
                if len(sheet.get("column_info", [])) > 15:
                    lines.append(f"- ... y {len(sheet['column_info']) - 15} columnas más")
            lines.append("")

    return "\n".join(lines)


def run_discovery(
    root_path: Path,
    output_dir: Path,
    output_json: bool = True,
    output_md: bool = True,
    recursive: bool = True,
    xlsx_only: bool = False,
) -> DiscoveryReport:
    """
    Ejecuta el descubrimiento completo de datos.

    Args:
        root_path: Ruta raíz del proyecto
        output_dir: Directorio para guardar reportes
        output_json: Si True, guarda reporte JSON
        output_md: Si True, guarda reporte Markdown
        recursive: Si True, busca en subdirectorios

    Returns:
        DiscoveryReport con todos los resultados
    """
    logger.info("Iniciando descubrimiento de datos en %s", root_path)
    excel_files = find_excel_files(root_path, recursive=recursive, xlsx_only=xlsx_only)
    logger.info("Encontrados %d archivos Excel", len(excel_files))

    if not excel_files:
        logger.warning("No se encontraron archivos Excel")
        return DiscoveryReport(
            timestamp=datetime.now().isoformat(),
            search_path=str(root_path),
            total_files_found=0,
            total_files_processed=0,
            total_files_failed=0,
            file_reports=[],
            summary={},
        )

    file_reports: list[FileReport] = []
    for i, fp in enumerate(excel_files, 1):
        logger.info("[%d/%d] Procesando %s", i, len(excel_files), fp.name)
        report = analyze_excel_file(fp)
        file_reports.append(report)

    successful = [r for r in file_reports if r.success]
    failed = [r for r in file_reports if not r.success]
    total_records = sum(r.total_rows for r in successful)
    inconsistencies = collect_inconsistencies(file_reports)

    discovery = DiscoveryReport(
        timestamp=datetime.now().isoformat(),
        search_path=str(root_path),
        total_files_found=len(excel_files),
        total_files_processed=len(successful),
        total_files_failed=len(failed),
        file_reports=[asdict(r) for r in file_reports],
        summary={
            "total_records": total_records,
            "total_size_mb": round(sum(r.file_size_mb for r in file_reports), 2),
        },
        inconsistencies=inconsistencies,
    )

    output_dir.mkdir(parents=True, exist_ok=True)

    if output_json:
        json_path = output_dir / "data_discovery_report.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(asdict(discovery), f, indent=2, ensure_ascii=False)
        logger.info("Reporte JSON guardado en %s", json_path)

    if output_md:
        md_path = output_dir / "data_discovery_report.md"
        md_content = generate_markdown_report(discovery)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        logger.info("Reporte Markdown guardado en %s", md_path)

    return discovery


def main() -> int:
    """Punto de entrada principal."""
    parser = argparse.ArgumentParser(
        description="Descubrimiento de datos - Análisis de Seguridad Colombia"
    )
    parser.add_argument(
        "--path",
        type=Path,
        default=Path.cwd(),
        help="Ruta raíz para buscar archivos Excel (default: directorio actual)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs"),
        help="Directorio para guardar reportes (default: docs/)",
    )
    parser.add_argument(
        "--no-json",
        action="store_true",
        help="No generar reporte JSON",
    )
    parser.add_argument(
        "--no-md",
        action="store_true",
        help="No generar reporte Markdown",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="No buscar en subdirectorios",
    )
    parser.add_argument(
        "--xlsx-only",
        action="store_true",
        help="Solo procesar archivos .xlsx (útil si xlrd no está instalado para .xls)",
    )

    args = parser.parse_args()

    if not args.path.exists():
        logger.error("La ruta %s no existe", args.path)
        return 1

    run_discovery(
        root_path=args.path,
        output_dir=args.output,
        output_json=not args.no_json,
        output_md=not args.no_md,
        recursive=not args.no_recursive,
        xlsx_only=args.xlsx_only,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
