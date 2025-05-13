#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/spam_sharing.py
# Last Modified: 2025-05-13 14:35:28 UTC
# Author: sehraks
# Description: Advanced spam sharing module for Facebook MonoToolkit

import os
import re
import json
import asyncio
import aiohttp
from typing import Dict, Tuple, Optional
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style
from .utils import Utils

class SpamSharing:
    def __init__(self) -> None:
        """Initialize SpamSharing with advanced configuration."""
        # Base configuration
        self.base_url = 'https://mbasic.facebook.com'
        self.max_retries = 3
        self.min_delay = 1
        self.success_count = 0
        self.error_count = 0
        
        # Mobile-optimized headers
        self.headers = {
            'authority': 'mbasic.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }

    async def _make_request(self, session: aiohttp.ClientSession, url: str, method: str = 'GET', 
                          data: Optional[Dict] = None, retry_count: int = 0) -> Optional[str]:
        """
        Make HTTP request with retry mechanism.
        
        Args:
            session (aiohttp.ClientSession): Active session
            url (str): Target URL
            method (str): HTTP method (GET/POST)
            data (Optional[Dict]): POST data if any
            retry_count (int): Current retry attempt
            
        Returns:
            Optional[str]: HTML content if successful, None otherwise
        """
        try:
            if method.upper() == 'GET':
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
            else:  # POST
                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        return await response.text()

            if retry_count < self.max_retries:
                await asyncio.sleep(self.min_delay * (retry_count + 1))
                return await self._make_request(session, url, method, data, retry_count + 1)
            return None
        except Exception as e:
            Utils.log_activity("HTTP Request", False, f"Error: {str(e)}")
            return None

    async def _get_share_token(self, session: aiohttp.ClientSession, url: str) -> Optional[Tuple[str, Dict]]:
        """
        Extract share token and form data from the share page.
        
        Args:
            session (aiohttp.ClientSession): Active session
            url (str): Post URL
            
        Returns:
            Optional[Tuple[str, Dict]]: Share URL and form data if found
        """
        try:
            html_content = await self._make_request(session, url)
            if not html_content:
                return None

            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find share form
            share_form = soup.find('form', {'method': 'post', 'action': True})
            if not share_form:
                return None

            # Extract form action URL and data
            action_url = self.base_url + share_form['action']
            form_data = {}
            
            # Get all input fields
            for input_tag in share_form.find_all('input'):
                if input_tag.get('name'):
                    form_data[input_tag['name']] = input_tag.get('value', '')

            return action_url, form_data
        except Exception as e:
            Utils.log_activity("Share Token Extraction", False, str(e))
            return None

    async def _perform_share(self, session: aiohttp.ClientSession, 
                           share_url: str, form_data: Dict) -> bool:
        """
        Perform the actual share operation.
        
        Args:
            session (aiohttp.ClientSession): Active session
            share_url (str): Share action URL
            form_data (Dict): Form data to submit
            
        Returns:
            bool: True if share successful
        """
        try:
            response_html = await self._make_request(
                session, 
                share_url, 
                method='POST',
                data=form_data
            )
            return bool(response_html)
        except Exception as e:
            Utils.log_activity("Share Operation", False, str(e))
            return False

    async def share_post(self, cookie: str, post_url: str, 
                        share_count: int, delay: int) -> Tuple[bool, str]:
        """
        Share a Facebook post multiple times.
        
        Args:
            cookie (str): Facebook cookie
            post_url (str): Post URL to share
            share_count (int): Number of times to share
            delay (int): Delay between shares
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            self.success_count = 0
            self.error_count = 0
            start_time = datetime.utcnow()

            # Clean and validate URL
            post_url = Utils.clean_facebook_url(post_url)
            if not Utils.validate_url(post_url):
                return False, "Invalid Facebook URL"

            # Convert to mobile URL
            if 'www.facebook.com' in post_url:
                post_url = post_url.replace('www.facebook.com', 'mbasic.facebook.com')

            # Set up session with cookie
            headers = self.headers.copy()
            headers['cookie'] = cookie

            async with aiohttp.ClientSession(headers=headers) as session:
                for i in range(share_count):
                    try:
                        # Get share token and form data
                        share_data = await self._get_share_token(session, post_url)
                        if not share_data:
                            self.error_count += 1
                            continue

                        share_url, form_data = share_data
                        
                        # Perform share
                        if await self._perform_share(session, share_url, form_data):
                            self.success_count += 1
                            Utils.print_status(
                                f"Share {self.success_count}/{share_count} completed",
                                "success"
                            )
                        else:
                            self.error_count += 1
                            Utils.print_status(
                                f"Share {i+1} failed",
                                "error"
                            )

                        # Add delay between shares
                        if i < share_count - 1:
                            await asyncio.sleep(delay)

                    except Exception as e:
                        self.error_count += 1
                        Utils.log_activity("Share Loop", False, str(e))
                        continue

                # Calculate statistics
                duration = (datetime.utcnow() - start_time).total_seconds()
                success_rate = (self.success_count / share_count) * 100

                result_message = (
                    f"Sharing completed!\n"
                    f"Success: {self.success_count}/{share_count} ({success_rate:.1f}%)\n"
                    f"Failed: {self.error_count}\n"
                    f"Duration: {duration:.1f} seconds"
                )

                return self.success_count > 0, result_message

        except Exception as e:
            Utils.log_activity("Share Post", False, str(e))
            return False, f"Share operation failed: {str(e)}"

    def get_statistics(self) -> Dict:
        """Get sharing operation statistics."""
        return {
            'success_count': self.success_count,
            'error_count': self.error_count,
            'total_attempts': self.success_count + self.error_count
        }
