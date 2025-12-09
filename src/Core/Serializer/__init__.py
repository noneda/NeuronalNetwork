from Core.Model import Model


class Serializer:
    @staticmethod
    def serialize(
        model_instance: Model, exclude: list[str] = None, include: list[str] = None
    ) -> dict:
        if not hasattr(model_instance, "_fields"):
            raise ValueError("Object is not a Model instance")

        exclude = exclude or []
        result = {}

        for field_name in model_instance._fields.keys():
            if include and field_name not in include:
                continue

            if field_name in exclude:
                continue

            value = getattr(model_instance, field_name, None)
            result[field_name] = value

        return result

    @staticmethod
    def serialize_many(
        model_instances: list[Model],
        exclude: list[str] = None,
        include: list[str] = None,
    ) -> list[dict]:
        return [
            Serializer.serialize(instance, exclude, include)
            for instance in model_instances
        ]
