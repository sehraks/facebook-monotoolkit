# modules/__init__.py

from .utils import Utils
from .cookie_manager import CookieManager
from .spam_sharing import SpamSharing

# Create convenience functions if needed
def clear_screen():
    return Utils.clear_screen()

def validate_input(*args, **kwargs):
    return Utils.validate_input(*args, **kwargs)

# Export the classes and functions
__all__ = ['Utils', 'CookieManager', 'SpamSharing', 'clear_screen', 'validate_input']
