<<<<<<< Updated upstream
=======
# 🧠 BasiNeuronalNetwork

**Red Neuronal para Predicción de Calificaciones** - Una aplicación que utiliza TensorFlow/Keras para predecir notas de examen basadas en horas de estudio, con una arquitectura  Hexagonal.

---

## 📦 ¿Qué es esta Aplicación?

BasiNeuronalNetwork es una plataforma que:
- **Entrena** una red neuronal con datos de estudio y calificaciones
- **Predice** notas de examen basadas en horas de estudio
- **Estructura** el código usando Clean Architecture (Controllers → Repository → Service → Model)
- **Persiste** datos en SQLite y modelos entrenados en SavedModel format

---

## ⚙️ Instalación (Python 3.11)

### 1️⃣ **Crear el Entorno Virtual**

```powershell
py -3.11 -m venv ./env
```

### 2️⃣ **Activar el Entorno Virtual**

**Windows (PowerShell):**
```powershell
./env/Scripts/Activate.ps1
```

**Windows (CMD):**
```cmd
./env/Scripts/activate.bat
```

**Linux/Mac:**
```bash
source env/bin/activate
```

### 3️⃣ **Instalar Dependencias**

```powershell
pip install -r requirements.txt
```

### 4️⃣ **Verificar Instalación**

```powershell
python -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__} ✅')"
```

### 5️⃣ **Ejecutar la Aplicación**

```powershell
python -m src
```

---

## 📋 Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| **tensorflow** | 2.20.0 | Framework de Deep Learning |
| **keras** | 3.12.0 | API de redes neuronales |
| **numpy** | 2.3.5 | Operaciones numéricas |
| **h5py** | 3.15.1 | Guardado/carga de modelos |
| **requests** | 2.32.5 | Solicitudes HTTP |
| **rich** | 14.2.0 | Outputs con estilo en terminal |

---

## 🗂️ Estructura del Proyecto

```
BasiNeuronalNetwork/
├── src/
│   ├── __main__.py              # Punto de entrada
│   ├── Application/
│   │   └── Controller/          # Adaptadores HTTP
│   ├── Core/
│   │   ├── Api/                 # Servidor HTTP
│   │   ├── Database/            # SQLite
│   │   ├── Logger/              # Logging
│   │   ├── Channels/            # WebSocket
│   │   └── NeuronalNetwork/     # Red neuronal
│   │       ├── seed.py          # Entrenamiento
│   │       └── __init__.py      # Predicción
│   ├── Domain/
│   │   ├── Model/               # Entidades
│   │   ├── Service/             # Operaciones técnicas
│   │   └── Repository/          # Lógica de negocio
│   └── Infrastructure/
│       └── Routes/              # Definición de endpoints
├── model_hours_study_saved/     # Modelo entrenado
├── uploads/                     # Archivos subidos
├── env/                         # Entorno virtual
├── requirements.txt             # Dependencias
└── README.md                    # Esta documentación
```

---

>>>>>>> Stashed changes
## Generalización de Términos

1. **Channel** -> Habla de una conexión WebSocket

2. **Model** -> Define la estructura de datos (Molde) que se va usar (Objeto con sus atributos), Es decir su Estado y reglas invariantes.
3. **Repository** -> Se encarga de aplicar la Entidad/Modele y definir los métodos que se van a usar, Es decir una Interfaz de acceso a las Entidades/Modelos.
4. **Service** -> Se encarga de aplicar la lógica de negocio teniendo en cuenta el Modelo y Repositorio.
5. **Infrastructure** -> La base de datos, Framework, I/O.
6. **Hash** -> función matemática que convierte cualquier dato de entrada (texto, archivo, contraseña) en una cadena de caracteres de longitud fija.
7. **Salt** -> es un dato aleatorio único que se añade a una contraseña antes de aplicarle una función hash, creando un hash diferente incluso para contraseñas idénticas.

## Dominio

```
 Controller / API
        ↓
 Repository  ← reglas + casos de uso
        ↓
 Service     ← operaciones técnicas
        ↓
 Model       ← datos + persistencia
        ↓
 Database
```

### Modelo:

define la estructura de los datos y cómo se persisten. Representa entidades del dominio.

### Repositorio:

es el punto de entrada al dominio; define los casos de uso y aplica reglas de negocio.

### Servicio:

ejecuta operaciones técnicas sobre los modelos (guardar, leer, filtrar), sin lógica de dominio.

> [!NOTE]
> Regla de Oro
>
> Si una decisión cambia cuando cambia el negocio → Repository
> Si una decisión cambia cuando cambia la tecnología → Service