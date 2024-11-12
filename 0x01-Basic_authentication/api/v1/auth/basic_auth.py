#!/usr/bin/env python3
"""Basic auth implemented"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """Basic auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """extract_base64_authorization_header"""
        if type(authorization_header) is not str:
            return None
        if not authorization_header:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        result = authorization_header.split(" ", 1)[1]
        return result

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Basic - Base64 decode"""
        if type(base64_authorization_header) is not str:
            return None
        if not base64_authorization_header:
            return None
        try:
            # Decode from Base64, then convert to UTF-8
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None
