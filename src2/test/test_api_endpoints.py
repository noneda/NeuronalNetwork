import pytest
import json
from utils.database import Database

class TestAPIEndpoints:
    """Tests para los endpoints de la API"""
    
    def test_health_check(self, flask_app):
        """Test: Health check endpoint"""
        response = flask_app.get('/api/health')
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['status'] == 'healthy'
    
    def test_register_endpoint_success(self, flask_app):
        """Test: Registro exitoso vía API"""
        payload = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'password': 'password123'
        }
        
        response = flask_app.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 201
        assert 'token' in data
        assert 'user_id' in data
    
    def test_register_endpoint_missing_fields(self, flask_app):
        """Test: Registro falla sin campos requeridos"""
        payload = {
            'username': 'apiuser'
            # Falta email y password
        }
        
        response = flask_app.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_register_endpoint_short_password(self, flask_app):
        """Test: Registro falla con contraseña corta"""
        payload = {
            'username': 'apiuser2',
            'email': 'api2@example.com',
            'password': '123'  # Muy corta
        }
        
        response = flask_app.post(
            '/api/auth/register',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_login_endpoint_success(self, flask_app, test_user):
        """Test: Login exitoso vía API"""
        payload = {
            'username': test_user['username'],
            'password': test_user['password']
        }
        
        response = flask_app.post(
            '/api/auth/login',
            data=json.dumps(payload),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert 'token' in data
        assert 'user' in data
    
    def test_login_endpoint_wrong_password(self, flask_app, test_user):
        """Test: Login falla con contraseña incorrecta"""
        payload = {
            'username': test_user['username'],
            'password': 'wrongpassword'
        }
        
        response = flask_app.post(
            '/api/auth/login',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_predict_endpoint_without_auth(self, flask_app):
        """Test: Predicción falla sin autenticación"""
        payload = {
            'text': 'This is a test'
        }
        
        response = flask_app.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        assert response.status_code == 401
    
    def test_predict_endpoint_with_auth(self, flask_app, test_token):
        """Test: Predicción exitosa con autenticación"""
        payload = {
            'text': 'This is a test prediction'
        }
        
        response = flask_app.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Authorization': f'Bearer {test_token}'}
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert 'prediction' in data
        assert 'confidence' in data
        assert 'prediction_id' in data
    
    def test_predict_endpoint_missing_text(self, flask_app, test_token):
        """Test: Predicción falla sin texto"""
        payload = {}
        
        response = flask_app.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Authorization': f'Bearer {test_token}'}
        )
        
        assert response.status_code == 400
    
    def test_predict_endpoint_short_text(self, flask_app, test_token):
        """Test: Predicción falla con texto muy corto"""
        payload = {
            'text': 'ab'  # Muy corto
        }
        
        response = flask_app.post(
            '/api/predict',
            data=json.dumps(payload),
            content_type='application/json',
            headers={'Authorization': f'Bearer {test_token}'}
        )
        
        assert response.status_code == 400
    
    def test_get_predictions_endpoint(self, flask_app, test_token, test_user, test_database):
        """Test: Obtener historial de predicciones"""
        # Crear algunas predicciones
        for i in range(3):
            test_database.save_prediction(
                user_id=test_user['id'],
                input_text=f"Test {i}",
                prediction_text="POSITIVE",
                confidence=0.8
            )
        
        response = flask_app.get(
            '/api/predictions',
            headers={'Authorization': f'Bearer {test_token}'}
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert 'predictions' in data
        assert len(data['predictions']) >= 3
    
    def test_get_specific_prediction_endpoint(self, flask_app, test_token, test_user, test_database):
        """Test: Obtener predicción específica"""
        # Crear predicción
        prediction_id = test_database.save_prediction(
            user_id=test_user['id'],
            input_text="Specific test",
            prediction_text="NEGATIVE",
            confidence=0.65
        )
        
        response = flask_app.get(
            f'/api/predictions/{prediction_id}',
            headers={'Authorization': f'Bearer {test_token}'}
        )
        data = json.loads(response.data)
        
        assert response.status_code == 200
        assert data['id'] == prediction_id
        assert data['input_text'] == "Specific test"