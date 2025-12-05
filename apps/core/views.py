from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        "status": "ok",
        "service": "reservas_citas",
        "version": "1.0"
    })
