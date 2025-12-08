from Core.Model import Model
from Core.Database import GlobalSqlite
# Clase base para inicializar cada Service con modelo Dinamico

class BaseService:
    """
    Clase base para los servicios que manejan modelos de datos. Proporciona
    funcionalidad comun para interactuar con el modelo especifico.

    Atributos:
        model (Model): El modelo de datos asociado con el servicio.
    Metodos:
        __init__(model: type[Model]): Inicializa el servicio con el modelo dado,
    
    configurando la base de datos y creando la tabla si no existe.

    Notes:
        Esto permite que los servicios hereden funcionalidad comun
        para manejar diferentes modelos de datos sin duplicar codigo.

        [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself): Don't Repeat Yourself. - Principio de no repeticion de codigo. Uncle Bob
    """

    model: Model = None

    def __init__(self, model: type[Model]):
        self.model = model
        db = GlobalSqlite.getDataBase()
        self.model.setup_db(db)
        self.model.create_table()
    