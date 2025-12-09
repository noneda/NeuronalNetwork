#!/bin/bash

echo "🧪 Probando endpoints de la API..."
echo ""

BASE_URL="http://localhost:5000/api"

# Health check
echo "1️⃣ Health Check"
curl -X GET $BASE_URL/health | jq
echo -e "\n"

# Registro
echo "2️⃣ Registrando nuevo usuario"
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser_'$(date +%s)'",
    "email": "test'$(date +%s)'@example.com",
    "password": "securepass123"
  }')
echo $REGISTER_RESPONSE | jq
TOKEN=$(echo $REGISTER_RESPONSE | jq -r '.token')
echo "Token obtenido: $TOKEN"
echo -e "\n"

# Login
echo "3️⃣ Login"
curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }' | jq
echo -e "\n"

# Predicción
echo "4️⃣ Realizando predicción"
PREDICTION=$(curl -s -X POST $BASE_URL/predict \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "text": "This is a test prediction for sentiment analysis"
  }')
echo $PREDICTION | jq
PREDICTION_ID=$(echo $PREDICTION | jq -r '.prediction_id')
echo -e "\n"

# Obtener historial
echo "5️⃣ Obteniendo historial de predicciones"
curl -s -X GET $BASE_URL/predictions \
  -H "Authorization: Bearer $TOKEN" | jq
echo -e "\n"

# Obtener predicción específica
echo "6️⃣ Obteniendo predicción específica"
curl -s -X GET $BASE_URL/predictions/$PREDICTION_ID \
  -H "Authorization: Bearer $TOKEN" | jq
echo -e "\n"

echo "✅ Pruebas completadas!"