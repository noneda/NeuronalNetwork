# **REST API CORE**

## **🎯 Uso de Decoradores**

```python
# Crear el router
router = Router()

# Definir rutas con decoradores
@router.get("/users")
def get_users(req: Request, res: Response):
    res.json({"users": users_db})

@router.post("/users")
@require_json  # Middleware para validar JSON
@validate_fields("name", "email")  # Middleware para validar campos
def create_user(req: Request, res: Response):
    new_user = req.body
    # Tu lógica de negocio aquí
    res.json(new_user, 201)

# Rutas con parámetros
@router.get("/users/:id")
def get_user(req: Request, res: Response):
    user_id = req.params['id']  # ← Acceso directo al parámetro
    res.json({"id": user_id})
```

## **✨ Características principales:**

### **1. Decoradores de rutas**

- `@router.get(path)` → GET
- `@router.post(path)` → POST
- `@router.put(path)` → PUT
- `@router.delete(path)` → DELETE
- `@router.route(path, methods=['GET', 'POST'])` → Múltiples métodos

### **2. Parámetros de URL**

```python
@router.get("/users/:id/posts/:post_id")
def handler(req: Request, res: Response):
    user_id = req.params['id']
    post_id = req.params['post_id']
```

### **3. Query Parameters**

```python
# GET /search?name=Juan&age=25
@router.get("/search")
def search(req: Request, res: Response):
    name = req.query.get('name')  # "Juan"
    age = req.query.get('age')    # "25"
```

### **4. Request Object**

```python
def handler(req: Request, res: Response):
    req.body       # Body JSON parseado
    req.params     # Parámetros de URL
    req.query      # Query parameters
    req.method     # GET, POST, etc.
    req.path       # Ruta completa
    req.client_ip  # IP del cliente
    req.headers    # Headers HTTP
```

### **5. Response Object**

```python
def handler(req: Request, res: Response):
    res.json({"key": "value"}, 200)  # Respuesta JSON
    res.text("Hello World", 200)      # Respuesta texto
```

### **6. Middlewares personalizados**

```python
@require_json  # Valida que haya JSON en el body
@validate_fields("name", "email", "password")  # Valida campos
def create_user(req: Request, res: Response):
    # Solo llega aquí si pasa las validaciones
    pass
```

## **📝 Ejemplo de uso:**

```python
# Crear router
router = Router()

# Tu lógica de negocio
@router.post("/neural/train")
@require_json
@validate_fields("data", "epochs")
def train_network(req: Request, res: Response):
    """Entrenar red neuronal"""
    data = req.body['data']
    epochs = req.body['epochs']

    # TODO: Tu lógica de entrenamiento
    result = your_neural_network.train(data, epochs)

    res.json({
        "status": "trained",
        "epochs": epochs,
        "accuracy": result.accuracy
    }, 200)

@router.get("/neural/predict/:model_id")
def predict(req: Request, res: Response):
    """Hacer predicción"""
    model_id = req.params['model_id']
    input_data = req.query.get('input')

    # TODO: Tu lógica de predicción
    prediction = your_model.predict(input_data)

    res.json({"prediction": prediction})
```

## **🚀 Probar la API:**

```bash
# GET todos los usuarios
curl http://localhost:8000/users

# GET usuario específico
curl http://localhost:8000/users/1

# POST crear usuario
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Pedro","email":"pedro@example.com"}'

# PUT actualizar usuario
curl -X PUT http://localhost:8000/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Juan Actualizado"}'

# DELETE eliminar
curl -X DELETE http://localhost:8000/users/1

# Query parameters
curl "http://localhost:8000/search?name=Juan"
```

