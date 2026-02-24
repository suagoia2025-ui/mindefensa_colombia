import { useState, useEffect } from 'react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import {
  getMetadata,
  getComparacionAnual,
  getTendencia,
  getDepartamentos,
  getTiposEvento,
  getConcentracion,
  getEstacionalidad,
  getSerieTemporal,
} from './api'
import './App.css'

const COLORS = ['#1e3a5f', '#2d5a87', '#3d7ab5', '#5a9ad4', '#7ab8e8', '#9cd4f7']
const ANOS_DISPONIBLES = Array.from({ length: 24 }, (_, i) => 2002 + i)

// Etiqueta legible de unidad para mostrar en gráficos
const UNIDAD_LABEL = { personas: 'personas', peso: 'kg', hectareas: 'ha', casos: 'casos' }
function formatearUnidad(u) {
  return UNIDAD_LABEL[u] || u
}

function App() {
  const [metadata, setMetadata] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [anosSeleccionados, setAnosSeleccionados] = useState(() =>
    ANOS_DISPONIBLES.reduce((acc, y) => ({ ...acc, [y]: [2020, 2021, 2022, 2023].includes(y) }), {})
  )
  const [tipoEvento, setTipoEvento] = useState('')
  const [departamento, setDepartamento] = useState('')

  const [filtrosAplicados, setFiltrosAplicados] = useState({ anos: [2020, 2021, 2022, 2023], tipoEvento: '', departamento: '' })
  const [chartsLoading, setChartsLoading] = useState(false)
  const [comparacion, setComparacion] = useState([])
  const [serieTemporal, setSerieTemporal] = useState([])
  const [departamentos, setDepartamentos] = useState([])
  const [tiposEvento, setTiposEvento] = useState([])
  const [concentracion, setConcentracion] = useState({ gini: 0, data: [] })
  const [estacionalidad, setEstacionalidad] = useState({ mes_pico: null, patron_mensual: [] })

  const anosActivos = Object.entries(anosSeleccionados)
    .filter(([, v]) => v)
    .map(([k]) => parseInt(k))

  const aplicarFiltros = () => {
    if (anosActivos.length === 0) return
    setFiltrosAplicados({ anos: anosActivos, tipoEvento, departamento })
  }

  const filters = {
    anos: filtrosAplicados.anos?.length ? filtrosAplicados.anos.join(',') : undefined,
    tipo_evento: filtrosAplicados.tipoEvento || undefined,
    departamento: filtrosAplicados.departamento || undefined,
  }

  const unidadFiltro = metadata?.unidades_tipo_evento?.[filtrosAplicados.tipoEvento]
  const sufijoUnidad = unidadFiltro ? ` [${formatearUnidad(unidadFiltro)}]` : ''

  const toggleAno = (ano) => {
    setAnosSeleccionados((prev) => ({ ...prev, [ano]: !prev[ano] }))
  }

  const seleccionarTodos = () => {
    setAnosSeleccionados(ANOS_DISPONIBLES.reduce((acc, y) => ({ ...acc, [y]: true }), {}))
  }

  const seleccionarNinguno = () => {
    setAnosSeleccionados(ANOS_DISPONIBLES.reduce((acc, y) => ({ ...acc, [y]: false }), {}))
  }

  useEffect(() => {
    getMetadata()
      .then(setMetadata)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (!metadata) return
    if (filtrosAplicados.anos?.length === 0) return

    setChartsLoading(true)
    const load = async () => {
      try {
        const [comp, serie, deptos, tipos, conc, est] = await Promise.all([
          getComparacionAnual(filters),
          getSerieTemporal(filters),
          getDepartamentos(filters),
          getTiposEvento(filters),
          getConcentracion(filters),
          getEstacionalidad(filters),
        ])
        setComparacion(comp.data || [])
        setSerieTemporal(serie.data || [])
        setDepartamentos(deptos.data || [])
        setTiposEvento(
          (tipos.data || []).map((d) => ({
            ...d,
            tipo_evento_etiqueta:
              d.unidad && d.unidad !== '—'
                ? `${d.tipo_evento} [${formatearUnidad(d.unidad)}]`
                : d.tipo_evento,
          }))
        )
        setConcentracion({ gini: conc.gini || 0, data: conc.data || [] })
        setEstacionalidad({
          mes_pico: est.mes_pico,
          patron_mensual: (est.patron_mensual || []).map((d) => ({
            ...d,
            promedio: Number(d.promedio),
          })),
        })
      } catch (e) {
        setError(e.message)
      } finally {
        setChartsLoading(false)
      }
    }

    load()
  }, [filtrosAplicados])

  if (loading) return <div className="loading">Cargando...</div>
  if (error) return <div className="error">Error: {error}. ¿Está corriendo el backend? (python -m uvicorn src.api.main:app --reload)</div>

  return (
    <div className="app">
      <header className="header">
        <h1>Análisis de Seguridad y Violencia - Colombia</h1>
        <p className="subtitle">Ministerio de Defensa • Datos oficiales</p>
      </header>

      <section className="filters">
        <div className="filter-group filter-anos">
          <label>Años</label>
          <div className="anos-actions">
            <button type="button" className="btn-link" onClick={seleccionarTodos}>Todos</button>
            <span>|</span>
            <button type="button" className="btn-link" onClick={seleccionarNinguno}>Ninguno</button>
          </div>
          <div className="anos-checkboxes">
            {ANOS_DISPONIBLES.map((ano) => (
              <label key={ano} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={anosSeleccionados[ano] || false}
                  onChange={() => toggleAno(ano)}
                />
                {ano}
              </label>
            ))}
          </div>
        </div>
        <div className="filter-group">
          <label>Tipo de evento</label>
          <select value={tipoEvento} onChange={(e) => setTipoEvento(e.target.value)}>
            <option value="">Todos</option>
            {metadata?.tipos_evento?.map((t) => (
              <option key={t} value={t}>
                {metadata?.unidades_tipo_evento?.[t]
                  ? `${t} [${formatearUnidad(metadata.unidades_tipo_evento[t])}]`
                  : t}
              </option>
            ))}
          </select>
        </div>
        <div className="filter-group">
          <label>Departamento</label>
          <select value={departamento} onChange={(e) => setDepartamento(e.target.value)}>
            <option value="">Todos</option>
            {metadata?.departamentos?.map((d) => (
              <option key={d} value={d}>{d}</option>
            ))}
          </select>
        </div>
        <div className="filter-group filter-actions">
          <label>&nbsp;</label>
          <div className="filter-buttons">
            <button
              type="button"
              className="btn-graficar"
              onClick={aplicarFiltros}
              disabled={anosActivos.length === 0}
              title={anosActivos.length === 0 ? 'Seleccione al menos un año' : ''}
            >
              Graficar
            </button>
            <a
              href={`/api/exportar?anos=${encodeURIComponent(filtrosAplicados.anos?.join(',') || '')}&tipo_evento=${encodeURIComponent(filtrosAplicados.tipoEvento)}&departamento=${encodeURIComponent(filtrosAplicados.departamento)}&formato=csv`}
              className="btn-export"
              download
            >
              Exportar CSV
            </a>
          </div>
        </div>
      </section>

      <main className="dashboard">
        {chartsLoading && (
          <div className="charts-loading">Cargando gráficos…</div>
        )}
        <div className="card full-width">
          <h2>Serie temporal{sufijoUnidad}</h2>
          <ResponsiveContainer width="100%" height={280}>
            <LineChart data={serieTemporal}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="periodo" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="total" stroke="#1e3a5f" strokeWidth={2} name="Total" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2>Comparación año a año{sufijoUnidad}</h2>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={comparacion}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="ano" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="total" fill="#2d5a87" name="Total" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2>Top departamentos{sufijoUnidad}</h2>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={departamentos} layout="vertical" margin={{ left: 80 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="departamento" width={80} />
              <Tooltip />
              <Bar dataKey="total" fill="#3d7ab5" name="Casos" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2>Top tipos de evento</h2>
          <p className="chart-desc">
            Cada tipo tiene su unidad de medida (personas, kg, ha, casos). No se deben comparar entre sí.
          </p>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={tiposEvento} layout="vertical" margin={{ left: 140 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis type="category" dataKey="tipo_evento_etiqueta" width={135} tick={{ fontSize: 11 }} />
              <Tooltip formatter={(v, name, props) => [Number(v).toLocaleString('es-CO'), props.payload.unidad ? formatearUnidad(props.payload.unidad) : 'Total']} />
              <Bar dataKey="total" fill="#5a9ad4" name="Total" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2>Concentración territorial{sufijoUnidad}</h2>
          <p className="metric">Índice Gini: <strong>{concentracion.gini?.toFixed(4) || 'N/A'}</strong></p>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={concentracion.data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="departamento" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="pct_acumulado" fill="#7ab8e8" name="% acumulado" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2>Estacionalidad (patrón mensual){sufijoUnidad}</h2>
          <p className="metric">
            Mes pico: <strong>{estacionalidad.mes_pico?.mes_nombre || 'N/A'}</strong>
            {estacionalidad.mes_pico?.pct_del_total && ` (${estacionalidad.mes_pico.pct_del_total}%)`}
          </p>
          <p className="chart-desc">
            Promedio de eventos en cada mes (entre los años seleccionados). Ej.: el valor de enero es el promedio de todos los eneros en el período.
          </p>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={estacionalidad.patron_mensual}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mes_nombre" />
              <YAxis
                label={{ value: 'Promedio anual', angle: -90, position: 'insideLeft' }}
                domain={[0, 'auto']}
                tickFormatter={(v) => (v >= 1e6 ? `${(v / 1e6).toFixed(1)}M` : v >= 1e3 ? `${(v / 1e3).toFixed(0)}k` : v)}
              />
              <Tooltip formatter={(v) => [Number(v).toLocaleString('es-CO'), 'Promedio anual']} />
              <Bar dataKey="promedio" fill="#9cd4f7" name="Promedio anual por mes" isAnimationActive={true} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </main>

      <footer className="footer">
        <p>Fuente: Ministerio de Defensa Nacional • Policía Nacional • Fiscalía General de la Nación</p>
        <p>Los datos se presentan de forma objetiva. Permitir al usuario sacar sus propias conclusiones.</p>
      </footer>
    </div>
  )
}

export default App
