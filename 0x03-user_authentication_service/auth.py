#!/usr/bin/python3
""" module for hashing the password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """saltes and hashes a given password string"""
    passw = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passw, salt)
    return hashed
