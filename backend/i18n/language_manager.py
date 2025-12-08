"""
Compatibility wrapper for language manager.
Re-exports LanguageManager from backend.core.language_manager.
"""
from backend.core.language_manager import LanguageManager  # noqa: F401

__all__ = ["LanguageManager"]
