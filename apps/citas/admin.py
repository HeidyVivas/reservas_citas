from django.contrib import admin
from .models import Cita, Servicio

# Configuración de Servicio en el admin.
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'duracion', 'precio']  # Columnas visibles en la tabla
    search_fields = ['nombre']  # Permite buscar servicios por nombre
    list_filter = ['duracion']  # Filtro lateral por duración del servicio


# Configuración del modelo Cita en el admin.
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ['servicio', 'cliente', 'fecha', 'hora', 'created_at']  # Lo que se ve en la tabla
    list_filter = ['fecha', 'servicio', 'created_at']  # Filtros laterales para ubicar citas más fácil
    search_fields = ['cliente__username', 'cliente__email', 'servicio__nombre']  # Búsqueda por cliente o servicio
    readonly_fields = ['created_at']  # Campo solo de lectura
    ordering = ['-fecha', '-hora']  # Ordena las citas de la más reciente a la más antigua


