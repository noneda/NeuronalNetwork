from Core.Logger import Logger
import time
import threading


if __name__ == "__main__":
    Logger.start("=== REST API Server and Native WebSocket ===\n")

    try:
        # Initialize WebSocket server on thread separate
        time.sleep(0.1)
        # Initialize a HTTP Server on thread principal
    except KeyboardInterrupt:
        Logger.warning("Interrupt signal received (Ctrl+C)")
        Logger.start("Closing servers...")
        Logger.shutdown()
