from Core import start_rest_server, start_websocket_server
from Core.Logger import Logger
import time
import threading


if __name__ == "__main__":
    Logger.start("=== REST API Server and Native WebSocket ===\n")

    # Initialize WebSocket server on thread separate
    ws_thread = threading.Thread(target=start_websocket_server, args=(8765,))
    ws_thread.daemon = True
    ws_thread.start()

    time.sleep(0.1)

    # Initialize a HTTP Server on thread principal
    try:
        start_rest_server(8000)
    except KeyboardInterrupt:
        Logger.warning("Interrupt signal received (Ctrl+C)")
        Logger.start("Closing servers...")
        Logger.shutdown()
