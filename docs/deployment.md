# Despliegue en producción — Análisis Seguridad Colombia

Documento generado según `deploy_prompt.md` (Fase 0). Actualizar la **URL de demo** cuando la instancia EC2 esté operativa.

## A. Sizing EC2

| Recurso | Recomendación |
|--------|----------------|
| **Instancia** | `t3.medium` (2 vCPU, 4 GiB RAM) como mínimo para demo/portafolio con **swap 4 GiB**. Si el dataset completo no cabe cómodamente en RAM, valorar `t3.large` (8 GiB). |
| **RAM / datos** | El dataset maestro (~7,4M filas) se cachea en memoria en la API (`pandas` vía `load_maestro`). Con 4 GiB + swap suele ser viable para consultas filtradas; monitorear `free -h` y latencia. |
| **EBS** | 30 GiB `gp3` suele bastar para Parquet, imágenes Docker y logs. |
| **AMI** | Ubuntu Server 24.04 LTS (x86_64). |

## B. Estrategia de datos

- Los Parquet/CSV **no** van en Git; se copian en el servidor bajo el árbol del proyecto montado en Docker.
- Ruta por defecto del código: `data/processed/eventos_seguridad_maestro` (`.parquet` o `.csv`).
- Alternativa en EC2: directorio dedicado (p. ej. `data/parquet/`) y variable de entorno **`EVENTOS_MAESTRO_PATH`** apuntando al archivo base (sin extensión o con `.parquet`/`.csv`).
- Transferencia: `scp`/`rsync` desde local, o sincronización desde S3 (documentar bucket y política IAM según tu cuenta).

## C. Dominio y SSL

- **Con dominio:** Let's Encrypt + Certbot; montar certificados en el contenedor nginx (ver comentarios en `docker-compose.prod.yml`).
- **Solo IP pública:** HTTP en puerto 80 es aceptable para demo de portafolio; actualizar CORS en `.env.production`.

## Archivos de despliegue en el repo

| Archivo | Uso |
|---------|-----|
| `docker-compose.prod.yml` | API + frontend nginx |
| `Dockerfile.api` | Imagen FastAPI |
| `frontend/Dockerfile.frontend` | Build estático + nginx runtime |
| `nginx/nginx.conf` | SPA + proxy `/api/` al backend |
| `.env.production.example` | Plantilla de variables (copiar a `.env.production` en el servidor) |

## Comandos rápidos (servidor)

```bash
cd ~/apps/analisis-seguridad/mindefensa_colombia
cp .env.production.example .env.production   # y editar ALLOWED_ORIGINS
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
curl -s http://127.0.0.1/api/health
```

## CI/CD (GitHub Actions)

Workflow: `.github/workflows/deploy.yml`. Se ejecuta en **push** a `master` o `main` (y manualmente con **Run workflow**).

### Secrets del repositorio

En GitHub: **Settings → Secrets and variables → Actions → New repository secret**.

| Secret | Valor ejemplo |
|--------|----------------|
| `EC2_HOST` | IP pública o Elastic IP (ej. `75.101.193.108`) |
| `EC2_USER` | `ubuntu` |
| `EC2_SSH_KEY` | Contenido completo de la clave **privada** que usa Actions para entrar al servidor (ver abajo) |
| `EC2_WORK_DIR` | Ruta absoluta del repo en EC2: `/home/ubuntu/apps/analisis-seguridad/mindefensa_colombia` |

**Clave SSH para CI:** no reutilices tu `.pem` personal en el secret si puedes evitarlo. Opción recomendada: en el servidor generar un par solo para GitHub (`ssh-keygen`), añadir la **pública** a `~/.ssh/authorized_keys` y guardar la **privada** en `EC2_SSH_KEY`. Así revocas CI sin tocar tu acceso habitual.

### Comprobar en EC2 antes del primer deploy

- El directorio `EC2_WORK_DIR` es un clone **git** del mismo repo (puede hacer `git pull`).
- Existe `.env.production` (no va en Git).
- Están los datos en `data/processed/eventos_seguridad_maestro.parquet`.

## URL de demo (portafolio)

Marcador en README y aquí: **`TU_ELASTIC_IP`** → reemplazar por tu IPv4 (ej. la Elastic IP asociada a la instancia).

| Recurso | URL |
|---------|-----|
| Dashboard | `http://TU_ELASTIC_IP/` |
| Metadatos | `http://TU_ELASTIC_IP/api/metadata` |
| Salud | `http://TU_ELASTIC_IP/api/health` |

### Tras asignar Elastic IP

Ejecutar en orden (sustituir `TU_ELASTIC_IP` por tu IPv4 real en cada sitio):

1. **AWS Console → EC2 → Instances:** anotar **Public IPv4 address** (debe coincidir con la Elastic IP asociada).
2. **Mac — SSH:** en `~/.ssh/config`, bloque `Host seguridad-colombia`, poner `HostName TU_ELASTIC_IP`.
3. **GitHub — Secrets:** editar `EC2_HOST` → valor `TU_ELASTIC_IP` (solo dígitos y puntos, sin `http://`).
4. **EC2 — CORS:** en el servidor:
   ```bash
   cd ~/apps/analisis-seguridad/mindefensa_colombia
   nano .env.production
   ```
   En `ALLOWED_ORIGINS` incluir al menos `http://TU_ELASTIC_IP` y `http://localhost`. Guardar y aplicar:
   ```bash
   docker compose -f docker-compose.prod.yml up -d
   ```
5. **Repo — documentación:** buscar y reemplazar en `README.md` y en este archivo el texto `TU_ELASTIC_IP` por tu IP (o dejar el marcador si prefieres no publicar la IP en Git).
6. **Comprobar:** abrir en el navegador `http://TU_ELASTIC_IP/` y `http://TU_ELASTIC_IP/api/health`.

## Checklist (resumen)

Ver checklist completo en `deploy_prompt.md` (secciones finales). Incluye: EC2, security groups, Elastic IP, swap, Docker, datos en disco, `.env.production`, health checks, systemd opcional, CI/CD y CloudWatch opcional.
