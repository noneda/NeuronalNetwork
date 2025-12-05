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
