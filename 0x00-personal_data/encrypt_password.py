#!/usr/bin/env python3
"""
This module provides a function to hash passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt."""
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed
