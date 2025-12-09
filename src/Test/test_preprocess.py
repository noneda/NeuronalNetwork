import pytest
import numpy as np
import pandas as pd

class TestPreprocessing:
    """Tests para preprocesamiento de datos"""
    
    def test_remove_null_values(self, corrupted_dataset):
        """Test: Eliminación de valores nulos"""
        features = corrupted_dataset['features']
        labels = corrupted_dataset['labels']
        
        # Identificar filas con NaN
        mask = ~(np.isnan(features).any(axis=1) | np.isnan(labels).flatten())
        clean_features = features[mask]
        clean_labels = labels[mask]
        
        assert not np.isnan(clean_features).any()
        assert not np.isnan(clean_labels).any()
        assert len(clean_features) < len(features)
    
    def test_remove_infinite_values(self, corrupted_dataset):
        """Test: Eliminación de valores infinitos"""
        features = corrupted_dataset['features']
        
        # Identificar filas con infinitos
        mask = ~np.isinf(features).any(axis=1)
        clean_features = features[mask]
        
        assert not np.isinf(clean_features).any()
        assert len(clean_features) < len(features)
    
    def test_normalize_data(self, clean_dataset):
        """Test: Normalización de datos"""
        features = clean_dataset['features']
        
        # Normalización Z-score
        mean = np.mean(features, axis=0)
        std = np.std(features, axis=0)
        normalized = (features - mean) / (std + 1e-8)
        
        assert np.abs(np.mean(normalized)) < 0.1
        assert np.abs(np.std(normalized) - 1.0) < 0.1
    
    def test_handle_outliers(self, clean_dataset):
        """Test: Manejo de outliers usando IQR"""
        features = clean_dataset['features']
        
        # Añadir outliers artificiales
        features[0, 0] = 100
        features[1, 0] = -100
        
        # Detectar outliers usando IQR
        Q1 = np.percentile(features, 25, axis=0)
        Q3 = np.percentile(features, 75, axis=0)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Clipear outliers
        clipped = np.clip(features, lower_bound, upper_bound)
        
        assert np.max(clipped[:, 0]) < 100
        assert np.min(clipped[:, 0]) > -100
    
    def test_split_train_test(self, clean_dataset):
        """Test: División train/test"""
        features = clean_dataset['features']
        labels = clean_dataset['labels']
        
        split_ratio = 0.8
        split_idx = int(len(features) * split_ratio)
        
        X_train = features[:split_idx]
        X_test = features[split_idx:]
        y_train = labels[:split_idx]
        y_test = labels[split_idx:]
        
        assert len(X_train) == 80
        assert len(X_test) == 20
        assert len(y_train) == 80
        assert len(y_test) == 20
    
    def test_feature_scaling_minmax(self, clean_dataset):
        """Test: Escalado Min-Max"""
        features = clean_dataset['features']
        
        min_val = np.min(features, axis=0)
        max_val = np.max(features, axis=0)
        scaled = (features - min_val) / (max_val - min_val + 1e-8)
        
        assert np.min(scaled) >= 0
        assert np.max(scaled) <= 1
    
    def test_handle_missing_categories(self, api_response_corrupted):
        """Test: Manejo de categorías faltantes"""
        records = api_response_corrupted['data']['records']
        df = pd.DataFrame(records)
        
        # Rellenar categorías faltantes
        df['category'].fillna('UNKNOWN', inplace=True)
        
        assert df['category'].isna().sum() == 0
        assert 'UNKNOWN' in df['category'].values
    
    def test_convert_invalid_types(self, api_response_corrupted):
        """Test: Conversión de tipos inválidos"""
        records = api_response_corrupted['data']['records']
        df = pd.DataFrame(records)
        
        # Convertir valores a numérico, forzando errores a NaN
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Eliminar NaN
        df_clean = df.dropna(subset=['value'])
        
        assert all(isinstance(x, (int, float)) for x in df_clean['value'])
        assert len(df_clean) < len(df)