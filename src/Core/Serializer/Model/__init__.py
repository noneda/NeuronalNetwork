from Core.Serializer import Serializer
from Core.Model import Model


class ModelSerializer(Serializer):
    model: Model = None
    exclude: list[str] = []
    include: list[str] = None

    def __init__(self, instance=None, many=False):
        self.instance = instance
        self.many = many

    def to_dict(self) -> dict | list[dict]:
        if self.many:
            return self.serialize_many(
                self.instance, exclude=self.exclude, include=self.include
            )
        else:
            return self.serialize(
                self.instance, exclude=self.exclude, include=self.include
            )

    @classmethod
    def from_model(cls, instance, many=False):
        return cls(instance=instance, many=many).to_dict()
