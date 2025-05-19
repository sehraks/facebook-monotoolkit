#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/fb-login.py
# Author: sehraks
# Role: Handles Facebook login and authentication operations

import os
import re
import base64
import json
import random
import string
import uuid
import requests
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.panel import Panel
from typing import Dict, Tuple, Optional

console = Console()

class FacebookLogin:
    def __init__(self):
        """Initialize FacebookLogin with necessary configurations."""
        # Get current Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        self.LAST_UPDATED = philippines_time.strftime("%B %d, %Y")
        self.CURRENT_TIME = philippines_time.strftime("%I:%M %p")
        self.CURRENT_USER = "sehraks"
        
        # API endpoints
        self.auth_url = "https://b-graph.facebook.com/auth/login"
        self.graph_url = "https://graph.facebook.com/me"
        
        # Default response timeout (seconds)
        self.timeout = 30
        
    def _generate_device_id(self) -> str:
        """Generate a random device ID."""
        return str(uuid.uuid4())

    def _generate_adid(self) -> str:
        """Generate a random advertising ID."""
        return ''.join(random.choices(string.hexdigits, k=16))

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Facebook API requests."""
        return {
            'authorization': 'OAuth 350685531728|62f8ce9f74b12f84c123cc23437a4a32',
            'x-fb-friendly-name': 'Authenticate',
            'x-fb-connection-type': 'Unknown',
            'accept-encoding': 'gzip, deflate',
            'content-type': 'application/x-www-form-urlencoded',
            'x-fb-http-engine': 'Liger',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
        }

    def get_user_info(self, token: str) -> Tuple[Optional[str], Optional[str]]:
        """Get user ID and name using access token."""
        try:
            response = requests.get(
                self.graph_url,
                params={'access_token': token},
                timeout=self.timeout
            )
            if response.status_code != 200:
                return None, None

            info = response.json()
            return info.get('id'), info.get('name')
        except Exception:
            return None, None

    def login(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate user with Facebook credentials.
        Returns: (success, message, account_data)
        """
        try:
            # First validate credentials format
            valid, message = self.validate_credentials(email, password)
            if not valid:
                return False, message, None

            # Use the b-api endpoint directly
            login_url = 'https://b-api.facebook.com/method/auth.login'
            data = {
                'adid': self._generate_adid(),
                'email': email,
                'password': password,
                'format': 'json',
                'device_id': self._generate_device_id(),
                'cpl': 'true',
                'family_device_id': self._generate_device_id(),
                'credentials_type': 'device_based_login_password',
                'generate_session_cookies': '1',
                'generate_analytics_claim': '1',
                'generate_machine_id': '1',
                'locale': 'en_US',
                'client_country_code': 'US',
                'api_key': '882a8490361da98702bf97a021ddc14d',
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32'
            }

            response = requests.post(
                login_url,
                data=data,
                headers=self._get_headers(),
                timeout=self.timeout
            )

            if response.status_code != 200:
                return False, f"Connection error (HTTP {response.status_code})", None

            result = response.json()

            if 'error_msg' in result:
                return False, f"Login failed: {result['error_msg']}", None

            access_token = result.get('access_token')
            if not access_token:
                return False, "Failed to get access token", None

            # Get user info
            user_info_url = f"https://graph.facebook.com/me?fields=id,name&access_token={access_token}"
            user_info = requests.get(user_info_url).json()

            if 'error' in user_info:
                return False, "Failed to get user information", None

            # Generate cookie string
            cookie_string = (
                f"c_user={user_info['id']}; "
                f"xs={result.get('session_cookies', [{'value': ''}])[0]['value']}; "
                f"fr={self._generate_random_cookie_value(32)}; "
                "sb=abc123; "
                "datr=xyz789; "
                "presence=EDvF3EtimeF1557226574EuserFA21B00000000000F2EstateFDutF0CEchF_7bCC"
            )

            # Create account data
            philippines_time = datetime.now(timezone(timedelta(hours=8)))
            account_data = {
                'id': base64.b64encode(os.urandom(8)).decode('utf-8')[:8],
                'name': user_info['name'],
                'user_id': user_info['id'],
                'cookie': cookie_string,
                'added_date': philippines_time.strftime('%Y-%m-%d %H:%M:%S'),
                'last_used': None,
                'status': 'active',
                'added_by': self.CURRENT_USER
            }

            return True, f"Successfully logged in as {user_info['name']}", account_data

        except requests.RequestException as e:
            return False, f"Network error: {str(e)}", None
        except json.JSONDecodeError:
            return False, "Invalid response from Facebook", None
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", None

    def _get_working_cookie(self, access_token: str) -> Tuple[Optional[str], str]:
        """Get a working cookie using the access token."""
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'en-US,en;q=0.9'
            }

            # First request to get initial cookies
            session = requests.Session()
            initial_response = session.get('https://business.facebook.com/', headers=headers, timeout=self.timeout)
            if initial_response.status_code != 200:
                return None, f"Failed to access business.facebook.com: HTTP {initial_response.status_code}"

            # Second request with access token
            params = {'access_token': access_token}
            response = session.get(
                'https://business.facebook.com/content_management',
                params=params,
                headers=headers,
                timeout=self.timeout
            )

            if response.status_code != 200:
                return None, f"Failed to get content management: HTTP {response.status_code}"

            # Get all cookies from the session
            cookies = session.cookies.get_dict()
            if not cookies:
                return None, "No cookies received from Facebook"

            # Check for required cookies
            if 'c_user' not in cookies or 'xs' not in cookies:
                return None, "Missing required cookies (c_user or xs)"

            # Format cookies into string
            cookie_parts = []
            for name, value in cookies.items():
                cookie_parts.append(f"{name}={value}")

            cookie_string = "; ".join(cookie_parts)
            return cookie_string, "Successfully obtained working cookie"

        except requests.Timeout:
            return None, "Connection timed out while getting cookies"
        except requests.RequestException as e:
            return None, f"Network error while getting cookies: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error while getting cookies: {str(e)}"

    def _generate_cookie_string(self, login_result: Dict) -> str:
        """Generate cookie string in the required format."""
        try:
            # Get current timestamp for cookie expiry
            current_time = int(datetime.now().timestamp())
            expiry_time = current_time + (30 * 24 * 60 * 60)  # 30 days from now
            timestamp_30days = current_time + (30 * 24 * 60 * 60)
            client_version = "2823"  # Updated client version

            cookies = [
                f"datr={self._generate_random_cookie_value(24)}",
                f"sb={self._generate_random_cookie_value(24)}",
                "m_pixel_ratio=3",
                "vpd=v1%3B648x360x3",
                "x-referer=eyJyIjoiL2hvbWUucGhwIiwiaCI6Ii9ob21lLnBocCIsInMiOiJtIn0%3D",
                "ps_l=1",
                "ps_n=1",
                "wd=360x820"
            ]

            # Add user-specific cookies
            if 'uid' in login_result:
                cookies.extend([
                    f"c_user={login_result['uid']}",
                    f"fr=0{self._generate_random_cookie_value(24)}.{current_time}..AAA.0.0.{timestamp_30days}.AWf8H659qoDBLQ9OxNb2vFhEXlc"
                ])

            # Add xs cookie if available
            if 'secret' in login_result:
                cookies.append(f"xs=8%3A{login_result['secret']}%3A2%3A{current_time}%3A-1%3A7867")

            # Add locale and final required cookies
            cookies.extend([
                "locale=en_US",
                f"fbl_st=101632993%3BT%3A{current_time}",
                f"wl_cbv=v2%3Bclient_version%3A{client_version}%3Btimestamp%3A{current_time}"
            ])

            return "; ".join(cookies)

        except Exception as e:
            console.print(f"[bold red]Error generating cookie string: {str(e)}[/]")
            return login_result.get('cookie_string', '')  # Fallback to basic cookie string

    def _generate_random_cookie_value(self, length: int) -> str:
        """Generate a random cookie value of specified length."""
        charset = string.ascii_letters + string.digits + '-_'
        return ''.join(random.choices(charset, k=length))

    def validate_credentials(self, email: str, password: str) -> Tuple[bool, str]:
        """Validate email/uid and password format."""
        # Email/UID validation
        email = email.strip()
        if not email:
            return False, "Email/UID cannot be empty"
        
        # Check if input is UID (all digits)
        is_uid = email.isdigit()
        
        if not is_uid:
            # Regular email validation
            if '@' not in email or '.' not in email:
                return False, "Invalid email format"
            
            # Basic email format check (username@domain.tld)
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
                return False, "Invalid email format"
        
        # Password validation
        password = password.strip()
        if not password:
            return False, "Password cannot be empty"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
            
        return True, "Credentials format valid"

    def log_login_attempt(self, email: str, success: bool, message: str) -> None:
        """Log login attempts for security tracking."""
        # Get Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        timestamp = philippines_time.strftime('%Y-%m-%d %I:%M %p')
        
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"login_attempts_{philippines_time.strftime('%Y%m')}.log")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                # Check if email is a UID (all digits)
                if email.isdigit():
                    masked_email = f"UID:{email[:2]}{'*' * (len(email) - 4)}{email[-2:]}"
                else:
                    masked_email = email[:3] + '*' * (len(email) - 6) + email[-3:]
                f.write(f"[{timestamp} GMT +8] {'UID' if email.isdigit() else 'Email'}: {masked_email} | Success: {success} | Message: {message}\n")
        except Exception as e:
            console.print(f"[bold red]Failed to log login attempt: {str(e)}[/]")

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
