from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError

def health(request):
    db_conn = connections['default']
    try:
        c = db_conn.cursor()
        c.execute("SELECT 1;")
        c.fetchone()
    except OperationalError:
        return JsonResponse({"status": "error", "db": "unavailable"}, status=503)
    return JsonResponse({"status": "ok"}, status=200)
