from Core.Model import Model
from Core.Model.Fields import IntegerField, TextField

class User(Model):
    """
    Modelo de Usuario que representa la tabla 'usuario' en la base de datos.
    Contiene los campos necesarios para almacenar la informacion de los usuarios,
    
    Define los campos:
        - userId: Identificador unico del usuario (clave primaria, autoincremental).
        - username: Nombre de usuario (unico, no nulo).
        - password: Contraseña del usuario (no nulo).
    """
    userId = IntegerField(primary_key=True, auto_increment=True, null=False)
    username = TextField(unique=True, null=False)
    password = TextField(null=False)

    _table_name = "usuario"