from Core.Serializer.Model import ModelSerializer
from Domain.Model.User import User


class UserSerializer(ModelSerializer):
    model = User
    exclude = ["password"]


class AllDataUserSerializer(ModelSerializer):
    model = User
    exclude = []
