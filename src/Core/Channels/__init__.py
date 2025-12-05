from Core.Logger import Logger
from Core.Channels.Router import WebSocketRouter
from Core.Channels.Message import WebSocketMessage
from Core.Channels.Utils.accept_key import generateAcceptKey

import socket as webSocket
import struct, json


class WebSocketHandler:
    """Handler WebSocket con soporte de eventos"""

    router: WebSocketRouter = None  # Se asigna desde fuera

    def __init__(self, client: webSocket.socket, address: tuple[str, int]):
        self._socket = client
        self._address = address
        self.connected = False
        self.client_data = {}  # Datos del cliente (ej: user_id, tokens, etc)

    def handshake(self):
        """Handshake WebSocket según RFC 6455"""
        try:
            data = self._socket.recv(1024).decode()
            headers: dict = {}

            for line in data.split("\r\n")[1:]:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    headers[key] = value

            if "Sec-WebSocket-Key" not in headers:
                return False

            key: str = generateAcceptKey(headers)
            response = (
                "HTTP/1.1 101 Switching Protocols\r\n"
                "Upgrade: websocket\r\n"
                "Connection: Upgrade\r\n"
                f"Sec-WebSocket-Accept: {key}\r\n\r\n"
            )

            self._socket.send(response.encode())
            self.connected = True

            Logger.success(
                f"WebSocket handshake exitoso con {self._address[0]}:{self._address[1]}"
            )

            return True
        except Exception as e:
            Logger.error(f"Handshake Error: {e}")
            return False

    def decode_frame(self, data):
        """Decodifica un frame WebSocket"""
        try:
            if len(data) < 2:
                return None

            byte1, byte2 = data[0], data[1]
            opcode = byte1 & 0x0F
            masked = byte2 & 0x80
            payload_length = byte2 & 0x7F

            offset = 2

            if payload_length == 126:
                payload_length = struct.unpack(">H", data[offset : offset + 2])[0]
                offset += 2
            elif payload_length == 127:
                # data[2:10] contiene la longitud del payload en 8 bytes
                payload_length = struct.unpack(">Q", data[offset : offset + 8])[0]
                offset += 8

            if masked:
                mask = data[offset : offset + 4]
                offset += 4
                payload = bytearray(data[offset : offset + payload_length])
                for i in range(len(payload)):
                    payload[i] ^= mask[i % 4]
                return payload.decode()

            return data[offset : offset + payload_length].decode()
        except Exception as e:
            Logger.error(f"Error decoding frame: {e}")
            return None

    def encode_frame(self, message):
        """Codifica un mensaje en frame WebSocket"""
        message_bytes = message.encode()
        frame = bytearray([0x81])  # Text frame

        length = len(message_bytes)
        if length < 126:
            frame.append(length)
        elif length < 65536:
            frame.append(126)
            frame.extend(struct.pack(">H", length))
        else:
            frame.append(127)
            frame.extend(struct.pack(">Q", length))

        frame.extend(message_bytes)
        return bytes(frame)

    def send_raw(self, message: str):
        """Envía mensaje raw (sin formato de evento)"""
        try:
            self._socket.send(self.encode_frame(message))
        except Exception as e:
            Logger.error(f"Error enviando mensaje: {e}")

    def emit(self, event: str, data: any):
        """Emite un evento al cliente"""
        try:
            message = json.dumps({"event": event, "data": data})
            self._socket.send(self.encode_frame(message))
            Logger.log(f"→ [{event}] to {self._address[0]}: {data}")
        except Exception as e:
            Logger.error(f"Error enviando evento: {e}")

    def broadcast(self, event: str, data: any, include_self: bool = False):
        """Broadcast a todos los clientes"""
        exclude = None if include_self else self
        self.router.broadcast_to_all(event, data, exclude)

    def handle(self):
        """Maneja la conexión WebSocket"""
        if not self.handshake():
            self._socket.close()
            return

        # Agregar a lista de clientes
        self.router.add_client(self)

        Logger.info(
            f"WebSocket client connected: {self._address[0]}:{self._address[1]}"
        )

        # Evento de conexión
        self.emit(
            "connected",
            {
                "message": "Conectado exitosamente",
                "client_id": f"{self._address[0]}:{self._address[1]}",
            },
        )

        try:
            while self.connected:
                data = self._socket.recv(4096)
                if not data:
                    break

                raw_message = self.decode_frame(data)
                if raw_message:
                    msg = WebSocketMessage(self, raw_message)
                    self.router.handle_event(msg)

        except Exception as e:
            Logger.error(f"WebSocket connection error: {e}")
        finally:
            self.connected = False
            self.router.remove_client(self)
            self._socket.close()
            Logger.warning(
                f"WebSocket client disconnected: {self._address[0]}:{self._address[1]}"
            )
