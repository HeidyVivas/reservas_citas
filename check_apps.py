#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from django.conf import settings

print('✓ INSTALLED_APPS cargadas:')
for app in settings.INSTALLED_APPS:
    if 'apps' in app or 'django' in app:
        print(f'  {app}')
