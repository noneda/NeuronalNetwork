from functools import wraps
from Core.Api.Request import Request
from Core.Api.Response import Response


def require_json(func):
    """Middleware que valida que el body sea JSON válido"""

    @wraps(func)
    def wrapper(req: Request, res: Response):
        if req.method in ["POST", "PUT", "PATCH"]:
            if not req.body:
                return res.json({"error": "Body JSON requerido"}, 400)
        return func(req, res)

    return wrapper
