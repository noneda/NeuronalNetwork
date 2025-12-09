from Core.Model import Model
from Core.Model.Fields import IntegerField, FloatField

# TODO: Eran formatos tipo Float XD
class Prediction(Model):
    id = IntegerField(primary_key=True, auto_increment=True, null=False)
    prompt = FloatField(null=False)
    response = FloatField(null=False)
    user = IntegerField(null=False)

    _table_name = "predcitions"
