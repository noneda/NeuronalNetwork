"""
Make a Process
"""

from .Channels import WebSocketHandler
from .Api import RESTApiHandle
from .Logger import Logger

import socket, threading, socketserver


def start_websocket_server(port=8765):
    """Start the WebSocket server"""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", port))
        server.listen(5)
        Logger.start(f"WebSocket server listening on ws://localhost:{port}")

        while True:
            client, address = server.accept()
            handler = WebSocketHandler(client, address)
            thread = threading.Thread(target=handler.handle)
            thread.start()

    except Exception as e:
        Logger.error(f"Fatal error in WebSocket server: {e}")


def start_rest_server(port=8000):
    """Start the REST API server"""
    try:
        with socketserver.TCPServer(("", port), RESTApiHandle) as httpd:
            Logger.start(f"REST API server running on http://localhost:{port}")
            httpd.serve_forever()
    except Exception as e:
        Logger.error(f"Fatal REST server error: {e}")
