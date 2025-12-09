import tensorflow as tf
from keras import layers, models
import numpy as np
from typing import Tuple
from utils.logger import Logger

class DeepLearningModel:
    """Modelo de Deep Learning para predicciones"""
    
    def __init__(self, input_dim: int = 10):
        self.logger = Logger()
        self.input_dim = input_dim
        self.model = None
        self.is_trained = False
        self.logger.info(f"DeepLearningModel initialized with input_dim={input_dim}")
    
    def build_model(self):
        """Construir arquitectura del modelo"""
        self.model = models.Sequential([
            layers.Dense(128, activation='relu', input_shape=(self.input_dim,)),
            layers.Dropout(0.3),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(16, activation='relu'),
            layers.Dense(1, activation='sigmoid')  # Para clasificación binaria
        ])
        
        self.model.compile(
            optimizer='adam',
            loss='binary_crossentropy',
            metrics=['accuracy', 'mae']
        )
        
        self.logger.info("Model architecture built successfully")
        return self.model
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray, 
              epochs: int = 40, batch_size: int = 32, validation_split: float = 0.2):
        """Entrenar el modelo"""
        if self.model is None:
            self.build_model()
        
        self.logger.info(f"Starting training: epochs={epochs}, batch_size={batch_size}")
        
        history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            verbose=1
        )
        
        self.is_trained = True
        self.logger.info("Training completed successfully")
        return history
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, float]:
        """Realizar predicción"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        predictions = self.model.predict(X)
        confidence = float(np.mean(predictions))
        
        self.logger.info(f"Prediction made with confidence: {confidence:.4f}")
        return predictions, confidence
    
    def predict_text(self, text: str) -> Tuple[str, float]:
        """
        Predicción desde texto (simulación)
        En un caso real, aquí habría procesamiento de texto
        """
        # Convertir texto a features (simulado)
        text_hash = hash(text) % 10000
        features = np.random.randn(1, self.input_dim) * (text_hash / 10000)
        
        predictions, confidence = self.predict(features)
        
        # Interpretar resultado
        result = "POSITIVE" if predictions[0][0] > 0.5 else "NEGATIVE"
        confidence_value = float(predictions[0][0])
        
        self.logger.info(f"Text prediction: '{text[:30]}...' -> {result} ({confidence_value:.4f})")
        return result, confidence_value
    
    def save_model(self, path: str = 'models/model.keras'):
        """Guardar modelo"""
        import os
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.model.save(path)
        self.logger.info(f"Model saved to {path}")
    
    def load_model(self, path: str = 'models/model.keras'):
        """Cargar modelo"""
        self.model = tf.keras.models.load_model(path)
        self.is_trained = True
        self.logger.info(f"Model loaded from {path}")
