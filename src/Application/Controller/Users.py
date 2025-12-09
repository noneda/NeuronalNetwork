from Domain.Repository.User import InterfaseUser
from Core.Api.Request import Request
from Core.Api.Response import Response
from Core.Api.Middleware.require_json import require_json
from Core.Api.Middleware.validate_fields import validate_fields

interfase = InterfaseUser()


@require_json
@validate_fields("name", "password")
def post_register(req: Request, res: Response):
    name = req.body["name"]
    password = req.body["password"]

    try:
        user = interfase.register(name, password)
        if user:
            res.json({"message": "User Create "}, 201)
        else:
            res.json({"message": "Error creating User"}, 400)
    except Exception as e:
        res.json({"message": "Error with Server...", "error": f"{e}"}, 500)


@require_json
@validate_fields("name", "password")
def post_login(req: Request, res: Response):
    name = req.body["name"]
    password = req.body["password"]

    try:
        if interfase.login(name, password):
            res.json({"message": "User Authenticate "}, 201)
        else:
            res.json({"message": "Unauthenticated"}, 400)
    except Exception as e:
        res.json({"message": "Error with Server...", "error": f"{e}"}, 500)
