"""
Util for WebSocket
"""

import base64
import hashlib


def generateAcceptKey(headers: dict[str, str]) -> str:
    """For security reasons, a hashed key is generated."""
    
    magic = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    return base64.b64encode(
        hashlib.sha1((headers["Sec-WebSocket-Key"] + magic).encode()).digest()
    ).decode()
