#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/cookie_manager.py
# Last Modified: 2025-05-13 16:01:51 UTC
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
        self.last_update = "2025-05-13 16:01:51"  # Current UTC time
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
            console.print(Panel(
                f"[bold red]❌ Error loading cookies: {str(e)}[/]",
                style="bold red"
            ))
            self.cookies = []

    def save_cookies(self) -> bool:
        """Save cookies to storage file."""
        try:
            data = {
                "cookies": self.cookies,
                "metadata": {
                    "last_update": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    "updated_by": self.current_user
                }
            }
            with open(self.cookies_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
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

        # Check for c_user presence
        if "c_user=" not in cookie_str:
            return False, "Invalid cookie: missing c_user"
            
        # Check for xs presence
        if "xs=" not in cookie_str:
            return False, "Invalid cookie: missing xs"

        # Extract and validate c_user value
        c_user_match = re.search(r'c_user=(\d+)', cookie_str)
        if not c_user_match or not c_user_match.group(1).isdigit():
            return False, "Invalid c_user value"

        return True, "Cookie validation successful"

    def add_cookie(self, cookie: str) -> Tuple[bool, str]:
        """Add a new cookie to storage."""
        try:
            # Basic validation
            cookie = cookie.strip()
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
                'cookie': cookie,
                'added_date': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'last_used': None,
                'status': 'active',
                'added_by': self.current_user
            }

            # Update existing or add new
            for idx, existing in enumerate(self.cookies):
                if existing['user_id'] == user_id:
                    self.cookies[idx] = account_data
                    if self.save_cookies():
                        console.print(Panel(
                            f"[bold green]✅ Updated existing account: {name}[/]",
                            style="bold green"
                        ))
                        return True, f"Updated existing account: {name}"
                    return False, "Failed to save cookie data"

            self.cookies.append(account_data)
            if self.save_cookies():
                console.print(Panel(
                    f"[bold green]✅ Added new account: {name}[/]",
                    style="bold green"
                ))
                return True, f"Added new account: {name}"
            return False, "Failed to save cookie data"

        except Exception as e:
            return False, f"Error adding cookie: {str(e)}"

    # ... [Previous methods remain the same, just add rich styling to their console outputs]

    def validate_all_cookies(self) -> List[Dict]:
        """Validate all stored cookies and return status report."""
        status_report = []
        table = Table(title="Cookie Validation Report")
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
