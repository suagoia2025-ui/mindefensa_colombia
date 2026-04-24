/**
 * Tailwind v4: tokens de color y tipografía viven principalmente en `src/styles/globals.css` (@theme).
 * Este archivo documenta el contrato del diseño y permite futuras extensiones (plugins, content).
 */
import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
} satisfies Config
