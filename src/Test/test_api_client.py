import pytest
import requests
from unittest.mock import patch, Mock
import json

class TestAPIClient:
    """Tests para el cliente de API"""
    
    def test_api_connection_success(self, api_response_valid):
        """Test: Conexión exitosa a la API"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = api_response_valid
            
            # Simular llamada a API
            response = requests.get("https://api.example.com/data")
            data = response.json()
            
            assert response.status_code == 200
            assert data["status"] == "success"
            assert len(data["data"]["records"]) == 50
    
    def test_api_connection_failure(self):
        """Test: Manejo de fallo de conexión"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError
            
            with pytest.raises(requests.exceptions.ConnectionError):
                requests.get("https://api.example.com/data")
    
    def test_api_timeout(self):
        """Test: Manejo de timeout"""
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.Timeout
            
            with pytest.raises(requests.exceptions.Timeout):
                requests.get("https://api.example.com/data", timeout=5)
    
    def test_api_invalid_json(self):
        """Test: Respuesta con JSON inválido"""
        with patch('requests.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)
            mock_get.return_value = mock_response
            
            response = requests.get("https://api.example.com/data")
            with pytest.raises(json.JSONDecodeError):
                response.json()
    
    def test_api_rate_limit(self):
        """Test: Manejo de rate limiting (429)"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 429
            mock_get.return_value.json.return_value = {
                "error": "Rate limit exceeded"
            }
            
            response = requests.get("https://api.example.com/data")
            assert response.status_code == 429
    
    def test_api_corrupted_response(self, api_response_corrupted):
        """Test: Respuesta con datos parcialmente corruptos"""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = api_response_corrupted
            
            response = requests.get("https://api.example.com/data")
            data = response.json()
            
            assert data["status"] == "success"
            # Verificar que hay datos corruptos
            records = data["data"]["records"]
            null_values = sum(1 for r in records if r.get("value") is None)
            assert null_values > 0