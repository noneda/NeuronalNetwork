"""
Make client for REST APi
"""

import http.server
import urllib.parse
import json

from ..Logger import Logger


class RESTApiHandle(http.server.BaseHTTPRequestHandler):
    """
    Controller REST API
    """

    def log_message(self, format, *args):
        """Override to use our logger instead of the default print"""
        pass

    def _set_header(self, status=200, content_type="application/json"):
        """Configuration from server PRIVATE"""

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        """CORS preflight"""

        Logger.log(f"OPTIONS {self.path} from {self.client_address[0]}")

        self._set_header()

    def _Res(self, data: dict) -> None:
        """Basic Response HTTP"""

        self.wfile.write(json.dumps(data).encode())

    def _Req(self) -> dict[str, any]:
        """Basic Request HTTP"""

        content_length = int(self.headers["Content-Length"])
        raw_data = self.rfile.read(content_length)
        return json.loads(raw_data.decode("utf-8"))

    def do_GET(self):
        """Get Method"""

        # * This make a parse PATH... For get a params
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        Logger.info(f"GET {path} from {self.client_address[0]}")

        # * This is a All Data
        if path == "/api/get":
            self._set_header()
            self._Res(
                # TODO: Here make a return All Data...
            )

        # * This is with params
        # ? Example → /api/get/{id}
        elif path.startswith("/api/get"):
            try:
                id = int(path.split("/")[-1])
                self._set_header(200)
                self._Res(
                    # TODO: Implement Logic to get a Data
                )
            except ValueError:
                self._set_header(400)
                self._Res({"error": "ID inválido"})
        else:
            self._set_headers(404)
            self._Res({"error": "Ruta no encontrada"})

    def POST(self):
        """POST Method"""

        Logger.info(f"POST {self.path} desde {self.client_address[0]}")

        if self.path == "/api/post":
            data = self._Req()

            # TODO: Logic for Insert Data to Neuronal Network
            self._set_headers(201)
            self.wfile.write(
                # TODO: Response
            )

        else:
            self._set_header(404)
            self._Res({"error": "Ruta no encontrada"})
