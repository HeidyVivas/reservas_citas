#!/usr/bin/env python
import re

# Leer el archivo
with open('config/settings/base.py', 'r') as f:
    content = f.read()

# Reemplazar la cadena incorrecta
content = content.replace(
    '"apps.users",`n    "apps.health",',
    '"apps.users",\n    "apps.health",'
)

# Si no tiene apps.health, agregarlo
if '"apps.health"' not in content:
    content = content.replace(
        '"apps.users",\n]',
        '"apps.users",\n    "apps.health",\n]'
    )

# Escribir el archivo
with open('config/settings/base.py', 'w') as f:
    f.write(content)

print('✓ Actualizado')
