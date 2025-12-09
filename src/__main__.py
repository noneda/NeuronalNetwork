from Core.Logger import Logger
from Core.Api import RestAPIHandler
from Infrastructure.Routes import makeRouter

import time
import socketserver

makeRouter(RestAPIHandler)

if __name__ == "__main__":
    Logger.start("=== REST API Server and Native WebSocket ===\n")
    try:
        # Initialize WebSocket server on thread separate
        # TODO: Si Quiere Intentar hágale... Yo no quiero estresarme
        time.sleep(0.1)
        with socketserver.TCPServer(("", 8000), RestAPIHandler) as httpd:
            print("Server running on http://localhost:8000")
            httpd.serve_forever()

    except KeyboardInterrupt:
        Logger.warning("Interrupt signal received (Ctrl+C)")
        Logger.start("Closing servers...")
        Logger.shutdown()
