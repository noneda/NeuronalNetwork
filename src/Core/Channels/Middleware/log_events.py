from Core.Channels.Message import WebSocketMessage
from Core.Logger import Logger


def log_events(msg: WebSocketMessage):
    """Middleware que logea todos los eventos"""
    Logger.log(f"← [{msg.event}] from {msg.client_ip}: {msg.data}")
    return True
