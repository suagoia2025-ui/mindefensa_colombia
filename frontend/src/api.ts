const API_BASE = '/api'

export type ApiFilterValue = string | number | string[] | undefined
export type ApiFilters = Record<string, ApiFilterValue>

export interface MetadataResponse {
  anos_disponibles: number[]
  tipos_evento: string[]
  unidades_tipo_evento: Record<string, string>
  departamentos: string[]
  total_registros: number
}

export interface SerieTemporalRow {
  periodo: string
  total: number
}

export interface DepartamentoRow {
  departamento: string
  total: number
}

export interface ConcentracionResponse {
  gini: number
  data: Array<{
    departamento: string
    total: number
    pct_total?: number
    pct_acumulado?: number
  }>
}

export interface MesPico {
  mes: number | null
  mes_nombre: string | null
  total?: number
  pct_del_total?: number
}

export interface PatronMensualRow {
  mes: number
  mes_nombre: string
  promedio: number
}

export interface EstacionalidadResponse {
  mes_pico: MesPico | null
  patron_mensual: PatronMensualRow[]
}

async function fetchApi<T>(path: string, params: ApiFilters = {}): Promise<T> {
  const url = new URL(path, window.location.origin)
  Object.entries(params).forEach(([k, v]) => {
    if (v != null && v !== '') {
      url.searchParams.set(k, Array.isArray(v) ? v.join(',') : String(v))
    }
  })
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json() as Promise<T>
}

export async function getMetadata(): Promise<MetadataResponse> {
  return fetchApi<MetadataResponse>(`${API_BASE}/metadata`)
}

export async function getDepartamentos(filters: ApiFilters = {}) {
  return fetchApi<{ data: DepartamentoRow[] }>(`${API_BASE}/departamentos`, {
    ...filters,
    top_n: filters.top_n ?? 15,
  })
}

export async function getConcentracion(filters: ApiFilters = {}) {
  return fetchApi<ConcentracionResponse>(`${API_BASE}/concentracion`, {
    ...filters,
    top_n: filters.top_n ?? 10,
  })
}

export async function getEstacionalidad(filters: ApiFilters = {}) {
  return fetchApi<EstacionalidadResponse>(`${API_BASE}/estacionalidad`, filters)
}

export async function getSerieTemporal(filters: ApiFilters = {}) {
  return fetchApi<{ data: SerieTemporalRow[] }>(`${API_BASE}/serie-temporal`, filters)
}
