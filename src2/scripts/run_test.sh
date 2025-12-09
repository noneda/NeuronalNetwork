#!/bin/bash

echo "🧪 Ejecutando suite de tests..."

# Activar entorno virtual si existe
if [ -d "env" ]; then
    source env/bin/activate
fi

# Tests unitarios
echo ""
echo "=== Tests Unitarios ==="
pytest tests/test_logger.py tests/test_database.py -v -m unit

# Tests de API
echo ""
echo "=== Tests de API ==="
pytest tests/test_api_client.py tests/test_api_endpoints.py -v -m api

# Tests de preprocesamiento
echo ""
echo "=== Tests de Preprocesamiento ==="
pytest tests/test_preprocess.py -v

# Tests de modelo
echo ""
echo "=== Tests de Modelo ==="
pytest tests/test_model_training.py -v

# Tests de integración
echo ""
echo "=== Tests de Integración ==="
pytest tests/test_integration.py tests/test_integration_full_system.py -v -m integration

# Generar reporte de cobertura
echo ""
echo "=== Generando Reporte de Cobertura ==="
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

echo ""
echo "✅ Tests completados!"
echo "📊 Reporte de cobertura generado en: htmlcov/index.html"
