import pytest
from utils.database import Database
import hashlib

class TestDatabase:
    """Tests para el Database Singleton"""
    
    def test_singleton_pattern(self, temp_db_path):
        """Test: Database es singleton"""
        Database._instance = None
        db1 = Database(db_path=temp_db_path)
        db2 = Database(db_path=temp_db_path)
        assert db1 is db2
        Database._instance = None
    
    def test_database_initialization(self, test_database):
        """Test: Base de datos se inicializa con tablas correctas"""
        conn = test_database._get_connection()
        cursor = conn.cursor()
        
        # Verificar que existen las tablas
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('users', 'predictions', 'sessions')
        """)
        tables = cursor.fetchall()
        table_names = [t[0] for t in tables]
        
        assert 'users' in table_names
        assert 'predictions' in table_names
        assert 'sessions' in table_names
        conn.close()
    
    def test_register_user_success(self, test_database):
        """Test: Registro exitoso de usuario"""
        user_id = test_database.register_user(
            username="newuser",
            email="new@example.com",
            password="password123"
        )
        
        assert user_id is not None
        assert isinstance(user_id, int)
        assert user_id > 0
    
    def test_register_duplicate_username(self, test_database, test_user):
        """Test: No se puede registrar username duplicado"""
        user_id = test_database.register_user(
            username=test_user['username'],
            email="different@example.com",
            password="password123"
        )
        
        assert user_id is None
    
    def test_register_duplicate_email(self, test_database, test_user):
        """Test: No se puede registrar email duplicado"""
        user_id = test_database.register_user(
            username="differentuser",
            email=test_user['email'],
            password="password123"
        )
        
        assert user_id is None
    
    def test_authenticate_user_success(self, test_database, test_user):
        """Test: Autenticación exitosa"""
        user = test_database.authenticate_user(
            username=test_user['username'],
            password=test_user['password']
        )
        
        assert user is not None
        assert user['id'] == test_user['id']
        assert user['username'] == test_user['username']
        assert user['email'] == test_user['email']
    
    def test_authenticate_user_wrong_password(self, test_database, test_user):
        """Test: Autenticación falla con contraseña incorrecta"""
        user = test_database.authenticate_user(
            username=test_user['username'],
            password="wrongpassword"
        )
        
        assert user is None
    
    def test_authenticate_nonexistent_user(self, test_database):
        """Test: Autenticación falla con usuario inexistente"""
        user = test_database.authenticate_user(
            username="nonexistent",
            password="password123"
        )
        
        assert user is None
    
    def test_password_hashing(self, test_database):
        """Test: Contraseñas se hashean correctamente"""
        password = "testpassword"
        salt = test_database._generate_salt()
        hash1 = test_database._hash_password(password, salt)
        hash2 = test_database._hash_password(password, salt)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 produce 64 caracteres hex
        assert hash1 != password
    
    def test_different_salts_produce_different_hashes(self, test_database):
        """Test: Diferentes salts producen diferentes hashes"""
        password = "testpassword"
        salt1 = test_database._generate_salt()
        salt2 = test_database._generate_salt()
        
        hash1 = test_database._hash_password(password, salt1)
        hash2 = test_database._hash_password(password, salt2)
        
        assert hash1 != hash2
    
    def test_create_session(self, test_database, test_user):
        """Test: Creación de sesión"""
        token = test_database.create_session(test_user['id'])
        
        assert token is not None
        assert len(token) > 20
    
    def test_validate_session_success(self, test_database, test_user, test_token):
        """Test: Validación exitosa de sesión"""
        user_id = test_database.validate_session(test_token)
        assert user_id == test_user['id']
    
    def test_validate_session_invalid_token(self, test_database):
        """Test: Validación falla con token inválido"""
        user_id = test_database.validate_session("invalid_token_xyz")
        assert user_id is None
    
    def test_save_prediction(self, test_database, test_user):
        """Test: Guardar predicción"""
        prediction_id = test_database.save_prediction(
            user_id=test_user['id'],
            input_text="Test input",
            prediction_text="POSITIVE",
            confidence=0.85
        )
        
        assert prediction_id is not None
        assert isinstance(prediction_id, int)
        assert prediction_id > 0
    
    def test_get_user_predictions(self, test_database, test_user):
        """Test: Obtener predicciones de usuario"""
        # Crear varias predicciones
        for i in range(5):
            test_database.save_prediction(
                user_id=test_user['id'],
                input_text=f"Test input {i}",
                prediction_text="POSITIVE",
                confidence=0.8 + (i * 0.02)
            )
        
        predictions = test_database.get_user_predictions(test_user['id'], limit=10)
        
        assert len(predictions) == 5
        assert all('input_text' in p for p in predictions)
        assert all('prediction_text' in p for p in predictions)
    
    def test_get_prediction_by_id(self, test_database, test_user):
        """Test: Obtener predicción por ID"""
        prediction_id = test_database.save_prediction(
            user_id=test_user['id'],
            input_text="Test input",
            prediction_text="NEGATIVE",
            confidence=0.75
        )
        
        prediction = test_database.get_prediction_by_id(prediction_id)
        
        assert prediction is not None
        assert prediction['id'] == prediction_id
        assert prediction['user_id'] == test_user['id']
        assert prediction['input_text'] == "Test input"
        assert prediction['prediction_text'] == "NEGATIVE"
        assert prediction['confidence'] == 0.75