"""
Websocket Instance
"""

import socket as webSocket
import struct
from .AcceptKey import generateAcceptKey
from ..Logger import Logger


class WebSocketHandler:
    """
    Private Data
    """

    connect: bool = False
    _socket: webSocket.socket
    _address: tuple[str, int]

    def __init__(self, client: webSocket.socket, address: tuple[str, int]):
        self._socket = client
        self._address = address

    def handshake(self):
        """
        Make handshake WebSocket about RFC 6455

        Before using WebSocket, you need to "update" a regular HTTP connection.
        """

        try:
            data = self._socket.recv(1024).decode()
            headers: dict = {}

            # ? This results in a change from the HTTP protocol to WebSocket.
            for line in data.split("\r\n")[1:]:
                if ": " in line:
                    key, value = line.split(": ", 1)
                    headers[key] = value

            if "Sec-WebSocket-Key" not in headers:
                return False

            key: str = generateAcceptKey(headers)
            response: tuple = (
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
            Logger.error(f"Handshake Error : {e} ")
            return False

    def decode_frame(self, data):
        """Decode a WebSocket frame"""
        # TODO: Understand this
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
        """Encode a message in a WebSocket frame"""
        # TODO: Understand this
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

    def send_message(self, message):
        """Send a message to the customer"""
        try:
            self.socket.send(self.encode_frame(message))
            Logger.log(f"→ Sent to {self._address[0]}: {message}")
        except Exception as e:
            Logger.error(f"Error enviando mensaje: {e}")

    def handle(self):
        """Handles the WebSocket connection"""
        if not self.handshake():
            self._socket.close()
            return

        Logger.info(
            f"WebSocket client connected: {self._address[0]}:{self._address[1]}"
        )

        try:
            while self.connected:
                data = self._socket.recv(4096)
                if not data:
                    break

                message = self.decode_frame(data)
                if message:
                    Logger.log(f"← Received from {self._address[0]}: {message}")
                    self.send_message(f"Echo: {message}")

        except Exception as e:
            Logger.error(f"WebSocket connection error: {e}")
        finally:
            self.socket.close()
            Logger.warning(
                f"WebSocket client disconnected: {self._address[0]}:{self._address[1]}"
            )
