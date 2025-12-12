#  Guía de Testing - Reservas Citas API

##  Estructura de Tests

```
apps/
├── core/
│   └── tests.py          # Tests de health check y documentación
├── users/
│   └── tests.py          # Tests de usuarios, permisos, autenticación
├── citas/
│   └── tests.py          # Tests de modelos y API de citas
```

##  Instalación de Dependencias

Las dependencias de testing ya están en `requirements.txt`:

```bash
pip install -r requirements.txt
```

O instalar solo testing:

```bash
pip install pytest pytest-django pytest-cov factory-boy
```

##  Ejecutar Tests

### **Todos los tests**
```bash
pytest
```

### **Tests con cobertura**
```bash
pytest --cov=apps --cov-report=html
```
Esto genera un reporte HTML en `htmlcov/index.html`

### **Tests de una aplicación específica**
```bash
pytest apps/users/                    # Solo tests de usuarios
pytest apps/citas/                    # Solo tests de citas
pytest apps/core/                     # Solo tests de core/health
```

### **Tests específicos**
```bash
pytest apps/users/tests.py::UserCreationTests::test_create_user_with_valid_data
```

### **Tests con verbosidad**
```bash
pytest -v                             # Más detallado
pytest -vv                            # Muy detallado
```

### **Tests lentos (si tienes marcas)**
```bash
pytest -m "not slow"                  # Excluir tests lentos
pytest -m "unit"                      # Solo tests unitarios
pytest -m "integration"               # Solo tests de integración
```

##  Tests Disponibles

### **Apps/Core/Tests.py** (Health Check)
- ✅ `test_health_check_endpoint_exists` - GET /api/health/ devuelve 200
- ✅ `test_health_check_response_format` - Respuesta tiene estructura esperada
- ✅ `test_health_status_api_endpoint` - GET /api/health/status/ devuelve 200
- ✅ `test_health_status_response_includes_database` - Response incluye estado de BD
- ✅ `test_swagger_ui_loads` - /docs/ carga sin errores
- ✅ `test_redoc_loads` - /redoc/ carga sin errores
- ✅ `test_openapi_json_available` - /openapi.json/ devuelve JSON válido

### **Apps/Users/Tests.py** (Usuarios y Permisos)
- ✅ `test_create_user_with_valid_data` - Crear usuario con datos válidos
- ✅ `test_user_profile_created_automatically` - Profile se crea automáticamente
- ✅ `test_user_email_unique` - Email debe ser único
- ✅ `test_profile_has_valid_roles` - Profile tiene rol válido
- ✅ `test_profile_string_representation` - __str__ funciona correctamente
- ✅ `test_cliente_role_assigned_correctly` - Cliente tiene rol cliente
- ✅ `test_empleado_role_assigned_correctly` - Empleado tiene rol empleado
- ✅ `test_unauthenticated_user_cannot_access_protected_endpoints` - Sin token → 401

### **Apps/Citas/Tests.py** (Citas y Reservas)
- ✅ `test_crear_servicio` - Crear servicio funciona
- ✅ `test_string_representation` - __str__ de Servicio funciona
- ✅ `test_crear_cita` - Crear cita funciona
- ✅ `test_cita_string_representation` - __str__ de Cita funciona
- ✅ `test_constraint_unique_cita_slot` - No permite duplicados en mismo horario
- ✅ `test_serializer_valido` - Serializer acepta datos válidos
- ✅ `test_serializer_fecha_pasada` - Serializer rechaza fechas en el pasado
- ✅ `test_list_citas_requires_authentication` - Listar requiere autenticación
- ✅ `test_authenticated_user_can_list_citas` - Usuario autenticado puede listar
- ✅ `test_create_cita_with_valid_data` - Crear cita por API
- ✅ `test_cita_estado_default_is_pendiente` - Estado default es pendiente
- ✅ `test_cancel_cita` - Cancelar cita funciona
- ✅ `test_cannot_cancel_completed_cita` - No puede cancelar completada

## 🎯 Meta de Cobertura

- **Target**: 50% de cobertura
- **Archivo**: `pytest.ini` configura `--cov-fail-under=50`
- **Reporte**: Se genera automáticamente en `htmlcov/`

Para ver el reporte después de ejecutar:
```bash
pytest --cov=apps --cov-report=html
open htmlcov/index.html        # macOS
start htmlcov/index.html       # Windows
xdg-open htmlcov/index.html    # Linux
```

## 🔧 Configuración en pytest.ini

```ini
[pytest]
DJANGO_SETTINGS_MODULE = config.settings.dev
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
testpaths = apps
```

Esto asegura que:
- ✅ Django carga settings de desarrollo
- ✅ Busca archivos `tests.py` y `test_*.py`
- ✅ Busca clases que empiecen con `Test`
- ✅ Busca funciones que empiecen con `test_`

## 💡 Consejos

1. **Correr tests antes de hacer push**:
   ```bash
   pytest && git push
   ```

2. **Ejecutar con menos verbosidad**:
   ```bash
   pytest -q
   ```

3. **Parar en el primer error**:
   ```bash
   pytest -x
   ```

4. **Mostrar print statements**:
   ```bash
   pytest -s
   ```

5. **Ejecutar último test que falló**:
   ```bash
   pytest --lf
   ```

## 📚 Recursos

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Django](https://pytest-django.readthedocs.io/)
- [Django Testing Docs](https://docs.djangoproject.com/en/stable/topics/testing/)

---

**Última actualización**: 12 de diciembre de 2025
**Estado**: Tests configurados y listos para ejecutar
