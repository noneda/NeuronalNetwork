from Domain.Service.Prediction import PredictionService
from Core.NeuronalNetwork import predict_note


class InterfasePrediction(PredictionService):

    def __init__(self):
        super().__init__()  # ← Y por q no hizo el Init Aquí???

    def create_for_user(self, user_id: int, prompt: float):
        predict = predict_note(prompt)
        result = predict["predicted_note"]
        return self.create_prediction(user_id, prompt, result)

