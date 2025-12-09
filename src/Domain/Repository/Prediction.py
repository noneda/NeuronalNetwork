from Domain.Service.Prediction import PredictionService
from Core.NeuronalNetwork import predict_note
from Core.Logger import Logger


class InterfasePrediction(PredictionService):

    def __init__(self):
        super().__init__()  # ← Y por q no hizo el Init Aquí???

    def create_for_user(self, user_id: int, prompt: float):
        try:
            predict = predict_note(prompt)

            if "error" in predict:
                Logger.log(f"❌ Error en predicción: {predict['error']}")
                raise ValueError(predict["error"])

            result = predict["predicted_note"]
            Logger.log(f"✅ Predicción completada: {result}")

            return self.create_prediction(user_id, prompt, result)
        except Exception as e:
            Logger.log(f"❌ Error en create_prediction: {str(e)}")
            raise
