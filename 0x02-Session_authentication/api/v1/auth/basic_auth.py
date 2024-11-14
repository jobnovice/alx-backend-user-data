#!/usr/bin/env python3
"""Basic auth implemented"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Basic - User credentials"""
        if decoded_base64_authorization_header is None:
            return None, None
        if type(decoded_base64_authorization_header) is not str:
            return None, None
        if ":" not in decoded_base64_authorization_header:
            return None, None
        bf_co, sp, af_co = decoded_base64_authorization_header.partition(":")
        return bf_co, af_co

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Basic - User object"""
        if user_email is None or not isinstance(
                user_email, str) or user_pwd is None or not isinstance(
                    user_pwd, str):
            return None
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve User instance for a request if Basic
        Authentication is valid."""

        # Step 1: Retrieve the authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Step 2: Extract the Base64 part of the Authorization header
        base64_auth = self.extract_base64_authorization_header(auth_header)
        if base64_auth is None:
            return None

        # Step 3: Decode the Base64 authorization
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        if decoded_auth is None:
            return None

        # Step 4: Extract the user email and password from decoded credentials
        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None

        # Step 5: Retrieve the User object based on email and password
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user  # Returns the User instance or None if auth fails
