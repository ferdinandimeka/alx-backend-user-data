#!/usr/bin/env python3
"""Hash password module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
