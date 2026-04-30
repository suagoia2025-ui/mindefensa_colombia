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
cd ~/apps/analisis-seguridad
cp .env.production.example .env.production   # y editar ALLOWED_ORIGINS / rutas
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
curl -s http://localhost/api/health
```

## URL de demo (portafolio)

- **Pendiente:** `http://<ELASTIC_IP>` o `https://<dominio>`
- Actualizar esta sección y el README cuando el despliegue esté completo.

## Checklist (resumen)

Ver checklist completo en `deploy_prompt.md` (secciones finales). Incluye: EC2, security groups, Elastic IP, swap, Docker, datos en disco, `.env.production`, health checks, systemd opcional, CI/CD y CloudWatch opcional.
