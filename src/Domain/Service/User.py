from Core.Model import Model
from Core.Database import GlobalSqlite
from Domain.Model.User import User
from Domain.Service import BaseService

# Para hashear la contraseña se necesita usar hashlib
import hashlib

class UserService(BaseService):
    

    def __init__(self):
        super().__init__(model=User)
        
    # No se que sera mejor indicar que es un Modelo o un definir directamente User
    def create_user(self, username: str, password: str) -> User:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.model.create(
            username=username,
            password=password_hash
        )
    
    def get_by_username(self, username: str) -> User:
        return self.model.filter(username=username).first()
    # TODO: Make Methods like... Hollow

    # * Example
    # def create(self, params, *args, **kwargs) -> dict[str, any]:
    #   pass
