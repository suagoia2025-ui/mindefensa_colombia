#!/usr/bin/env python3
"""
Inicia el servidor API del dashboard.

Ejecutar desde la raíz del proyecto:
    python run_dashboard.py

Luego en otra terminal, iniciar el frontend:
    cd frontend && npm run dev
"""

import sys
from pathlib import Path

# Asegurar proyecto en path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
