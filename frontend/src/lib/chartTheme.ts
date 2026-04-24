/**
 * Tokens para Recharts: referencias a variables CSS definidas en `styles/globals.css`.
 * Evita literales hex en componentes (Fase A — diseño por tokens).
 */
export const chart = {
  linePrimary: 'var(--chart-line-primary)',
  bar2: 'var(--chart-bar-2)',
  bar4: 'var(--chart-bar-4)',
  bar5: 'var(--chart-bar-5)',
  grid: 'var(--chart-grid)',
  axis: 'var(--chart-axis)',
} as const

export const tooltipStyles = {
  contentStyle: {
    backgroundColor: 'var(--tooltip-bg)',
    border: '1px solid var(--tooltip-border)',
    borderRadius: '8px',
    color: 'var(--tooltip-text)',
  },
  labelStyle: { color: 'var(--tooltip-text)' },
} as const
