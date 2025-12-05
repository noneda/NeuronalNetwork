import http.server

from Core.Logger import Logger
from .Router import Router
from .Response import Response
from .Request import Request


class RestAPIHandler(http.server.BaseHTTPRequestHandler):
    """Handler HTTP que usa el router"""

    router: Router = None  # Se asigna desde fuera

    def log_message(self, format, *args):
        """Override para usar nuestro logger"""
        pass

    def _handle_request(self):
        """Procesa la petición usando el router"""
        req = Request(self)
        res = Response(self)

        Logger.info(f"{req.method} {req.path} from {req.client_ip}")

        # Buscar ruta
        handler, params = self.router.find_route(req.method, req.path)

        if handler:
            req._params = params
            try:
                handler(req, res)
            except Exception as e:
                Logger.error(f"Error en handler: {e}")
                res.json({"error": "Error interno del servidor"}, 500)
        else:
            Logger.warning(f"Ruta no encontrada: {req.method} {req.path}")
            res.json({"error": "Ruta no encontrada"}, 404)

    def do_GET(self):
        self._handle_request()

    def do_POST(self):
        self._handle_request()

    def do_PUT(self):
        self._handle_request()

    def do_DELETE(self):
        self._handle_request()

    def do_PATCH(self):
        self._handle_request()

    def do_OPTIONS(self):
        res = Response(self)
        res.json({}, 200)
