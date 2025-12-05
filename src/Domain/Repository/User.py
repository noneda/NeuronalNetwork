from Domain.Service.User import UserService
from Domain.Model.User import User


class InterfaseUser(UserService):

    def __init__(self):
        super().__init__(User)

    # TODO: Make Methods with Business Logic

    # * Example
    # def create(self, params, *args, **kwargs) -> dict[str, any]:
    # TODO: Logic
