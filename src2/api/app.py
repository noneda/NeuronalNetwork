from flask import Flask, request, jsonify
from functools import wraps
from typing import Optional
from utils.database import Database
from utils.logger import Logger
from model.neural_net import DeepLearningModel
import numpy as np

import os
import matplotlib.pyplot as plt

app = Flask(__name__)
db = Database()
logger = Logger()
model = DeepLearningModel()

# Generar un gráfico de pérdida/Precisión (loss/Accuracy)
def plot_training_history(history, metric: str, filename: str = "plots/loss.png"):

    os.makedirs("plots", exist_ok=True)
    
    plt.figure()
    plt.plot(history.history[metric], label=f"Training {metric.capitalize()}")
    plt.plot(history.history[f"val_{metric}"], label=f"Validation {metric.capitalize()}")
    plt.xlabel("Epochs")
    plt.ylabel(metric.capitalize())
    plt.title(f"Training vs Validation {metric.capitalize()}")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

# Inicializar y entrenar modelo (en producción esto se haría offline)
def init_model():
    """Inicializar modelo con datos de ejemplo"""
    logger.info("Initializing model...")
    if os.path.exists("models/model.keras"):
        model.load_model()
        logger.info("Model loaded from disk")
        return
    
    X_train = np.random.randn(1000, 10)
    y_train = (np.random.randn(1000, 1) > 0).astype(float)
    history = model.train(X_train, y_train, epochs=10)
    logger.info("Model initialized and trained")
    plot_training_history(history, metric="loss", filename="plots/loss.png")
    # guardar modelo
    model.save_model()

# Decorador para autenticación
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            logger.warning("Request without authorization token")
            return jsonify({'error': 'Authorization token required'}), 401
        
        # Remover "Bearer " si existe
        if token.startswith('Bearer '):
            token = token[7:]
        
        user_id = db.validate_session(token)
        
        if user_id is None:
            logger.warning("Invalid or expired token")
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Pasar user_id a la función
        return f(user_id=user_id, *args, **kwargs)
    
    return decorated_function


# ============= ENDPOINTS DE AUTENTICACIÓN =============

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Endpoint para registro de usuario"""
    try:
        data = request.get_json()
        
        # Validar datos
        if not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        # Validaciones básicas
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        # Registrar usuario
        user_id = db.register_user(username, email, password)
        
        if user_id is None:
            return jsonify({'error': 'Username or email already exists'}), 409
        
        # Crear sesión
        token = db.create_session(user_id)
        
        logger.info(f"New user registered: {username}")
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user_id,
            'token': token
        }), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Endpoint para login de usuario"""
    try:
        data = request.get_json()
        
        if not all(k in data for k in ['username', 'password']):
            return jsonify({'error': 'Missing username or password'}), 400
        
        username = data['username']
        password = data['password']
        
        # Autenticar
        user = db.authenticate_user(username, password)
        
        if user is None:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Crear sesión
        token = db.create_session(user['id'])
        
        logger.info(f"User logged in: {username}")
        
        return jsonify({
            'message': 'Login successful',
            'user': user,
            'token': token
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# ============= ENDPOINTS DE PREDICCIÓN =============

@app.route('/api/predict', methods=['POST'])
@require_auth
def predict(user_id: int):
    """Endpoint para realizar predicción"""
    try:
        data = request.get_json()
        
        if 'text' not in data:
            return jsonify({'error': 'Missing text field'}), 400
        
        input_text = data['text']
        
        if not input_text or len(input_text) < 3:
            return jsonify({'error': 'Text must be at least 3 characters'}), 400
        
        # Realizar predicción
        prediction, confidence = model.predict_text(input_text)
        
        # Guardar en base de datos
        prediction_id = db.save_prediction(
            user_id=user_id,
            input_text=input_text,
            prediction_text=prediction,
            confidence=confidence
        )
        
        logger.info(f"Prediction made for user_id={user_id}, prediction_id={prediction_id}")
        
        return jsonify({
            'prediction_id': prediction_id,
            'input': input_text,
            'prediction': prediction,
            'confidence': confidence
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Prediction failed'}), 500


@app.route('/api/predictions', methods=['GET'])
@require_auth
def get_predictions(user_id: int):
    """Obtener historial de predicciones del usuario"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        predictions = db.get_user_predictions(user_id, limit)
        
        logger.info(f"Retrieved {len(predictions)} predictions for user_id={user_id}")
        
        return jsonify({
            'predictions': predictions,
            'count': len(predictions)
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving predictions: {str(e)}")
        return jsonify({'error': 'Failed to retrieve predictions'}), 500


@app.route('/api/predictions/<int:prediction_id>', methods=['GET'])
@require_auth
def get_prediction(user_id: int, prediction_id: int):
    """Obtener predicción específica"""
    try:
        prediction = db.get_prediction_by_id(prediction_id)
        
        if prediction is None:
            return jsonify({'error': 'Prediction not found'}), 404
        
        # Verificar que la predicción pertenece al usuario
        if prediction['user_id'] != user_id:
            logger.warning(f"User {user_id} tried to access prediction {prediction_id}")
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(prediction), 200
        
    except Exception as e:
        logger.error(f"Error retrieving prediction: {str(e)}")
        return jsonify({'error': 'Failed to retrieve prediction'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_trained': model.is_trained
    }), 200


# ============= INICIALIZACIÓN =============

if __name__ == '__main__':
    logger.info("Starting Deep Learning API...")
    init_model()
    app.run(debug=True, host='0.0.0.0', port=5000)