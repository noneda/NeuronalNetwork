from Domain.Service.User import UserService
from Domain.Model.User import User
import hashlib


class InterfaseUser(UserService):

    def __init__(self):
        super().__init__()  # ← Sin pasar el Modelo, ya lo tiene el Servicio XD

    def register(self, username: str, password: str) -> User | None:
        if self.get_by_username(username):
            raise Exception("El usuario ya existe")

        return self().create_user(username, password)

    def login(self, username: str, password: str) -> bool:
        user = self().get_by_username(username)

        if not user:
            return False

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return user.password == password_hash
