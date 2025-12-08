from Domain.Service.User import UserService
from Domain.Model.User import User
import hashlib


class InterfaseUser(UserService):
    """
    Porque aqui hay logica pero en prediction no?
    Porque en Prediction solo se hace un CRUD simple,
    
    mientras que en User hay reglas de dominio (hash de contraseña).
    
    las reglas de dominio son la logica de negocio que define
    como se comporta la aplicacion en relacion a los usuarios.

    Por ejemplo, al registrar un usuario, se debe verificar
    que el nombre de usuario no exista ya, y al iniciar sesion,
    se debe validar que la contraseña coincida con el hash almacenado.

    En resumen, las reglas de dominio son las que definen
    el comportamiento y las restricciones de la aplicacion en relacion
    a los usuarios, y por eso se implementan en el Repository.

    Y la logica de negocio es la que implementa esas reglas.

    ----
    ## Porque el repositorio se comporta como un proxy del servicio?

    Porque el repositorio define el contexto de uso del servicio.

    **Un Repositorio es un PROXY semantico**.
    """

    def __init__(self):
        super().__init__(User)

    # TODO: Make Methods with Business Logic
    def register(self, username: str, password: str) -> User|None:
        if self.get_by_username(username):
            raise Exception("El usuario ya existe")
        
        return self.create_user(username, password)

    def login(self, username: str, password: str) -> bool:
        user = self.get_by_username(username)

        if not user:
            return False
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return user.password == password_hash

    # * Example
    # def create(self, params, *args, **kwargs) -> dict[str, any]:
    # TODO: Logic
