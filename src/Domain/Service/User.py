from Domain.Model.User import User
from Domain.Service import BaseService
import hashlib


class UserService(BaseService[User]):

    def __init__(self):
        super().__init__(model=User)

    def create_user(self, username: str, password: str) -> User:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return self.create(username=username, password=password_hash)

    def get_by_username(self, username: str) -> User | None:
        return self.model.filter(username=username).first()
