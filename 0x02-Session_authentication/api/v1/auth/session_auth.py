#!/usr/bin/env python3
"""new authentication mechanism"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Session based authentication implemented"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for the user with the user_id"""
        if not user_id:
            return None
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        ssid = str(uuid.uuid4())
        self.user_id_by_session_id[f'{ssid}'] = user_id
        return ssid
