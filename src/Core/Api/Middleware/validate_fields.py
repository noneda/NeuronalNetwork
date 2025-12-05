from functools import wraps
from Core.Api.Request import Request
from Core.Api.Response import Response


def validate_fields(*required_fields):
    """Middleware que valida campos requeridos en el body"""

    def decorator(func):
        @wraps(func)
        def wrapper(req: Request, res: Response):
            missing = [f for f in required_fields if f not in req.body]
            if missing:
                return res.json({"error": "Campos faltantes", "missing": missing}, 400)
            return func(req, res)

        return wrapper

    return decorator
