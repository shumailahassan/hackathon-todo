import re
from typing import Optional


def is_valid_email(email: str) -> bool:
    """
    Validate email format according to standard email format requirements.
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None


def validate_email_format(email: str) -> tuple[bool, str]:
    """
    Validate email format and return (is_valid, error_message).
    """
    if not email:
        return False, "Email is required"

    if not is_valid_email(email):
        return False, "Invalid email format"

    if len(email) > 254:  # RFC 5321 limit
        return False, "Email is too long"

    return True, ""


def is_valid_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength according to security requirements.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"

    if not any(not c.isalnum() for c in password):
        return False, "Password must contain at least one special character"

    return True, ""


def is_valid_name(name: str) -> tuple[bool, str]:
    """
    Validate name format and return (is_valid, error_message).
    """
    if not name:
        return False, "Name is required"

    if len(name) > 100:
        return False, "Name is too long (max 100 characters)"

    if len(name.strip()) == 0:
        return False, "Name cannot be empty or whitespace only"

    return True, ""