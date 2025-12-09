from Core.Model import Model
from Core.Model.Fields import IntegerField, ForeignKey, FloatField
from Domain.Model.User import User


# TODO: Eran formatos tipo Float XD
class Prediction(Model):
    id = IntegerField(primary_key=True, auto_increment=True, null=False)
    prompt = FloatField(null=False)
    response = FloatField(null=False)
    user = ForeignKey(User, on_delete="CASCADE", related_name="predictions")

    _table_name = "predcitions"
