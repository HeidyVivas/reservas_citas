from django.contrib import admin
from .models import Cita, Servicio

# El modelo Servicio en el panel de administración.
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'duracion', 'precio']  # Muestra estos campos en la lista de servicios
    search_fields = ['nombre']  # Permite buscar un servicio por su nombre
    list_filter = ['duracion']  # Filtro rápido para organizar servicios por duración


# Ajustes del modelo Cita dentro del admin.
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['servicio', 'cliente', 'fecha', 'hora', 'created_at']  # Campos visibles al listar las citas
    list_filter = ['fecha', 'servicio', 'created_at']  # Filtros para encontrar citas según fecha o servicio
    search_fields = ['cliente__username', 'cliente__email', 'servicio__nombre']  # Búsqueda por cliente o nombre del servicio
    readonly_fields = ['created_at']  # Evita que la fecha de creación sea modificada
    ordering = ['-fecha', '-hora']  # Muestra primero las citas más recientes


