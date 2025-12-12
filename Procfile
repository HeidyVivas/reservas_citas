# ============================================================================
# Comando para iniciar la app en producción usando Gunicorn
# ============================================================================
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --log-file -
# - config.wsgi: archivo WSGI de Django
# - --bind 0.0.0.0:$PORT: se enlaza al puerto que Render asigna
# - --log-file -: logs en stdout (se ven en la consola de Render)

# ============================================================================
# Comando para ejecutar migraciones al desplegar
# ============================================================================
release: python manage.py migrate --noinput
# - Aplica todas las migraciones pendientes
# - --noinput: evita preguntas interactivas, útil para despliegues automáticos
