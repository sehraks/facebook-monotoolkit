#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/spam_sharing.py
# Last Modified: 2025-05-13 15:38:25 UTC
# Author: sehraks

import aiohttp
import asyncio
import re
import os
from datetime import datetime
from typing import Dict, Tuple, Optional
from colorama import Fore, Style

class SpamSharing:
    def __init__(self):
        """Initialize SpamSharing with necessary configurations."""
        self.last_update = "2025-05-13 15:38:25"  # Current UTC time
        self.current_user = "sehraks"  # Current user's login
        self.share_api_url = "https://b-graph.facebook.com/me/feed"
        self.max_shares_per_day = 200000
        self.default_headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "sec-ch-ua": '"Chromium";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0"
        }
        self._init_logging()

    def _init_logging(self) -> None:
        """Initialize logging directory."""
        self.log_dir = "logs"
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _log_share_activity(self, user_id: str, success: bool, message: str) -> None:
        """Log sharing activity to file."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        log_file = os.path.join(self.log_dir, f"share_activity_{datetime.now().strftime('%Y%m')}.log")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] User: {user_id} | Success: {success} | Message: {message}\n")
        except Exception as e:
            print(f"{Fore.RED}Failed to log activity: {str(e)}{Style.RESET_ALL}")

    async def _get_access_token(self, session: aiohttp.ClientSession, cookie: str) -> Tuple[Optional[str], str]:
        """Get Facebook access token from business.facebook.com."""
        headers = self.default_headers.copy()
        headers["cookie"] = cookie

        try:
            async with session.get("https://business.facebook.com/content_management", headers=headers) as response:
                if response.status != 200:
                    return None, f"Failed to fetch token: HTTP {response.status}"
                
                data = await response.text()
                match = re.search(r'EAAG(.*?)",', data)
                
                if not match:
                    return None, "Could not extract access token. Cookie may be invalid."
                
                access_token = f"EAAG{match.group(1)}"
                return access_token, ""
                
        except Exception as e:
            return None, f"Failed to get token: {str(e)}"

    async def _perform_share(self, 
                           session: aiohttp.ClientSession,
                           token: str,
                           cookie: str,
                           post_path: str,
                           share_count: int,
                           delay: float) -> Tuple[int, str]:
        """Perform the actual sharing operation."""
        headers = self.default_headers.copy()
        headers.update({
            "accept-encoding": "gzip, deflate",
            "host": "b-graph.facebook.com",
            "cookie": cookie
        })

        successful_shares = 0
        c_user_match = re.search(r'c_user=(\d+)', cookie)
        user_id = c_user_match.group(1) if c_user_match else "unknown"

        print(f"{Fore.CYAN}Starting share operation...{Style.RESET_ALL}")
        
        for i in range(share_count):
            try:
                share_url = f"{self.share_api_url}?link=https://mbasic.facebook.com/{post_path}&published=0&access_token={token}"
                
                async with session.post(share_url, headers=headers) as response:
                    try:
                        data = await response.json()
                    except Exception:
                        data = {"error": {"message": "Invalid JSON response"}}

                    if "id" in data:
                        successful_shares += 1
                        print(f"{Fore.GREEN}[{successful_shares}/{share_count}] Share successful{Style.RESET_ALL}")
                        self._log_share_activity(user_id, True, f"Share {successful_shares}/{share_count}")
                    else:
                        error_msg = data.get("error", {}).get("message", "Unknown error")
                        self._log_share_activity(user_id, False, f"Share failed: {error_msg}")
                        return successful_shares, f"Share operation blocked: {error_msg}"

            except Exception as e:
                error_msg = str(e)
                self._log_share_activity(user_id, False, f"Share failed: {error_msg}")
                return successful_shares, f"Share operation failed: {error_msg}"

            if i < share_count - 1:  # Don't delay after the last share
                await asyncio.sleep(delay)

        return successful_shares, "Share operation completed successfully"

    def validate_post_url(self, url: str) -> Tuple[bool, str]:
        """Validate Facebook post URL format."""
        if not url.startswith("https://www.facebook.com/"):
            return False, "Invalid URL: Must start with https://www.facebook.com/"

        # Common Facebook post URL patterns
        patterns = [
            r'^https://www\.facebook\.com/[^/]+/posts/\d+/?$',
            r'^https://www\.facebook\.com/groups/\d+/permalink/\d+/?$',
            r'^https://www\.facebook\.com/photo\.php\?fbid=\d+',
            r'^https://www\.facebook\.com/[^/]+/photos/[^/]+/\d+/?$',
            r'^https://www\.facebook\.com/permalink\.php\?story_fbid=\d+&id=\d+/?$'
        ]

        for pattern in patterns:
            if re.match(pattern, url):
                return True, self._extract_post_path(url)

        return False, "Invalid post URL format"

    def _extract_post_path(self, url: str) -> str:
        """Extract the post path from a Facebook URL."""
        path = url.replace("https://www.facebook.com/", "")
        return path.rstrip('/')

    def share_post(self, cookie: str, post_url: str, share_count: int, delay: int) -> Tuple[bool, str]:
        """Share a Facebook post multiple times."""
        if share_count > self.max_shares_per_day:
            return False, f"Share count exceeds maximum limit of {self.max_shares_per_day}"

        # Validate post URL
        valid_url, post_path = self.validate_post_url(post_url)
        if not valid_url:
            return False, post_path

        async def _share():
            async with aiohttp.ClientSession() as session:
                # Get access token
                token, token_error = await self._get_access_token(session, cookie)
                if not token:
                    return False, token_error

                # Perform sharing
                shares_completed, share_message = await self._perform_share(
                    session, token, cookie, post_path, share_count, delay
                )

                if shares_completed == share_count:
                    return True, f"Successfully completed {shares_completed} shares"
                elif shares_completed > 0:
                    return False, f"Partially completed: {shares_completed}/{share_count} shares. {share_message}"
                else:
                    return False, share_message

        try:
            return asyncio.run(_share())
        except Exception as e:
            return False, f"Share operation failed: {str(e)}"

    def get_share_limits(self) -> Dict:
        """Get current sharing limits and status."""
        return {
            "max_shares_per_day": self.max_shares_per_day,
            "last_updated": self.last_update,
            "updated_by": self.current_user
        }
