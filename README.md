
# Sistema de Análisis de Seguridad Colombia

Sistema de análisis de datos del Ministerio de Defensa de Colombia para evaluar el estado de seguridad y violencia comparado con años anteriores.

## Estructura del Proyecto

```
├── config/               # YAML de ETL y unidades (p. ej. etl.yaml)
├── data/
│   ├── raw/              # Archivos Excel originales sin modificar
│   ├── processed/        # Datos procesados y normalizados
│   └── schemas/          # Definición de estructuras de datos
├── src/
│   ├── etl/              # Extracción, transformación y carga
│   ├── analysis/         # Módulos de análisis estadístico
│   ├── config/           # Unidades por tipo de evento (Python)
│   └── api/              # Backend API (FastAPI)
├── frontend/             # Dashboard React + Vite
├── docs/                 # Documentación y reportes generados
├── 01_data_discovery.py
├── 02_run_etl.py
├── 03_run_analysis.py
└── run_dashboard.py
```

## Instalación

```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias para archivos .xls (DANE PIB)

Para procesar archivos Excel legacy (.xls), instalar:

```bash
pip install xlrd>=2.0.0
```

## Pipeline ETL

Consolida los archivos Excel del Ministerio de Defensa en un dataset maestro:

```bash
python 02_run_etl.py
```

- **Entrada**: `MINISTERIO DE DEFENSA/*.xlsx` (excluye INDICADORES)
- **Salida**: `data/processed/eventos_seguridad_maestro.parquet` (o .csv si no hay pyarrow)
- **Además (con PyArrow)**: `data/processed/partitions/*.parquet` por indicador y `data/processed/catalog.json` para carga rápida en la API
- **Resultado**: ~7.4M registros normalizados con esquema unificado

Para formato Parquet: `pip install pyarrow`

Si ya tienes el maestro y solo faltan particiones + catálogo: `python scripts/rebuild_partitions.py`

Ver `docs/ETL_PIPELINE.md` para diseño detallado.

## Módulo de Análisis

Análisis estadístico sobre el dataset maestro:

```bash
python 03_run_analysis.py
python 03_run_analysis.py --anos 2020 2021 2022 2023
python 03_run_analysis.py --tipo "HOMICIDIO INTENCIONAL"
python 03_run_analysis.py --output data/processed/analisis_resultados.json
```

Incluye: comparación año a año, tendencia lineal, top departamentos/tipos, índice Gini, mes pico.

Ver `docs/ANALISIS_MODULO_DISEÑO.md` para diseño.

## Dashboard interactivo

Dashboard web con **React 19 + Vite 7 + TypeScript + Tailwind CSS v4** (tema oscuro, paleta copper) y **Recharts**. Backend **FastAPI + Pandas**.

```bash
# Terminal 1: Backend API
python run_dashboard.py

# Terminal 2: Frontend React
cd frontend
npm install
npm run dev
```

Abrir **http://localhost:5173**

**Funcionalidades:** Serie temporal, top departamentos, concentración (Gini), estacionalidad. Filtros por año (2002–2025), tipo de evento y departamento; hay que elegir un **tipo de evento concreto** y pulsar **Graficar** (con «Todos» los gráficos permanecen vacíos). Exportar CSV. En la cabecera hay enlace a los datos oficiales en Excel del MinDefensa.

**Instrucciones de uso:** Ver [docs/COMO_USAR_EL_DASHBOARD.md](docs/COMO_USAR_EL_DASHBOARD.md).

### Ejecución con Docker

Para levantar el dashboard con contenedores (API + frontend con nginx):

```bash
# Asegurar que existan los datos procesados (una vez)
python 02_run_etl.py

# Construir y levantar
docker compose up --build
```

- **Dashboard:** http://localhost (puerto 80)
- **API directa:** http://localhost:8000

La carpeta `data/` se monta como volumen; el backend lee `data/processed/eventos_seguridad_maestro.csv` (o .parquet). Detener: `docker compose down`.

**Producción (EC2 / demo):** guía de arquitectura, `docker-compose.prod.yml`, variables y checklist en [docs/deployment.md](docs/deployment.md). En el servidor: copiar `.env.production.example` a `.env.production` y ajustar `ALLOWED_ORIGINS`.

**Demo pública (Elastic IP):** en los archivos del repo sustituye el marcador `TU_ELASTIC_IP` por la **IPv4 pública** que muestra EC2 (sin `http://` en los comandos; sí en las URLs).

| Recurso | URL |
|---------|-----|
| Dashboard | `http://TU_ELASTIC_IP/` |
| Metadatos API | `http://TU_ELASTIC_IP/api/metadata` |
| Salud API | `http://TU_ELASTIC_IP/api/health` |

Pasos para dejar todo alineado con la IP: ver [docs/deployment.md](docs/deployment.md) → sección **Tras asignar Elastic IP**.

---

## Uso del Script de Descubrimiento

El script `01_data_discovery.py` analiza todos los archivos Excel del proyecto y genera un reporte detallado.

### Ejecución básica

```bash
python 01_data_discovery.py
```

### Opciones

| Opción | Descripción |
|--------|-------------|
| `--path RUTA` | Ruta raíz para buscar archivos (default: directorio actual) |
| `--output RUTA` | Directorio para guardar reportes (default: docs/) |
| `--no-json` | No generar reporte JSON |
| `--no-md` | No generar reporte Markdown |
| `--no-recursive` | No buscar en subdirectorios |
| `--xlsx-only` | Solo procesar .xlsx (útil sin xlrd instalado) |

### Ejemplos

```bash
# Solo archivos del Ministerio de Defensa (.xlsx)
python 01_data_discovery.py --xlsx-only

# Buscar solo en carpeta específica
python 01_data_discovery.py --path "MINISTERIO DE DEFENSA" --output docs

# Guardar reportes en data/processed
python 01_data_discovery.py --output data/processed
```

### Reportes generados

- **docs/data_discovery_report.md** – Reporte legible con resumen ejecutivo, inconsistencias y detalle por archivo
- **docs/data_discovery_report.json** – Datos estructurados para procesamiento automatizado

## Fuentes de Datos

- **Ministerio de Defensa de Colombia**: Indicadores de seguridad, homicidios, hurtos, erradicación, etc.
- **DANE**: PIB y datos económicos (carpeta DANE PIB)
- **Policía Nacional**
- **Fiscalía General de la Nación**

## Consideraciones de Neutralidad

- Los datos se presentan de forma objetiva sin interpretaciones políticas
- Se incluyen intervalos de confianza y limitaciones metodológicas
- Se citan fuentes oficiales
- El usuario puede sacar sus propias conclusiones

## Licencia

Proyecto de análisis para uso interno/investigación.
