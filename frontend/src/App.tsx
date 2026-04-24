import { useEffect, useMemo, useState } from 'react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import {
  getConcentracion,
  getDepartamentos,
  getEstacionalidad,
  getMetadata,
  getSerieTemporal,
  type ConcentracionResponse,
  type DepartamentoRow,
  type EstacionalidadResponse,
  type MetadataResponse,
  type PatronMensualRow,
  type SerieTemporalRow,
} from './api'
import { Header } from './components/layout/Header'
import { ANOS_DISPONIBLES, ANOS_PRESELECCIONADOS } from './config/dashboard'
import { ui } from './config/messages'
import { chart, tooltipStyles } from './lib/chartTheme'

const UNIDAD_LABEL: Record<string, string> = {
  personas: 'personas',
  peso: 'kg',
  hectareas: 'ha',
  casos: 'casos',
}

function formatearUnidad(u: string): string {
  return UNIDAD_LABEL[u] ?? u
}

type AnosMap = Record<number, boolean>

interface FiltrosAplicados {
  anos: number[]
  tipoEvento: string
  departamento: string
}

function App() {
  const [metadata, setMetadata] = useState<MetadataResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [anosSeleccionados, setAnosSeleccionados] = useState<AnosMap>(() =>
    ANOS_DISPONIBLES.reduce<AnosMap>((acc, y) => {
      acc[y] = ANOS_PRESELECCIONADOS.includes(y)
      return acc
    }, {}),
  )
  const [tipoEvento, setTipoEvento] = useState('')
  const [departamento, setDepartamento] = useState('')

  const [filtrosAplicados, setFiltrosAplicados] = useState<FiltrosAplicados>({
    anos: [...ANOS_PRESELECCIONADOS],
    tipoEvento: '',
    departamento: '',
  })
  const [chartsLoading, setChartsLoading] = useState(false)
  const [serieTemporal, setSerieTemporal] = useState<SerieTemporalRow[]>([])
  const [departamentos, setDepartamentos] = useState<DepartamentoRow[]>([])
  const [concentracion, setConcentracion] = useState<ConcentracionResponse>({ gini: 0, data: [] })
  const [estacionalidad, setEstacionalidad] = useState<EstacionalidadResponse>({
    mes_pico: null,
    patron_mensual: [],
  })

  const anosActivos = Object.entries(anosSeleccionados)
    .filter(([, v]) => v)
    .map(([k]) => parseInt(k, 10))

  const aplicarFiltros = () => {
    if (anosActivos.length === 0) return
    setFiltrosAplicados({ anos: anosActivos, tipoEvento, departamento })
  }

  const filters = useMemo(
    () => ({
      anos: filtrosAplicados.anos?.length ? filtrosAplicados.anos.join(',') : undefined,
      tipo_evento: filtrosAplicados.tipoEvento || undefined,
      departamento: filtrosAplicados.departamento || undefined,
    }),
    [filtrosAplicados.anos, filtrosAplicados.tipoEvento, filtrosAplicados.departamento],
  )

  /** «Todos» en tipo de evento = sin filtro: no se consulta la API ni se grafica. */
  const hayTipoEventoSeleccionado = Boolean(filtrosAplicados.tipoEvento?.trim())

  const unidadFiltro = metadata?.unidades_tipo_evento?.[filtrosAplicados.tipoEvento]
  const sufijoUnidad = unidadFiltro ? ` [${formatearUnidad(unidadFiltro)}]` : ''

  const toggleAno = (ano: number) => {
    setAnosSeleccionados((prev) => ({ ...prev, [ano]: !prev[ano] }))
  }

  const seleccionarTodos = () => {
    setAnosSeleccionados(ANOS_DISPONIBLES.reduce<AnosMap>((acc, y) => ({ ...acc, [y]: true }), {}))
  }

  const seleccionarNinguno = () => {
    setAnosSeleccionados(ANOS_DISPONIBLES.reduce<AnosMap>((acc, y) => ({ ...acc, [y]: false }), {}))
  }

  useEffect(() => {
    getMetadata()
      .then(setMetadata)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (!metadata) return
    if (!filters.anos) return

    if (!hayTipoEventoSeleccionado) {
      setSerieTemporal([])
      setDepartamentos([])
      setConcentracion({ gini: 0, data: [] })
      setEstacionalidad({ mes_pico: null, patron_mensual: [] })
      setChartsLoading(false)
      return
    }

    setChartsLoading(true)
    const load = async () => {
      try {
        const [serie, deptos, conc, est] = await Promise.all([
          getSerieTemporal(filters),
          getDepartamentos(filters),
          getConcentracion(filters),
          getEstacionalidad(filters),
        ])
        setSerieTemporal(serie.data ?? [])
        setDepartamentos(deptos.data ?? [])
        setConcentracion({ gini: conc.gini ?? 0, data: conc.data ?? [] })
        setEstacionalidad({
          mes_pico: est.mes_pico,
          patron_mensual: (est.patron_mensual ?? []).map((d: PatronMensualRow) => ({
            ...d,
            promedio: Number(d.promedio),
          })),
        })
      } catch (e) {
        setError(e instanceof Error ? e.message : ui.app.errorDesconocido)
      } finally {
        setChartsLoading(false)
      }
    }

    void load()
  }, [metadata, filters, hayTipoEventoSeleccionado])

  if (loading) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-surface-void px-6">
        <div className="h-12 w-48 skeleton-pulse" />
        <div className="h-4 w-72 skeleton-pulse" />
        <p className="font-body text-sm text-warm-stone">{ui.app.loadingMetadatos}</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="mx-auto max-w-lg rounded-xl border border-copper-rich bg-surface-charcoal p-8 text-center">
        <p className="font-display text-xl text-copper-light">{ui.app.errorTitulo}</p>
        <p className="mt-3 font-body text-sm text-warm-cream">{error}</p>
        <p className="mt-4 font-body text-xs text-warm-stone">
          {ui.app.errorHelpPart1}
          <code className="rounded bg-surface-graphite px-1 text-warm-white">{ui.app.runDashboardCmd}</code>
          {ui.app.errorHelpPart2}
          <code className="rounded bg-surface-graphite px-1">{ui.app.apiContainerName}</code>
          {ui.app.errorHelpPart3}
        </p>
      </div>
    )
  }

  return (
    <div className="app mx-auto min-h-screen max-w-[1400px] px-4 pb-12 pt-2">
      <Header />

      <section className="filter-shell mt-8 flex flex-wrap gap-6">
        <div className="min-w-[280px] flex-1">
          <span className="label-dark">{ui.filters.labelAnos}</span>
          <div className="mb-2 mt-1 flex gap-2 text-sm text-warm-cream">
            <button type="button" className="btn-ghost border-0 p-0" onClick={seleccionarTodos}>
              {ui.filters.anosTodos}
            </button>
            <span className="text-warm-ash">|</span>
            <button type="button" className="btn-ghost border-0 p-0" onClick={seleccionarNinguno}>
              {ui.filters.anosNinguno}
            </button>
          </div>
          <div className="max-h-[120px] overflow-y-auto rounded-lg border border-surface-smoke bg-surface-graphite p-2">
            <div className="flex flex-wrap gap-x-4 gap-y-1">
              {ANOS_DISPONIBLES.map((ano) => (
                <label
                  key={ano}
                  className="flex cursor-pointer items-center gap-1.5 whitespace-nowrap font-body text-xs text-warm-cream"
                >
                  <input
                    type="checkbox"
                    checked={anosSeleccionados[ano] ?? false}
                    onChange={() => toggleAno(ano)}
                    className="accent-copper"
                  />
                  {ano}
                </label>
              ))}
            </div>
          </div>
        </div>
        <div className="flex min-w-[180px] flex-col gap-1">
          <label htmlFor="tipo" className="label-dark">
            {ui.filters.labelTipoEvento}
          </label>
          <select
            id="tipo"
            value={tipoEvento}
            onChange={(e) => setTipoEvento(e.target.value)}
            className="input-dark min-w-[180px]"
          >
            <option value="">{ui.filters.opcionTodos}</option>
            {metadata?.tipos_evento?.map((t) => (
              <option key={t} value={t}>
                {metadata?.unidades_tipo_evento?.[t]
                  ? `${t} [${formatearUnidad(metadata.unidades_tipo_evento[t])}]`
                  : t}
              </option>
            ))}
          </select>
        </div>
        <div className="flex min-w-[180px] flex-col gap-1">
          <label htmlFor="depto" className="label-dark">
            {ui.filters.labelDepartamento}
          </label>
          <select
            id="depto"
            value={departamento}
            onChange={(e) => setDepartamento(e.target.value)}
            className="input-dark min-w-[180px]"
          >
            <option value="">{ui.filters.opcionTodos}</option>
            {metadata?.departamentos?.map((d) => (
              <option key={d} value={d}>
                {d}
              </option>
            ))}
          </select>
        </div>
        <div className="flex flex-col justify-end gap-2 self-end">
          <span className="label-dark opacity-0">{ui.filters.labelAcciones}</span>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              className="btn-primary"
              onClick={aplicarFiltros}
              disabled={anosActivos.length === 0}
              title={anosActivos.length === 0 ? ui.filters.graficarDisabledTitle : ''}
            >
              {ui.filters.botonGraficar}
            </button>
            <a
              href={`/api/exportar?anos=${encodeURIComponent(filtrosAplicados.anos?.join(',') ?? '')}&tipo_evento=${encodeURIComponent(filtrosAplicados.tipoEvento)}&departamento=${encodeURIComponent(filtrosAplicados.departamento)}&formato=csv`}
              className="btn-export"
              download
            >
              {ui.filters.exportarCsv}
            </a>
          </div>
        </div>
      </section>

      <main className="mt-8 grid min-w-0 grid-cols-1 gap-6 md:grid-cols-[repeat(auto-fit,minmax(380px,1fr))]">
        {chartsLoading && hayTipoEventoSeleccionado && (
          <div className="col-span-full rounded-xl border border-accent-steelblue bg-surface-obsidian px-4 py-4 text-center font-body text-sm text-warm-cream">
            {ui.charts.cargando}
          </div>
        )}

        <section className="card-dashboard col-span-full">
          <h2 className="font-display text-xl tracking-wide text-warm-white">
            {ui.charts.serieTemporalTitulo}
            {sufijoUnidad}
          </h2>
          <p className="mt-1 font-body text-sm text-warm-stone">{ui.charts.serieTemporalDesc}</p>
          <div
            className={`relative mt-4 w-full min-w-0 ${!hayTipoEventoSeleccionado ? 'opacity-40' : ''}`}
          >
            <ResponsiveContainer width="100%" height={280} minWidth={0}>
              <LineChart data={hayTipoEventoSeleccionado ? serieTemporal : []}>
                <CartesianGrid stroke={chart.grid} strokeDasharray="3 3" />
                <XAxis dataKey="periodo" stroke={chart.axis} tick={{ fill: 'var(--tooltip-text)', fontSize: 11 }} />
                <YAxis stroke={chart.axis} tick={{ fill: 'var(--tooltip-text)', fontSize: 11 }} />
                <Tooltip {...tooltipStyles} />
                <Legend wrapperStyle={{ color: 'var(--tooltip-text)' }} />
                <Line
                  type="monotone"
                  dataKey="total"
                  stroke={chart.linePrimary}
                  strokeWidth={2}
                  name={ui.charts.leyendaTotal}
                />
              </LineChart>
            </ResponsiveContainer>
            {!hayTipoEventoSeleccionado && (
              <p className="pointer-events-none absolute inset-0 flex items-center justify-center px-4 text-center font-body text-sm text-warm-stone">
                {ui.charts.sinTipoOverlay}
              </p>
            )}
          </div>
        </section>

        <section className="card-dashboard">
          <h2 className="font-display text-xl text-warm-white">
            {ui.charts.topDeptosTitulo}
            {sufijoUnidad}
          </h2>
          <p className="mt-1 font-body text-sm text-warm-stone">{ui.charts.topDeptosDesc}</p>
          <div
            className={`relative mt-4 w-full min-w-0 ${!hayTipoEventoSeleccionado ? 'opacity-40' : ''}`}
          >
            <ResponsiveContainer width="100%" height={240} minWidth={0}>
              <BarChart
                data={hayTipoEventoSeleccionado ? departamentos : []}
                layout="vertical"
                margin={{ left: 88 }}
              >
                <CartesianGrid stroke={chart.grid} strokeDasharray="3 3" />
                <XAxis type="number" stroke={chart.axis} tick={{ fill: 'var(--tooltip-text)', fontSize: 11 }} />
                <YAxis
                  type="category"
                  dataKey="departamento"
                  width={86}
                  stroke={chart.axis}
                  tick={{ fill: 'var(--tooltip-text)', fontSize: 10 }}
                />
                <Tooltip {...tooltipStyles} />
                <Bar dataKey="total" fill={chart.bar2} name={ui.charts.leyendaTotal} />
              </BarChart>
            </ResponsiveContainer>
            {!hayTipoEventoSeleccionado && (
              <p className="pointer-events-none absolute inset-0 flex items-center justify-center px-4 text-center font-body text-sm text-warm-stone">
                {ui.charts.sinTipoOverlay}
              </p>
            )}
          </div>
        </section>

        <section className="card-dashboard">
          <h2 className="font-display text-xl text-warm-white">
            {ui.charts.concentracionTitulo}
            {sufijoUnidad}
          </h2>
          <p className="mt-1 font-body text-sm text-warm-stone">{ui.charts.concentracionDesc}</p>
          <p className="mt-2 font-body text-sm text-warm-cream">
            {ui.charts.giniEtiqueta}{' '}
            <strong className="text-accent-gold">
              {hayTipoEventoSeleccionado
                ? (concentracion.gini?.toFixed(4) ?? ui.charts.na)
                : ui.charts.emDash}
            </strong>
          </p>
          <div
            className={`relative mt-4 w-full min-w-0 ${!hayTipoEventoSeleccionado ? 'opacity-40' : ''}`}
          >
            <ResponsiveContainer width="100%" height={220} minWidth={0}>
              <BarChart data={hayTipoEventoSeleccionado ? concentracion.data : []}>
                <CartesianGrid stroke={chart.grid} strokeDasharray="3 3" />
                <XAxis dataKey="departamento" stroke={chart.axis} tick={{ fill: 'var(--tooltip-text)', fontSize: 10 }} />
                <YAxis stroke={chart.axis} tick={{ fill: 'var(--tooltip-text)', fontSize: 11 }} />
                <Tooltip {...tooltipStyles} />
                <Bar dataKey="pct_acumulado" fill={chart.bar4} name={ui.charts.leyendaPctAcumulado} />
              </BarChart>
            </ResponsiveContainer>
            {!hayTipoEventoSeleccionado && (
              <p className="pointer-events-none absolute inset-0 flex items-center justify-center px-4 text-center font-body text-sm text-warm-stone">
                {ui.charts.sinTipoOverlay}
              </p>
            )}
          </div>
        </section>

        <section className="card-dashboard">
          <h2 className="font-display text-xl text-warm-white">
            {ui.charts.estacionalidadTitulo}
            {sufijoUnidad}
          </h2>
          <p className="mt-1 font-body text-sm text-warm-stone">
            {ui.charts.estacionalidadMesPico}{' '}
            <strong className="text-warm-white">
              {hayTipoEventoSeleccionado
                ? (estacionalidad.mes_pico?.mes_nombre ?? ui.charts.na)
                : ui.charts.emDash}
            </strong>
            {hayTipoEventoSeleccionado &&
              estacionalidad.mes_pico?.pct_del_total != null &&
              ` (${estacionalidad.mes_pico.pct_del_total}%)`}
          </p>
          <p className="mt-2 max-w-prose font-body text-xs italic text-warm-stone">{ui.charts.estacionalidadDesc}</p>
          <div
            className={`relative mt-4 w-full min-w-0 ${!hayTipoEventoSeleccionado ? 'opacity-40' : ''}`}
          >
            <ResponsiveContainer width="100%" height={220} minWidth={0}>
              <BarChart data={hayTipoEventoSeleccionado ? estacionalidad.patron_mensual : []}>
                <CartesianGrid stroke={chart.grid} strokeDasharray="3 3" />
                <XAxis dataKey="mes_nombre" stroke={chart.axis} tick={{ fill: 'var(--tooltip-text)', fontSize: 10 }} />
                <YAxis
                  stroke={chart.axis}
                  tick={{ fill: 'var(--tooltip-text)', fontSize: 10 }}
                  tickFormatter={(v: number) =>
                    v >= 1e6 ? `${(v / 1e6).toFixed(1)}M` : v >= 1e3 ? `${(v / 1e3).toFixed(0)}k` : String(v)
                  }
                  domain={[0, 'auto']}
                  label={{
                    value: ui.charts.ejePromedioAnual,
                    angle: -90,
                    position: 'insideLeft',
                    fill: 'var(--chart-axis)',
                    fontSize: 11,
                  }}
                />
                <Tooltip
                  {...tooltipStyles}
                  formatter={(v) => [
                    Number(v ?? 0).toLocaleString('es-CO'),
                    ui.charts.tooltipPromedioAnual,
                  ]}
                />
                <Bar dataKey="promedio" fill={chart.bar5} name={ui.charts.barPromedioNombre} />
              </BarChart>
            </ResponsiveContainer>
            {!hayTipoEventoSeleccionado && (
              <p className="pointer-events-none absolute inset-0 flex items-center justify-center px-4 text-center font-body text-sm text-warm-stone">
                {ui.charts.sinTipoOverlay}
              </p>
            )}
          </div>
        </section>
      </main>

      <footer className="mt-12 border-t border-surface-smoke pt-8 text-center font-body text-xs text-warm-stone">
        <p>{ui.footer.fuente}</p>
        <p className="mt-1 text-warm-ash">{ui.footer.disclaimer}</p>
      </footer>
    </div>
  )
}

export default App
