from Domain.Repository.User import InterfaseUser
from Core.Api.Request import Request
from Core.Api.Response import Response
from Application.Serializer.User import UserSerializer, AllDataUserSerializer

interfase = InterfaseUser()


def post_register(req: Request, res: Response):
    name = req.body["name"]
    password = req.body["password"]

    try:
        user = interfase.register(name, password)
        if user:
            send = UserSerializer.from_model(user)
            res.json({"message": "User Create", "user": send}, 201)
        else:
            res.json({"message": "Error creating User"}, 400)
    except Exception as e:
        res.json({"message": "Error with Server...", "error": f"{e}"}, 500)


def post_login(req: Request, res: Response):
    name = req.body["name"]
    password = req.body["password"]

    try:
        if interfase.login(name, password):
            res.json({"message": "User Authenticate"}, 201)
        else:
            res.json({"message": "Unauthenticated"}, 400)
    except Exception as e:
        res.json({"message": "Error with Server...", "error": f"{e}"}, 500)


def get_me(req: Request, res: Response):
    name: str = req.params["name"]
    try:
        user = interfase.get_by_username(name)
        if user:
            send = AllDataUserSerializer.from_model(user)
            res.json({"data": send}, 201)
        else:
            res.json({"message": "Error getting your User"}, 400)
    except Exception as e:
        res.json({"message": "Error with Server...", "error": f"{e}"}, 500)
