import sqlite3
from datetime import datetime


class Field:
    def __init__(
        self,
        sql_type,
        primary_key=False,
        auto_increment=False,
        null=True,
        unique=False,
        default=None,
    ):
        self.sql_type = sql_type
        self.primary_key = primary_key
        self.auto_increment = auto_increment
        self.null = null
        self.unique = unique
        self.default = default
        self.column_name = None

    def to_sql(self):
        parts = [self.column_name, self.sql_type]

        if self.primary_key:
            parts.append("PRIMARY KEY")
        if self.auto_increment:
            parts.append("AUTOINCREMENT")
        if not self.null:
            parts.append("NOT NULL")
        if self.unique:
            parts.append("UNIQUE")
        if self.default is not None:
            parts.append(f"DEFAULT {self.default}")

        return " ".join(parts)

    def to_python(self, value):
        return value

    def to_sql_value(self, value):
        return value


class IntegerField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)


class TextField(Field):
    def __init__(self, max_length=None, **kwargs):
        sql_type = f"VARCHAR({max_length})" if max_length else "TEXT"
        super().__init__(sql_type, **kwargs)


class FloatField(Field):
    def __init__(self, **kwargs):
        super().__init__("REAL", **kwargs)


class BooleanField(Field):
    def __init__(self, **kwargs):
        super().__init__("INTEGER", **kwargs)

    def to_python(self, value):
        return bool(value) if value is not None else None

    def to_sql_value(self, value):
        return 1 if value else 0


class DateTimeField(Field):
    def __init__(self, auto_now=False, auto_now_add=False, **kwargs):
        super().__init__("TEXT", **kwargs)
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value)

    def to_sql_value(self, value):
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return value


class ForeignKey(Field):
    def __init__(self, to, on_delete="CASCADE", related_name=None, **kwargs):
        super().__init__("INTEGER", **kwargs)
        self.to = to
        self.on_delete = on_delete
        self.related_name = related_name
        self.is_foreign_key = True

    def to_sql(self):
        base_sql = super().to_sql()
        reference_table = (
            self.to._table_name if hasattr(self.to, "_table_name") else self.to
        )

        pk_field = None
        if hasattr(self.to, "_fields"):
            for name, field in self.to._fields.items():
                if field.primary_key:
                    pk_field = name
                    break

        pk_field = pk_field or "id"

        base_sql += (
            f" REFERENCES {reference_table}({pk_field}) ON DELETE {self.on_delete}"
        )
        return base_sql

    def get_related_object(self, instance):
        if not hasattr(instance, self.column_name):
            return None

        fk_value = getattr(instance, self.column_name)
        if fk_value is None:
            return None

        return self.to.get(id=fk_value)


class OneToOneField(ForeignKey):
    def __init__(self, to, on_delete="CASCADE", related_name=None, **kwargs):
        kwargs["unique"] = True
        super().__init__(to, on_delete, related_name, **kwargs)
        self.is_one_to_one = True


class ManyToManyField:
    def __init__(self, to, through=None, related_name=None):
        self.to = to
        self.through = through
        self.related_name = related_name
        self.is_many_to_many = True
        self.column_name = None

    def create_through_table(self, source_model):
        if self.through:
            return

        source_table = source_model._table_name
        target_table = (
            self.to._table_name if hasattr(self.to, "_table_name") else self.to
        )

        through_table_name = f"{source_table}_{self.column_name}"

        sql = f"""
        CREATE TABLE IF NOT EXISTS {through_table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {source_table}_id INTEGER NOT NULL,
            {target_table}_id INTEGER NOT NULL,
            FOREIGN KEY ({source_table}_id) REFERENCES {source_table}(id) ON DELETE CASCADE,
            FOREIGN KEY ({target_table}_id) REFERENCES {target_table}(id) ON DELETE CASCADE,
            UNIQUE({source_table}_id, {target_table}_id)
        )
        """

        cursor = source_model._db.cursor()
        cursor.execute(sql)
        source_model._db.commit()

        self.through_table = through_table_name
        self.source_column = f"{source_table}_id"
        self.target_column = f"{target_table}_id"

    def get_manager(self, instance):
        return ManyToManyManager(instance, self)


class ManyToManyManager:
    def __init__(self, instance, field):
        self.instance = instance
        self.field = field
        self.through_table = field.through_table
        self.source_column = field.source_column
        self.target_column = field.target_column

    def add(self, *objects):
        cursor = self.instance._db.cursor()
        for obj in objects:
            try:
                cursor.execute(
                    f"INSERT INTO {self.through_table} ({self.source_column}, {self.target_column}) VALUES (?, ?)",
                    (self.instance.id, obj.id),
                )
            except sqlite3.IntegrityError:
                pass
        self.instance._db.commit()

    def remove(self, *objects):
        cursor = self.instance._db.cursor()
        for obj in objects:
            cursor.execute(
                f"DELETE FROM {self.through_table} WHERE {self.source_column} = ? AND {self.target_column} = ?",
                (self.instance.id, obj.id),
            )
        self.instance._db.commit()

    def all(self):
        cursor = self.instance._db.cursor()
        cursor.execute(
            f"SELECT {self.target_column} FROM {self.through_table} WHERE {self.source_column} = ?",
            (self.instance.id,),
        )

        ids = [row[0] for row in cursor.fetchall()]

        if not ids:
            return []

        placeholders = ",".join(["?"] * len(ids))
        target_table = self.field.to._table_name

        cursor.execute(
            f"SELECT * FROM {target_table} WHERE id IN ({placeholders})", ids
        )

        results = []
        for row in cursor.fetchall():
            obj = self.field.to._from_db(row, cursor.description)
            results.append(obj)

        return results

    def clear(self):
        cursor = self.instance._db.cursor()
        cursor.execute(
            f"DELETE FROM {self.through_table} WHERE {self.source_column} = ?",
            (self.instance.id,),
        )
        self.instance._db.commit()

    def count(self):
        cursor = self.instance._db.cursor()
        cursor.execute(
            f"SELECT COUNT(*) FROM {self.through_table} WHERE {self.source_column} = ?",
            (self.instance.id,),
        )
        return cursor.fetchone()[0]
