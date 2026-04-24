import { MIN_DEFENSA_INFORMACION_ESTADISTICA } from '../../config/externalLinks'
import { ui } from '../../config/messages'

/**
 * Cabecera del dashboard: logo SuaGO, identidad visual y gradiente copper en el título (Fase A).
 * El subtítulo ancla la fuente oficial sin interpretación política.
 */
export function Header() {
  return (
    <header className="border-b border-surface-smoke pb-8 pt-6 text-center">
      <div className="mb-5 flex justify-center">
        <img
          src="/logo-suago.png"
          alt={ui.header.logoAlt}
          width={112}
          height={112}
          className="h-24 w-24 rounded-full object-cover shadow-[0_8px_32px_rgba(0,0,0,0.45)] ring-1 ring-surface-smoke md:h-28 md:w-28"
          decoding="async"
        />
      </div>
      <p className="font-body text-xs font-semibold uppercase tracking-[0.2em] text-accent-gold">
        {ui.header.eyebrow}
      </p>
      <h1 className="font-display mt-3 text-4xl tracking-wide md:text-5xl">
        <span className="gradient-copper-text">{ui.header.titleAccent}</span>
        <span className="block font-display text-warm-white md:inline md:before:content-['_']">
          {ui.header.titleRest}
        </span>
      </h1>
      <p className="mx-auto mt-4 max-w-2xl font-body text-sm italic text-warm-stone">{ui.header.lead}</p>
      <p className="mt-5 font-body text-sm text-warm-stone">
        <a
          href={MIN_DEFENSA_INFORMACION_ESTADISTICA}
          target="_blank"
          rel="noopener noreferrer"
          className="text-accent-gold underline decoration-warm-stone/50 underline-offset-2 transition-colors hover:text-warm-cream"
        >
          {ui.header.linkDatasetsExcel}
        </a>
      </p>
    </header>
  )
}
