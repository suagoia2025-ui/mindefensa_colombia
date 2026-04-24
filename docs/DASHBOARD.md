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

## Docker y nginx (timeouts de proxy)

Con **Docker Compose**, el frontend se sirve con **nginx** (`frontend/nginx.conf`) y las peticiones a `/api/` se reenvían al contenedor `api:8000`. Las consultas con muchos años pueden tardar varios minutos; los valores por defecto de nginx suelen cortar antes y devolver **502 Bad Gateway**.

En `location /api/` están definidos (valores actuales del repo):

| Directiva | Valor | Rol |
|-----------|--------|-----|
| `proxy_connect_timeout` | 300s | Tiempo máximo para establecer conexión con el upstream |
| `proxy_send_timeout` | 600s | Tiempo máximo para enviar el cuerpo de la petición al upstream |
| `proxy_read_timeout` | 600s | Tiempo máximo de espera de la **respuesta** del upstream (lo más relevante para consultas pesadas) |

Tras cambiar `nginx.conf`, hay que **reconstruir** la imagen del frontend para que el contenedor use la nueva configuración.

En **desarrollo local** (`npm run dev`), Vite hace de proxy hacia `http://localhost:8000` con `timeout` y `proxyTimeout` de **600_000 ms** (10 minutos) en `frontend/vite.config.ts`, en la misma línea de evitar cortes por espera larga.

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
| GET /api/comparacion-anual | Comparación año a año con variación % (API disponible; el UI del dashboard no usa este endpoint) |
| GET /api/tendencia | Tendencia lineal del período |
| GET /api/departamentos | Top departamentos por cantidad |
| GET /api/tipos-evento | Top tipos de evento (API disponible; el dashboard actual no muestra este gráfico) |
| GET /api/concentracion | Índice Gini y concentración |
| GET /api/estacionalidad | Patrón mensual, mes pico |
| GET /api/serie-temporal | Serie temporal (por año o mes) |
| GET /api/exportar | Exportar datos filtrados (CSV/Excel) |

## Parámetros de filtro

- `anos`: Años separados por coma (ej: 2020,2021,2022)
- `tipo_evento`: Nombre del tipo de evento
- `departamento`: Nombre del departamento

En el **frontend** actual, si no se aplica un `tipo_evento` concreto (equivalente a «Todos» en el desplegable), **no se llaman** los endpoints de gráficos y los paneles quedan vacíos hasta que el usuario elige un tipo y pulsa **Graficar**.

## Visualizaciones

- **Serie temporal**: Línea con evolución por año (o mes, según API)
- **Top departamentos**: Barras horizontales
- **Concentración**: Índice Gini + % acumulado por departamento
- **Estacionalidad**: Patrón mensual promedio

## Exportación

El botón "Exportar CSV" descarga hasta 100.000 registros con los filtros aplicados.

Para Excel: `GET /api/exportar?formato=excel` (requiere openpyxl)

## Textos de la interfaz

Las cadenas visibles del dashboard (español) están centralizadas en `frontend/src/config/messages.ts` (`export const ui`). Las URLs externas quedan en `frontend/src/config/externalLinks.ts`.
