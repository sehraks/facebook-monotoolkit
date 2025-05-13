#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/profile_guard.py
# Last Modified: 2025-05-13 11:59:39 UTC
# Author: sehraks
# Description: Profile Picture Guard implementation for Facebook MonoToolkit

import aiohttp
import json
import re
import uuid
from typing import Tuple, Dict, Optional, Any
from datetime import datetime
from colorama import Fore, Style
from .utils import Utils

class ProfileGuard:
    def __init__(self) -> None:
        """Initialize ProfileGuard with default values."""
        # API Configuration
        self.api_version = "v19.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
        self.graphql_url = f"{self.base_url}/graphql"
        
        # Default headers for requests
        self.headers = {
            'authority': 'graph.facebook.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    async def _get_user_info(self, session: aiohttp.ClientSession, cookie: str) -> Optional[Dict[str, Any]]:
        """
        Get user information including ID and current guard status.
        
        Args:
            session (aiohttp.ClientSession): Active session
            cookie (str): Facebook cookie
            
        Returns:
            Optional[Dict[str, Any]]: User information or None if failed
        """
        try:
            headers = self.headers.copy()
            headers['cookie'] = cookie
            
            fields = "id,name,profile_picture_guard"
            async with session.get(
                f"{self.base_url}/me?fields={fields}",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    Utils.print_status("Invalid or expired cookie", "error")
                    return None
                else:
                    Utils.print_status(f"Failed to get user info: Status {response.status}", "error")
                    return None
        except aiohttp.ClientError as e:
            Utils.print_status(f"Network error: {str(e)}", "error")
            return None
        except Exception as e:
            Utils.print_status(f"Unexpected error: {str(e)}", "error")
            return None

    async def _verify_guard_status(self, session: aiohttp.ClientSession, 
                                 user_id: str, cookie: str) -> Tuple[bool, str]:
        """
        Verify if profile guard is active and working.
        
        Args:
            session (aiohttp.ClientSession): Active session
            user_id (str): Facebook user ID
            cookie (str): Facebook cookie
            
        Returns:
            Tuple[bool, str]: (status, message)
        """
        try:
            headers = self.headers.copy()
            headers['cookie'] = cookie
            
            async with session.get(
                f"{self.base_url}/{user_id}?fields=profile_picture_guard",
                headers=headers
            ) as response:
                if response.status != 200:
                    return False, "Failed to verify guard status"
                    
                data = await response.json()
                if data.get('profile_picture_guard', False):
                    return True, "Profile Guard is already active"
                return False, "Profile Guard is not active"
                
        except Exception as e:
            return False, f"Error verifying guard status: {str(e)}"

    async def _activate_guard(self, session: aiohttp.ClientSession, 
                            user_id: str, cookie: str) -> Tuple[bool, str]:
        """
        Activate profile picture guard using GraphQL API.
        
        Args:
            session (aiohttp.ClientSession): Active session
            user_id (str): Facebook user ID
            cookie (str): Facebook cookie
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            headers = self.headers.copy()
            headers['cookie'] = cookie
            headers['content-type'] = 'application/x-www-form-urlencoded'
            
            # Prepare GraphQL mutation
            mutation_id = str(uuid.uuid4())
            variables = {
                "0": {
                    "is_shielded": True,
                    "actor_id": user_id,
                    "client_mutation_id": mutation_id
                }
            }
            
            data = {
                "variables": json.dumps(variables),
                "doc_id": "1477043292367183"  # Facebook's Profile Guard mutation ID
            }
            
            async with session.post(self.graphql_url, headers=headers, data=data) as response:
                if response.status != 200:
                    return False, f"API Error: Status {response.status}"
                    
                result = await response.json()
                
                # Check for various error conditions
                if 'errors' in result:
                    error_msg = result['errors'][0].get('message', 'Unknown error')
                    return False, f"API Error: {error_msg}"
                    
                if result.get('data', {}).get('profile_picture_guard_set', {}).get('success'):
                    return True, "Successfully activated Profile Guard"
                    
                return False, "Failed to activate Profile Guard"
                
        except aiohttp.ClientError as e:
            return False, f"Network error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    async def activate_profile_guard(self, cookie: str) -> Tuple[bool, str]:
        """
        Main method to activate profile picture guard.
        
        Args:
            cookie (str): Facebook cookie for authentication
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        async with aiohttp.ClientSession() as session:
            try:
                # Get user information
                user_info = await self._get_user_info(session, cookie)
                if not user_info:
                    return False, "Failed to get user information"
                
                user_id = user_info.get('id')
                if not user_id:
                    return False, "Could not determine user ID"
                
                # Check current guard status
                guard_active, status_msg = await self._verify_guard_status(session, user_id, cookie)
                if guard_active:
                    return False, status_msg
                
                # Attempt to activate guard
                success, message = await self._activate_guard(session, user_id, cookie)
                if not success:
                    return False, message
                
                # Verify activation
                verify_success, verify_msg = await self._verify_guard_status(session, user_id, cookie)
                if not verify_success:
                    return False, "Activation seemed successful but verification failed"
                
                return True, "Profile Guard successfully activated and verified"
                
            except Exception as e:
                return False, f"Error during guard activation: {str(e)}"

    def activate_guard(self, cookie: str) -> Tuple[bool, str]:
        """
        Synchronous wrapper for activate_profile_guard.
        
        Args:
            cookie (str): Facebook cookie
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            import asyncio
            
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run the async activation
            return loop.run_until_complete(self.activate_profile_guard(cookie))
            
        except Exception as e:
            return False, f"System error: {str(e)}"

    def get_guard_status(self, cookie: str) -> Tuple[bool, str]:
        """
        Get current profile guard status.
        
        Args:
            cookie (str): Facebook cookie
            
        Returns:
            Tuple[bool, str]: (is_active, status_message)
        """
        try:
            import asyncio
            
            async def check_status():
                async with aiohttp.ClientSession() as session:
                    user_info = await self._get_user_info(session, cookie)
                    if not user_info:
                        return False, "Could not fetch guard status"
                    
                    if user_info.get('profile_picture_guard', False):
                        return True, "Profile Guard is active"
                    return False, "Profile Guard is not active"
            
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            return loop.run_until_complete(check_status())
            
        except Exception as e:
            return False, f"Error checking guard status: {str(e)}"
