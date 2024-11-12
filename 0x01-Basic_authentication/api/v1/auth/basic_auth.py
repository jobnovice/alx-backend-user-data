#!/usr/bin/env python3
"""Basic auth implemented"""
from api.v1.auth.auth import Auth


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
