from Core.Model import Model
from Core.Database import GlobalSqlite
from typing import TypeVar, Generic


T = TypeVar("T", bound=Model)


class BaseService(Generic[T]):

    model: type[Model] = None

    def __init__(self, model: type[T]):
        self.model = model
        db = GlobalSqlite.get_database()
        self.model.setup_db(db)
        self.model.create_table()

    def create(self, **kwargs) -> T:
        return self.model.create(**kwargs)

    def get(self, **kwargs) -> T:
        return self.model.get(**kwargs)

    def filter(self, **kwargs):
        return self.model.filter(**kwargs)

    def all(self):
        return self.model.all()

    def delete(self, instance: T):
        instance.delete()
