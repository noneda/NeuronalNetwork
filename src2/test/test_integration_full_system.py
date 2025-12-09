import pytest
import numpy as np
from utils.database import Database
from utils.logger import Logger
from model.neural_net import DeepLearningModel
import json

class TestFullSystemIntegration:
    """Tests de integración del sistema completo"""
    
    def test_complete_user_workflow(self, test_database):
        """Test: Flujo completo de usuario"""
        # 1. Registro
        user_id = test_database.register_user(
            username="workflow_user",
            email="workflow@test.com",
            password="secure123"
        )
        assert user_id is not None
        
        # 2. Login
        user = test_database.authenticate_user("workflow_user", "secure123")
        assert user is not None
        assert user['id'] == user_id
        
        # 3. Crear sesión
        token = test_database.create_session(user_id)
        assert token is not None
        
        # 4. Validar sesión
        validated_user_id = test_database.validate_session(token)
        assert validated_user_id == user_id
        
        # 5. Guardar predicción
        prediction_id = test_database.save_prediction(
            user_id=user_id,
            input_text="Integration test",
            prediction_text="POSITIVE",
            confidence=0.92
        )
        assert prediction_id is not None
        
        # 6. Recuperar predicciones
        predictions = test_database.get_user_predictions(user_id)
        assert len(predictions) > 0
        assert predictions[0]['id'] == prediction_id
    
    def test_model_training_and_prediction_integration(self):
        """Test: Integración completa de modelo"""
        # 1. Crear modelo
        model = DeepLearningModel(input_dim=10)
        
        # 2. Entrenar
        X_train = np.random.randn(100, 10)
        y_train = (np.random.randn(100, 1) > 0).astype(float)
        history = model.train(X_train, y_train, epochs=5, verbose=0)
        
        assert 'loss' in history.history
        assert model.is_trained
        
        # 3. Predecir
        prediction, confidence = model.predict_text("Test integration")
        assert prediction in ['POSITIVE', 'NEGATIVE']
        assert 0 <= confidence <= 1
    
    def test_api_to_database_integration(self, flask_app, test_database):
        """Test: Integración API -> Base de datos"""
        # Registro vía API
        register_payload = {
            'username': 'integration_user',
            'email': 'integration@test.com',
            'password': 'password123'
        }
        
        response = flask_app.post(
            '/api/auth/register',
            data=json.dumps(register_payload),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        token = data['token']
        
        # Hacer predicción vía API
        predict_payload = {
            'text': 'API integration test'
        }
        
        response = flask_app.post(
            '/api/predict',
            data=json.dumps(predict_payload),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        prediction_id = data['prediction_id']
        
        # Verificar en base de datos
        prediction = test_database.get_prediction_by_id(prediction_id)
        assert prediction is not None
        assert prediction['input_text'] == 'API integration test'
    
    def test_concurrent_predictions(self, test_database):
        """Test: Múltiples predicciones concurrentes"""
        # Crear múltiples usuarios
        user_ids = []
        for i in range(5):
            user_id = test_database.register_user(
                username=f"concurrent_user_{i}",
                email=f"concurrent_{i}@test.com",
                password="password123"
            )
            user_ids.append(user_id)
        
        # Cada usuario hace predicciones
        for user_id in user_ids:
            for j in range(3):
                prediction_id = test_database.save_prediction(
                    user_id=user_id,
                    input_text=f"Concurrent test {j}",
                    prediction_text="POSITIVE",
                    confidence=0.8
                )
                assert prediction_id is not None
        
        # Verificar que cada usuario tiene sus predicciones
        for user_id in user_ids:
            predictions = test_database.get_user_predictions(user_id)
            assert len(predictions) == 3