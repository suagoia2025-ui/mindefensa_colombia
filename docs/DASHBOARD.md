# Dashboard - Documentación

## Arquitectura

```
Frontend (React + Vite)          Backend (FastAPI)
     localhost:5173                  localhost:8000
           │                              │
           │  /api/* (proxy)              │
           └─────────────────────────────┘
                          │
                          ▼
              Dataset maestro (CSV/Parquet)
```

## Inicio rápido

```bash
# 1. Asegurar que existe el dataset maestro
python 02_run_etl.py

# 2. Iniciar backend
python run_dashboard.py

# 3. En otra terminal: iniciar frontend
cd frontend
npm install
npm run dev

# 4. Abrir http://localhost:5173
```

## Endpoints API

| Endpoint | Descripción |
|----------|-------------|
| GET /api/metadata | Años, tipos de evento, departamentos disponibles |
| GET /api/comparacion-anual | Comparación año a año con variación % |
| GET /api/tendencia | Tendencia lineal del período |
| GET /api/departamentos | Top departamentos por cantidad |
| GET /api/tipos-evento | Top tipos de evento |
| GET /api/concentracion | Índice Gini y concentración |
| GET /api/estacionalidad | Patrón mensual, mes pico |
| GET /api/serie-temporal | Serie temporal (por año o mes) |
| GET /api/exportar | Exportar datos filtrados (CSV/Excel) |

## Parámetros de filtro

- `anos`: Años separados por coma (ej: 2020,2021,2022)
- `tipo_evento`: Nombre del tipo de evento
- `departamento`: Nombre del departamento

## Visualizaciones

- **Serie temporal**: Línea con evolución por año
- **Comparación año a año**: Barras por año
- **Top departamentos**: Barras horizontales
- **Top tipos de evento**: Barras horizontales
- **Concentración**: Índice Gini + % acumulado por departamento
- **Estacionalidad**: Patrón mensual promedio

## Exportación

El botón "Exportar CSV" descarga hasta 100.000 registros con los filtros aplicados.

Para Excel: `GET /api/exportar?formato=excel` (requiere openpyxl)
