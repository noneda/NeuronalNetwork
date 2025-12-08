from Core.Model import Model
from Core.Database import GlobalSqlite
from Domain.Model.Predicts import Prediction
from Domain.Service import BaseService

class PredictionService(BaseService):
    """
    Se extiende BaseService para heredar la funcionalidad basica de CRUD
    y se especifica el modelo Prediction para que el servicio.

    ## [Note 1](Linea 29) funcion create_prediction. 

    No se que sera mejor indicar que es un Modelo o un definir directamente Predict

    ## [Note 2](Linea 29) funcion create_prediction. 

    Analizando la funcion el debe retornar el resultado de BD osea un Str? O Objeto
    No el modelo jjsjs, Pero el **METODO** Model.create retorna `Any` <- Toca cambiar eso. :)
    Ya me confundi. El crea una prediccion jaja, Entonces si devuelve un Modelo. Cuando pueda me escribe para 
    Hablar sobre esta KK.
    """

    # Aqui esta usando el Modelo Predic,
    # Pero si queremos declarar el Modelo desde el Core,
    # Toca agregar la propiedad "Model" y pasarselo al super (@override)
    def __init__(self):
        super().__init__(model=Prediction)

    def create_prediction(self, user_id: int, promt: str, result: str) -> Model:
        return self.model.create(
            userId = user_id,
            predPromt = promt,
            predRes = result
        )
    
    def get_by_user(self, user_id: int):
        return self.model.filter(userId=user_id).order_by("-idPred")