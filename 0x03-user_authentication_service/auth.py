#!/usr/bin/env python3
""" module for hashing the password"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """saltes and hashes a given password string"""
    passw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passw, salt)
    return hashed


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
