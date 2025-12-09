from Domain.Model.Predicts import Prediction
from Domain.Service import BaseService


class PredictionService(BaseService[Prediction]):

    def __init__(self):
        super().__init__(model=Prediction)

    def create_prediction(self, user: int, prompt: float, result: float) -> Prediction:
        return self.create(user=user, prompt=prompt, response=result)

    def get_by_user(self, user: int) -> Prediction | None:
        return self.model.filter(user=user).order_by("-id")
