from Core.Model import Model
from Core.Database import GlobalSqlite


class UserService:
    model: Model = None

    def __init__(self, model: Model):
        self.model = model
        self.model.setUp(GlobalSqlite.getDataBase())
        self.model.create_table()

    # TODO: Make Methods like... Hollow

    # * Example
    # def create(self, params, *args, **kwargs) -> dict[str, any]:
    #   pass
