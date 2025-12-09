# Sistema Deep Learning con API y Autenticación

Sistema completo de Deep Learning con API REST, autenticación de usuarios y persistencia en SQLite3.

## 🌟 Características

- **API REST completa** con Flask
- **Autenticación segura** con tokens de sesión
- **Hashing de contraseñas** con SHA256 + salt
- **Base de datos SQLite3** con patrón Singleton
- **Logger centralizado** con patrón Singleton
- **Modelo de Deep Learning** con TensorFlow
- **Suite completa de tests** con pytest
- **Cobertura de código** superior al 90%

## 📁 Estructura del Proyecto

```
.
├── src/
│   ├── data/              # Carga y limpieza de datos
│   ├── model/             # Modelo de Deep Learning
│   │   └── neural_net.py
│   ├── api/               # API REST
│   │   └── app.py
│   ├── utils/             # Utilidades (Logger, Database)
│   │   ├── logger.py
│   │   └── database.py
│   ├── visualization/     # Visualizaciones
│   └── main.py           # Orquestador principal
├── tests/                # Suite de tests
│   ├── conftest.py
│   ├── test_logger.py
│   ├── test_database.py
│   ├── test_api_endpoints.py
│   ├── test_preprocess.py
│   ├── test_model_training.py
│   └── test_integration_full_system.py
├── scripts/              # Scripts de utilidad
├── data/                 # Base de datos SQLite
├── logs/                 # Logs de la aplicación
├── models/               # Modelos entrenados
└── requirements.txt
```

## 🚀 Instalación Rápida

```bash
# Clonar repositorio
git clone <repo-url>
cd deep-learning-api

# Ejecutar script de inicialización
chmod +x scripts/init_project.sh
./scripts/init_project.sh

# O instalación manual
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 🧪 Ejecutar Tests

```bash
# Todos los tests con cobertura
make test

# Tests específicos
pytest tests/test_database.py -v
pytest tests/test_api_endpoints.py -v

# Con cobertura detallada
make coverage

# Tests por categoría
make test-unit
make test-integration
make test-api
```

## 🏃 Ejecutar la Aplicación

### Opción 1: Script automático
```bash
chmod +x scripts/start_api.sh
./scripts/start_api.sh
```

### Opción 2: Manual
```bash
# Inicializar sistema
python -m src.main

# Iniciar API
python -m src.api.app
```

La API estará disponible en `http://localhost:5000`

## 📡 Endpoints de la API

### Autenticación

**Registro de Usuario**
```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "usuario",
  "email": "email@example.com",
  "password": "password123"
}

Response: {
  "user_id": 1,
  "token": "abc123...",
  "message": "User registered successfully"
}
```

**Login**
```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "usuario",
  "password": "password123"
}

Response: {
  "user": {...},
  "token": "abc123...",
  "message": "Login successful"
}
```

### Predicciones

**Realizar Predicción** (requiere autenticación)
```bash
POST /api/predict
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "Texto para analizar"
}

Response: {
  "prediction_id": 1,
  "input": "Texto para analizar",
  "prediction": "POSITIVE",
  "confidence": 0.85
}
```

**Obtener Historial**
```bash
GET /api/predictions?limit=10
Authorization: Bearer <token>

Response: {
  "predictions": [...],
  "count": 10
}
```

**Obtener Predicción Específica**
```bash
GET /api/predictions/{id}
Authorization: Bearer <token>

Response: {
  "id": 1,
  "input_text": "...",
  "prediction_text": "POSITIVE",
  "confidence": 0.85,
  "created_at": "2025-12-08T10:00:00"
}
```

## 🗄️ Esquema de Base de Datos

### Tabla: users
```sql
id              INTEGER PRIMARY KEY
username        TEXT UNIQUE NOT NULL
email           TEXT UNIQUE NOT NULL
password_hash   TEXT NOT NULL
salt            TEXT NOT NULL
created_at      TIMESTAMP
last_login      TIMESTAMP
```

### Tabla: predictions
```sql
id              INTEGER PRIMARY KEY
user_id         INTEGER FK -> users.id
input_text      TEXT NOT NULL
prediction_text TEXT NOT NULL
confidence      REAL
created_at      TIMESTAMP
```

### Tabla: sessions
```sql
id              INTEGER PRIMARY KEY
user_id         INTEGER FK -> users.id
token           TEXT UNIQUE NOT NULL
expires_at      TIMESTAMP
created_at      TIMESTAMP
```

## 🔒 Seguridad

- **Contraseñas**: Hasheadas con SHA256 + salt único por usuario
- **Tokens**: Generados con `secrets.token_urlsafe(32)`
- **Sesiones**: Expiración configurable (24 horas por defecto)
- **Validación**: Todos los endpoints requieren autenticación excepto registro/login

## 🧪 Cobertura de Tests

Los tests cubren:

✅ **Logger Singleton**: Inicialización, métodos de logging, creación de archivos
✅ **Database Singleton**: CRUD completo, autenticación, sesiones, predicciones
✅ **API Endpoints**: Registro, login, predicciones, autorización
✅ **Modelo DL**: Creación, entrenamiento, predicción, guardado/carga
✅ **Preprocesamiento**: Limpieza de datos corruptos, normalización, outliers
✅ **Integración**: Flujos completos de usuario, API → DB, concurrencia

## 📊 Ejemplo de Uso Completo

```python
from src.utils.database import Database
from src.model.neural_net import DeepLearningModel

# 1. Registrar usuario
db = Database()
user_id = db.register_user("usuario", "email@test.com", "pass123")

# 2. Autenticar
user = db.authenticate_user("usuario", "pass123")
token = db.create_session(user['id'])

# 3. Entrenar modelo
model = DeepLearningModel()
X_train, y_train = load_data()  # Tu función de carga
model.train(X_train, y_train)

# 4. Predecir
prediction, confidence = model.predict_text("Texto de prueba")

# 5. Guardar predicción
prediction_id = db.save_prediction(
    user_id=user_id,
    input_text="Texto de prueba",
    prediction_text=prediction,
    confidence=confidence
)

# 6. Consultar historial
predictions = db.get_user_predictions(user_id, limit=10)
```

## 🐛 Troubleshooting

**Error: ModuleNotFoundError**
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Instalar en modo desarrollo
pip install -e .
```

**Error: Database locked**
```bash
# Eliminar base de datos de prueba
rm data/app.db
```

**Tests fallan por sesiones**
```bash
# Limpiar cache de pytest
pytest --cache-clear
```

## 📝 Licencia

MIT License

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, crea un issue primero para discutir cambios importantes.

---

**Desarrollado usando TensorFlow, Flask y pytest**