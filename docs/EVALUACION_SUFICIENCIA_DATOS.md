# Evaluación de Suficiencia de Datos para el Proyecto

**Fecha:** Febrero 2026  
**Objetivo:** Determinar si los datos disponibles son suficientes para el sistema de análisis de seguridad Colombia.

---

## 1. Resumen Ejecutivo

| Criterio | Estado | Observación |
|----------|--------|-------------|
| **Análisis de tendencias** | ✅ Suficiente | 23 años de datos (2003-2025) |
| **Comparaciones año a año** | ✅ Suficiente | Series completas en archivos detallados |
| **Análisis por departamento/municipio** | ✅ Suficiente | COD_DEPTO, COD_MUNI, nombres en todos los archivos |
| **Indicadores tasa por 100k** | ⚠️ Parcial | Tasas nacionales en INDICADORES; municipales requieren población DANE |
| **Impacto económico** | ⚠️ Parcial | DANE PIB disponible (.xls) pero requiere xlrd |
| **Patrones estacionales** | ✅ Suficiente | Fechas a nivel día permiten análisis mensual/trimestral |

**Conclusión:** Los datos son **suficientes para iniciar el pipeline ETL** y el dashboard principal. Algunos indicadores avanzados requerirán datos complementarios (población DANE para tasas municipales).

---

## 2. Inventario de Datos Disponibles

### 2.1 Ministerio de Defensa (42 archivos .xlsx)

| Categoría | Archivos | Registros aprox. | Rango temporal |
|-----------|----------|------------------|----------------|
| **Delitos contra la vida** | HOMICIDIO INTENCIONAL, HOMICIDIO ACCIDENTES TRÁNSITO, MASACRES, LESIONES | ~2.5M | 2003-2025 |
| **Hurto** | HURTO A COMERCIO, RESIDENCIAS, VEHÍCULOS, PERSONAS, etc. | ~2.4M | 2003-2025 |
| **Violencia** | VIOLENCIA INTRAFAMILIAR, DELITOS SEXUALES | ~1M | 2003-2025 |
| **Narcotráfico** | ERRADICACIÓN, INCAUTACIONES, HOJA DE COCA, ASPERSIÓN | ~600K | 2003-2025 |
| **Otros** | EXTORSIÓN, SECUESTRO, TERRORISMO, AFECTACIÓN FUERZA PÚBLICA | ~200K | 2007-2025 |
| **Total** | 41 archivos transaccionales | **~7.4 millones** | 2003-2025 |

### 2.2 Archivo INDICADORES (resumen nacional)

- **Contenido:** Agregados anuales y tasas por 100k habitantes (a nivel nacional)
- **Período:** 2003-2025
- **Hojas:** Año corrido, Año corrido tasa, Año completo, Año completo tasa
- **Dato crítico:** Ya incluye tasas por 100k calculadas → confirma que Mindefensa usa proyecciones poblacionales DANE a nivel nacional

### 2.3 DANE PIB (24 archivos .xls)

- **Estado:** Requieren `pip install xlrd` para lectura
- **Contenido:** PIB oferta/demanda, índices, series 1994-2011
- **Uso:** Impacto económico del conflicto/violencia

---

## 3. Requisitos del Proyecto vs. Datos

### 3.1 ✅ CUBIERTO CON DATOS ACTUALES

| Requisito | Fuente | Observación |
|-----------|--------|-------------|
| Tendencias y comparaciones año a año | Archivos MinDefensa | FECHA_HECHO a nivel día |
| Análisis por departamento | COD_DEPTO, DEPARTAMENTO | 32 departamentos |
| Análisis por municipio | COD_MUNI, MUNICIPIO | ~1,100 municipios |
| Análisis por tipo de evento | 41 categorías de archivos | Cada archivo = un tipo |
| Patrones estacionales | FECHA_HECHO | Agregación mensual/trimestral |
| Dataset maestro consolidado | ETL desde 41 archivos | Parquet normalizado |

### 3.2 ⚠️ REQUIERE DATOS COMPLEMENTARIOS

| Requisito | Dato faltante | Acción recomendada |
|-----------|---------------|---------------------|
| **Tasa por 100k a nivel municipal/departamental** | Población proyectada DANE | Descargar de [certificados-poblacion DANE](https://sitios.dane.gov.co/certificados-poblacion/) o usar proyecciones por departamento |
| **Impacto económico detallado** | PIB por departamento | DANE PIB tiene nacional; DNP/publicaciones pueden tener desagregación |
| **Validación geográfica completa** | Diccionario DIVIPOLA | Descargar de DANE o crear desde datos |

### 3.3 Limitaciones metodológicas (documentar)

1. **Cambio metodológico 2016-2017:** El archivo INDICADORES documenta actualización de sistemas Policía-Fiscalía y aplicación "A Denunciar". Los delitos de hurto, extorsión, etc. pueden tener ruptura de serie.
2. **Inconsistencias de columnas:** 24 estructuras distintas entre archivos → el ETL debe mapear a un esquema unificado.
3. **Variación de nombres:** `FECHA_HECHO` vs `FECHA HECHO`, `CANTIDAD` vs `VICTIMAS` vs `CASOS`.

---

## 4. Variaciones de Estructura (para ETL)

El ETL debe normalizar las siguientes variantes de columnas:

| Columna unificada | Variantes en origen |
|-------------------|---------------------|
| `fecha` | FECHA_HECHO, FECHA HECHO |
| `valor` (conteo) | VICTIMAS, CANTIDAD, CASOS, CAPTURAS |
| `cod_depto` | COD_DEPTO |
| `cod_muni` | COD_MUNI |
| `departamento` | DEPARTAMENTO |
| `municipio` | MUNICIPIO |
| `tipo_evento` | Deriva del nombre del archivo |

**Columnas adicionales por tipo** (opcionales en esquema final):
- ZONA, SEXO, TIPO CULTIVO, UNIDAD_MEDIDA, DESCRIPCION CONDUCTA, etc.

---

## 5. Recomendación

**Proceder con el Pipeline ETL** con los datos actuales. El diseño debe:

1. **Fase 1 (ETL actual):** Consolidar los 41 archivos de delitos/eventos en dataset maestro Parquet.
2. **Fase 2 (opcional):** Integrar población DANE cuando se descargue, para habilitar tasas por 100k a nivel territorial.
3. **Fase 3 (opcional):** Integrar DANE PIB (instalando xlrd) para módulo de impacto económico.

Los datos son suficientes para cumplir el objetivo principal: **evaluar el estado de seguridad y violencia comparado con años anteriores**.
