# Módulo de Análisis - Diseño

## Objetivo

Proporcionar análisis estadístico sobre el dataset maestro de seguridad para:
- Comparaciones año a año
- Tendencias temporales
- Concentración geográfica
- Patrones estacionales

**Fuente:** Ministerio de Defensa Colombia - Datos de criminalidad y violencia  
**Scope actual:** Análisis central (sin tasas por 100k ni impacto económico)

---

## Arquitectura

```
data/processed/eventos_seguridad_maestro.*
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                 data_loader.py                           │
│  Carga dataset, filtros (año, depto, tipo_evento)       │
└─────────────────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┬───────────────┐
        ▼           ▼           ▼               ▼
┌─────────────┐ ┌──────────┐ ┌─────────────┐ ┌──────────────┐
│ tendencias  │ │agregacio-│ │ concentracion│ │ estacionalidad│
│             │ │   nes    │ │              │ │              │
│ • YoY       │ │ • Depto  │ │ • Índice     │ │ • Mensual    │
│ • Tendencia │ │ • Munici-│ │   Gini       │ │ • Trimestral │
│   lineal    │ │   pio    │ │ • Top N %    │ │ • Mes típico │
│ • Variación │ │ • Evento │ │   territorios│ │   de pico    │
└─────────────┘ └──────────┘ └─────────────┘ └──────────────┘
```

---

## Componentes

### 1. Comparaciones año a año (tendencias.py)

| Función | Descripción | Salida |
|---------|-------------|--------|
| `comparacion_anual()` | Total por año, variación % vs año anterior | DataFrame año, total, var_pct |
| `tendencia_lineal()` | Regresión simple para dirección de tendencia | pendiente, R², dirección |
| `resumen_por_periodo()` | Agregado por año y tipo de evento | DataFrame pivot |

### 2. Agregaciones (agregaciones.py)

| Función | Descripción | Salida |
|---------|-------------|--------|
| `por_departamento()` | Conteo por departamento, con ranking | DataFrame con % del total |
| `por_municipio()` | Conteo por municipio (opcional: top N) | DataFrame |
| `por_tipo_evento()` | Conteo por categoría de delito | DataFrame |
| `cruze_territorio_evento()` | Depto x Tipo evento (pivot) | DataFrame |

### 3. Índices de concentración (concentracion.py)

| Función | Descripción | Salida |
|---------|-------------|--------|
| `indice_gini()` | Concentración territorial (0=uniforme, 1=max concentración) | float |
| `top_n_concentracion()` | % del total acumulado por top N departamentos | DataFrame |
| `ranking_municipios()` | Municipios con mayor carga, % acumulado | DataFrame |

### 4. Patrones estacionales (estacionalidad.py)

| Función | Descripción | Salida |
|---------|-------------|--------|
| `patron_mensual()` | Promedio por mes (1-12) en el período | DataFrame |
| `patron_trimestral()` | Agregado por trimestre | DataFrame |
| `mes_pico()` | Mes con mayor incidencia histórica | int, mes_nombre |
| `estacionalidad_por_tipo()` | Patrón mensual por tipo de evento | DataFrame |

---

## API de uso

```python
from src.analysis import load_maestro, comparacion_anual, por_departamento

# Cargar datos (con filtros opcionales)
df = load_maestro(anos=[2020, 2021, 2022], tipo_evento="HOMICIDIO INTENCIONAL")

# Comparación año a año
result = comparacion_anual(df)

# Top departamentos
deptos = por_departamento(df, top_n=10)
```

---

## Consideraciones de neutralidad

- Presentar datos objetivos sin interpretaciones políticas
- Incluir metadatos: fechas de datos, fuente, limitaciones
- Permitir al usuario sacar sus propias conclusiones
