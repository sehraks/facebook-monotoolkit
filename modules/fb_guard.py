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
        """Check if profile shield is active using multiple Facebook API approaches."""
        try:
            headers = {
                'Authorization': f'Bearer {token}',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'Accept': 'application/json'
            }
            
            # Method 1: Check profile visibility settings
            try:
                profile_url = f'https://graph.facebook.com/v18.0/{uid}?fields=id,name,picture,posts.limit(1),albums.limit(1)'
                response = requests.get(profile_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # If we can access posts and albums freely, shield is likely OFF
                    if 'posts' in data and 'albums' in data:
                        if data.get('posts', {}).get('data') and data.get('albums', {}).get('data'):
                            return False, ""
                    
                    # If posts/albums are restricted or empty, shield might be ON
                    if ('posts' not in data or not data.get('posts', {}).get('data')) and \
                       ('albums' not in data or not data.get('albums', {}).get('data')):
                        return True, ""
                        
            except Exception as e:
                console.print(f"[yellow]Method 1 failed: {str(e)}[/]")
            
            # Method 2: Check timeline/feed accessibility
            try:
                feed_url = f'https://graph.facebook.com/v18.0/{uid}/feed?limit=1'
                response = requests.get(feed_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    # If we can access feed, shield is likely OFF
                    if data.get('data'):
                        return False, ""
                elif response.status_code == 403 or 'permission' in response.text.lower():
                    # If access is denied, shield is likely ON
                    return True, ""
                    
            except Exception as e:
                console.print(f"[yellow]Method 2 failed: {str(e)}[/]")
            
            # Method 3: Check privacy settings directly
            try:
                privacy_url = f'https://graph.facebook.com/v18.0/{uid}/privacy_settings'
                response = requests.get(privacy_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    # Look for shield-related settings
                    if 'profile_picture_guard' in data:
                        return data['profile_picture_guard'], ""
                    if 'timeline_review' in data and data['timeline_review']:
                        return True, ""
                        
            except Exception as e:
                console.print(f"[yellow]Method 3 failed: {str(e)}[/]")
            
            # Method 4: Try to access profile picture with different parameters
            try:
                pic_url = f'https://graph.facebook.com/v18.0/{uid}/picture?redirect=false&width=500&height=500'
                response = requests.get(pic_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    # Check if profile picture is protected
                    if 'url' in data:
                        pic_response = requests.head(data['url'], timeout=5)
                        if pic_response.status_code != 200:
                            return True, ""  # Picture is protected, shield likely ON
                        else:
                            # Picture is accessible, but let's check one more thing
                            pass
                            
            except Exception as e:
                console.print(f"[yellow]Method 4 failed: {str(e)}[/]")
            
            # Method 5: Check using me endpoint with specific fields
            try:
                me_url = f'https://graph.facebook.com/v18.0/me?fields=id,name,picture,timeline_visibility,profile_pic_guard'
                response = requests.get(me_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    # Check for explicit shield indicators
                    if 'profile_pic_guard' in data:
                        return data['profile_pic_guard'], ""
                    if 'timeline_visibility' in data:
                        if data['timeline_visibility'] == 'protected':
                            return True, ""
                        elif data['timeline_visibility'] == 'public':
                            return False, ""
                            
            except Exception as e:
                console.print(f"[yellow]Method 5 failed: {str(e)}[/]")
            
            # Method 6: Last resort - try the original GraphQL method with better parsing
            try:
                graphql_data = {
                    'query': '''
                    query ProfileShieldStatus($id: ID!) {
                        user(id: $id) {
                            id
                            profilePictureGuard
                            timelineVisibility
                            canViewTimeline
                        }
                    }
                    ''',
                    'variables': {'id': uid}
                }
                
                response = requests.post(
                    'https://graph.facebook.com/graphql',
                    json=graphql_data,
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    text = response.text.lower()
                    # More comprehensive text analysis
                    shield_on_indicators = [
                        'profilepictureguard":true',
                        'profile_picture_guard":true',
                        'shield":true',
                        'protected":true',
                        'guarded":true'
                    ]
                    
                    shield_off_indicators = [
                        'profilepictureguard":false',
                        'profile_picture_guard":false',
                        'shield":false',
                        'public":true'
                    ]
                    
                    if any(indicator in text for indicator in shield_on_indicators):
                        return True, ""
                    elif any(indicator in text for indicator in shield_off_indicators):
                        return False, ""
                        
            except Exception as e:
                console.print(f"[yellow]Method 6 failed: {str(e)}[/]")
            
            # If all methods fail, return None
            return None, "Could not determine shield status using any available method"
            
        except Exception as e:
            return None, f"Error checking shield status: {str(e)}"

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
