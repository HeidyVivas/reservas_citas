from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

def health(request):
    """
    Endpoint simple de Health Check.
    Verifica si la base de datos está disponible.
    Retorna:
    - 200 OK si la DB responde
    - 503 SERVICE UNAVAILABLE si hay error de conexión
    """
    # Obtener la conexión por defecto de la base de datos
    db_conn = connections['default']
    try:
        # Intentar ejecutar un SELECT simple para comprobar la DB
        c = db_conn.cursor()
        c.execute("SELECT 1;")
        c.fetchone()  # Recuperar un resultado (aunque no lo usamos)
    except OperationalError:
        # Si falla la conexión, retornar error 503
        return JsonResponse({"status": "error", "db": "unavailable"}, status=503)

    # Si la DB está bien, retornar estado OK
    return JsonResponse({"status": "ok"}, status=200)
