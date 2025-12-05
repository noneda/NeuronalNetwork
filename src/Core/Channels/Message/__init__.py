import json


class WebSocketMessage:
    """Objeto que encapsula un mensaje WebSocket"""

    def __init__(self, handler, raw_data: str):
        self.handler = handler
        self.raw = raw_data
        self.client_ip = handler._address[0]
        self.client_port = handler._address[1]
        self._data = None
        self._event = None

    @property
    def data(self) -> dict[str, any]:
        """Parsea el mensaje como JSON"""
        if self._data is None:
            try:
                parsed = json.loads(self.raw)
                self._event = parsed.get("event", "message")
                self._data = parsed.get("data", {})
            except:
                self._event = "message"
                self._data = {"text": self.raw}
        return self._data

    @property
    def event(self) -> str:
        """Obtiene el tipo de evento"""
        if self._event is None:
            _ = self.data  # Fuerza el parseo
        return self._event

    @property
    def text(self) -> str:
        """Obtiene el texto del mensaje"""
        return self.raw

    def emit(self, event: str, data: any):
        """Emite un mensaje al cliente"""
        self.handler.emit(event, data)

    def broadcast(self, event: str, data: any, include_self: bool = False):
        """Broadcast a todos los clientes conectados"""
        self.handler.broadcast(event, data, include_self)
