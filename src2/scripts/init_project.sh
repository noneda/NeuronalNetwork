#!/bin/bash

echo "🚀 Inicializando proyecto Deep Learning API..."

# Crear estructura de directorios
echo "📁 Creando estructura de directorios..."
mkdir -p src2/data
mkdir -p src2/model
mkdir -p src2/api
mkdir -p src2/utils
mkdir -p src2/visualization
mkdir -p tests
mkdir -p logs
mkdir -p data
mkdir -p models

# Crear archivos __init__.py
touch src2/__init__.py
touch src2/data/__init__.py
touch src2/model/__init__.py
touch src2/api/__init__.py
touch src2/utils/__init__.py
touch src2/visualization/__init__.py
touch tests/__init__.py

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv env

# Activar entorno virtual
echo "✅ Activando entorno virtual..."
source env/bin/activate

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Proyecto inicializado correctamente!"
echo ""
echo "Para activar el entorno virtual, ejecuta:"
echo "  source env/bin/activate"
echo ""
echo "Para ejecutar los tests:"
echo "  pytest tests/ -v"
echo ""
echo "Para iniciar la API:"
echo "  python -m src2.api.app"
