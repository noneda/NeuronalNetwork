from Core.Model import Model
from Core.Model.Fields import IntegerField, TextField

class Prediction(Model):
    """
    Modelo de Prediccion que representa la tabla 'predcitions' en la base de datos.
    Contiene los campos necesarios para almacenar las predicciones generadas
    por el sistema de red neuronal.

    Define los campos:
        - predictionId: Identificador unico de la prediccion (clave primaria, autoincremental).
        - predPromt: Texto del prompt utilizado para generar la prediccion (no nulo).
        - predRes: Resultado de la prediccion generada (no nulo).
        - userId: Identificador del usuario que genero la prediccion (no nulo).
    """

    predictionId = IntegerField(primary_key=True, auto_increment=True, null=False)
    # Que sera mejor? -> pred o prediction, para indicar el campo (Lo mejor seria el descriptivo -> prediction).
    predPromt = TextField(null=False)
    predRes = TextField(null=False)
    userId = IntegerField(null=False)

    _table_name = "predcitions"

    # SQLite acepta foreing key, Pero el ORM de CORE no soporta constraints, asi que la relacion
    # es logica, no fisica.
