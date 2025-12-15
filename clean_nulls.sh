#!/bin/bash
cd /c/Users/juanj/Downloads/reservas_citas
for file in $(find . -name "*.py" -type f); do
  if file "$file" | grep -q "null"; then
    echo "Limpiando: $file"
    tr -d '\000' < "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"
  fi
done
echo "Limpieza completada"
