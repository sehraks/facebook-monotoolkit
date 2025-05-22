#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/fb_guard.py

import json
import uuid
import requests
import time
import re
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

    def _log_response_details(self, response, method_name):
        """Log detailed response information for debugging."""
        console.print(f"[blue]--- {method_name} Response Details ---[/]")
        console.print(f"[blue]Status Code: {response.status_code}[/]")
        console.print(f"[blue]Headers: {dict(response.headers)}[/]")
        
        # Check for Facebook's blocking mechanisms
        response_text = response.text.lower()
        blocking_indicators = [
            ('Captcha Required', 'captcha_required'),
            ('Checkpoint Required', 'checkpoint_required'),
            ('Rate Limited', 'rate_limit'),
            ('Bot Detected', 'automated_request'),
            ('Login Required', 'login_form'),
            ('Session Expired', 'session_expired'),
            ('Access Denied', 'access_denied')
        ]
        
        for indicator_name, indicator_text in blocking_indicators:
            if indicator_text in response_text:
                console.print(f"[red]⚠️ {indicator_name} detected in response![/]")
        
        # Log first 500 characters of response
        console.print(f"[blue]Response Preview: {response.text[:500]}...[/]")
        console.print("[blue]--- End Response Details ---[/]")

    def _check_shield_status_mbasic(self, cookie: str, uid: str) -> Tuple[Optional[bool], str]:
        """Check shield status using mbasic.facebook.com (legacy mobile site)."""
        try:
            console.print("[bold yellow]→ Checking via mbasic.facebook.com (legacy mobile)...[/]")
            
            # Create session with cookies
            session = requests.Session()
            
            # Parse and set cookies
            for cookie_item in cookie.split(';'):
                if '=' in cookie_item and cookie_item.strip():
                    try:
                        name, value = cookie_item.strip().split('=', 1)
                        session.cookies.set(name.strip(), value.strip())
                    except ValueError:
                        continue
            
            # Use simple headers that won't trigger bot detection
            headers = {
                'User-Agent': 'Mozilla/5.0 (Mobile; rv:40.0) Gecko/40.0 Firefox/40.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            # Method 1: Check profile settings page on mbasic
            try:
                settings_url = f'https://mbasic.facebook.com/privacy/touch/profile_picture_guard/?profile_id={uid}'
                response = session.get(settings_url, headers=headers, timeout=20)
                
                self._log_response_details(response, "mbasic Profile Guard Settings")
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    # Look for specific patterns in mbasic's simpler HTML
                    if 'profile picture guard is on' in content or 'guard is currently on' in content:
                        console.print("[green]✓ mbasic: Shield is ON[/]")
                        return True, ""
                    elif 'profile picture guard is off' in content or 'turn on profile picture guard' in content:
                        console.print("[green]✓ mbasic: Shield is OFF[/]")
                        return False, ""
                    elif 'enable profile picture guard' in content:
                        console.print("[green]✓ mbasic: Shield is OFF (enable option found)[/]")
                        return False, ""
                    elif 'disable profile picture guard' in content:
                        console.print("[green]✓ mbasic: Shield is ON (disable option found)[/]")
                        return True, ""
                        
            except Exception as e:
                console.print(f"[red]✗ mbasic settings check failed: {str(e)}[/]")
            
            # Method 2: Check privacy settings main page
            try:
                privacy_url = 'https://mbasic.facebook.com/privacy/'
                response = session.get(privacy_url, headers=headers, timeout=20)
                
                self._log_response_details(response, "mbasic Privacy Settings")
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    # Look for profile picture guard mentions
                    if 'profile picture guard' in content:
                        # Extract the specific section about profile guard
                        guard_section = self._extract_guard_section(content)
                        if guard_section:
                            if 'on' in guard_section or 'enabled' in guard_section:
                                console.print("[green]✓ mbasic privacy: Shield is ON[/]")
                                return True, ""
                            elif 'off' in guard_section or 'disabled' in guard_section:
                                console.print("[green]✓ mbasic privacy: Shield is OFF[/]")
                                return False, ""
                                
            except Exception as e:
                console.print(f"[red]✗ mbasic privacy check failed: {str(e)}[/]")
            
            # Method 3: Check own profile page on mbasic
            try:
                profile_url = f'https://mbasic.facebook.com/{uid}'
                response = session.get(profile_url, headers=headers, timeout=20)
                
                self._log_response_details(response, "mbasic Profile Page")
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    # Look for profile picture related indicators
                    if 'profile picture is protected' in content:
                        console.print("[green]✓ mbasic profile: Shield is ON[/]")
                        return True, ""
                    elif 'change profile picture' in content and 'upload' in content:
                        console.print("[green]✓ mbasic profile: Shield is OFF[/]")
                        return False, ""
                        
            except Exception as e:
                console.print(f"[red]✗ mbasic profile check failed: {str(e)}[/]")
            
            return None, "Could not determine shield status from mbasic"
            
        except Exception as e:
            return None, f"mbasic check error: {str(e)}"

    def _extract_guard_section(self, content: str) -> str:
        """Extract the section about profile picture guard from HTML content."""
        try:
            # Look for content around "profile picture guard"
            guard_index = content.find('profile picture guard')
            if guard_index != -1:
                # Extract 200 characters before and after
                start = max(0, guard_index - 200)
                end = min(len(content), guard_index + 200)
                return content[start:end]
        except:
            pass
        return ""

    def _check_shield_status_touch(self, cookie: str, uid: str) -> Tuple[Optional[bool], str]:
        """Check shield status using touch.facebook.com (another legacy interface)."""
        try:
            console.print("[bold yellow]→ Checking via touch.facebook.com...[/]")
            
            session = requests.Session()
            
            # Parse and set cookies
            for cookie_item in cookie.split(';'):
                if '=' in cookie_item and cookie_item.strip():
                    try:
                        name, value = cookie_item.strip().split('=', 1)
                        session.cookies.set(name.strip(), value.strip())
                    except ValueError:
                        continue
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us',
                'Accept-Encoding': 'gzip, deflate'
            }
            
            # Try touch interface for privacy settings
            try:
                touch_url = f'https://touch.facebook.com/privacy/touch/profile_picture_guard/?profile_id={uid}'
                response = session.get(touch_url, headers=headers, timeout=20)
                
                self._log_response_details(response, "touch.facebook.com Guard Settings")
                
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    # Check for guard status indicators
                    if 'guard is on' in content or 'currently protected' in content:
                        console.print("[green]✓ touch: Shield is ON[/]")
                        return True, ""
                    elif 'guard is off' in content or 'not protected' in content:
                        console.print("[green]✓ touch: Shield is OFF[/]")
                        return False, ""
                        
            except Exception as e:
                console.print(f"[red]✗ touch interface check failed: {str(e)}[/]")
            
            return None, "Could not determine shield status from touch interface"
            
        except Exception as e:
            return None, f"touch interface error: {str(e)}"

    def _check_shield_status_direct_cookie(self, cookie: str, uid: str) -> Tuple[Optional[bool], str]:
        """Check shield status by analyzing cookie values directly."""
        try:
            console.print("[bold yellow]→ Analyzing cookie for shield indicators...[/]")
            
            # Parse cookie into dictionary
            cookie_dict = {}
            for cookie_item in cookie.split(';'):
                if '=' in cookie_item and cookie_item.strip():
                    try:
                        name, value = cookie_item.strip().split('=', 1)
                        cookie_dict[name.strip()] = value.strip()
                    except ValueError:
                        continue
            
            console.print(f"[blue]Available cookies: {list(cookie_dict.keys())}[/]")
            
            # Check for specific privacy-related cookies that might indicate shield status
            privacy_cookies = ['pp', 'privacy', 'guard', 'shield', 'protection']
            found_indicators = []
            
            for cookie_name, cookie_value in cookie_dict.items():
                for indicator in privacy_cookies:
                    if indicator in cookie_name.lower() or indicator in cookie_value.lower():
                        found_indicators.append(f"{cookie_name}={cookie_value}")
            
            if found_indicators:
                console.print(f"[blue]Privacy-related cookies found: {found_indicators}[/]")
                
                # Analyze the values for on/off indicators
                combined_values = ' '.join(found_indicators).lower()
                if 'on' in combined_values or 'true' in combined_values or '1' in combined_values:
                    console.print("[green]✓ Cookie analysis: Shield might be ON[/]")
                    return True, ""
                elif 'off' in combined_values or 'false' in combined_values or '0' in combined_values:
                    console.print("[green]✓ Cookie analysis: Shield might be OFF[/]")
                    return False, ""
            
            return None, "No shield indicators found in cookies"
            
        except Exception as e:
            return None, f"Cookie analysis error: {str(e)}"

    def _check_shield_status(self, token: str, uid: str, cookie: str) -> Tuple[Optional[bool], str]:
        """Check if profile shield is active using multiple fallback methods."""
        try:
            # Method 1: Try mbasic (most reliable)
            status, error = self._check_shield_status_mbasic(cookie, uid)
            if status is not None:
                return status, error
            
            # Method 2: Try touch interface
            status, error = self._check_shield_status_touch(cookie, uid)
            if status is not None:
                return status, error
            
            # Method 3: Direct cookie analysis (last resort)
            status, error = self._check_shield_status_direct_cookie(cookie, uid)
            if status is not None:
                return status, error
            
            # If all methods fail, return None
            console.print("[red]✗ All shield detection methods failed[/]")
            return None, "Could not determine shield status using any available method"
            
        except Exception as e:
            return None, f"Error during shield status check: {str(e)}"

    def _toggle_shield_mbasic(self, cookie: str, uid: str, enable: bool) -> Tuple[bool, str]:
        """Toggle shield using mbasic interface."""
        try:
            console.print(f"[bold yellow]→ Toggling shield via mbasic.facebook.com...[/]")
            
            session = requests.Session()
            
            # Parse and set cookies
            for cookie_item in cookie.split(';'):
                if '=' in cookie_item and cookie_item.strip():
                    try:
                        name, value = cookie_item.strip().split('=', 1)
                        session.cookies.set(name.strip(), value.strip())
                    except ValueError:
                        continue
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Mobile; rv:40.0) Gecko/40.0 Firefox/40.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': f'https://mbasic.facebook.com/{uid}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # First, get the settings page to extract form data
            settings_url = f'https://mbasic.facebook.com/privacy/touch/profile_picture_guard/?profile_id={uid}'
            response = session.get(settings_url, headers=headers, timeout=20)
            
            self._log_response_details(response, "mbasic Toggle Preparation")
            
            if response.status_code == 200:
                # Extract form data and action URL
                form_data = self._extract_form_data(response.text)
                
                if form_data:
                    # Modify the form data for our toggle action
                    form_data['profile_picture_guard'] = '1' if enable else '0'
                    
                    # Submit the form
                    form_response = session.post(
                        settings_url, 
                        data=form_data, 
                        headers=headers, 
                        timeout=20
                    )
                    
                    self._log_response_details(form_response, "mbasic Toggle Submit")
                    
                    if form_response.status_code == 200:
                        response_text = form_response.text.lower()
                        
                        # Check for success indicators
                        success_indicators = [
                            'settings saved',
                            'updated successfully',
                            'guard is now on' if enable else 'guard is now off',
                            'protection enabled' if enable else 'protection disabled'
                        ]
                        
                        if any(indicator in response_text for indicator in success_indicators):
                            action = "turned on" if enable else "turned off"
                            return True, f"✅ You {action} your Facebook Profile Shield."
            
            return False, "Could not toggle shield via mbasic interface"
            
        except Exception as e:
            return False, f"mbasic toggle error: {str(e)}"

    def _extract_form_data(self, html_content: str) -> dict:
        """Extract form data from HTML content."""
        try:
            form_data = {}
            
            # Look for hidden input fields
            hidden_inputs = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*>', html_content, re.IGNORECASE)
            
            for input_tag in hidden_inputs:
                name_match = re.search(r'name=["\']([^"\']+)["\']', input_tag)
                value_match = re.search(r'value=["\']([^"\']*)["\']', input_tag)
                
                if name_match:
                    name = name_match.group(1)
                    value = value_match.group(1) if value_match else ''
                    form_data[name] = value
            
            return form_data
            
        except Exception as e:
            console.print(f"[red]Form data extraction error: {str(e)}[/]")
            return {}

    def toggle_profile_shield(self, account: Dict, enable: bool = True) -> Tuple[bool, str]:
        """Toggle Facebook profile shield using legacy interfaces."""
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
            
            if not cookie:
                return False, "No valid cookie found for this account"

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

            # Try to toggle using mbasic interface
            success, message = self._toggle_shield_mbasic(cookie, account['user_id'], enable)
            
            if success:
                return True, message
            else:
                # If mbasic fails, return a generic error
                action = "activate" if enable else "deactivate"
                return False, f"❌ Failed to {action} Profile Shield. Facebook may have changed their interface or your session may have expired."

        except requests.exceptions.Timeout:
            return False, "❌ Request timed out. Please check your internet connection and try again."
        except requests.exceptions.RequestException as e:
            return False, f"❌ Network error: {str(e)}"
        except Exception as e:
            return False, f"❌ Unexpected error: {str(e)}"
