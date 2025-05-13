import json
import os
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import base64

class CookieManager:
    def __init__(self):
        """Initialize the CookieManager with necessary file paths and data structures."""
        self.base_dir = "cookies-storage"
        self.cookies_file = os.path.join(self.base_dir, "cookies.json")
        self.cookies: List[Dict] = []
        self._ensure_storage_exists()
        self.load_cookies()

    def _ensure_storage_exists(self) -> None:
        """Ensure the storage directory exists."""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
        if not os.path.exists(self.cookies_file):
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def load_cookies(self) -> None:
        """Load cookies from storage file."""
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'r', encoding='utf-8') as f:
                    self.cookies = json.load(f)
        except Exception as e:
            print(f"Error loading cookies: {str(e)}")
            self.cookies = []

    def save_cookies(self) -> bool:
        """Save cookies to storage file."""
        try:
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(self.cookies, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving cookies: {str(e)}")
            return False

    def _extract_user_info(self, cookie_str: str) -> Tuple[str, str]:
        """Extract user ID and name from cookie string."""
        try:
            # Extract c_user value using regex
            c_user_match = re.search(r'c_user=(\d+)', cookie_str)
            if not c_user_match:
                return 'unknown', 'Unknown_User'
            
            user_id = c_user_match.group(1)
            name = f"Facebook_{user_id[:6]}..." if len(user_id) > 6 else f"Facebook_{user_id}"
            return user_id, name
        except Exception:
            return 'unknown', 'Unknown_User'

    def _validate_cookie(self, cookie_str: str) -> Tuple[bool, str]:
        """Validate cookie string contains required fields."""
        if not cookie_str or not isinstance(cookie_str, str):
            return False, "Invalid cookie format"

        required_fields = ['c_user=', 'xs=']
        missing_fields = [field for field in required_fields if field not in cookie_str]
        
        if missing_fields:
            return False, f"Missing required cookie fields: {', '.join(f.rstrip('=') for f in missing_fields)}"

        # Check for c_user value
        c_user_match = re.search(r'c_user=(\d+)', cookie_str)
        if not c_user_match or not c_user_match.group(1).isdigit():
            return False, "Invalid c_user value"

        return True, "Cookie validation successful"

    def add_cookie(self, cookie: str) -> Tuple[bool, str]:
        """Add a new cookie to storage."""
        try:
            # Validate cookie format and required fields
            valid, message = self._validate_cookie(cookie)
            if not valid:
                return False, message

            # Extract user info
            user_id, name = self._extract_user_info(cookie)
            if user_id == 'unknown':
                return False, "Could not extract user ID from cookie"

            # Prepare account data
            account_data = {
                'id': base64.b64encode(os.urandom(8)).decode('utf-8')[:8],
                'name': name,
                'user_id': user_id,
                'cookie': cookie.strip(),
                'added_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'last_used': None,
                'status': 'active'
            }

            # Update existing or add new
            for idx, existing in enumerate(self.cookies):
                if existing['user_id'] == user_id:
                    self.cookies[idx] = account_data
                    if self.save_cookies():
                        return True, f"Updated existing account: {name}"
                    return False, "Failed to save cookie data"

            self.cookies.append(account_data)
            if self.save_cookies():
                return True, f"Added new account: {name}"
            return False, "Failed to save cookie data"

        except Exception as e:
            return False, f"Error adding cookie: {str(e)}"

    def remove_cookie(self, user_id: str) -> Tuple[bool, str]:
        """Remove a cookie from storage."""
        for idx, account in enumerate(self.cookies):
            if account['user_id'] == user_id:
                del self.cookies[idx]
                self.save_cookies()
                return True, f"Removed account with user ID: {user_id}"
        return False, f"Account with user ID {user_id} not found"

    def get_cookie(self, user_id: str) -> Optional[Dict]:
        """Get a specific cookie by user ID."""
        for account in self.cookies:
            if account['user_id'] == user_id:
                return account
        return None

    def update_last_used(self, user_id: str) -> bool:
        """Update the last used timestamp for a cookie."""
        for account in self.cookies:
            if account['user_id'] == user_id:
                account['last_used'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                self.save_cookies()
                return True
        return False

    def has_cookies(self) -> bool:
        """Check if there are any stored cookies."""
        return len(self.cookies) > 0

    def get_all_accounts(self) -> List[Dict]:
        """Get list of all stored accounts."""
        return sorted(self.cookies, key=lambda x: x.get('last_used', ''), reverse=True)

    def get_active_accounts(self) -> List[Dict]:
        """Get list of active accounts."""
        return [acc for acc in self.cookies if acc.get('status') == 'active']

    def format_cookie_display(self, cookie: str) -> str:
        """Format cookie string for display (masked version)."""
        return cookie[:20] + "..." + cookie[-10:] if len(cookie) > 30 else cookie

    def export_cookies(self, export_path: str) -> Tuple[bool, str]:
        """Export cookies to a file."""
        try:
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(self.cookies, f, indent=4)
            return True, f"Successfully exported cookies to {export_path}"
        except Exception as e:
            return False, f"Failed to export cookies: {str(e)}"

    def import_cookies(self, import_path: str) -> Tuple[bool, str]:
        """Import cookies from a file."""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                imported_cookies = json.load(f)
            
            if not isinstance(imported_cookies, list):
                return False, "Invalid import file format"

            success_count = 0
            for cookie_data in imported_cookies:
                if 'cookie' in cookie_data:
                    success, _ = self.add_cookie(cookie_data['cookie'])
                    if success:
                        success_count += 1

            return True, f"Successfully imported {success_count} cookies"
        except Exception as e:
            return False, f"Failed to import cookies: {str(e)}"

    def clear_cookies(self) -> Tuple[bool, str]:
        """Clear all stored cookies."""
        try:
            self.cookies = []
            self.save_cookies()
            return True, "Successfully cleared all cookies"
        except Exception as e:
            return False, f"Failed to clear cookies: {str(e)}"

    def validate_all_cookies(self) -> List[Dict]:
        """Validate all stored cookies and return status report."""
        status_report = []
        for account in self.cookies:
            valid, message = self._validate_cookie(account['cookie'])
            status_report.append({
                'user_id': account['user_id'],
                'name': account['name'],
                'valid': valid,
                'message': message
            })
        return status_report

    def get_cookie_info(self, cookie: str) -> Dict:
        """Extract and return detailed information about a cookie."""
        valid, message = self._validate_cookie(cookie)
        if not valid:
            return {'error': message}

        user_id, _ = self._extract_user_info(cookie)
        return {
            'user_id': user_id,
            'creation_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'cookie_length': len(cookie),
            'has_required_fields': valid,
            'validation_message': message
        }
