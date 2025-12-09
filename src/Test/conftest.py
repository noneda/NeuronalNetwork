import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, Mock
import tensorflow as tf

@pytest.fixture
def clean_dataset():
    """Dataset limpio para pruebas"""
    return {
        'features': np.random.randn(100, 10),
        'labels': np.random.randn(100, 1)
    }

@pytest.fixture
def corrupted_dataset():
    """Dataset con datos corruptos"""
    features = np.random.randn(100, 10)
    features[10:15] = np.nan  # valores nulos
    features[20:25] = np.inf  # valores infinitos
    features[30:35] = -np.inf  # valores infinitos negativos
    
    labels = np.random.randn(100, 1)
    labels[5:10] = np.nan
    
    return {
        'features': features,
        'labels': labels
    }

@pytest.fixture
def api_response_valid():
    """Respuesta válida de la API"""
    return {
        "status": "success",
        "data": {
            "timestamp": "2025-12-08T10:00:00Z",
            "records": [
                {"id": i, "value": float(i * 1.5), "category": "A"}
                for i in range(50)
            ]
        }
    }

@pytest.fixture
def api_response_corrupted():
    """Respuesta de API con datos corruptos"""
    records = []
    for i in range(50):
        record = {"id": i}
        # Introducir varios tipos de corrupción
        if i % 5 == 0:
            record["value"] = None  # valores nulos
        elif i % 7 == 0:
            record["value"] = "invalid"  # tipo incorrecto
        elif i % 11 == 0:
            record["value"] = float('inf')  # infinito
        else:
            record["value"] = float(i * 1.5)
        
        if i % 3 == 0:
            record["category"] = None
        else:
            record["category"] = "A"
        
        records.append(record)
    
    return {
        "status": "success",
        "data": {
            "timestamp": "2025-12-08T10:00:00Z",
            "records": records
        }
    }

@pytest.fixture
def mock_model():
    """Modelo mock para pruebas"""
    model = MagicMock()
    model.fit.return_value.history = {
        'loss': [0.5, 0.4, 0.3],
        'val_loss': [0.6, 0.5, 0.4],
        'mae': [0.3, 0.25, 0.2],
        'val_mae': [0.35, 0.3, 0.25]
    }
    model.predict.return_value = np.array([[0.5], [0.6], [0.7]])
    return model

@pytest.fixture
def sample_dataframe():
    """Fixture that returns a sample pandas DataFrame."""
    data = {
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    }
    df = pd.DataFrame(data)
    return df