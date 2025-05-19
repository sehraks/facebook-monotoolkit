#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/cookie_manager.py
# Last Modified: 2025-05-15 05:14:02 UTC
# Author: sehraks

import json
import os
import re
import base64
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class CookieManager:
    def __init__(self):
        """Initialize the CookieManager with necessary file paths and data structures."""
        self.base_dir = "cookies-storage"
        self.cookies_file = os.path.join(self.base_dir, "cookies.json")
        self.cookies: List[Dict] = []
        self.last_update = "2025-05-15 05:14:02"  # Current UTC time
        self.current_user = "sehraks"  # Current user's login
        self._ensure_storage_exists()
        self.load_cookies()

    def _ensure_storage_exists(self) -> None:
        """Ensure the storage directory exists."""
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
            console.print(Panel(
                "[bold green]✅ Created storage directory[/]",
                style="bold green"
            ))

        if not os.path.exists(self.cookies_file):
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "cookies": [],
                    "metadata": {
                        "last_update": self.last_update,
                        "updated_by": self.current_user
                    }
                }, f, indent=4)
            console.print(Panel(
                "[bold green]✅ Initialized cookies storage file[/]",
                style="bold green"
            ))

    def load_cookies(self) -> None:
        """Load cookies from storage file."""
        try:
            if os.path.exists(self.cookies_file):
                with open(self.cookies_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "cookies" in data:
                        self.cookies = data["cookies"]
                    else:
                        self.cookies = data if isinstance(data, list) else []
        except Exception as e:
            self.cookies = []
            return False

    def save_cookies(self) -> bool:
        """Save cookies to storage file."""
        try:
            data = {
                "cookies": self.cookies,
                "metadata": {
                    "last_update": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_by": self.current_user,
                    "last_active_account": self.current_account_id if hasattr(self, 'current_account_id') else None
                }
            }
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False

    def _extract_user_info(self, cookie_str: str) -> Tuple[str, str]:
        """Extract user ID and name from cookie string."""
        c_user_match = re.search(r'c_user=(\d+)', cookie_str)
        if not c_user_match:
            return 'unknown', 'Unknown User'
        
        user_id = c_user_match.group(1)
        
        # Try to extract name from cookie if available
        name_match = re.search(r'name=([^;]+)', cookie_str)
        name = name_match.group(1) if name_match else f"Facebook_{user_id}"
        
        return user_id, name

    def _validate_cookie(self, cookie_str: str) -> Tuple[bool, str]:
        """Validate cookie string contains required fields."""
        if not cookie_str or not isinstance(cookie_str, str):
            return False, "Invalid cookie format"

        if "c_user=" not in cookie_str:
            return False, "Invalid cookie: missing c_user"
            
        if "xs=" not in cookie_str:
            return False, "Invalid cookie: missing xs"

        c_user_match = re.search(r'c_user=(\d+)', cookie_str)
        if not c_user_match or not c_user_match.group(1).isdigit():
            return False, "Invalid c_user value"

        return True, "Cookie validation successful"

    def has_cookies(self) -> bool:
        """Check if there are any stored cookies."""
        try:
            return bool(self.cookies)
        except Exception:
            return False

    def add_cookie(self, cookie: str, account_name: str = None) -> Tuple[bool, str]:
        """Add a new cookie to storage."""
        try:
            cookie = cookie.strip()
            valid, message = self._validate_cookie(cookie)
            if not valid:
                return False, message

            user_id, default_name = self._extract_user_info(cookie)
            if user_id == 'unknown':
                return False, "Could not extract user ID from cookie"

            # Create or update account data
            account_data = {
                'id': base64.b64encode(os.urandom(8)).decode('utf-8')[:8],
                'name': account_name if account_name else default_name,
                'user_id': user_id,
                'cookie': cookie,
                'added_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'last_used': None,
                'status': 'active',
                'added_by': self.current_user
            }

            # Update existing or add new
            for idx, existing in enumerate(self.cookies):
                if existing['user_id'] == user_id:
                    # Always preserve the existing name unless explicitly provided
                    if not account_name and 'name' in existing:
                        account_data['name'] = existing['name']
                    self.cookies[idx] = account_data
                    if self.save_cookies():
                        return True, f"Updated existing account: {account_data['name']}"
                    return False, "Failed to save cookie data"

            self.cookies.append(account_data)
            if self.save_cookies():
                return True, f"Added new account: {account_data['name']}"
            return False, "Failed to save cookie data"

        except Exception as e:
            return False, f"Error adding cookie: {str(e)}"

    def get_all_accounts(self) -> List[Dict]:
        """Get list of all stored accounts."""
        try:
            return self.cookies
        except Exception:
            return []

    def get_active_accounts(self) -> List[Dict]:
        """Get list of active accounts."""
        try:
            return [acc for acc in self.cookies if acc.get('status') == 'active']
        except Exception:
            return []

    def remove_cookie(self, account: Dict) -> bool:
        """Remove a cookie from storage."""
        try:
            self.cookies = [c for c in self.cookies if c['id'] != account['id']]
            return self.save_cookies()
        except Exception:
            return False

    def get_cookie(self, user_id: str) -> Optional[Dict]:
        """Get a specific cookie by user ID."""
        try:
            for account in self.cookies:
                if account['user_id'] == user_id:
                    return account
            return None
        except Exception:
            return None

    def update_last_used(self, user_id: str) -> bool:
        """Update the last used timestamp for a cookie."""
        try:
            for account in self.cookies:
                if account['user_id'] == user_id:
                    account['last_used'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                    return self.save_cookies()
            return False
        except Exception:
            return False

    def format_cookie_display(self, cookie: str) -> str:
        """Format cookie string for display (masked version)."""
        if len(cookie) > 30:
            return cookie[:20] + "..." + cookie[-10:]
        return cookie

    def validate_all_cookies(self) -> List[Dict]:
        """Validate all stored cookies and return status report."""
        try:
            status_report = []
            table = Table(
                title="[bold cyan] Cookie Validation Report[/]",
                show_header=True,
                header_style="bold magenta"
            )
            
            table.add_column("User ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Status", style="magenta")
            table.add_column("Message", style="yellow")
            
            for account in self.cookies:
                valid, message = self._validate_cookie(account['cookie'])
                status = "✅ Valid" if valid else "❌ Invalid"
                
                table.add_row(
                    account['user_id'],
                    account['name'],
                    status,
                    message
                )
                
                status_report.append({
                    'user_id': account['user_id'],
                    'name': account['name'],
                    'valid': valid,
                    'message': message,
                    'last_validated': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                })
            
            console.print(table)
            return status_report
        except Exception:
            return []

    def get_cookie_info(self, cookie: str) -> Dict:
        """Extract and return detailed information about a cookie."""
        try:
            valid, message = self._validate_cookie(cookie)
            if not valid:
                return {'error': message}

            user_id, _ = self._extract_user_info(cookie)
            return {
                'user_id': user_id,
                'creation_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'cookie_length': len(cookie),
                'has_required_fields': valid,
                'validation_message': message,
                'checked_by': self.current_user
            }
        except Exception as e:
            return {'error': str(e)}
