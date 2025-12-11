from django.contrib import admin
from .models import Cita, Servicio

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'duracion', 'precio']
    search_fields = ['nombre']
    list_filter = ['duracion']


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['servicio', 'cliente', 'fecha', 'hora', 'created_at']
    list_filter = ['fecha', 'servicio', 'created_at']
    search_fields = ['cliente__username', 'cliente__email', 'servicio__nombre']
    readonly_fields = ['created_at']
    ordering = ['-fecha', '-hora']


