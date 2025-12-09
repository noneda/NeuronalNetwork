import pytest
import numpy as np
import tensorflow as tf
from unittest.mock import Mock, patch

class TestModelTraining:
    """Tests para entrenamiento del modelo"""
    
    def test_model_creation(self):
        """Test: Creación del modelo"""
        input_dim = 10
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(input_dim,)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(1)
        ])
        
        assert len(model.layers) == 5
        assert model.layers[0].units == 128
        assert model.layers[2].units == 64
    
    def test_model_compilation(self):
        """Test: Compilación del modelo"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        assert model.optimizer is not None
        assert model.loss == 'mse'
    
    def test_model_training_with_clean_data(self, clean_dataset):
        """Test: Entrenamiento con datos limpios"""
        X_train = clean_dataset['features']
        y_train = clean_dataset['labels']
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        history = model.fit(X_train, y_train, epochs=3, verbose=0)
        
        assert 'loss' in history.history
        assert len(history.history['loss']) == 3
        assert history.history['loss'][-1] >= 0
    
    def test_model_training_fails_with_corrupted_data(self, corrupted_dataset):
        """Test: Entrenamiento falla con datos corruptos"""
        X_train = corrupted_dataset['features']
        y_train = corrupted_dataset['labels']
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        
        # El entrenamiento debería fallar o producir NaN
        with pytest.raises(Exception):
            model.fit(X_train, y_train, epochs=1, verbose=0)
    
    def test_model_prediction(self, clean_dataset):
        """Test: Predicción del modelo"""
        X_train = clean_dataset['features']
        y_train = clean_dataset['labels']
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        model.fit(X_train, y_train, epochs=2, verbose=0)
        
        # Predecir
        X_test = np.random.randn(5, 10)
        predictions = model.predict(X_test, verbose=0)
        
        assert predictions.shape == (5, 1)
        assert not np.isnan(predictions).any()
    
    def test_model_save_and_load(self, clean_dataset, tmp_path):
        """Test: Guardar y cargar modelo"""
        X_train = clean_dataset['features']
        y_train = clean_dataset['labels']
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        model.fit(X_train, y_train, epochs=2, verbose=0)
        
        # Guardar
        model_path = tmp_path / "model.keras"
        model.save(model_path)
        
        # Cargar
        loaded_model = tf.keras.models.load_model(model_path)
        
        # Verificar que hace las mismas predicciones
        X_test = np.random.randn(5, 10)
        pred1 = model.predict(X_test, verbose=0)
        pred2 = loaded_model.predict(X_test, verbose=0)
        
        np.testing.assert_array_almost_equal(pred1, pred2)
    
    def test_early_stopping(self, clean_dataset):
        """Test: Early stopping durante entrenamiento"""
        X_train = clean_dataset['features']
        y_train = clean_dataset['labels']
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        
        early_stop = tf.keras.callbacks.EarlyStopping(
            monitor='loss',
            patience=2,
            restore_best_weights=True
        )
        
        history = model.fit(
            X_train, y_train,
            epochs=100,
            callbacks=[early_stop],
            verbose=0
        )
        
        # Debería detenerse antes de 100 epochs
        assert len(history.history['loss']) < 100
    
    def test_validation_split(self, clean_dataset):
        """Test: División de validación"""
        X_train = clean_dataset['features']
        y_train = clean_dataset['labels']
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(10,)),
            tf.keras.layers.Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        
        history = model.fit(
            X_train, y_train,
            epochs=3,
            validation_split=0.2,
            verbose=0
        )
        
        assert 'val_loss' in history.history
        assert len(history.history['val_loss']) == 3