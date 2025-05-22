#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/cookie_manager.py
# Author: sehraks

import json
import os
import requests
import re
import base64
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timezone, timedelta  # Added timezone and timedelta
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
                
        # Get current Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        self.LAST_UPDATED = philippines_time.strftime("%B %d, %Y")
        self.CURRENT_TIME = philippines_time.strftime("%I:%M %p")
        self.CURRENT_USER = "sehraks"
                
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
                philippines_time = datetime.now(timezone(timedelta(hours=8)))
                json.dump({
                    "cookies": [],
                    "metadata": {
                        "last_update_date": philippines_time.strftime("%B %d, %Y"),
                        "last_update_time": philippines_time.strftime("%I:%M %p +8 GMT (PH)"),
                        "updated_by": self.CURRENT_USER
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

    def save_cookies(self) -> bool:
                """Save cookies to storage file."""
                try:
                        philippines_time = datetime.now(timezone(timedelta(hours=8)))
                        data = {
                                "cookies": self.cookies,
                                "metadata": {
                                        "last_update_date": philippines_time.strftime("%B %d, %Y"),
                                        "last_update_time": philippines_time.strftime("%I:%M %p +8 GMT (PH)"),
                                        "updated_by": self.CURRENT_USER,
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

    def add_cookie(self, cookie: str, account_name: str = None, access_token: str = None) -> Tuple[bool, str]:
        """Add a new cookie to storage."""
        try:
                if cookie is None:
                        return False, "Cookie cannot be empty"
                
                cookie = cookie.strip()
                valid, message = self._validate_cookie(cookie)
                if not valid:
                        return False, message

                user_id, default_name = self._extract_user_info(cookie)
                if user_id == 'unknown':
                        return False, "Could not extract user ID from cookie"

                # Get token from cookie
                try:
                        headers = {
                                'Cookie': cookie,
                                'authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                                'x-fb-friendly-name': 'Authenticate',
                                'x-fb-connection-type': 'Unknown',
                                'accept-encoding': 'gzip, deflate',
                                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                                'accept-language': 'en-US,en;q=0.9',
                                'content-type': 'application/x-www-form-urlencoded',
                                'x-fb-http-engine': 'Liger',
                                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
                        }
                        
                        # Try multiple endpoints to get token
                        endpoints = [
                            'https://business.facebook.com/business_locations',
                            'https://www.facebook.com/adsmanager/manage/campaigns',
                            'https://developers.facebook.com/'
                        ]
                        
                        access_token = 'N/A'
                        for endpoint in endpoints:
                            try:
                                response = requests.get(endpoint, headers=headers, timeout=30)
                                if response.ok:
                                    # Look for both EAAG and EAAB tokens
                                    token = re.search(r'(EAAG\w+|EAAB\w+)', response.text)
                                    if token:
                                        access_token = token.group(0)
                                        break
                            except:
                                continue
                except:
                        access_token = 'N/A'

                # Get current PH time
                philippines_time = datetime.now(timezone(timedelta(hours=8)))
                formatted_date = philippines_time.strftime("%B %d, %Y")
                formatted_time = philippines_time.strftime("%I:%M %p +8 GMT (PH)")

                # Create or update account data
                account_data = {
                        'id': base64.b64encode(os.urandom(8)).decode('utf-8')[:8],
                        'name': account_name if account_name else default_name,
                        'user_id': user_id,
                        'cookie': cookie,
                        'token': access_token,
                        'added_date': formatted_date,
                        'added_time': formatted_time,
                        'last_used': None,
                        'status': 'active',
                        'added_by': self.CURRENT_USER
                }

                # Update existing or add new
                for idx, existing in enumerate(self.cookies):
                        if existing['user_id'] == user_id:
                                # Preserve existing token if new one not provided
                                if access_token == 'N/A' and 'token' in existing:
                                        account_data['token'] = existing['token']
                                
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

    def set_current_account(self, account_id: str) -> None:
        """Set the current account ID."""
        self.current_account_id = account_id
        self.save_cookies()

    def get_current_account(self) -> Optional[Dict]:
        """Get the currently active account."""
        try:
            with open(self.cookies_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                last_active_id = data.get("metadata", {}).get("last_active_account")
                if last_active_id:
                    for cookie in self.cookies:
                        if cookie.get('id') == last_active_id:
                            return cookie
        except Exception:
            pass
        return None if not self.cookies else self.cookies[0]

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
                        philippines_time = datetime.now(timezone(timedelta(hours=8)))
                        for account in self.cookies:
                                if account['user_id'] == user_id:
                                        account['last_used_date'] = philippines_time.strftime("%B %d, %Y")
                                        account['last_used_time'] = philippines_time.strftime("%I:%M %p +8 GMT (PH)")
                                        return self.save_cookies()
                        return False
                except Exception:
                        return False

    def format_cookie_display(self, cookie: str, token: str = None) -> Tuple[str, str]:
        """Format cookie and token strings for display (masked version)."""
        try:
            # Handle cookie masking
            if cookie and len(cookie) > 30:
                masked_cookie = cookie[:20] + "..." + cookie[-10:]
            else:
                masked_cookie = cookie if cookie else "N/A"

            # Handle token masking
            if token and len(token) > 30:
                masked_token = token[:20] + "..." + token[-10:]
            else:
                masked_token = token if token else "N/A"

            return masked_cookie, masked_token
        except Exception:
            return "Error masking cookie", "Error masking token"

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
