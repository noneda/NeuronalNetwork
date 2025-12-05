from Core.Logger import Logger

import re, urllib


class Router:
    """Router para registrar rutas con decoradores"""

    def __init__(self):
        self.routes = {
            "GET": [],
            "POST": [],
            "PUT": [],
            "DELETE": [],
            "PATCH": [],
            "OPTIONS": [],
        }

    def _add_route(self, method: str, path: str, handler: callable):
        """Agrega una ruta al router"""
        # Convertir /user/:id a regex /user/(?P<id>[^/]+)
        pattern = re.sub(r":(\w+)", r"(?P<\1>[^/]+)", path)
        pattern = f"^{pattern}$"

        self.routes[method].append(
            {"pattern": re.compile(pattern), "path": path, "handler": handler}
        )
        Logger.success(f"Ruta registrada: {method} {path}")

    def route(self, path: str, methods: list = ["GET"]):
        """Decorador para registrar rutas"""

        def decorator(func: callable):
            for method in methods:
                self._add_route(method.upper(), path, func)
            return func

        return decorator

    def get(self, path: str):
        """Decorador para GET"""
        return self.route(path, ["GET"])

    def post(self, path: str):
        """Decorador para POST"""
        return self.route(path, ["POST"])

    def put(self, path: str):
        """Decorador para PUT"""
        return self.route(path, ["PUT"])

    def delete(self, path: str):
        """Decorador para DELETE"""
        return self.route(path, ["DELETE"])

    def find_route(self, method: str, path: str):
        """Busca una ruta que coincida con el path"""
        parsed = urllib.parse.urlparse(path)
        clean_path = parsed.path

        for route in self.routes.get(method, []):
            match = route["pattern"].match(clean_path)
            if match:
                return route["handler"], match.groupdict()

        return None, {}
