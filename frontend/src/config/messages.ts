/**
 * Cadenas visibles del dashboard (español).
 * Centraliza textos de UI para revisión y posible i18n.
 */
export const ui = {
  header: {
    logoAlt: 'SuaGO',
    eyebrow: 'Dashboard · Ministerio de Defensa · Datos oficiales',
    titleAccent: 'Seguridad y violencia',
    titleRest: 'Colombia',
    lead:
      'Explora tendencias y territorio con filtros. Cada indicador lleva su unidad: compara con criterio, no sumes peras con manzanas.',
    linkDatasetsExcel: 'Descarga los dataset en excel',
  },
  app: {
    loadingMetadatos: 'Preparando el tablero y los metadatos…',
    errorTitulo: 'No pudimos cargar el dashboard',
    errorDesconocido: 'Error desconocido',
    errorHelpPart1: 'Comprueba que la API esté en marcha (por ejemplo ',
    errorHelpPart2: ') o que el contenedor ',
    errorHelpPart3: ' esté arriba si usas Docker.',
    runDashboardCmd: 'python run_dashboard.py',
    apiContainerName: 'api',
  },
  filters: {
    labelAnos: 'Años',
    anosTodos: 'Todos',
    anosNinguno: 'Ninguno',
    labelTipoEvento: 'Tipo de evento',
    labelDepartamento: 'Departamento',
    opcionTodos: 'Todos',
    labelAcciones: 'Acciones',
    botonGraficar: 'Graficar',
    graficarDisabledTitle: 'Seleccione al menos un año',
    exportarCsv: 'Exportar CSV',
  },
  charts: {
    cargando: 'Cargando gráficos con los filtros aplicados…',
    sinTipoOverlay:
      'Seleccione un tipo de evento (distinto de «Todos») y pulse Graficar.',
    serieTemporalTitulo: 'Serie temporal',
    serieTemporalDesc:
      'Evolución del agregado en el tiempo según tu selección (año o mes según API).',
    topDeptosTitulo: 'Top departamentos',
    topDeptosDesc: 'Departamentos con mayor volumen en el filtro actual.',
    concentracionTitulo: 'Concentración territorial',
    concentracionDesc:
      'Gini y acumulado por departamento: qué tan concentrado está el fenómeno en pocos territorios.',
    giniEtiqueta: 'Índice Gini:',
    estacionalidadTitulo: 'Estacionalidad (patrón mensual)',
    estacionalidadMesPico: 'Mes pico:',
    estacionalidadDesc:
      'Promedio anual por mes entre los años seleccionados (cada barra es el promedio de ese mes en distintos años).',
    na: 'N/A',
    emDash: '—',
    leyendaTotal: 'Total',
    leyendaPctAcumulado: '% acumulado',
    ejePromedioAnual: 'Promedio anual',
    tooltipPromedioAnual: 'Promedio anual',
    barPromedioNombre: 'Promedio anual por mes',
  },
  footer: {
    fuente:
      'Fuente: Ministerio de Defensa Nacional · Policía Nacional · Fiscalía General de la Nación',
    disclaimer:
      'Datos presentados de forma objetiva; la interpretación queda a criterio del usuario.',
  },
} as const
