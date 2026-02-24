/**
 * Cliente API para el backend FastAPI
 * Usa proxy en desarrollo: /api -> localhost:8000
 */

const API_BASE = '/api';

async function fetchApi(path, params = {}) {
  const url = new URL(path, window.location.origin);
  Object.entries(params).forEach(([k, v]) => {
    if (v != null && v !== '') {
      url.searchParams.set(k, Array.isArray(v) ? v.join(',') : v);
    }
  });
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export async function getMetadata() {
  return fetchApi(`${API_BASE}/metadata`);
}

export async function getComparacionAnual(filters = {}) {
  return fetchApi(`${API_BASE}/comparacion-anual`, filters);
}

export async function getTendencia(filters = {}) {
  return fetchApi(`${API_BASE}/tendencia`, filters);
}

export async function getDepartamentos(filters = {}) {
  return fetchApi(`${API_BASE}/departamentos`, { ...filters, top_n: filters.top_n || 15 });
}

export async function getTiposEvento(filters = {}) {
  return fetchApi(`${API_BASE}/tipos-evento`, { ...filters, top_n: filters.top_n || 15 });
}

export async function getConcentracion(filters = {}) {
  return fetchApi(`${API_BASE}/concentracion`, { ...filters, top_n: filters.top_n || 10 });
}

export async function getEstacionalidad(filters = {}) {
  return fetchApi(`${API_BASE}/estacionalidad`, filters);
}

export async function getSerieTemporal(filters = {}) {
  return fetchApi(`${API_BASE}/serie-temporal`, filters);
}
