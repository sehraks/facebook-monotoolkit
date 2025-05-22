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
        """Check if the profile is locked using alternative methods."""
        try:
            # First attempt: Check using profile information
            headers = {
                'Authorization': f'OAuth {token}',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
            }
            
            # Try multiple endpoints to verify lock status
            endpoints = [
                ('https://graph.facebook.com/v18.0/me?fields=id,name,profile_status,is_profile_locked', 'profile_status'),
                ('https://graph.facebook.com/graphql', 'timeline_lock_state'),
                ('https://www.facebook.com/api/graphql/', 'profile_lock_state')
            ]

            for url, field in endpoints:
                try:
                    if 'graphql' in url:
                        # For GraphQL endpoints
                        data = {
                            'variables': json.dumps({
                                'profileID': token.split('|')[0] if '|' in token else None
                            }),
                            'doc_id': '1477043292367183'
                        }
                        response = requests.post(url, headers=headers, json=data, timeout=10)
                    else:
                        # For REST endpoints
                        response = requests.get(url, headers=headers, timeout=10)

                    if response.status_code == 200:
                        data = response.json()
                        
                        # Check various possible response formats
                        if 'is_profile_locked' in str(data):
                            return data.get('is_profile_locked', False), ""
                        elif field in str(data):
                            return 'LOCKED' in str(data).upper(), ""
                        elif 'error' in data:
                            if 'locked' in str(data['error']).lower():
                                return True, ""

                except Exception:
                    continue

            # If we reach here, try one last method using the user's timeline
            try:
                user_id = token.split('|')[0] if '|' in token else None
                if user_id:
                    timeline_url = f'https://graph.facebook.com/{user_id}/feed'
                    response = requests.get(timeline_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        return False, ""  # If we can access the feed, profile is not locked
                    elif 'locked' in response.text.lower():
                        return True, ""
            except Exception:
                pass

            # If all checks pass without finding a lock, assume it's not locked
            return False, ""

        except Exception as e:
            return False, f"Error checking profile lock status: {str(e)}"

    def _check_shield_status(self, token: str, uid: str) -> Tuple[bool, str]:
        """Check if profile shield is active."""
        try:
            # Improved data payload for checking shield status
            data = {
                'variables': json.dumps({
                    '0': {
                        'is_shielded': True,
                        'actor_id': uid,
                        'client_mutation_id': str(uuid.uuid4())
                    }
                }),
                'doc_id': '1477043292367183',
                'method': 'post'
            }
            
            headers = {
                'Authorization': f'OAuth {token}',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'Content-Type': 'application/json',
                'Accept': '*/*'
            }
            
            # First try: Direct GraphQL query
            response = requests.post(
                'https://graph.facebook.com/graphql',
                json=data,
                headers=headers
            )
            
            if response.status_code == 200:
                response_text = response.text
                
                # Multiple checks for shield status
                shield_indicators = [
                    'is_shielded\":true',
                    'shield_enabled\":true',
                    'profile_picture_shield\":true',
                    'profile_shield_status\":\"enabled'
                ]
                
                for indicator in shield_indicators:
                    if indicator in response_text.lower():
                        return True, ""
                
                # If response is good but no shield indicators found
                if 'is_shielded\":false' in response_text:
                    return False, ""
                
                # Try parsing the full response
                try:
                    json_response = response.json()
                    if isinstance(json_response, dict):
                        # Check nested data structure
                        if 'data' in json_response:
                            data = json_response['data']
                            if isinstance(data, dict):
                                for key, value in data.items():
                                    if isinstance(value, dict) and 'is_shielded' in value:
                                        return value['is_shielded'], ""
                except:
                    pass
                
                # Fallback: Check profile endpoint
                profile_response = requests.get(
                    f'https://graph.facebook.com/{uid}?fields=protection_status&access_token={token}',
                    headers=headers
                )
                
                if profile_response.status_code == 200:
                    profile_data = profile_response.json()
                    if 'protection_status' in profile_data:
                        return profile_data['protection_status'] in ['enabled', 'active', True], ""
            
            return False, f"Could not determine shield status"
            
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
