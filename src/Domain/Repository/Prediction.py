from Domain.Service.Prediction import PredictionService

class InterfasePrediction(PredictionService):
    """
    ## Por qué el Repositorio tiene un método similar al del Service pero con Nombre distinto?
    
    Se declara como "create_for_user" para que sea más claro el propósito
    del método en el contexto del Repositorio.

    ya que:
     - el Service define **COMO** se hace la creación, pero no el contexto.
     - el Repository define **QUE** se hace.

    ## Porque no hay logica de negocio en este Repositorio?

    Porque en este caso, la creación de predicciones no requiere
    reglas de dominio adicionales más allá del simple CRUD.

    Un repositorio **NO** está obligado a tener lógica de negocio.
    Solo debe tenerla cuando las reglas de dominio lo exigen. 

    Prediccion en este caso:
        - No validad unicidad.
        - No valida permisos.
        - No valida estados.
        - No hay reglas de negocio complejas.
        - Solo crea y recupera datos.
    """
    def create_for_user(self, user_id: int, prompt: str, result: str):
        return self.create_prediction(user_id, prompt, result)