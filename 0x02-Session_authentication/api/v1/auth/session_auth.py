#!/usr/bin/env python3
"""new authentication mechanism"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Session based authentication implemented"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session id for the user with the user_id"""
        if not user_id:
            return None
        if type(user_id) is not str:
            return None
        ssid = str(uuid.uuid4())
        self.user_id_by_session_id[f'{ssid}'] = user_id
        return ssid

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retrieves a user_id(the user) from the session id provided"""
        if not session_id:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(f'{session_id}')

    def current_user(self, request=None):
        """returns the current user based on cookie value"""
        if request is None:
            return None

        # Retrieve the session cookie
        session_id = self.session_cookie(request)
        if not session_id:
            return None

        # Get the User ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None

        # Retrieve the User instance from the database
        user = User.get(user_id)
        return user
