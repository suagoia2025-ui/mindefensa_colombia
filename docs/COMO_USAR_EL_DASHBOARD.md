# Cómo usar el dashboard

Instrucciones para usar el dashboard de Análisis de Seguridad y Violencia (Colombia).

---

## 1. Iniciar el dashboard

### Opción A: Con Docker (recomendado para producción o despliegue)

1. **Asegurar que existan los datos procesados** (una vez):
   ```bash
   python 02_run_etl.py
   ```

2. **Construir y levantar contenedores:**
   ```bash
   docker compose up --build
   ```

3. **Abrir en el navegador:** http://localhost (el frontend sirve en el puerto 80 y redirige `/api` al backend).

Para detener: `docker compose down`.

### Opción B: Sin Docker (desarrollo local)

### Primera vez (instalación)

1. **Asegurar que existan los datos procesados.**  
   Si aún no lo has hecho, ejecuta el ETL una vez:
   ```bash
   python 02_run_etl.py
   ```

2. **Instalar dependencias del frontend:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Cada vez que quieras usar el dashboard

Abre **dos terminales** en la carpeta del proyecto.

**Terminal 1 – Backend (API):**
```bash
python run_dashboard.py
```
Deja esta terminal abierta. Debe mostrar algo como: `Uvicorn running on http://0.0.0.0:8000`.

**Terminal 2 – Frontend (página web):**
```bash
cd frontend
npm run dev
```
Deja esta terminal abierta. Verás una URL, normalmente: `http://localhost:5173`.

3. **Abrir el dashboard en el navegador:**  
   Entra a **http://localhost:5173**.

---

## 2. Filtros

En la parte superior del dashboard hay tres filtros:

| Filtro | Uso |
|--------|-----|
| **Años** | Años a analizar, separados por coma. Ejemplo: `2020,2021,2022,2023` o `2015,2020,2024`. Rango disponible en los datos: **2002 a 2025**. |
| **Tipo de evento** | Desplegable con categorías (homicidio intencional, hurtos, violencia intrafamiliar, etc.). "Todos" = no filtrar por tipo. |
| **Departamento** | Desplegable con departamentos. "Todos" = Colombia completo. |

Al cambiar cualquier filtro, los gráficos se actualizan solos.

---

## 3. Gráficos y qué significan

- **Serie temporal**  
  Evolución del total de eventos por año (o por período). Sirve para ver tendencias en el tiempo.

- **Comparación año a año**  
  Barras con el total por año. Útil para ver si un año sube o baja respecto al anterior.

- **Top departamentos**  
  Departamentos con más casos en el período y filtros elegidos. Ordenado de mayor a menor.

- **Top tipos de evento**  
  Tipos de delito/evento con más registros. Permite ver qué categorías dominan.

- **Concentración territorial**  
  Índice Gini (0 = muy repartido, 1 = muy concentrado) y barras de % acumulado por departamento. Muestra si los eventos se concentran en pocos departamentos.

- **Estacionalidad (patrón mensual)**  
  Promedio por mes (enero a diciembre) y mes en el que suele haber más eventos ("mes pico").

---

## 4. Exportar datos

- **Botón "Exportar CSV"**  
  Descarga un archivo CSV con los datos que estás viendo según los filtros actuales (hasta 100.000 filas).  
  Úsalo para analizar en Excel o en otro programa.

---

## 5. Consejos rápidos

- Para comparar varios años: pon en **Años** algo como `2018,2019,2020,2021,2022`.
- Para un solo tipo de delito: elige ese tipo en **Tipo de evento** y deja **Departamento** en "Todos" para ver el país.
- Para un departamento: elige el departamento y, si quieres, restringe también el **Tipo de evento**.
- El año **2025** puede estar incompleto; para “año completo” usa hasta **2024**.

---

## 6. Si algo no funciona

- **"Error: ... ¿Está corriendo el backend?"**  
  Asegúrate de tener el backend en marcha en otra terminal: `python run_dashboard.py`.

- **Página en blanco o no carga**  
  Confirma que entras a **http://localhost:5173** (frontend) y que en la otra terminal está corriendo `npm run dev` dentro de `frontend`.

- **No hay datos**  
  Verifica que hayas ejecutado antes el ETL: `python 02_run_etl.py`, y que exista el archivo en `data/processed/` (por ejemplo `eventos_seguridad_maestro.csv`).
