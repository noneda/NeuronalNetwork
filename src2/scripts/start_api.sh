#!/bin/bash

echo "🚀 Iniciando API de Deep Learning..."

# Activar entorno virtual
if [ -d "env" ]; then
    source env/bin/activate
fi

# Verificar que las dependencias están instaladas
python -c "import tensorflow, flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Faltan dependencias. Ejecuta: pip install -r requirements.txt"
    exit 1
fi

# Inicializar base de datos y modelo
echo "🔧 Inicializando sistema..."
python -m src2.main

# Iniciar servidor Flask
echo "🌐 Iniciando servidor en http://localhost:5000"
python -m src2.api.app
