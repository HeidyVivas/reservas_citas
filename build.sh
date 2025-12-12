#!/bin/bash
# build.sh - Script de build para Render

set -o errexit

echo "==> Instalando dependencias..."
pip install -r requirements.txt

echo "==> Ejecutando migraciones..."
python manage.py migrate --noinput

echo "==> Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "==> Build completado exitosamente!"
