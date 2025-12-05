from Core.Channels.Message import WebSocketMessage
from Core.Logger import Logger


def require_auth(msg: WebSocketMessage):
    """Middleware de ejemplo para requerir autenticación"""
    # Aquí podrías validar un token
    if msg.event != "auth" and not hasattr(msg.handler, "authenticated"):
        msg.emit("error", {"message": "No autenticado"})
        return False
    return True
