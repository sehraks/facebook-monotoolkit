#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/cookie_manager.py
# Last Modified: 2025-05-14 10:38:07 UTC
# Author: sehraks

import json
import os
import re
import base64
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

console = Console()

class CookieManager:
    def __init__(self):
        """Initialize the CookieManager with encryption setup."""
        self.base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cookies-storage")
        self.backup_dir = os.path.join(self.base_dir, ".backup")
        self.cookies_file = os.path.join(self.base_dir, "cookies.enc")
        self.key_file = os.path.join(self.base_dir, ".cookiekey")
        self.cookies: List[Dict] = []
        self.last_update = "2025-05-14 10:38:07"
        self.current_user = "sehraks"
        
        self._ensure_storage_exists()
        self._initialize_encryption()
        self.load_cookies()

    def _initialize_encryption(self) -> None:
        """Initialize or load encryption key."""
        if not os.path.exists(self.key_file):
            # Generate new key if none exists
            password = base64.b64encode(os.urandom(32)).decode('utf-8')
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=480000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            with open(self.key_file, 'wb') as f:
                f.write(salt + key)
            os.chmod(self.key_file, 0o600)
        
        # Load existing key
        with open(self.key_file, 'rb') as f:
            data = f.read()
            salt = data[:16]
            key = data[16:]
        
        self.cipher = Fernet(key)

    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        return self.cipher.encrypt(data.encode()).decode()

    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def _ensure_storage_exists(self) -> None:
        """Ensure the storage directory exists with proper permissions."""
        # Create main storage directory
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir, mode=0o700)
        
        # Create backup directory
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir, mode=0o700)

        if not os.path.exists(self.cookies_file):
            self._create_initial_storage()

    def _create_initial_storage(self) -> None:
        """Create initial encrypted storage file."""
        initial_data = {
            "cookies": [],
            "metadata": {
                "last_update": self.last_update,
                "updated_by": self.current_user,
                "created_at": self.last_update,
                "version": "3.51"
            }
        }
        with open(self.cookies_file, 'w', encoding='utf-8') as f:
            json.dump(initial_data, f, indent=4)
        os.chmod(self.cookies_file, 0o600)

    def create_backup(self) -> bool:
        """Create an encrypted backup of the cookies."""
        try:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(self.backup_dir, f"cookies_backup_{timestamp}.enc")
            
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'rb') as src, open(backup_file, 'wb') as dst:
                    dst.write(src.read())
                os.chmod(backup_file, 0o600)
                return True
        except Exception as e:
            console.print(Panel(
                f"[bold red]❌ Backup failed: {str(e)}[/]",
                style="bold red"
            ))
        return False

    def rotate_encryption_key(self) -> bool:
        """Rotate encryption key for security."""
        try:
            # Create backup before key rotation
            if not self.create_backup():
                return False

            # Decrypt all current cookies
            decrypted_cookies = self.cookies.copy()
            
            # Generate new key
            self._initialize_encryption()
            
            # Re-encrypt with new key
            self.cookies = decrypted_cookies
            return self.save_cookies()
        except Exception as e:
            console.print(Panel(
                f"[bold red]❌ Key rotation failed: {str(e)}[/]",
                style="bold red"
            ))
            return False

    def load_cookies(self) -> None:
        """Load and decrypt cookies from storage file."""
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "cookies" in data:
                        # Decrypt all cookies
                        decrypted_cookies = []
                        for account in data["cookies"]:
                            try:
                                decrypted_account = account.copy()
                                decrypted_account['cookie'] = self._decrypt_data(account['cookie'])
                                decrypted_cookies.append(decrypted_account)
                            except Exception as e:
                                console.print(Panel(
                                    f"[bold red]❌ Error decrypting cookie for {account.get('name', 'unknown')}: {str(e)}[/]",
                                    style="bold red"
                                ))
                        self.cookies = decrypted_cookies
                    else:
                        self.cookies = []
        except Exception as e:
            console.print(Panel(
                f"[bold red]❌ Error loading cookies: {str(e)}[/]",
                style="bold red"
            ))
            self.cookies = []
            self._attempt_recovery()

    def _attempt_recovery(self) -> bool:
        """Attempt to recover from storage corruption."""
        try:
            backup_files = sorted([f for f in os.listdir(self.backup_dir) if f.startswith("cookies_backup_")])
            if not backup_files:
                return False

            latest_backup = os.path.join(self.backup_dir, backup_files[-1])
            with open(latest_backup, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and "cookies" in data:
                    self.cookies = data["cookies"]
                    return self.save_cookies()
        except Exception:
            return False
        return False

    def save_cookies(self) -> bool:
        """Encrypt and save cookies to storage file."""
        try:
            # Create backup before saving
            self.create_backup()

            # Encrypt all cookies before saving
            encrypted_cookies = []
            for account in self.cookies:
                encrypted_account = account.copy()
                encrypted_account['cookie'] = self._encrypt_data(account['cookie'])
                encrypted_cookies.append(encrypted_account)

            data = {
                "cookies": encrypted_cookies,
                "metadata": {
                    "last_update": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_by": self.current_user,
                    "version": "3.51"
                }
            }

            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            os.chmod(self.cookies_file, 0o600)
            return True
        except Exception as e:
            console.print(Panel(
                f"[bold red]❌ Error saving cookies: {str(e)}[/]",
                style="bold red"
            ))
            return False

    def _extract_user_info(self, cookie_str: str) -> Tuple[str, str]:
        """Extract user ID and name from cookie string."""
        c_user_match = re.search(r'c_user=(\d+)', cookie_str)
        if not c_user_match:
            return 'unknown', 'Unknown_User'
        
        user_id = c_user_match.group(1)
        name = f"Facebook_{user_id}"
        return user_id, name

    def _validate_cookie(self, cookie_str: str) -> Tuple[bool, str]:
        """Validate cookie string contains required fields."""
        if not cookie_str or not isinstance(cookie_str, str):
            return False, "Invalid cookie format"

        required_fields = ['c_user', 'xs', 'datr', 'sb']
        missing_fields = [field for field in required_fields if field not in cookie_str]
        if missing_fields:
            return False, f"Missing required cookie fields: {', '.join(missing_fields)}"
            
        c_user_match = re.search(r'c_user=(\d+)', cookie_str)
        if not c_user_match or not c_user_match.group(1).isdigit():
            return False, "Invalid c_user value"

        if len(cookie_str) < 100:
            return False, "Cookie appears too short to be valid"

        return True, "Cookie validation successful"

    def has_cookies(self) -> bool:
        """Check if there are any stored cookies."""
        return len(self.cookies) > 0

    def get_all_accounts(self) -> List[Dict]:
        """Get all stored accounts."""
        return self.cookies

    def remove_cookie(self, account: Dict) -> bool:
        """Remove a cookie from storage."""
        try:
            self.cookies = [c for c in self.cookies if c['id'] != account['id']]
            return self.save_cookies()
        except Exception as e:
            console.print(Panel(
                f"[bold red]❌ Error removing cookie: {str(e)}[/]",
                style="bold red"
            ))
            return False

    def add_cookie(self, cookie: str) -> Tuple[bool, str]:
        """Add a new cookie to encrypted storage."""
        try:
            cookie = cookie.strip()
            valid, message = self._validate_cookie(cookie)
            if not valid:
                return False, message

            user_id, name = self._extract_user_info(cookie)
            if user_id == 'unknown':
                return False, "Could not extract user ID from cookie"

            account_data = {
                'id': base64.b64encode(os.urandom(8)).decode('utf-8')[:8],
                'name': name,
                'user_id': user_id,
                'cookie': cookie,
                'added_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'last_used': None,
                'status': 'active',
                'added_by': self.current_user
            }

            # Check for existing account
            for idx, existing in enumerate(self.cookies):
                if existing['user_id'] == user_id:
                    self.cookies[idx] = account_data
                    if self.save_cookies():
                        return True, f"Updated existing account: {name}"
                    return False, "Failed to save cookie data"

            # Add new account
            self.cookies.append(account_data)
            if self.save_cookies():
                return True, f"Added new account: {name}"
            return False, "Failed to save cookie data"

        except Exception as e:
            return False, f"Error adding cookie: {str(e)}"

    def update_cookie_status(self, account: Dict, status: str) -> bool:
        """Update cookie status and last used timestamp."""
        try:
            for cookie in self.cookies:
                if cookie['id'] == account['id']:
                    cookie['status'] = status
                    cookie['last_used'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    return self.save_cookies()
            return False
        except Exception as e:
            console.print(Panel(
                f"[bold red]❌ Error updating cookie status: {str(e)}[/]",
                style="bold red"
            ))
            return False
