# Reporte de Descubrimiento de Datos

**Fecha de generación:** 2026-02-07T12:33:43.904795
**Ruta de búsqueda:** /Users/ricardo_suarez1983/Analisis_defensa_colombia

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| Archivos Excel encontrados | 42 |
| Archivos procesados exitosamente | 42 |
| Archivos con errores | 0 |
| Total de registros | 7,415,628 |
| Inconsistencias detectadas | 20 |

## Inconsistencias Detectadas

- **divipola_format** (DESVINCULADOS.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **divipola_format** (HURTO PERSONAS.xlsx): COD_DEPTO: códigos con formato distinto a 1-2 dígitos
- **divipola_format** (HURTO PERSONAS.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **divipola_format** (INCAUTACIONES MINERIA.xlsx): COD_DEPTO: códigos con formato distinto a 1-2 dígitos
- **divipola_format** (INCAUTACIONES MINERIA.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **divipola_format** (INCAUTACIÓN DE BASE DE COCA.xlsx): COD_DEPTO: códigos con formato distinto a 1-2 dígitos
- **divipola_format** (INCAUTACIÓN DE BASE DE COCA.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **divipola_format** (INCAUTACIÓN DE COCAINA.xlsx): COD_DEPTO: códigos con formato distinto a 1-2 dígitos
- **divipola_format** (INCAUTACIÓN DE COCAINA.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **divipola_format** (INCAUTACIÓN DE HEROINA.xlsx): COD_DEPTO: códigos con formato distinto a 1-2 dígitos
- **divipola_format** (INCAUTACIÓN DE HEROINA.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **divipola_format** (INCAUTACIÓN DE MARIHUANA.xlsx): COD_DEPTO: códigos con formato distinto a 1-2 dígitos
- **divipola_format** (INCAUTACIÓN DE MARIHUANA.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **date_format** (INDICADORES DE SEGUR Y RESULT OPER ENERO-DICIEMBRE 2025.xlsx): Columna 'Unnamed: 2': >10% de fechas no parseables
- **date_format** (INDICADORES DE SEGUR Y RESULT OPER ENERO-DICIEMBRE 2025.xlsx): Columna 'Unnamed: 2': >10% de fechas no parseables
- **divipola_format** (INSUMOS LIQUIDOS.xlsx): COD_DEPTO: códigos con formato distinto a 1-2 dígitos
- **divipola_format** (INSUMOS LIQUIDOS.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **divipola_format** (INSUMOS SOLIDOS.xlsx): COD_DEPTO: códigos con formato distinto a 1-2 dígitos
- **divipola_format** (INSUMOS SOLIDOS.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos
- **divipola_format** (LESIONES ACCIDENTES DE TRÁNSITO.xlsx): COD_MUNI: códigos con formato distinto a 4-5 dígitos

## Detalle por Archivo

### AFECTACIÓN A LA FUERZA PÚBLICA.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/AFECTACIÓN A LA FUERZA PÚBLICA.xlsx
- **Tamaño:** 0.81 MB
- **Estado:** ✓ OK
- **Total filas:** 21,038
- **Tiempo procesamiento:** 0.86 s

#### Hoja: AFECTACION A LA FUERZA PÚBLICA
- Filas: 21,038 | Columnas: 8
- **Rango temporal:** 2010-01-01 a 2025-12-27 (col: FECHA HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 835

**Columnas:**
- `FECHA HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `NOMBRE_FUERZA` (object) - Nulos: 0.0%
- `ACCION` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### ASPERSION.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/ASPERSION.xlsx
- **Tamaño:** 0.41 MB
- **Estado:** ✓ OK
- **Total filas:** 9,889
- **Tiempo procesamiento:** 0.26 s

#### Hoja: ASPERSION
- Filas: 9,889 | Columnas: 7
- **Rango temporal:** 2003-01-01 a 2015-09-30 (col: FECHA HECHO)
- **Departamentos únicos:** 24
- **Municipios únicos:** 269

**Columnas:**
- `FECHA HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDADES DE MEDIDA` (object) - Nulos: 0.0%

### CAPTURAS POR MINERÍA ILEGAL.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/CAPTURAS POR MINERÍA ILEGAL.xlsx
- **Tamaño:** 0.19 MB
- **Estado:** ✓ OK
- **Total filas:** 5,845
- **Tiempo procesamiento:** 0.15 s

#### Hoja: Sheet 1
- Filas: 5,845 | Columnas: 7
- **Rango temporal:** 2010-08-09 a 2025-12-28 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 681

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CAPTURAS` (int64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### DELITOS CONTRA EL MEDIO AMBIENTE.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/DELITOS CONTRA EL MEDIO AMBIENTE.xlsx
- **Tamaño:** 2.43 MB
- **Estado:** ✓ OK
- **Total filas:** 81,825
- **Tiempo procesamiento:** 2.08 s

#### Hoja: Sheet 1
- Filas: 81,825 | Columnas: 8
- **Rango temporal:** 2003-01-01 a 2025-12-24 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1013

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `DESCRIPCION CONDUCTA` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### DELITOS INFORMÁTICOS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/DELITOS INFORMÁTICOS.xlsx
- **Tamaño:** 11.5 MB
- **Estado:** ✓ OK
- **Total filas:** 456,520
- **Tiempo procesamiento:** 11.38 s

#### Hoja: Sheet 1
- Filas: 456,520 | Columnas: 7
- **Rango temporal:** 2006-05-13 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1013

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `DESCRIPCION CONDUCTA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### DELITOS SEXUALES.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/DELITOS SEXUALES.xlsx
- **Tamaño:** 12.21 MB
- **Estado:** ✓ OK
- **Total filas:** 426,533
- **Tiempo procesamiento:** 10.89 s

#### Hoja: Sheet 1
- Filas: 426,533 | Columnas: 8
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1030

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `SEXO` (object) - Nulos: 0.23%
- `CANTIDAD` (int64) - Nulos: 0.0%

### DESMOVILIZADOS ELN.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/DESMOVILIZADOS ELN.xlsx
- **Tamaño:** 0.2 MB
- **Estado:** ✓ OK
- **Total filas:** 5,261
- **Tiempo procesamiento:** 0.17 s

#### Hoja: DESMOVILIZADOS ELN
- Filas: 5,261 | Columnas: 7
- **Rango temporal:** 2002-08-08 a 2025-08-06 (col: FECHA HECHO)
- **Departamentos únicos:** 30
- **Municipios únicos:** 357

**Columnas:**
- `FECHA HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `GRUPO` (object) - Nulos: 0.0%
- `CANTIDAD ` (int64) - Nulos: 0.0%

### DESVINCULADOS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/DESVINCULADOS.xlsx
- **Tamaño:** 0.25 MB
- **Estado:** ✓ OK
- **Total filas:** 6,549
- **Tiempo procesamiento:** 0.19 s

#### Hoja: DESVINCULADOS
- Filas: 6,549 | Columnas: 7
- **Rango temporal:** 2003-01-01 a 2025-08-25 (col: FECHA HECHO)
- **Departamentos únicos:** 32
- **Municipios únicos:** 481

**Columnas:**
- `FECHA HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.03%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.03%
- `GRUPO` (object) - Nulos: 0.0%
- `CANTIDAD ` (int64) - Nulos: 0.0%

### ERRADICACIÓN.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/ERRADICACIÓN.xlsx
- **Tamaño:** 4.65 MB
- **Estado:** ✓ OK
- **Total filas:** 145,336
- **Tiempo procesamiento:** 3.62 s

#### Hoja: Sheet 1
- Filas: 145,336 | Columnas: 8
- **Rango temporal:** 2007-01-01 a 2025-12-18 (col: FECHA_HECHO)
- **Departamentos únicos:** 28
- **Municipios únicos:** 489

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `TIPO CULTIVO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### EXTORSIÓN.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/EXTORSIÓN.xlsx
- **Tamaño:** 2.79 MB
- **Estado:** ✓ OK
- **Total filas:** 121,252
- **Tiempo procesamiento:** 2.4 s

#### Hoja: Sheet 1
- Filas: 121,252 | Columnas: 6
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1004

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### HOJA DE COCA.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HOJA DE COCA.xlsx
- **Tamaño:** 0.49 MB
- **Estado:** ✓ OK
- **Total filas:** 16,557
- **Tiempo procesamiento:** 0.37 s

#### Hoja: Sheet 1
- Filas: 16,557 | Columnas: 7
- **Rango temporal:** 2010-01-03 a 2025-12-30 (col: FECHA_HECHO)
- **Departamentos únicos:** 30
- **Municipios únicos:** 310

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### HOMICIDIO ACCIDENTES DE TRÁNSITO.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HOMICIDIO ACCIDENTES DE TRÁNSITO.xlsx
- **Tamaño:** 2.81 MB
- **Estado:** ✓ OK
- **Total filas:** 121,716
- **Tiempo procesamiento:** 2.3 s

#### Hoja: Sheet 1
- Filas: 121,716 | Columnas: 6
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 998

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### HOMICIDIO INTENCIONAL.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HOMICIDIO INTENCIONAL.xlsx
- **Tamaño:** 9.4 MB
- **Estado:** ✓ OK
- **Total filas:** 334,537
- **Tiempo procesamiento:** 9.76 s

#### Hoja: Sheet 1
- Filas: 334,537 | Columnas: 8
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1024

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `SEXO` (object) - Nulos: 0.0%
- `VICTIMAS` (int64) - Nulos: 0.0%

### HURTO A COMERCIO.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HURTO A COMERCIO.xlsx
- **Tamaño:** 14.35 MB
- **Estado:** ✓ OK
- **Total filas:** 660,655
- **Tiempo procesamiento:** 13.48 s

#### Hoja: Sheet 1
- Filas: 660,655 | Columnas: 6
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1025

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### HURTO A RESIDENCIAS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HURTO A RESIDENCIAS.xlsx
- **Tamaño:** 15.11 MB
- **Estado:** ✓ OK
- **Total filas:** 599,316
- **Tiempo procesamiento:** 16.73 s

#### Hoja: Sheet 1
- Filas: 599,316 | Columnas: 7
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1023

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### HURTO ABIGEATO.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HURTO ABIGEATO.xlsx
- **Tamaño:** 1.36 MB
- **Estado:** ✓ OK
- **Total filas:** 49,192
- **Tiempo procesamiento:** 1.11 s

#### Hoja: Sheet 1
- Filas: 49,192 | Columnas: 7
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 32
- **Municipios únicos:** 956

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### HURTO DE VEHÍCULOS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HURTO DE VEHÍCULOS.xlsx
- **Tamaño:** 11.05 MB
- **Estado:** ✓ OK
- **Total filas:** 374,164
- **Tiempo procesamiento:** 10.4 s

#### Hoja: Sheet 1
- Filas: 374,164 | Columnas: 8
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 984

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CLASE BIEN HURTO` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### HURTO ENTIDADES FINANCIERAS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HURTO ENTIDADES FINANCIERAS.xlsx
- **Tamaño:** 0.08 MB
- **Estado:** ✓ OK
- **Total filas:** 2,518
- **Tiempo procesamiento:** 0.1 s

#### Hoja: Sheet 1
- Filas: 2,518 | Columnas: 6
- **Rango temporal:** 2003-01-02 a 2025-12-16 (col: FECHA_HECHO)
- **Departamentos únicos:** 32
- **Municipios únicos:** 323

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### HURTO PERSONAS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/HURTO PERSONAS.xlsx
- **Tamaño:** 14.92 MB
- **Estado:** ✓ OK
- **Total filas:** 626,346
- **Tiempo procesamiento:** 12.86 s

#### Hoja: Sheet 1
- Filas: 626,346 | Columnas: 6
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 34
- **Municipios únicos:** 1028

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (object) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (object) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### INCAUTACIONES MINERIA.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INCAUTACIONES MINERIA.xlsx
- **Tamaño:** 0.23 MB
- **Estado:** ✓ OK
- **Total filas:** 6,778
- **Tiempo procesamiento:** 0.38 s

#### Hoja: Sheet 1
- Filas: 6,778 | Columnas: 8
- **Rango temporal:** 2010-08-23 a 2025-12-26 (col: FECHA_HECHO)
- **Departamentos únicos:** 34
- **Municipios únicos:** 630

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CLASE DE BIEN` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### INCAUTACIÓN DE BASE DE COCA.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INCAUTACIÓN DE BASE DE COCA.xlsx
- **Tamaño:** 4.84 MB
- **Estado:** ✓ OK
- **Total filas:** 170,488
- **Tiempo procesamiento:** 3.76 s

#### Hoja: Sheet 1
- Filas: 170,488 | Columnas: 7
- **Rango temporal:** 2010-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 42
- **Municipios únicos:** 922

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### INCAUTACIÓN DE BASUCO.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INCAUTACIÓN DE BASUCO.xlsx
- **Tamaño:** 6.43 MB
- **Estado:** ✓ OK
- **Total filas:** 230,430
- **Tiempo procesamiento:** 5.45 s

#### Hoja: Sheet 1
- Filas: 230,430 | Columnas: 7
- **Rango temporal:** 2010-01-01 a 2025-12-30 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 912

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### INCAUTACIÓN DE COCAINA.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INCAUTACIÓN DE COCAINA.xlsx
- **Tamaño:** 4.21 MB
- **Estado:** ✓ OK
- **Total filas:** 147,699
- **Tiempo procesamiento:** 3.28 s

#### Hoja: Sheet 1
- Filas: 147,699 | Columnas: 7
- **Rango temporal:** 2010-01-01 a 2025-12-30 (col: FECHA_HECHO)
- **Departamentos únicos:** 50
- **Municipios únicos:** 979

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (object) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (object) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### INCAUTACIÓN DE HEROINA.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INCAUTACIÓN DE HEROINA.xlsx
- **Tamaño:** 0.32 MB
- **Estado:** ✓ OK
- **Total filas:** 10,674
- **Tiempo procesamiento:** 0.26 s

#### Hoja: Sheet 1
- Filas: 10,674 | Columnas: 7
- **Rango temporal:** 2010-01-01 a 2025-12-26 (col: FECHA_HECHO)
- **Departamentos únicos:** 37
- **Municipios únicos:** 398

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (object) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (object) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### INCAUTACIÓN DE MARIHUANA.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INCAUTACIÓN DE MARIHUANA.xlsx
- **Tamaño:** 13.58 MB
- **Estado:** ✓ OK
- **Total filas:** 481,299
- **Tiempo procesamiento:** 12.12 s

#### Hoja: Sheet 1
- Filas: 481,299 | Columnas: 7
- **Rango temporal:** 2010-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 50
- **Municipios únicos:** 1025

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### INCAUTACIÓN ORO Y MERCURIO.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INCAUTACIÓN ORO Y MERCURIO.xlsx
- **Tamaño:** 0.05 MB
- **Estado:** ✓ OK
- **Total filas:** 906
- **Tiempo procesamiento:** 0.08 s

#### Hoja: Sheet 1
- Filas: 906 | Columnas: 8
- **Rango temporal:** 2011-03-24 a 2025-12-28 (col: FECHA_HECHO)
- **Departamentos únicos:** 28
- **Municipios únicos:** 144

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CLASE DE BIEN` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD_MEDIDA` (object) - Nulos: 0.0%

### INDICADORES DE SEGUR Y RESULT OPER ENERO-DICIEMBRE 2025.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INDICADORES DE SEGUR Y RESULT OPER ENERO-DICIEMBRE 2025.xlsx
- **Tamaño:** 1.03 MB
- **Estado:** ✓ OK
- **Total filas:** 569
- **Tiempo procesamiento:** 0.16 s

#### Hoja: Año corrido
- Filas: 108 | Columnas: 25
- **Rango temporal:** 1970-01-01 a 1970-01-01 (col: Unnamed: 2)

**Columnas:**
- `Unnamed: 0` (object) - Nulos: 99.07%
- `MINISTERIO DE DEFENSA NACIONAL` (object) - Nulos: 8.33%
- `Unnamed: 2` (object) - Nulos: 58.33%
- `Unnamed: 3` (object) - Nulos: 58.33%
- `Unnamed: 4` (object) - Nulos: 50.93%
- `Unnamed: 5` (object) - Nulos: 50.93%
- `Unnamed: 6` (object) - Nulos: 50.93%
- `Unnamed: 7` (object) - Nulos: 50.93%
- `Unnamed: 8` (object) - Nulos: 50.93%
- `Unnamed: 9` (object) - Nulos: 27.78%
- `Unnamed: 10` (object) - Nulos: 27.78%
- `Unnamed: 11` (object) - Nulos: 27.78%
- `Unnamed: 12` (object) - Nulos: 27.78%
- `Unnamed: 13` (object) - Nulos: 27.78%
- `Unnamed: 14` (object) - Nulos: 27.78%
- ... y 10 columnas más

#### Hoja: Año corrido tasa
- Filas: 102 | Columnas: 25
- **Rango temporal:** 1970-01-01 a 1970-01-01 (col: Unnamed: 2)

**Columnas:**
- `Unnamed: 0` (float64) - Nulos: 100.0%
- `MINISTERIO DE DEFENSA NACIONAL` (object) - Nulos: 74.51%
- `Unnamed: 2` (object) - Nulos: 81.37%
- `Unnamed: 3` (object) - Nulos: 81.37%
- `Unnamed: 4` (object) - Nulos: 81.37%
- `Unnamed: 5` (object) - Nulos: 81.37%
- `Unnamed: 6` (object) - Nulos: 80.39%
- `Unnamed: 7` (object) - Nulos: 80.39%
- `Unnamed: 8` (object) - Nulos: 81.37%
- `Unnamed: 9` (object) - Nulos: 81.37%
- `Unnamed: 10` (object) - Nulos: 81.37%
- `Unnamed: 11` (object) - Nulos: 81.37%
- `Unnamed: 12` (object) - Nulos: 81.37%
- `Unnamed: 13` (object) - Nulos: 81.37%
- `Unnamed: 14` (object) - Nulos: 81.37%
- ... y 10 columnas más

#### Hoja: Año completo
- Filas: 107 | Columnas: 25

**Columnas:**
- `Unnamed: 0` (float64) - Nulos: 100.0%
- `MINISTERIO DE DEFENSA NACIONAL` (object) - Nulos: 7.48%
- `Unnamed: 2` (float64) - Nulos: 50.47%
- `Unnamed: 3` (float64) - Nulos: 50.47%
- `Unnamed: 4` (float64) - Nulos: 50.47%
- `Unnamed: 5` (float64) - Nulos: 50.47%
- `Unnamed: 6` (float64) - Nulos: 50.47%
- `Unnamed: 7` (float64) - Nulos: 50.47%
- `Unnamed: 8` (float64) - Nulos: 50.47%
- `Unnamed: 9` (float64) - Nulos: 27.1%
- `Unnamed: 10` (float64) - Nulos: 27.1%
- `Unnamed: 11` (float64) - Nulos: 27.1%
- `Unnamed: 12` (float64) - Nulos: 27.1%
- `Unnamed: 13` (float64) - Nulos: 27.1%
- `Unnamed: 14` (float64) - Nulos: 27.1%
- ... y 10 columnas más

#### Hoja: Año completo tasa
- Filas: 102 | Columnas: 25

**Columnas:**
- `Unnamed: 0` (float64) - Nulos: 100.0%
- `MINISTERIO DE DEFENSA NACIONAL` (object) - Nulos: 74.51%
- `Unnamed: 2` (float64) - Nulos: 81.37%
- `Unnamed: 3` (float64) - Nulos: 81.37%
- `Unnamed: 4` (float64) - Nulos: 81.37%
- `Unnamed: 5` (float64) - Nulos: 81.37%
- `Unnamed: 6` (float64) - Nulos: 80.39%
- `Unnamed: 7` (float64) - Nulos: 80.39%
- `Unnamed: 8` (float64) - Nulos: 81.37%
- `Unnamed: 9` (float64) - Nulos: 81.37%
- `Unnamed: 10` (float64) - Nulos: 81.37%
- `Unnamed: 11` (float64) - Nulos: 81.37%
- `Unnamed: 12` (float64) - Nulos: 81.37%
- `Unnamed: 13` (float64) - Nulos: 81.37%
- `Unnamed: 14` (float64) - Nulos: 81.37%
- ... y 10 columnas más

#### Hoja: METODOLOGÍA A DENUNCIAR
- Filas: 50 | Columnas: 2

**Columnas:**
- `MINISTERIO DE DEFENSA NACIONAL` (object) - Nulos: 94.0%
- `Unnamed: 1` (object) - Nulos: 90.0%

#### Hoja: NUEVA METODOLOGIA FGN
- Filas: 50 | Columnas: 2

**Columnas:**
- `MINISTERIO DE DEFENSA NACIONAL` (object) - Nulos: 94.0%
- `Unnamed: 1` (object) - Nulos: 96.0%

#### Hoja: ACLARACIONES METODOLÓGICAS
- Filas: 50 | Columnas: 2

**Columnas:**
- `MINISTERIO DE DEFENSA NACIONAL` (object) - Nulos: 96.0%
- `Unnamed: 1` (object) - Nulos: 96.0%

### INSUMOS LIQUIDOS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INSUMOS LIQUIDOS.xlsx
- **Tamaño:** 2.12 MB
- **Estado:** ✓ OK
- **Total filas:** 53,210
- **Tiempo procesamiento:** 1.34 s

#### Hoja: Sheet 1
- Filas: 53,210 | Columnas: 8
- **Rango temporal:** 2010-01-02 a 2025-10-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 50
- **Municipios únicos:** 773

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (object) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `TIPO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD DE MEDIDA` (object) - Nulos: 0.0%

### INSUMOS SOLIDOS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INSUMOS SOLIDOS.xlsx
- **Tamaño:** 1.76 MB
- **Estado:** ✓ OK
- **Total filas:** 44,922
- **Tiempo procesamiento:** 1.2 s

#### Hoja: Sheet 1
- Filas: 44,922 | Columnas: 8
- **Rango temporal:** 2010-01-02 a 2025-10-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 46
- **Municipios únicos:** 712

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (float64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (object) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `TIPO` (object) - Nulos: 0.0%
- `CANTIDAD` (float64) - Nulos: 0.0%
- `UNIDAD DE MEDIDA` (object) - Nulos: 0.0%

### INVASIÓN DE TIERRAS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/INVASIÓN DE TIERRAS.xlsx
- **Tamaño:** 0.59 MB
- **Estado:** ✓ OK
- **Total filas:** 15,009
- **Tiempo procesamiento:** 0.4 s

#### Hoja: INVASION DE TIERRAS
- Filas: 15,009 | Columnas: 8
- **Rango temporal:** 2003-01-01 a 2025-08-28 (col: FECHA HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 908

**Columnas:**
- `FECHA HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `DESCRIPCION CONDUCTA` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### LESIONES ACCIDENTES DE TRÁNSITO.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/LESIONES ACCIDENTES DE TRÁNSITO.xlsx
- **Tamaño:** 13.12 MB
- **Estado:** ✓ OK
- **Total filas:** 605,139
- **Tiempo procesamiento:** 12.84 s

#### Hoja: Sheet 1
- Filas: 605,139 | Columnas: 6
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 34
- **Municipios únicos:** 1001

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CASOS` (int64) - Nulos: 0.0%

### LESIONES COMUNES.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/LESIONES COMUNES.xlsx
- **Tamaño:** 23.74 MB
- **Estado:** ✓ OK
- **Total filas:** 887,429
- **Tiempo procesamiento:** 22.54 s

#### Hoja: Sheet 1
- Filas: 887,429 | Columnas: 7
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1030

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `SEXO` (object) - Nulos: 0.04%
- `CANTIDAD` (int64) - Nulos: 0.0%

### MASACRES.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/MASACRES.xlsx
- **Tamaño:** 0.03 MB
- **Estado:** ✓ OK
- **Total filas:** 366
- **Tiempo procesamiento:** 0.12 s

#### Hoja: Sheet 1
- Filas: 366 | Columnas: 7
- **Rango temporal:** 2022-01-02 a 2025-12-20 (col: FECHA_HECHO)
- **Departamentos únicos:** 29
- **Municipios únicos:** 193

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CASOS` (int64) - Nulos: 0.0%
- `VICTIMAS` (int64) - Nulos: 0.0%

### MINAS INTERVENIDAS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/MINAS INTERVENIDAS.xlsx
- **Tamaño:** 0.36 MB
- **Estado:** ✓ OK
- **Total filas:** 13,764
- **Tiempo procesamiento:** 0.3 s

#### Hoja: Sheet 1
- Filas: 13,764 | Columnas: 6
- **Rango temporal:** 2010-01-04 a 2025-12-27 (col: FECHA_HECHO)
- **Departamentos únicos:** 32
- **Municipios únicos:** 707

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### PIRATERÍA TERRESTRE.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/PIRATERÍA TERRESTRE.xlsx
- **Tamaño:** 0.3 MB
- **Estado:** ✓ OK
- **Total filas:** 10,387
- **Tiempo procesamiento:** 0.24 s

#### Hoja: Sheet 1
- Filas: 10,387 | Columnas: 7
- **Rango temporal:** 2003-01-03 a 2025-12-03 (col: FECHA_HECHO)
- **Departamentos únicos:** 28
- **Municipios únicos:** 524

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### PUENTES Y VÍAS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/PUENTES Y VÍAS.xlsx
- **Tamaño:** 0.06 MB
- **Estado:** ✓ OK
- **Total filas:** 1,334
- **Tiempo procesamiento:** 0.05 s

#### Hoja: Sheet 1
- Filas: 1,334 | Columnas: 7
- **Rango temporal:** 2003-01-01 a 2025-11-14 (col: FECHA_HECHO)
- **Departamentos únicos:** 31
- **Municipios únicos:** 283

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CLASE BIEN` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### SECUESTRO.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/SECUESTRO.xlsx
- **Tamaño:** 0.3 MB
- **Estado:** ✓ OK
- **Total filas:** 10,083
- **Tiempo procesamiento:** 0.25 s

#### Hoja: Sheet 1
- Filas: 10,083 | Columnas: 7
- **Rango temporal:** 2003-01-01 a 2025-12-27 (col: FECHA_HECHO)
- **Departamentos únicos:** 32
- **Municipios únicos:** 784

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `DESCRIPCION CONDUCTA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### SOMETIDOS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/SOMETIDOS.xlsx
- **Tamaño:** 0.1 MB
- **Estado:** ✓ OK
- **Total filas:** 2,202
- **Tiempo procesamiento:** 0.08 s

#### Hoja: SOMETIDOS
- Filas: 2,202 | Columnas: 7
- **Rango temporal:** 2020-11-11 a 2025-08-28 (col: FECHA HECHO)
- **Departamentos únicos:** 31
- **Municipios únicos:** 249

**Columnas:**
- `FECHA HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `GRUPO` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### TERRORISMO.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/TERRORISMO.xlsx
- **Tamaño:** 0.46 MB
- **Estado:** ✓ OK
- **Total filas:** 14,714
- **Tiempo procesamiento:** 0.4 s

#### Hoja: Sheet 1
- Filas: 14,714 | Columnas: 8
- **Rango temporal:** 2003-01-01 a 2025-12-27 (col: FECHA_HECHO)
- **Departamentos únicos:** 32
- **Municipios únicos:** 727

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `DESCRIPCION CONDUCTA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### TRATA DE PERSONAS Y TRÁFICO DE MIGRANTES.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/TRATA DE PERSONAS Y TRÁFICO DE MIGRANTES.xlsx
- **Tamaño:** 0.14 MB
- **Estado:** ✓ OK
- **Total filas:** 4,910
- **Tiempo procesamiento:** 0.14 s

#### Hoja: Sheet 1
- Filas: 4,910 | Columnas: 7
- **Rango temporal:** 2003-12-27 a 2025-12-13 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 292

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `DESCRIPCION CONDUCTA` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%

### VIOLENCIA INTRAFAMILIAR.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/VIOLENCIA INTRAFAMILIAR.xlsx
- **Tamaño:** 18.86 MB
- **Estado:** ✓ OK
- **Total filas:** 636,903
- **Tiempo procesamiento:** 16.58 s

#### Hoja: Sheet 1
- Filas: 636,903 | Columnas: 8
- **Rango temporal:** 2003-01-01 a 2025-12-31 (col: FECHA_HECHO)
- **Departamentos únicos:** 33
- **Municipios únicos:** 1028

**Columnas:**
- `FECHA_HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `ZONA` (object) - Nulos: 0.0%
- `SEXO` (object) - Nulos: 0.15%
- `CANTIDAD` (int64) - Nulos: 0.0%

### VOLADURA DE OLEODUCTOS.xlsx

- **Ruta:** /Users/ricardo_suarez1983/Analisis_defensa_colombia/MINISTERIO DE DEFENSA/VOLADURA DE OLEODUCTOS.xlsx
- **Tamaño:** 0.06 MB
- **Estado:** ✓ OK
- **Total filas:** 1,364
- **Tiempo procesamiento:** 0.11 s

#### Hoja: VOLADURA DE OLEODUCTOS
- Filas: 1,364 | Columnas: 6
- **Rango temporal:** 2007-01-17 a 2025-11-17 (col: FECHA HECHO)
- **Departamentos únicos:** 15
- **Municipios únicos:** 59

**Columnas:**
- `FECHA HECHO` (datetime64[ns]) - Nulos: 0.0%
- `COD_DEPTO` (int64) - Nulos: 0.0%
- `DEPARTAMENTO` (object) - Nulos: 0.0%
- `COD_MUNI` (int64) - Nulos: 0.0%
- `MUNICIPIO` (object) - Nulos: 0.0%
- `CANTIDAD` (int64) - Nulos: 0.0%
