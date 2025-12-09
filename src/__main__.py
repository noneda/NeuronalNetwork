from Core.Logger import Logger
from Core.Api.Router import Router
from Core.Api import RestAPIHandler

from Infrastructure.Routes.Users import register_user_routes
from Infrastructure.Routes.Predictions import register_prediction_routes

import time
import socketserver

router = Router()

register_prediction_routes(router)
register_user_routes(router)

RestAPIHandler.router = router


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
