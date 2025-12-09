from Core.Model.Fields import Field, ManyToManyField


class ModelMeta(type):
    def __new__(mcs, name, bases, attrs):
        if name == "Model":
            return super().__new__(mcs, name, bases, attrs)

        fields = {}
        many_to_many_fields = {}

        for key, value in list(attrs.items()):
            if isinstance(value, ManyToManyField):
                value.column_name = key
                many_to_many_fields[key] = value
                attrs.pop(key)
            elif isinstance(value, Field):
                value.column_name = key
                fields[key] = value
                attrs.pop(key)

        attrs["_fields"] = fields
        attrs["_many_to_many_fields"] = many_to_many_fields
        attrs["_table_name"] = attrs.get("_table_name", name.lower())

        return super().__new__(mcs, name, bases, attrs)
