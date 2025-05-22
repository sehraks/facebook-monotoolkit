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

    def _check_shield_status(self, token: str, uid: str) -> Tuple[Optional[bool], str]:
        """Check if profile shield is active using the correct Facebook endpoint."""
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            console.print("[bold yellow]→ Checking Profile Guard status via Facebook API...[/]")
            
            # Method 1: Use Facebook's actual profile guard endpoint
            try:
                # This is the correct endpoint for checking profile picture guard
                guard_url = f'https://graph.facebook.com/v18.0/me?fields=profile_picture_guard'
                response = requests.get(guard_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[blue]Profile Guard API Response: {data}[/]")
                    
                    if 'profile_picture_guard' in data:
                        is_protected = data['profile_picture_guard']
                        if is_protected:
                            console.print("[green]✓ Profile Guard API: Shield is ON[/]")
                            return True, ""
                        else:
                            console.print("[green]✓ Profile Guard API: Shield is OFF[/]")
                            return False, ""
                else:
                    console.print(f"[red]✗ Profile Guard API failed: Status {response.status_code}[/]")
                    
            except Exception as e:
                console.print(f"[red]✗ Profile Guard API error: {str(e)}[/]")
            
            # Method 2: Check using GraphQL with the correct query
            try:
                console.print("[bold yellow]→ Checking via GraphQL query...[/]")
                
                graphql_payload = {
                    'variables': json.dumps({
                        'scale': 1,
                        'id': uid
                    }),
                    'doc_id': '25497947053478820'  # This is Facebook's doc_id for profile guard queries
                }
                
                graphql_response = requests.post(
                    'https://graph.facebook.com/graphql',
                    data=graphql_payload,
                    headers=headers,
                    timeout=15
                )
                
                if graphql_response.status_code == 200:
                    response_text = graphql_response.text
                    console.print(f"[blue]GraphQL Response (first 300 chars): {response_text[:300]}...[/]")
                    
                    # Look for the actual shield status in the response
                    if 'profile_picture_guard' in response_text.lower():
                        if '"profile_picture_guard":true' in response_text.lower():
                            console.print("[green]✓ GraphQL: Shield is ON[/]")
                            return True, ""
                        elif '"profile_picture_guard":false' in response_text.lower():
                            console.print("[green]✓ GraphQL: Shield is OFF[/]")
                            return False, ""
                    
                    # Alternative patterns to look for
                    if 'is_profile_picture_guarded":true' in response_text.lower():
                        console.print("[green]✓ GraphQL: Shield is ON (alternative pattern)[/]")
                        return True, ""
                    elif 'is_profile_picture_guarded":false' in response_text.lower():
                        console.print("[green]✓ GraphQL: Shield is OFF (alternative pattern)[/]")
                        return False, ""
                        
                else:
                    console.print(f"[red]✗ GraphQL failed: Status {graphql_response.status_code}[/]")
                    
            except Exception as e:
                console.print(f"[red]✗ GraphQL error: {str(e)}[/]")
            
            # Method 3: Check privacy settings endpoint
            try:
                console.print("[bold yellow]→ Checking privacy settings...[/]")
                
                privacy_url = f'https://graph.facebook.com/v18.0/me/privacy_settings'
                privacy_response = requests.get(privacy_url, headers=headers, timeout=15)
                
                if privacy_response.status_code == 200:
                    privacy_data = privacy_response.json()
                    console.print(f"[blue]Privacy Settings: {privacy_data}[/]")
                    
                    # Check for profile guard in privacy settings
                    privacy_str = str(privacy_data).lower()
                    if 'profile_picture_guard' in privacy_str:
                        if 'true' in privacy_str:
                            console.print("[green]✓ Privacy Settings: Shield is ON[/]")
                            return True, ""
                        else:
                            console.print("[green]✓ Privacy Settings: Shield is OFF[/]")
                            return False, ""
                            
                else:
                    console.print(f"[red]✗ Privacy settings failed: Status {privacy_response.status_code}[/]")
                    
            except Exception as e:
                console.print(f"[red]✗ Privacy settings error: {str(e)}[/]")
            
            # Method 4: Try the original approach with correct parameters
            try:
                console.print("[bold yellow]→ Trying original shield check method...[/]")
                
                original_payload = {
                    'variables': json.dumps({
                        'profileID': uid,
                        'scale': 1
                    }),
                    'doc_id': '1477043292367183'
                }
                
                original_response = requests.post(
                    'https://graph.facebook.com/graphql',
                    data=original_payload,
                    headers=headers,
                    timeout=15
                )
                
                if original_response.status_code == 200:
                    original_text = original_response.text.lower()
                    console.print(f"[blue]Original method response (first 200 chars): {original_text[:200]}...[/]")
                    
                    # Check for shield indicators
                    shield_patterns = [
                        'is_shielded":true',
                        'profile_guard":true',
                        'profile_picture_guard":true',
                        'shield_enabled":true'
                    ]
                    
                    no_shield_patterns = [
                        'is_shielded":false',
                        'profile_guard":false',
                        'profile_picture_guard":false',
                        'shield_enabled":false'
                    ]
                    
                    if any(pattern in original_text for pattern in shield_patterns):
                        console.print("[green]✓ Original method: Shield is ON[/]")
                        return True, ""
                    elif any(pattern in original_text for pattern in no_shield_patterns):
                        console.print("[green]✓ Original method: Shield is OFF[/]")
                        return False, ""
                        
                else:
                    console.print(f"[red]✗ Original method failed: Status {original_response.status_code}[/]")
                    
            except Exception as e:
                console.print(f"[red]✗ Original method error: {str(e)}[/]")
            
            console.print("[red]✗ All detection methods failed[/]")
            return None, "Could not determine shield status - all methods failed"
            
        except Exception as e:
            console.print(f"[red]✗ Critical error in shield detection: {str(e)}[/]")
            return None, f"Critical error during shield status check: {str(e)}"

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

            # Check current shield status with proper delay
            console.print(Panel(
                "[bold white]🔄 Checking current shield status...[/]",
                style="bold cyan",
                border_style="cyan"
            ))
            
            # Add progress indicator for the delay
            for i in range(6):
                console.print(f"[bold cyan]{'.' * (i + 1)}[/]", end="")
                time.sleep(1)
            console.print()  # New line after dots

            # Get current shield status
            current_status, shield_error = self._check_shield_status(token, account['user_id'])
            
            # Check if shield is already in the desired state
            if current_status is not None and not shield_error:
                if current_status and enable:
                    return False, "❕ Your Profile Shield was already turned on from the start, no need to use this feature."
                elif not current_status and not enable:
                    return False, "❕ Your Profile Shield was already turned off from the start, no need to use this feature."
            elif shield_error:
                # If we can't determine the status, we should still try but warn the user
                console.print(Panel(
                    f"[bold yellow]⚠️ Warning: {shield_error}[/]",
                    style="bold yellow",
                    border_style="yellow"
                ))
                console.print(Panel(
                    "[bold white]🔄 Proceeding with operation anyway...[/]",
                    style="bold cyan",
                    border_style="cyan"
                ))
                time.sleep(1)

            # Toggle shield
            action_text = "Activating" if enable else "Deactivating"
            console.print(Panel(
                f"[bold white]🔄 {action_text} Profile Shield...[/]",
                style="bold cyan",
                border_style="cyan"
            ))
            time.sleep(1)

            # Make the initial request to toggle shield
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
            
            headers = {
                'Authorization': f"OAuth {token}",
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
            }

            response = requests.post(
                'https://graph.facebook.com/graphql',
                json=data,
                headers=headers,
                timeout=15
            )

            if response.status_code != 200:
                return False, f"Request failed with status {response.status_code}: {response.text}"

            # Verify the change was successful by checking the new status
            console.print(Panel(
                "[bold white]🔄 Verifying shield status change...[/]",
                style="bold cyan",
                border_style="cyan"
            ))
            time.sleep(2)  # Give some time for the change to propagate

            # Check the new status
            new_status, verify_error = self._check_shield_status(token, account['user_id'])
            
            if new_status is not None and not verify_error:
                if new_status == enable:
                    # Success - the status matches what we wanted
                    action = "turned on" if enable else "turned off"
                    return True, f"✅ You {action} your Facebook Profile Shield."
                else:
                    # The status doesn't match what we wanted
                    action = "activate" if enable else "deactivate"
                    return False, f"❌ Failed to {action} Profile Shield. Status verification failed."
            else:
                # Could not verify status, but check response for success indicators
                response_text = response.text.lower()
                success_patterns = [
                    'success',
                    'mutation_success',
                    f'is_shielded":{str(enable).lower()}',
                    'profile_shield_updated'
                ]
                
                if any(pattern in response_text for pattern in success_patterns):
                    action = "turned on" if enable else "turned off"
                    return True, f"✅ You {action} your Facebook Profile Shield."
                else:
                    action = "activate" if enable else "deactivate"
                    return False, f"❌ Failed to {action} Profile Shield. Please try again."

        except requests.exceptions.Timeout:
            return False, "❌ Request timed out. Please check your internet connection and try again."
        except requests.exceptions.RequestException as e:
            return False, f"❌ Network error: {str(e)}"
        except Exception as e:
            return False, f"❌ Unexpected error: {str(e)}"
