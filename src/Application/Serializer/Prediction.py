from Core.Serializer.Model import ModelSerializer
from Domain.Model.Predicts import Prediction


class PredictionSerializer(ModelSerializer):
    model = Prediction
