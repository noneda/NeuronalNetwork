import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, Mock
import tensorflow as tf
import requests

class TestIntegration:
    """Tests de integración del pipeline completo"""
    
    def test_full_pipeline_with_clean_data(self, api_response_valid):
        """Test: Pipeline completo con datos limpios"""
        # 1. Simular carga desde API
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = api_response_valid
            
            import requests
            response = requests.get("https://api.example.com/data")
            data = response.json()
        
        # 2. Convertir a DataFrame
        df = pd.DataFrame(data['data']['records'])
        
        # 3. Preprocesar
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna()
        
        # 4. Preparar datos
        features = df[['value']].values
        labels = (features * 0.5).reshape(-1, 1)  # target simulado
        
        # 5. Normalizar
        mean = np.mean(features)
        std = np.std(features)
        features_norm = (features - mean) / (std + 1e-8)
        
        # 6. Crear y entrenar modelo
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(16, activation='relu', input_shape=(1,)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        history = model.fit(features_norm, labels, epochs=3, verbose=0)
        
        # 7. Predecir
        predictions = model.predict(features_norm[:5], verbose=0)
        
        # Verificaciones
        assert len(df) == 50
        assert 'loss' in history.history
        assert predictions.shape == (5, 1)
    
    def test_full_pipeline_with_corrupted_data(self, api_response_corrupted):
        """Test: Pipeline completo con datos corruptos"""
        # 1. Simular carga desde API
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = api_response_corrupted
            
            import requests
            response = requests.get("https://api.example.com/data")
            data = response.json()
        
        # 2. Convertir a DataFrame
        df = pd.DataFrame(data['data']['records'])
        initial_len = len(df)
        
        # 3. Limpiar datos corruptos
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['value'])
        df = df[~np.isinf(df['value'])]
        
        # 4. Verificar que se eliminaron datos corruptos
        assert len(df) < initial_len
        assert len(df) > 0  # Pero todavía hay datos válidos
        
        # 5. Continuar con pipeline si hay suficientes datos
        if len(df) >= 10:
            features = df[['value']].values
            labels = (features * 0.5).reshape(-1, 1)
            
            # Normalizar
            features_norm = (features - np.mean(features)) / (np.std(features) + 1e-8)
            
            # Entrenar
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(16, activation='relu', input_shape=(1,)),
                tf.keras.layers.Dense(1)
            ])
            model.compile(optimizer='adam', loss='mse')
            history = model.fit(features_norm, labels, epochs=2, verbose=0)
            
            assert 'loss' in history.history
    
    def test_api_retry_logic(self):
        """Test: Lógica de reintentos en caso de fallo de API"""
        max_retries = 3
        attempt = 0
        
        with patch('requests.get') as mock_get:
            # Primeros dos intentos fallan, tercero tiene éxito
            def side_effect(*args, **kwargs):
                nonlocal attempt
                attempt += 1
                if attempt < 3:
                    raise requests.exceptions.ConnectionError
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"status": "success"}
                return mock_response
            
            mock_get.side_effect = side_effect
            
            # Simular reintentos
            for retry in range(max_retries):
                try:
                    response = requests.get("https://api.example.com/data")
                    if response.status_code == 200:
                        break
                except requests.exceptions.ConnectionError:
                    if retry == max_retries - 1:
                        pytest.fail("Max retries reached")
            
            assert attempt == 3
            assert response.status_code == 200