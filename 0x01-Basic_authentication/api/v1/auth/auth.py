#!/usr/bin/env python3
""" created a new module to handle authentication for our app"""
from flask import request
from typing import List, TypeVar


class Auth:
    """new class implemented for authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path always ends with a '/'
        path = path + '/' if not path.endswith('/') else path

        for excluded_path in excluded_paths:
            # Ensure excluded path ends with '/'
            normalized_excluded = excluded_path
            if not excluded_path.endswith('/'):
                normalized_excluded += '/'

            # Check if excluded_path has a wildcard "*"
            if '*' in normalized_excluded:
                if path.startswith(normalized_excluded[:-1]):
                    return False
            elif path == normalized_excluded:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """that returns None"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
