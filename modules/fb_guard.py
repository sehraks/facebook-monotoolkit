#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/fb_guard.py

import json
import uuid
import requests
import time
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.panel import Panel
from typing import Dict, Tuple, Optional

console = Console()

class FacebookGuard:
    def __init__(self):
        """Initialize FacebookGuard with necessary configurations."""
        # Get current Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        self.last_update = philippines_time.strftime("%Y-%m-%d %H:%M:%S")
        self.current_user = "sehraks"

    def _check_profile_lock_status(self, token: str) -> Tuple[bool, str]:
        """Check if the profile is locked."""
        try:
            headers = {'Authorization': f'OAuth {token}'}
            response = requests.get(
                'https://graph.facebook.com/me?fields=is_profile_locked',
                headers=headers
            )
            data = response.json()
            
            if 'is_profile_locked' in data:
                return data['is_profile_locked'], ""
            return False, "Could not determine profile lock status"
            
        except Exception as e:
            return False, f"Error checking profile lock status: {str(e)}"

    def _check_shield_status(self, token: str, uid: str) -> Tuple[bool, str]:
        """Check if profile shield is active."""
        try:
            data = {
                'variables': json.dumps({
                    '0': {
                        'actor_id': uid,
                        'client_mutation_id': str(uuid.uuid4())
                    }
                }),
                'doc_id': '1477043292367183'
            }
            headers = {'Authorization': f'OAuth {token}'}
            
            response = requests.post(
                'https://graph.facebook.com/graphql',
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                return 'is_shielded\":true' in response.text, ""
            return False, f"Error: HTTP {response.status_code}"
            
        except Exception as e:
            return False, f"Error checking shield status: {str(e)}"

    def toggle_profile_shield(self, account: Dict, enable: bool = True) -> Tuple[bool, str]:
        """Toggle Facebook profile shield."""
        try:
            # Initial status message
            console.print(Panel(
                "[bold white]🔄 Initializing Profile Shield operation...[/]",
                style="bold cyan",
                border_style="cyan"
            ))
            time.sleep(1)

            token = account.get('token')
            if not token or token == 'N/A':
                return False, "No valid token found for this account"

            # Check profile lock status
            console.print(Panel(
                "[bold white]🔄 Checking profile lock status...[/]",
                style="bold cyan",
                border_style="cyan"
            ))
            time.sleep(1)

            is_locked, lock_error = self._check_profile_lock_status(token)
            if is_locked:
                return False, "Profile is locked. Please unlock your profile first"
            elif lock_error:
                return False, lock_error

            # Check current shield status
            console.print(Panel(
                "[bold white]🔄 Checking current shield status...[/]",
                style="bold cyan",
                border_style="cyan"
            ))
            time.sleep(1)

            is_shielded, shield_error = self._check_shield_status(token, account['user_id'])
            if shield_error:
                return False, shield_error

            if enable and is_shielded:
                return False, "Your Facebook Profile Shield was already activated"
            elif not enable and not is_shielded:
                return False, "Your Facebook Profile Shield is not active"

            # Toggle shield
            console.print(Panel(
                f"[bold white]🔄 {'Activating' if enable else 'Deactivating'} Profile Shield...[/]",
                style="bold cyan",
                border_style="cyan"
            ))
            time.sleep(1)

            data = {
                'variables': json.dumps({
                    '0': {
                        'is_shielded': enable,
                        'session_id': str(uuid.uuid4()),
                        'actor_id': account['user_id'],
                        'client_mutation_id': str(uuid.uuid4())
                    }
                }),
                'method': 'post',
                'doc_id': '1477043292367183'
            }
            
            headers = {'Authorization': f"OAuth {token}"}
            response = requests.post(
                'https://graph.facebook.com/graphql',
                json=data,
                headers=headers
            )

            if response.status_code != 200:
                return False, f"Request failed: {response.text}"

            success_check = 'is_shielded\":true' if enable else 'is_shielded\":false'
            if success_check in response.text:
                action = "turned on" if enable else "turned off"
                return True, f"You {action} your Facebook Profile Shield"
            
            return False, "Unexpected response from Facebook"

        except Exception as e:
            return False, f"Error: {str(e)}"
