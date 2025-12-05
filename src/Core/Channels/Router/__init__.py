from Core.Channels.Message import WebSocketMessage
from Core.Logger import Logger

import json


class WebSocketRouter:
    """Router para eventos WebSocket con decoradores"""

    def __init__(self):
        self.events: dict[str, callable] = {}
        self.middlewares = []
        self.clients = []  # Lista de clientes conectados

    def on(self, event: str):
        """Decorador para registrar eventos"""

        def decorator(func: callable):
            self.events[event] = func
            Logger.success(f"Evento WebSocket registrado: '{event}'")
            return func

        return decorator

    def use(self, middleware: callable):
        """Registra un middleware global"""
        self.middlewares.append(middleware)
        Logger.success(f"Middleware WebSocket registrado")
        return middleware

    def handle_event(self, msg: WebSocketMessage):
        """Maneja un evento recibido"""
        event = msg.event

        # Ejecutar middlewares
        for middleware in self.middlewares:
            result = middleware(msg)
            if result is False:
                return  # Middleware bloqueó el evento

        # Buscar handler
        handler = self.events.get(event)
        if handler:
            try:
                handler(msg)
            except Exception as e:
                Logger.error(f"Error en handler '{event}': {e}")
        else:
            Logger.warning(f"Evento sin handler: '{event}'")

    def add_client(self, client):
        """Agrega un cliente a la lista"""
        self.clients.append(client)

    def remove_client(self, client):
        """Remueve un cliente de la lista"""
        if client in self.clients:
            self.clients.remove(client)

    def broadcast_to_all(self, event: str, data: any, exclude=None):
        """Broadcast a todos los clientes"""
        message = json.dumps({"event": event, "data": data})
        for client in self.clients:
            if client != exclude and client.connected:
                try:
                    client.send_raw(message)
                except Exception as e:
                    Logger.error(f"Error en broadcast: {e}")
