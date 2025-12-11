# Generated migration to update Servicio and Cita models

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('citas', '0001_initial'),
    ]

    operations = [
        # Remove the constraint first
        migrations.RemoveConstraint(
            model_name='cita',
            name='unique_cita_slot',
        ),
        # Drop the old Cita table  
        migrations.RemoveField(
            model_name='cita',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='cita',
            name='servicio',
        ),
        migrations.DeleteModel(
            name='Cita',
        ),
        migrations.DeleteModel(
            name='Servicio',
        ),
        # Create new Servicio model with updated fields
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('duracion', models.IntegerField(help_text='Duración en minutos')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
                'ordering': ['nombre'],
            },
        ),
        # Create new Cita model with updated fields
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(help_text='Fecha de la cita')),
                ('hora', models.TimeField(help_text='Hora de la cita')),
                ('estado', models.CharField(
                    choices=[
                        ('pendiente', 'Pendiente'),
                        ('aprobada', 'Aprobada'),
                        ('rechazada', 'Rechazada'),
                        ('completada', 'Completada'),
                        ('cancelada', 'Cancelada'),
                    ],
                    default='pendiente',
                    help_text='Estado actual de la cita',
                    max_length=20
                )),
                ('notas', models.TextField(blank=True, help_text='Notas adicionales', null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('cliente', models.ForeignKey(
                    help_text='Cliente que solicita la cita',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='citas_como_cliente',
                    to=settings.AUTH_USER_MODEL
                )),
                ('empleado', models.ForeignKey(
                    blank=True,
                    help_text='Empleado asignado (opcional)',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='citas_asignadas',
                    to=settings.AUTH_USER_MODEL
                )),
                ('servicio', models.ForeignKey(
                    help_text='Servicio a reservar',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='citas',
                    to='citas.servicio'
                )),
            ],
            options={
                'verbose_name': 'Cita',
                'verbose_name_plural': 'Citas',
                'ordering': ['-fecha', '-hora'],
                'indexes': [
                    models.Index(fields=['estado', '-fecha'], name='citas_cita_estado_fecha_idx'),
                    models.Index(fields=['cliente', '-fecha'], name='citas_cita_cliente_fecha_idx'),
                ],
            },
        ),
        migrations.AddConstraint(
            model_name='cita',
            constraint=models.UniqueConstraint(fields=['fecha', 'hora', 'servicio'], name='unique_cita_slot'),
        ),
    ]

