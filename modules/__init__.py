"""
Facebook MonoToolkit Package
--------------------------
This package contains modules for Facebook automation tasks including:
- Cookie management
- Spam sharing functionality
- Utility functions
"""

from .cookie_manager import CookieManager
from .spam_sharing import SpamSharing
from .utils import clear_screen, validate_input

__version__ = "1.0.0"
__author__ = "sehraks"
__all__ = [
    'CookieManager',
    'SpamSharing',
    'clear_screen',
    'validate_input'
]
