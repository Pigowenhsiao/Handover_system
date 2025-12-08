"""
Compatibility wrapper for authentication utilities.
Delegates to backend.core.security so existing imports continue to work.
"""
from backend.core.security import get_password_hash, verify_password, create_access_token, verify_token  # noqa: F401

__all__ = ["get_password_hash", "verify_password", "create_access_token", "verify_token"]
