"""
Script principal para orquestar el sistema completo
"""
from utils.logger import Logger
from utils.database import Database
from model.neural_net import DeepLearningModel
import numpy as np

def main():
    """Función principal"""
    logger = Logger()
    logger.info("=" * 60)
    logger.info("Starting Deep Learning System")
    logger.info("=" * 60)
    
    # Inicializar base de datos
    db = Database()
    logger.info("Database initialized")
    
    # Crear usuario de prueba
    user_id = db.register_user(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    
    if user_id:
        logger.info(f"Test user created with ID: {user_id}")
    else:
        logger.info("Test user already exists, authenticating...")
        user = db.authenticate_user("testuser", "password123")
        user_id = user['id'] if user else None
    
    # Inicializar y entrenar modelo
    model = DeepLearningModel(input_dim=10)
    logger.info("Model created")
    
    # Datos de entrenamiento simulados
    X_train = np.random.randn(1000, 10)
    y_train = (np.random.randn(1000, 1) > 0).astype(float)
    
    logger.info("Training model...")
    history = model.train(X_train, y_train, epochs=20, batch_size=32)
    
    # Hacer predicción de prueba
    test_text = "This is a test prediction"
    prediction, confidence = model.predict_text(test_text)
    
    logger.info(f"Test prediction: {prediction} (confidence: {confidence:.4f})")
    
    # Guardar predicción en base de datos
    if user_id:
        prediction_id = db.save_prediction(
            user_id=user_id,
            input_text=test_text,
            prediction_text=prediction,
            confidence=confidence
        )
        logger.info(f"Prediction saved with ID: {prediction_id}")
        
        # Recuperar predicciones del usuario
        predictions = db.get_user_predictions(user_id, limit=5)
        logger.info(f"User has {len(predictions)} predictions")
    
    # Guardar modelo
    model.save_model()
    
    logger.info("=" * 60)
    logger.info("System initialization completed successfully")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()