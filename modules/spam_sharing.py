import asyncio
import json
import re
import aiohttp
from typing import Dict, Tuple, Optional
from datetime import datetime
from colorama import Fore, Style
from .utils import Utils

class SpamSharing:
    def __init__(self) -> None:
        """Initialize SpamSharing with default values."""
        self.headers = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.9',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    async def _get_fb_dtsg(self, session: aiohttp.ClientSession, cookie: str) -> Optional[str]:
        """
        Extract fb_dtsg token from Facebook page.
        
        Args:
            session (aiohttp.ClientSession): Active session
            cookie (str): Facebook cookie
            
        Returns:
            Optional[str]: fb_dtsg token if found, None otherwise
        """
        try:
            headers = self.headers.copy()
            headers['cookie'] = cookie
            
            async with session.get('https://www.facebook.com', headers=headers) as response:
                if response.status != 200:
                    return None
                    
                text = await response.text()
                match = re.search(r'"DTSGInitialData",\[\],{"token":"(.*?)"}', text)
                if match:
                    return match.group(1)
                return None
        except Exception as e:
            Utils.print_status(f"Error getting fb_dtsg: {str(e)}", "error")
            return None

    async def _share_post_once(self, 
                             session: aiohttp.ClientSession, 
                             post_url: str,
                             fb_dtsg: str,
                             cookie: str) -> bool:
        """
        Share a Facebook post once.
        
        Args:
            session (aiohttp.ClientSession): Active session
            post_url (str): URL of the post to share
            fb_dtsg (str): Facebook DTSG token
            cookie (str): Facebook cookie
            
        Returns:
            bool: True if share was successful
        """
        try:
            # Extract post ID from URL
            post_id_match = re.search(r'/posts/(\d+)', post_url)
            if not post_id_match:
                Utils.print_status("Invalid post URL format", "error")
                return False

            post_id = post_id_match.group(1)
            share_url = f'https://www.facebook.com/share/dialog/submit/'

            headers = self.headers.copy()
            headers['cookie'] = cookie
            headers['content-type'] = 'application/x-www-form-urlencoded'

            data = {
                'fb_dtsg': fb_dtsg,
                'shareID': post_id,
                'share_type': 22,
                '__a': 1
            }

            async with session.post(share_url, headers=headers, data=data) as response:
                if response.status == 200:
                    return True
                else:
                    Utils.print_status(f"Share failed with status {response.status}", "error")
                    return False

        except Exception as e:
            Utils.print_status(f"Error sharing post: {str(e)}", "error")
            return False

    def share_post(self, cookie: str, post_url: str, share_count: int, delay: int) -> Tuple[bool, str]:
        """
        Share a Facebook post multiple times.
        
        Args:
            cookie (str): Facebook cookie for authentication
            post_url (str): URL of the post to share
            share_count (int): Number of times to share
            delay (int): Delay between shares in seconds
            
        Returns:
            Tuple[bool, str]: (success, message) pair
        """
        # Clean and validate the URL
        post_url = Utils.clean_facebook_url(post_url)
        if not Utils.validate_url(post_url):
            return False, "Invalid Facebook post URL format"

        async def _share_multiple():
            try:
                async with aiohttp.ClientSession() as session:
                    # Get fb_dtsg token
                    fb_dtsg = await self._get_fb_dtsg(session, cookie)
                    if not fb_dtsg:
                        return False, "Failed to get Facebook authentication token"

                    successful_shares = 0
                    
                    for i in range(share_count):
                        # Show progress
                        progress_bar = Utils.create_progress_bar(i + 1, share_count)
                        print(f"\r{Fore.CYAN}Progress: {progress_bar}{Style.RESET_ALL}", end='')
                        
                        # Attempt to share
                        if await self._share_post_once(session, post_url, fb_dtsg, cookie):
                            successful_shares += 1
                        
                        # Wait before next share
                        if i < share_count - 1:  # Don't delay after last share
                            await asyncio.sleep(delay)
                    
                    print()  # New line after progress bar
                    
                    if successful_shares == 0:
                        return False, "Failed to share post"
                    elif successful_shares < share_count:
                        return True, f"Partially successful: {successful_shares}/{share_count} shares completed"
                    else:
                        return True, f"Successfully shared post {share_count} times"
                        
            except Exception as e:
                return False, f"Error during sharing: {str(e)}"

        # Run the async function
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        return loop.run_until_complete(_share_multiple())

    def get_post_info(self, post_url: str, cookie: str) -> Dict:
        """
        Get information about a Facebook post.
        
        Args:
            post_url (str): URL of the post
            cookie (str): Facebook cookie for authentication
            
        Returns:
            Dict: Post information
        """
        # Clean the URL first
        post_url = Utils.clean_facebook_url(post_url)
        
        # This is a placeholder for future implementation
        # Could fetch post title, author, share count, etc.
        return {
            "url": post_url,
            "timestamp": datetime.now().isoformat(),
            "status": "info retrieved"
        }
