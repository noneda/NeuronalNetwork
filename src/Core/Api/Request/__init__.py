import json, urllib


class Request:
    """Objeto que encapsula la petición HTTP"""

    def __init__(self, handler):
        self.handler = handler
        self.path = handler.path
        self.method = handler.command
        self.headers = handler.headers
        self.client_ip = handler.client_address[0]
        self._body = None
        self._params = {}
        self._query = {}

    @property
    def body(self) -> dict[str, any]:
        """Lee el body JSON de la petición"""
        if self._body is None and self.method in ["POST", "PUT", "PATCH"]:
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length > 0:
                    raw_data = self.handler.rfile.read(content_length)
                    self._body = json.loads(raw_data.decode("utf-8"))
                else:
                    self._body = {}
            except:
                self._body = {}
        return self._body or {}

    @property
    def params(self) -> dict[str, str]:
        """Parámetros de la URL (ej: /user/:id)"""
        return self._params

    @property
    def query(self) -> dict[str, str]:
        """Query parameters (ej: /api?name=Juan&age=25)"""
        if not self._query:
            parsed = urllib.parse.urlparse(self.path)
            self._query = dict(urllib.parse.parse_qsl(parsed.query))
        return self._query
