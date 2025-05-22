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
        """Check if profile shield is active using direct web scraping approach."""
        try:
            # Method 1: Direct profile page check (most reliable)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Cookie': f'c_user={uid}; xs={token};'
            }
            
            console.print("[bold yellow]→ Checking profile page directly...[/]")
            
            try:
                # Check the profile page directly
                profile_url = f'https://www.facebook.com/{uid}'
                response = requests.get(profile_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    page_content = response.text.lower()
                    
                    # Look for shield indicators in the HTML
                    shield_on_patterns = [
                        'profile picture guard',
                        'profile picture is protected',
                        'profile guard is on',
                        'profile shield',
                        'picture guard active',
                        'protected profile picture'
                    ]
                    
                    shield_off_patterns = [
                        'add profile picture',
                        'change profile picture',
                        'update profile picture',
                        'profile picture visible'
                    ]
                    
                    shield_on_count = sum(1 for pattern in shield_on_patterns if pattern in page_content)
                    shield_off_count = sum(1 for pattern in shield_off_patterns if pattern in page_content)
                    
                    if shield_on_count > shield_off_count and shield_on_count > 0:
                        console.print("[green]✓ Shield appears to be ON (found protection indicators)[/]")
                        return True, ""
                    elif shield_off_count > 0:
                        console.print("[green]✓ Shield appears to be OFF (found normal profile indicators)[/]")
                        return False, ""
                        
            except Exception as e:
                console.print(f"[red]✗ Direct profile check failed: {str(e)}[/]")
            
            # Method 2: Mobile Facebook check
            console.print("[bold yellow]→ Checking mobile Facebook...[/]")
            
            try:
                mobile_headers = {
                    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
                    'Cookie': f'c_user={uid}; xs={token};'
                }
                
                mobile_url = f'https://m.facebook.com/{uid}'
                response = requests.get(mobile_url, headers=mobile_headers, timeout=15)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    if 'profile picture guard' in content or 'protected' in content:
                        console.print("[green]✓ Mobile check: Shield is ON[/]")
                        return True, ""
                    elif 'timeline' in content and 'posts' in content:
                        console.print("[green]✓ Mobile check: Shield is OFF[/]")
                        return False, ""
                        
            except Exception as e:
                console.print(f"[red]✗ Mobile check failed: {str(e)}[/]")
            
            # Method 3: Graph API with session cookies
            console.print("[bold yellow]→ Checking via Graph API with session...[/]")
            
            try:
                api_headers = {
                    'Authorization': f'Bearer {token}',
                    'Cookie': f'c_user={uid}; xs={token};',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                # Check privacy settings
                privacy_url = f'https://graph.facebook.com/v18.0/me/privacy'
                response = requests.get(privacy_url, headers=api_headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    console.print(f"[blue]Privacy data: {str(data)[:200]}...[/]")
                    
                    # Look for shield-related settings
                    privacy_str = str(data).lower()
                    if 'guard' in privacy_str or 'shield' in privacy_str or 'protected' in privacy_str:
                        if 'true' in privacy_str:
                            console.print("[green]✓ Graph API: Shield is ON[/]")
                            return True, ""
                        elif 'false' in privacy_str:
                            console.print("[green]✓ Graph API: Shield is OFF[/]")
                            return False, ""
                            
            except Exception as e:
                console.print(f"[red]✗ Graph API check failed: {str(e)}[/]")
            
            # Method 4: Photo access test
            console.print("[bold yellow]→ Testing photo access...[/]")
            
            try:
                photo_headers = {
                    'Authorization': f'Bearer {token}',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                # Try to access photos
                photos_url = f'https://graph.facebook.com/v18.0/{uid}/photos?limit=1'
                response = requests.get(photos_url, headers=photo_headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('data'):
                        console.print("[green]✓ Photo access: Shield is OFF (photos accessible)[/]")
                        return False, ""
                elif response.status_code == 403:
                    console.print("[green]✓ Photo access: Shield is ON (photos restricted)[/]")
                    return True, ""
                    
            except Exception as e:
                console.print(f"[red]✗ Photo access test failed: {str(e)}[/]")
            
            # Method 5: Simple token validation approach
            console.print("[bold yellow]→ Final validation check...[/]")
            
            try:
                # Check basic profile info access
                basic_url = f'https://graph.facebook.com/v18.0/me?access_token={token}'
                response = requests.get(basic_url, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    user_id = data.get('id')
                    
                    if user_id:
                        # Try to access another user's view of this profile
                        public_url = f'https://graph.facebook.com/v18.0/{user_id}?fields=name,picture&access_token={token}'
                        pub_response = requests.get(public_url, timeout=15)
                        
                        if pub_response.status_code == 200:
                            pub_data = pub_response.json()
                            if 'picture' in pub_data and pub_data['picture'].get('data', {}).get('url'):
                                # Try to access the picture URL
                                pic_url = pub_data['picture']['data']['url']
                                pic_response = requests.head(pic_url, timeout=10)
                                
                                if pic_response.status_code == 200:
                                    console.print("[green]✓ Final check: Shield is OFF (picture accessible)[/]")
                                    return False, ""
                                else:
                                    console.print("[green]✓ Final check: Shield is ON (picture protected)[/]")
                                    return True, ""
                                    
            except Exception as e:
                console.print(f"[red]✗ Final validation failed: {str(e)}[/]")
            
            console.print("[red]✗ All methods failed to determine shield status[/]")
            return None, "Could not determine shield status after trying all available methods"
            
        except Exception as e:
            return None, f"Error during shield status check: {str(e)}"

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
