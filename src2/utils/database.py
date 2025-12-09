import sqlite3
import hashlib
import secrets
from threading import Lock
from datetime import datetime
from typing import Optional, Dict, List
# Logger
from utils.logger import Logger

class Database:
    """Singleton Database Manager usando SQLite3"""
    _instance = None
    _lock = Lock()
    
    def __new__(cls, db_path: str = 'data/app.db'):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, db_path: str = 'data/app.db'):
        if self._initialized:
            return
        
        self._initialized = True
        self.db_path = db_path
        self.connection_lock = Lock()
        self.logger = Logger()
        
        # Crear directorio si no existe
        import os
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Inicializar base de datos
        self._init_db()
        self.logger.info("Database initialized successfully")
    
    def _get_connection(self):
        """Obtener conexión thread-safe"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _init_db(self):
        """Inicializar tablas de la base de datos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla de usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP
                )
            ''')
            
            # Tabla de predicciones
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    input_text TEXT NOT NULL,
                    prediction_text TEXT NOT NULL,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Tabla de sesiones (opcional, para tokens)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def _hash_password(self, password: str, salt: str) -> str:
        """Hash de contraseña con SHA256 y salt"""
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _generate_salt(self) -> str:
        """Generar salt aleatorio"""
        return secrets.token_hex(16)
    
    def register_user(self, username: str, email: str, password: str) -> Optional[int]:
        """Registrar nuevo usuario"""
        with self.connection_lock:
            try:
                salt = self._generate_salt()
                password_hash = self._hash_password(password, salt)
                
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO users (username, email, password_hash, salt)
                        VALUES (?, ?, ?, ?)
                    ''', (username, email, password_hash, salt))
                    conn.commit()
                    user_id = cursor.lastrowid
                    
                self.logger.info(f"User registered: {username} (ID: {user_id})")
                return user_id
            except sqlite3.IntegrityError as e:
                self.logger.error(f"Registration failed: {e}")
                return None
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Autenticar usuario"""
        with self.connection_lock:
            try:
                with self._get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        SELECT id, username, email, password_hash, salt
                        FROM users WHERE username = ?
                    ''', (username,))
                    
                    user = cursor.fetchone()
                    
                    if user is None:
                        self.logger.warning(f"Login attempt for non-existent user: {username}")
                        return None
                    
                    # Verificar password
                    password_hash = self._hash_password(password, user['salt'])
                    
                    if password_hash == user['password_hash']:
                        # Actualizar last_login
                        cursor.execute('''
                            UPDATE users SET last_login = CURRENT_TIMESTAMP
                            WHERE id = ?
                        ''', (user['id'],))
                        conn.commit()
                        
                        self.logger.info(f"User authenticated: {username}")
                        return {
                            'id': user['id'],
                            'username': user['username'],
                            'email': user['email']
                        }
                    else:
                        self.logger.warning(f"Failed login attempt for user: {username}")
                        return None
            except Exception as e:
                self.logger.error(f"Authentication error: {e}")
                return None
    
    def create_session(self, user_id: int, expires_in_hours: int = 24) -> str:
        """Crear sesión de usuario"""
        with self.connection_lock:
            token = secrets.token_urlsafe(32)
            expires_at = datetime.now().timestamp() + (expires_in_hours * 3600)
            
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sessions (user_id, token, expires_at)
                    VALUES (?, ?, datetime(?, 'unixepoch'))
                ''', (user_id, token, expires_at))
                conn.commit()
            
            self.logger.info(f"Session created for user_id: {user_id}")
            return token
    
    def validate_session(self, token: str) -> Optional[int]:
        """Validar token de sesión"""
        with self.connection_lock:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_id FROM sessions
                    WHERE token = ? AND expires_at > CURRENT_TIMESTAMP
                ''', (token,))
                
                result = cursor.fetchone()
                return result['user_id'] if result else None
    
    def save_prediction(self, user_id: int, input_text: str, 
                       prediction_text: str, confidence: float = None) -> int:
        """Guardar predicción en la base de datos"""
        with self.connection_lock:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO predictions 
                    (user_id, input_text, prediction_text, confidence)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, input_text, prediction_text, confidence))
                conn.commit()
                prediction_id = cursor.lastrowid
            
            self.logger.info(f"Prediction saved: ID={prediction_id}, user_id={user_id}")
            return prediction_id
    
    def get_user_predictions(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Obtener predicciones de un usuario"""
        with self.connection_lock:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, input_text, prediction_text, confidence, created_at
                    FROM predictions
                    WHERE user_id = ?
                    ORDER BY created_at DESC
                    LIMIT ?
                ''', (user_id, limit))
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
    
    def get_prediction_by_id(self, prediction_id: int) -> Optional[Dict]:
        """Obtener predicción por ID"""
        with self.connection_lock:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT p.*, u.username
                    FROM predictions p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.id = ?
                ''', (prediction_id,))
                
                row = cursor.fetchone()
                return dict(row) if row else None
