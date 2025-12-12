#!/usr/bin/env python
import os
import sys

root = r'c:\Users\juanj\Downloads\reservas_citas'
os.chdir(root)

cleaned = []
for dirpath, dirnames, filenames in os.walk('.'):
    for fn in filenames:
        if fn.endswith('.py'):
            filepath = os.path.join(dirpath, fn)
            try:
                with open(filepath, 'rb') as f:
                    data = f.read()
                if b'\x00' in data:
                    clean_data = data.replace(b'\x00', b'')
                    with open(filepath, 'wb') as f:
                        f.write(clean_data)
                    cleaned.append(filepath)
                    print(f'✓ Limpiado: {filepath}')
            except Exception as e:
                print(f'ERROR en {filepath}: {e}')

if not cleaned:
    print('No se encontraron bytes NUL.')
else:
    print(f'\n✓ Total limpiado: {len(cleaned)} archivo(s)')
    sys.exit(0)
