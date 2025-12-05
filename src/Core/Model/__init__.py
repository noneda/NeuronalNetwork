from Core.Model.Meta import ModelMeta
from Core.Model.QuerySet import QuerySet

from Core.Model.Fields import DateTimeField

from datetime import datetime


class Model(metaclass=ModelMeta):
    _fields = {}
    _table_name = ""
    _db = None

    def __init__(self, **kwargs):
        self._is_new = True

        for name, field in self._fields.items():
            value = kwargs.get(name, field.default)
            setattr(self, name, value)

    @classmethod
    def setup_db(cls, db):
        cls._db = db

    @classmethod
    def create_table(cls):
        columns = [field.to_sql() for field in cls._fields.values()]
        sql = f"CREATE TABLE IF NOT EXISTS {cls._table_name} ({', '.join(columns)})"

        cursor = cls._db.cursor()
        cursor.execute(sql)
        cls._db.commit()

    @classmethod
    def drop_table(cls):
        sql = f"DROP TABLE IF EXISTS {cls._table_name}"
        cursor = cls._db.cursor()
        cursor.execute(sql)
        cls._db.commit()

    @classmethod
    def all(cls):
        return QuerySet(cls, cls._db)

    @classmethod
    def filter(cls, **kwargs):
        return cls.all().filter(**kwargs)

    @classmethod
    def get(cls, **kwargs):
        return cls.all().get(**kwargs)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj

    def save(self):
        if self._is_new:
            self._insert()
        else:
            self._update()

    def _insert(self):
        fields_to_insert = {}
        for name, field in self._fields.items():
            if field.auto_increment:
                continue

            value = getattr(self, name, None)

            if (
                isinstance(field, DateTimeField)
                and field.auto_now_add
                and value is None
            ):
                value = datetime.now()
                setattr(self, name, value)

            fields_to_insert[name] = field.to_sql_value(value)

        names = list(fields_to_insert.keys())
        values = list(fields_to_insert.values())
        placeholders = ", ".join(["?"] * len(values))

        sql = f"INSERT INTO {self._table_name} ({', '.join(names)}) VALUES ({placeholders})"

        cursor = self._db.cursor()
        cursor.execute(sql, values)
        self._db.commit()

        for name, field in self._fields.items():
            if field.auto_increment:
                setattr(self, name, cursor.lastrowid)

        self._is_new = False

    def _update(self):
        pk_field = None
        pk_value = None
        for name, field in self._fields.items():
            if field.primary_key:
                pk_field = name
                pk_value = getattr(self, name)
                break

        if not pk_field:
            raise Exception("Cannot update without primary key")

        sets = []
        values = []
        for name, field in self._fields.items():
            if name == pk_field:
                continue

            value = getattr(self, name)

            if isinstance(field, DateTimeField) and field.auto_now:
                value = datetime.now()
                setattr(self, name, value)

            sets.append(f"{name} = ?")
            values.append(field.to_sql_value(value))

        values.append(pk_value)
        sql = f"UPDATE {self._table_name} SET {', '.join(sets)} WHERE {pk_field} = ?"

        cursor = self._db.cursor()
        cursor.execute(sql, values)
        self._db.commit()

    def delete(self):
        pk_field = None
        pk_value = None
        for name, field in self._fields.items():
            if field.primary_key:
                pk_field = name
                pk_value = getattr(self, name)
                break

        if not pk_field:
            raise Exception("Cannot delete without primary key")

        sql = f"DELETE FROM {self._table_name} WHERE {pk_field} = ?"
        cursor = self._db.cursor()
        cursor.execute(sql, [pk_value])
        self._db.commit()

    @classmethod
    def _from_db(cls, row, description):
        obj = cls.__new__(cls)
        obj._is_new = False

        for i, col in enumerate(description):
            name = col[0]
            value = row[i]

            if name in cls._fields:
                field = cls._fields[name]
                value = field.to_python(value)

            setattr(obj, name, value)

        return obj

    def __repr__(self):
        fields_str = ", ".join([f"{k}={getattr(self, k)}" for k in self._fields.keys()])
        return f"<{self.__class__.__name__}({fields_str})>"
