# Pipeline ETL - Diseño e Implementación

## Arquitectura

```
MINISTERIO DE DEFENSA/*.xlsx
        │
        ▼
┌───────────────────┐
│   EXTRACCIÓN      │  Lectura de Excel, detección de estructura
│   (extractors)    │  Exclusión: INDICADORES (resumen agregado)
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  TRANSFORMACIÓN   │  Normalización de columnas
│  (transformers)   │  Validación temporal (1990-2030)
│                   │  Validación geográfica (DIVIPOLA)
│                   │  Esquema unificado
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│     CARGA         │  Parquet (o CSV si no hay pyarrow)
│   (loaders)       │  data/processed/eventos_seguridad_maestro.*
└───────────────────┘
```

## Esquema del Dataset Maestro

| Columna          | Tipo   | Descripción                              |
|------------------|--------|------------------------------------------|
| `fecha`          | date   | Fecha del hecho                          |
| `ano`            | int16  | Año (para agregaciones)                  |
| `mes`            | int8   | Mes 1-12 (estacionalidad)                |
| `cod_depto`      | string | Código DIVIPOLA departamento (2 dígitos) |
| `cod_muni`       | string | Código DIVIPOLA municipio (5 dígitos)    |
| `departamento`   | string | Nombre departamento                      |
| `municipio`      | string | Nombre municipio                         |
| `tipo_evento`    | string | Categoría (del nombre del archivo)       |
| `cantidad`       | int32  | Víctimas/casos/cantidad                  |
| `archivo_origen` | string | Archivo Excel de origen                  |

## Uso

```bash
# Ejecución estándar
python 02_run_etl.py

# Con configuración personalizada
python 02_run_etl.py --config config/etl.yaml

# Desde otro directorio
python 02_run_etl.py --project-root /ruta/al/proyecto
```

## Configuración

Archivo: `config/etl.yaml`

- **input.base_path**: Directorio con archivos Excel
- **output.base_path**: Directorio de salida
- **exclude_files**: Archivos a excluir (ej. INDICADORES)
- **validation**: Rango temporal válido (min_year, max_year)

## Normalización de Columnas

El ETL detecta automáticamente las variantes de nombres:

| Destino | Variantes en origen |
|---------|---------------------|
| fecha | FECHA_HECHO, FECHA HECHO |
| cantidad | VICTIMAS, CANTIDAD, CASOS, CAPTURAS |
| cod_depto | COD_DEPTO |
| cod_muni | COD_MUNI |

## Validaciones Aplicadas

1. **Temporal**: Fechas entre 1990-2030, sin fechas futuras
2. **Geográfica**: Códigos DIVIPOLA (depto 1-2 dígitos, muni 4-5)
3. **Cantidad**: Valores < 1 se ajustan a 1
4. **Completitud**: Filas sin fecha, cod_depto o cod_muni se eliminan

## Dependencias

- **pyarrow**: Para formato Parquet (recomendado)
- Sin pyarrow: se guarda como CSV automáticamente

```bash
pip install pyarrow  # Para formato Parquet
```
