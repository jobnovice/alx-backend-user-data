#!/usr/bin/env python3
""" module for hashing the password"""
import bcrypt
from db import DB
from user import User
from typing import Optional
import uuid


def _hash_password(password: str) -> bytes:
    """saltes and hashes a given password string"""
    passw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passw, salt)
    return hashed


def _generate_uuid() -> str:
    """generating unique user id """
    u_id = str(uuid.uuid4())
    return u_id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user by first checking it exists or not"""
        user = self._db.find_user_by(email=email)
        if user:
            raise ValueError(f"User ${email} already exists.")
        else:
            ne_user = self._db.add_user(email, _hash_password(password))
            return ne_user

    def valid_login(self, email: str, password: str) -> bool:
        """vallidates user using it's credentials"""
        user = self._db.find_user_by(email=email)
        if user:
            passw = password.encode('utf-8')
            if bcrypt.checkpw(passw, user.hashed_password):
                return True
            else:
                return False
        else:
            return False

    def create_session(self, email: str) -> str:
        """creates a sessionId for a prticular user and returns the Id"""
        try:
            user = self._db.find_user_by(email=email)
            u_id = _generate_uuid()
            user.session_id = u_id
        except Exception as e:
            return None
        return u_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """find user by the session Id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception as e:
            return None
        return user
