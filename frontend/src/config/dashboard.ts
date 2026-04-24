/**
 * Rango de años del filtro del dashboard (alineado con el README / datos del ETL).
 * Si el maestro incluye otros años, conviene alinear ANO_MAX con metadata de la API.
 */
export const ANO_MIN = 2002
export const ANO_MAX = 2025

export const ANOS_DISPONIBLES = Array.from(
  { length: ANO_MAX - ANO_MIN + 1 },
  (_, i) => ANO_MIN + i,
)

/** Años marcados al cargar la página (antes de pulsar Graficar). */
export const ANOS_PRESELECCIONADOS: readonly number[] = [2020, 2021, 2022, 2023]
