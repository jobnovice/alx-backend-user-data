#!/usr/bin/env python3
""" created a new module to handle authentication for our app"""
from flask import request
from typing import List, TypeVar


class Auth:
    """new class implemented for authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None or not excluded_paths:
            return True

        path = path.rstrip('/')
        for excluded in excluded_paths:
            excluded = excluded.rstrip('/')
            if path == excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """that returns None"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
