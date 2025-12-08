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