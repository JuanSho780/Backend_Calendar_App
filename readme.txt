#################################################################
#                     PLANIFYME PROJECT                         #
#                     Archivo: .gitignore                       #
#################################################################
# Bienvenido a tu archivo .gitignore oficial del proyecto.
# Este documento fue creado para mantener tu repositorio limpio,
# ordenado y libre de archivos innecesarios.
#
# ───────────────────────────────────────────────────────────────
# SECCIÓN 1: CONFIGURACIÓN GLOBAL
# ───────────────────────────────────────────────────────────────
# Ignoramos las carpetas comunes del sistema operativo y del IDE.
#################################################################

# Archivos del sistema operativo
.DS_Store
Thumbs.db
desktop.ini

# Archivos de configuración de IDE
.vscode/
.idea/
*.iml
*.suo
*.user
*.rsuser

#################################################################
# SECCIÓN 2: ENTORNOS Y DEPENDENCIAS
#################################################################

# Node.js
node_modules/
npm-debug.log*
yarn-error.log*

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
venv/
env/
.env
.env.local
.env.development
.env.production
.env.test

# Java
*.class
*.jar
*.war
*.ear
*.classpath
*.project
*.settings/

#################################################################
# SECCIÓN 3: COMPILACIÓN Y DEPLOY
#################################################################
# Todo lo generado por procesos de build o empaquetado.
dist/
build/
out/
coverage/
.cache/
.tmp/
.next/
.nuxt/
*.map

#################################################################
# SECCIÓN 4: ARCHIVOS BINARIOS Y TEMPORALES
#################################################################
# Archivos grandes o generados que no deberían subirse.
*.zip
*.tar
*.gz
*.rar
*.7z
*.exe
*.dll
*.so
*.bin
*.dat
*.bak
*.old
*.swp
*.swo
*.tmp
*.log
logs/

#################################################################
# SECCIÓN 5: IMÁGENES Y MULTIMEDIA
#################################################################
# Este proyecto puede contener imágenes de diseño,
# pero los originales en alta calidad no deben subirse.
*.psd
*.ai
*.tiff
*.bmp
*.raw
designs/
drafts/
backups/

#################################################################
# SECCIÓN 6: DOCKER Y CONTENEDORES
#################################################################
# Archivos específicos de Docker y contenedores.
docker-compose.override.yml
*.dockerfile
*.dockerignore

#################################################################
# SECCIÓN 7: BASES DE DATOS
#################################################################
# Archivos de bases de datos o backups.
*.db
*.sqlite
*.sql
dump/
backups/
migrations/

#################################################################
# SECCIÓN 8: DOCUMENTACIÓN Y REPORTES
#################################################################
# Si bien la documentación es importante, no se suben archivos
# generados automáticamente o grandes exportaciones.
*.pdf
*.docx
*.xlsx
*.pptx
*.csv
*.ods
*.odt
*.json
*.xml

#################################################################
# SECCIÓN 9: CONFIGURACIONES PERSONALES
#################################################################
# Cualquier archivo de configuración local.
config.local
settings.local
notes.txt
draft.txt
*.local
*.private

#################################################################
# SECCIÓN 10: PROYECTOS WEB
#################################################################
# Archivos generados por frameworks frontend.
public/
static/
temp/
cache/
npm-debug.log*
package-lock.json
yarn.lock
pnpm-lock.yaml

#################################################################
# SECCIÓN 11: ARCHIVOS DE PRUEBA
#################################################################
# Ignora todo lo que sea resultado de tests automáticos.
coverage/
htmlcov/
.tox/
.mypy_cache/
pytest_cache/
*.spec.js
*.test.js

#################################################################
# SECCIÓN 12: REGLAS PERSONALIZADAS DEL EQUIPO
#################################################################
# Este bloque está reservado para agregar reglas específicas
# según lo que cada desarrollador necesite ignorar.
# Ejemplo:
#   !keep_this_folder/
#   ignore_this_temp_stuff/

#################################################################
# NOTAS FINALES
#################################################################
# Si llegas hasta aquí, felicidades 🎉
# Significa que te importa mantener un proyecto limpio.
# Recuerda: subir solo lo necesario ayuda a todos.
#
# “Un buen .gitignore es como una buena taza de café:
#   no se nota cuando está bien hecho, pero lo echas de menos
#   cuando no está.” ☕
#
#################################################################

# Fin del archivo .gitignore
#################################################################
