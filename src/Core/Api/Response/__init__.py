import json


class Response:
    """Objeto que encapsula la respuesta HTTP"""

    def __init__(self, handler):
        self.handler = handler
        self.status_code = 200
        self.headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }

    def json(self, data: dict[str, any], status: int = 200):
        """Envía respuesta JSON"""
        self.status_code = status
        self.handler.send_response(status)
        for key, value in self.headers.items():
            self.handler.send_header(key, value)
        self.handler.end_headers()
        self.handler.wfile.write(json.dumps(data).encode())

    def text(self, data: str, status: int = 200):
        """Envía respuesta de texto plano"""
        self.status_code = status
        self.handler.send_response(status)
        self.handler.send_header("Content-Type", "text/plain")
        for key, value in self.headers.items():
            if key != "Content-Type":
                self.handler.send_header(key, value)
        self.handler.end_headers()
        self.handler.wfile.write(data.encode())
