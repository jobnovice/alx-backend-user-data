#!/usr/bin/env python3
""" created a new module to handle authentication for our app"""
from flask import request
from typing import List, TypeVar


class Auth:
    """new class implemented for authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        return False

    def authorization_header(self, request=None) -> str:
        """that returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
