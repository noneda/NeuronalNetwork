from Core.Channels.Message import WebSocketMessage
from Core.Logger import Logger


def validate_json(msg: WebSocketMessage):
    """Middleware que valida que el mensaje sea JSON válido"""
    try:
        _ = msg.data
        return True
    except:
        msg.emit("error", {"message": "JSON inválido"})
        return False
