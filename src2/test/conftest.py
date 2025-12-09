import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, MagicMock, patch
import tensorflow as tf
import os, sys
import tempfile
import shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

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
    features[10:15] = np.nan
    features[20:25] = np.inf
    features[30:35] = -np.inf
    
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
        if i % 5 == 0:
            record["value"] = None
        elif i % 7 == 0:
            record["value"] = "invalid"
        elif i % 11 == 0:
            record["value"] = float('inf')
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
def temp_db_path():
    """Path temporal para base de datos de prueba"""
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, 'test.db')
    yield db_path
    shutil.rmtree(temp_dir)

@pytest.fixture
def test_database(temp_db_path):
    """Instancia de Database para pruebas"""
    from utils.database import Database
    # Resetear singleton para pruebas
    Database._instance = None
    Database._initialized = False
    db = Database(db_path=temp_db_path)
    yield db
    Database._instance = None
    Database._initialized = False

@pytest.fixture
def test_logger():
    """Instancia de Logger para pruebas"""
    from utils.logger import Logger
    Logger._instance = None
    Logger._initialized = False
    logger = Logger()
    yield logger
    Logger._instance = None
    Logger._initialized = False

@pytest.fixture
def test_user(test_database):
    """Usuario de prueba registrado"""
    user_id = test_database.register_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )
    return {
        'id': user_id,
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpass123'
    }

@pytest.fixture
def test_token(test_database, test_user):
    """Token de sesión para pruebas"""
    return test_database.create_session(test_user['id'])

@pytest.fixture
def flask_app():
    """Aplicación Flask para pruebas"""
    from api.app import app, db, model
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client