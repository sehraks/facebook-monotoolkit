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

    def _check_shield_status(self, token: str, uid: str, cookie: str) -> Tuple[Optional[bool], str]:
        """Check if profile shield is active using cookie-based session."""
        try:
            console.print("[bold yellow]→ Checking Profile Guard status...[/]")
            
            # Create session with cookies
            session = requests.Session()
            
            # Parse and set cookies
            try:
                for cookie_item in cookie.split(';'):
                    if '=' in cookie_item:
                        name, value = cookie_item.strip().split('=', 1)
                        session.cookies.set(name, value)
            except Exception as e:
                console.print(f"[red]✗ Cookie parsing failed: {str(e)}[/]")
                return None, f"Cookie parsing error: {str(e)}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # Method 1: Check profile guard via Facebook's mobile interface
            try:
                # Get the profile guard settings page
                guard_url = f'https://m.facebook.com/privacy/touch/profile_picture_guard/?profile_id={uid}'
                response = session.get(guard_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    # Look for specific patterns that indicate shield status
                    if 'profile picture guard is on' in content or 'profile guard is active' in content:
                        console.print("[green]✓ Mobile interface: Shield is ON[/]")
                        return True, ""
                    elif 'profile picture guard is off' in content or 'turn on profile picture guard' in content:
                        console.print("[green]✓ Mobile interface: Shield is OFF[/]")
                        return False, ""
                        
            except Exception as e:
                console.print(f"[red]✗ Mobile interface check failed: {str(e)}[/]")
            
            # Method 2: Check via Facebook's AJAX endpoint
            try:
                ajax_url = 'https://www.facebook.com/ajax/privacy/profile_picture_guard_status.php'
                ajax_data = {
                    'profile_id': uid,
                    '__a': '1',
                    '__req': 'fetchdata',
                    'fb_dtsg': self._extract_fb_dtsg(session, headers)
                }
                
                ajax_response = session.post(ajax_url, data=ajax_data, headers=headers, timeout=15)
                
                if ajax_response.status_code == 200:
                    ajax_text = ajax_response.text.lower()
                    console.print(f"[blue]AJAX Response sample: {ajax_text[:100]}...[/]")
                    
                    if 'guard":true' in ajax_text or 'shielded":true' in ajax_text:
                        console.print("[green]✓ AJAX check: Shield is ON[/]")
                        return True, ""
                    elif 'guard":false' in ajax_text or 'shielded":false' in ajax_text:
                        console.print("[green]✓ AJAX check: Shield is OFF[/]")
                        return False, ""
                        
            except Exception as e:
                console.print(f"[red]✗ AJAX check failed: {str(e)}[/]")
            
            # Method 3: Check via direct profile access
            try:
                profile_url = f'https://www.facebook.com/{uid}'
                profile_response = session.get(profile_url, headers=headers, timeout=15)
                
                if profile_response.status_code == 200:
                    profile_content = profile_response.text.lower()
                    
                    # Look for profile guard indicators in the profile page
                    guard_indicators = [
                        'profile picture guard',
                        'profile picture is protected',
                        'picture guard is on',
                        'profilepictureguard":true'
                    ]
                    
                    no_guard_indicators = [
                        'change profile picture',
                        'update profile picture',
                        'profilepictureguard":false'
                    ]
                    
                    guard_count = sum(1 for indicator in guard_indicators if indicator in profile_content)
                    no_guard_count = sum(1 for indicator in no_guard_indicators if indicator in profile_content)
                    
                    if guard_count > 0 and guard_count > no_guard_count:
                        console.print("[green]✓ Profile page: Shield is ON[/]")
                        return True, ""
                    elif no_guard_count > 0:
                        console.print("[green]✓ Profile page: Shield is OFF[/]")
                        return False, ""
                        
            except Exception as e:
                console.print(f"[red]✗ Profile page check failed: {str(e)}[/]")
            
            # Method 4: Check using Graph API with session cookies
            try:
                graph_headers = {
                    'Authorization': f'Bearer {token}',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
                }
                
                # Try to get profile information that might include guard status
                graph_url = f'https://graph.facebook.com/v18.0/{uid}?fields=id,name'
                graph_response = session.get(graph_url, headers=graph_headers, timeout=15)
                
                if graph_response.status_code == 200:
                    # Now try to access the profile picture with different parameters
                    pic_url = f'https://graph.facebook.com/v18.0/{uid}/picture?redirect=false&type=large'
                    pic_response = session.get(pic_url, headers=graph_headers, timeout=10)
                    
                    if pic_response.status_code == 200:
                        pic_data = pic_response.json()
                        if 'url' in pic_data:
                            # Try to access the actual picture URL
                            actual_pic_response = session.head(pic_data['url'], timeout=10)
                            if actual_pic_response.status_code != 200:
                                console.print("[green]✓ Graph API: Shield is ON (picture protected)[/]")
                                return True, ""
                            else:
                                console.print("[green]✓ Graph API: Shield is OFF (picture accessible)[/]")
                                return False, ""
                                
            except Exception as e:
                console.print(f"[red]✗ Graph API check failed: {str(e)}[/]")
            
            console.print("[red]✗ All detection methods failed[/]")
            return None, "Could not determine shield status using available methods"
            
        except Exception as e:
            console.print(f"[red]✗ Critical error in shield detection: {str(e)}[/]")
            return None, f"Critical error during shield status check: {str(e)}"

    def _extract_fb_dtsg(self, session, headers):
        """Extract fb_dtsg token from Facebook page."""
        try:
            response = session.get('https://www.facebook.com/', headers=headers, timeout=10)
            if response.status_code == 200:
                import re
                dtsg_match = re.search(r'"DTSGInitialData".*?"token":"([^"]+)"', response.text)
                if dtsg_match:
                    return dtsg_match.group(1)
        except:
            pass
        return str(uuid.uuid4())

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
            cookie = account.get('cookie')
            
            if not token or token == 'N/A':
                return False, "No valid token found for this account"
            
            if not cookie:
                return False, "No valid cookie found for this account"

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
            current_status, shield_error = self._check_shield_status(token, account['user_id'], cookie)
            
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

            # Create session with cookies for the toggle operation
            session = requests.Session()
            
            # Parse and set cookies
            for cookie_item in cookie.split(';'):
                if '=' in cookie_item:
                    name, value = cookie_item.strip().split('=', 1)
                    session.cookies.set(name, value)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            }

            # Method 1: Try mobile interface toggle
            try:
                fb_dtsg = self._extract_fb_dtsg(session, headers)
                
                toggle_url = 'https://m.facebook.com/privacy/touch/profile_picture_guard/'
                toggle_data = {
                    'profile_id': account['user_id'],
                    'enable_guard': '1' if enable else '0',
                    'fb_dtsg': fb_dtsg,
                    '__a': '1'
                }
                
                response = session.post(toggle_url, data=toggle_data, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    response_text = response.text.lower()
                    
                    # Check for success indicators
                    if enable and ('guard is now on' in response_text or 'guard enabled' in response_text):
                        return True, "✅ You turned on your Facebook Profile Shield."
                    elif not enable and ('guard is now off' in response_text or 'guard disabled' in response_text):
                        return True, "✅ You turned off your Facebook Profile Shield."
                        
            except Exception as e:
                console.print(f"[red]Mobile toggle failed: {str(e)}[/]")

            # Method 2: Try GraphQL mutation (fallback)
            try:
                data = {
                    'variables': json.dumps({
                        'input': {
                            'is_shielded': enable,
                            'actor_id': account['user_id'],
                            'client_mutation_id': str(uuid.uuid4())
                        }
                    }),
                    'doc_id': '1477043292367183'  # Using your original doc_id
                }
                
                headers_gql = {
                    'Authorization': f"Bearer {token}",
                    'Content-Type': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36'
                }

                response = session.post(
                    'https://graph.facebook.com/graphql',
                    json=data,
                    headers=headers_gql,
                    timeout=15
                )

                if response.status_code == 200:
                    response_text = response.text.lower()
                    
                    # Check for success patterns
                    success_patterns = [
                        'success',
                        f'is_shielded":{str(enable).lower()}',
                        'profile_guard_updated'
                    ]
                    
                    if any(pattern in response_text for pattern in success_patterns):
                        action = "turned on" if enable else "turned off"
                        return True, f"✅ You {action} your Facebook Profile Shield."
                        
            except Exception as e:
                console.print(f"[red]GraphQL toggle failed: {str(e)}[/]")

            # If we reach here, the operation may have failed
            action = "activate" if enable else "deactivate"
            return False, f"❌ Failed to {action} Profile Shield. Please try again."

        except requests.exceptions.Timeout:
            return False, "❌ Request timed out. Please check your internet connection and try again."
        except requests.exceptions.RequestException as e:
            return False, f"❌ Network error: {str(e)}"
        except Exception as e:
            return False, f"❌ Unexpected error: {str(e)}"
