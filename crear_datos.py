#!/usr/bin/env python
"""
Script autoejecutable para crear datos de prueba
Ejecutar con: python crear_datos.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from django.contrib.auth.models import User
from apps.citas.models import Servicio, Cita
from datetime import datetime, timedelta

print("="*70)
print("CREANDO DATOS DE PRUEBA PARA LA API")
print("="*70)

# ==================== CREAR USUARIOS ====================
print("\n1️⃣ CREANDO USUARIOS...")

usuarios_data = [
    {'username': 'cliente1', 'email': 'cliente1@example.com', 'is_staff': False},
    {'username': 'cliente2', 'email': 'cliente2@example.com', 'is_staff': False},
    {'username': 'cliente3', 'email': 'cliente3@example.com', 'is_staff': False},
    {'username': 'empleado1', 'email': 'empleado1@example.com', 'is_staff': True},
    {'username': 'empleado2', 'email': 'empleado2@example.com', 'is_staff': True},
]

usuarios = {}
for datos in usuarios_data:
    user, created = User.objects.get_or_create(
        username=datos['username'],
        defaults={
            'email': datos['email'],
            'is_staff': datos['is_staff'],
            'is_superuser': False
        }
    )
    usuarios[datos['username']] = user
    if created:
        user.set_password('pass123')
        user.save()
        print(f"✅ {datos['username']} creado")
    else:
        print(f"✅ {datos['username']} ya existe")

# ==================== CREAR SERVICIOS ====================
print("\n2️⃣ CREANDO SERVICIOS...")

servicios_data = [
    {'nombre': 'Consulta General', 'duracion': 30, 'precio': 50.00},
    {'nombre': 'Consulta Especializada', 'duracion': 45, 'precio': 100.00},
    {'nombre': 'Laboratorio', 'duracion': 20, 'precio': 75.00},
    {'nombre': 'Ecografía', 'duracion': 30, 'precio': 150.00},
    {'nombre': 'Cirugía Menor', 'duracion': 60, 'precio': 500.00},
]

servicios = {}
for datos in servicios_data:
    servicio, created = Servicio.objects.get_or_create(
        nombre=datos['nombre'],
        defaults={
            'duracion': datos['duracion'],
            'precio': datos['precio']
        }
    )
    servicios[datos['nombre']] = servicio
    if created:
        print(f"✅ {datos['nombre']} creado (${datos['precio']})")
    else:
        print(f"✅ {datos['nombre']} ya existe")

# ==================== CREAR CITAS ====================
print("\n3️⃣ CREANDO CITAS...")

hoy = datetime.now().date()
citas_data = [
    # Cliente 1
    {'cliente': 'cliente1', 'servicio': 'Corte de cabello', 'fecha': 1, 'hora': '10:00:00', 'estado': 'pendiente'},
    {'cliente': 'cliente1', 'servicio': 'Tinte', 'fecha': 2, 'hora': '14:30:00', 'estado': 'aprobada', 'empleado': 'empleado1'},
    {'cliente': 'cliente1', 'servicio': 'Masaje', 'fecha': 3, 'hora': '16:00:00', 'estado': 'completada', 'empleado': 'empleado1'},
    
    # Cliente 2
    {'cliente': 'cliente2', 'servicio': 'Manicure', 'fecha': 1, 'hora': '11:00:00', 'estado': 'pendiente'},
    {'cliente': 'cliente2', 'servicio': 'Pedicure', 'fecha': 2, 'hora': '15:00:00', 'estado': 'aprobada', 'empleado': 'empleado2'},
    {'cliente': 'cliente2', 'servicio': 'Corte de cabello', 'fecha': 4, 'hora': '09:00:00', 'estado': 'completada', 'empleado': 'empleado2'},
    
    # Cliente 3
    {'cliente': 'cliente3', 'servicio': 'Tinte', 'fecha': 2, 'hora': '13:00:00', 'estado': 'pendiente'},
    {'cliente': 'cliente3', 'servicio': 'Masaje', 'fecha': 3, 'hora': '17:00:00', 'estado': 'rechazada'},
    {'cliente': 'cliente3', 'servicio': 'Manicure', 'fecha': 5, 'hora': '11:30:00', 'estado': 'aprobada', 'empleado': 'empleado1'},
]

count = 0
for datos in citas_data:
    try:
        fecha = hoy + timedelta(days=datos['fecha'])
        cliente = usuarios[datos['cliente']]
        servicio = servicios[datos['servicio']]
        empleado = usuarios.get(datos.get('empleado'))
        
        cita, created = Cita.objects.get_or_create(
            fecha=fecha,
            hora=datos['hora'],
            cliente=cliente,
            servicio=servicio,
            defaults={
                'estado': datos['estado'],
                'empleado': empleado,
                'notas': f'Cita de prueba'
            }
        )
        
        if created:
            print(f"✅ Cita #{cita.id}: {cliente.username} → {servicio.nombre} ({cita.estado})")
            count += 1
    except Exception as e:
        print(f"❌ Error: {e}")

# ==================== RESUMEN ====================
print("\n" + "="*70)
print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
print("="*70)

print(f"\n📊 RESUMEN:")
print(f"   • Usuarios: {User.objects.count()}")
print(f"   • Servicios: {Servicio.objects.count()}")
print(f"   • Citas: {Cita.objects.count()}")
print(f"   • Citas pendientes: {Cita.objects.filter(estado='pendiente').count()}")
print(f"   • Citas aprobadas: {Cita.objects.filter(estado='aprobada').count()}")
print(f"   • Citas completadas: {Cita.objects.filter(estado='completada').count()}")
print(f"   • Citas rechazadas: {Cita.objects.filter(estado='rechazada').count()}")

print("\n🌐 ACCEDE A SWAGGER EN:")
print("   http://127.0.0.1:8000/swagger/")

print("\n" + "="*70)
