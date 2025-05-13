import aiohttp
import asyncio
import re
import json
import time
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from colorama import Fore, Style

class SpamSharing:
    def __init__(self):
        """Initialize the SpamSharing class with necessary configurations."""
        self.share_api_url = "https://b-graph.facebook.com/me/feed"
        self.business_url = "https://business.facebook.com/content_management"
        self.mbasic_url = "https://mbasic.facebook.com"
        self.default_headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en-US,en;q=0.9",
            "sec-ch-ua": '"Chromium";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": "Android",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1"
        }

    async def get_token(self, session: aiohttp.ClientSession, cookie: str) -> Tuple[Optional[str], str]:
        """
        Get Facebook access token using the provided cookie.
        Returns tuple of (token, error_message).
        """
        headers = self.default_headers.copy()
        headers["cookie"] = cookie

        try:
            async with session.get(self.business_url, headers=headers, timeout=30) as response:
                if response.status != 200:
                    return None, f"Failed to fetch token: HTTP {response.status}"

                data = await response.text()
                
                # Try different token patterns
                patterns = [
                    r'EAAG\w+',  # Standard token pattern
                    r'EAAB\w+',  # Business token pattern
                    r'EAA\w+',   # Generic token pattern
                ]

                for pattern in patterns:
                    match = re.search(pattern, data)
                    if match:
                        return match.group(0), ""

                return None, "Could not extract access token. Cookie may be invalid."

        except asyncio.TimeoutError:
            return None, "Request timed out while fetching token"
        except Exception as e:
            return None, f"Failed to get token: {str(e)}"

    def normalize_url(self, url: str) -> str:
        """Normalize Facebook URL to a standard format."""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url

    def extract_post_id(self, url: str) -> Optional[str]:
        """Extract post ID from various Facebook URL formats."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        query = parse_qs(parsed.query)

        # Pattern 1: /posts/<post_id>
        if 'posts' in path:
            match = re.search(r'/posts/(\d+)', path)
            if match:
                return match.group(1)

        # Pattern 2: /permalink/<post_id>
        if 'permalink' in path:
            match = re.search(r'/permalink/(\d+)', path)
            if match:
                return match.group(1)

        # Pattern 3: story_fbid in query
        if 'story_fbid' in query:
            return query['story_fbid'][0]

        # Pattern 4: ?p= format
        if 'p' in query:
            return query['p'][0]

        return None

    def validate_post_url(self, url: str) -> Tuple[bool, str]:
        """
        Validate Facebook post URL format and extract sharing path.
        Returns tuple of (is_valid, result).
        """
        try:
            url = self.normalize_url(url)
            if not url.startswith(("https://www.facebook.com/", "https://facebook.com/", "https://m.facebook.com/")):
                return False, "Invalid URL. Must be a Facebook post URL."

            parsed = urlparse(url)
            path = parsed.path.strip("/")
            post_id = self.extract_post_id(url)

            if post_id:
                return True, post_id
            elif (re.match(r"^.+/posts/\d+$", path) or 
                  re.match(r"^groups/\d+/permalink/\d+$", path) or 
                  "story_fbid" in parsed.query):
                return True, path
            
            return False, "Invalid post URL format. Could not extract post information."

        except Exception as e:
            return False, f"URL validation error: {str(e)}"

    async def check_share_limit(self, session: aiohttp.ClientSession, token: str) -> Tuple[bool, int]:
        """Check if account has reached sharing limits."""
        try:
            url = f"https://graph.facebook.com/v17.0/me/feed?limit=5&access_token={token}"
            async with session.get(url) as response:
                if response.status != 200:
                    return False, 0
                
                data = await response.json()
                recent_shares = len([post for post in data.get('data', [])
                                  if post.get('created_time', '') > 
                                  (datetime.utcnow() - timedelta(hours=1)).isoformat()])
                
                return recent_shares < 30, 30 - recent_shares  # Assuming limit is 30 shares per hour
        except Exception:
            return True, 30  # If check fails, assume no limit reached

    async def do_share(self, session: aiohttp.ClientSession, token: str, cookie: str,
                      post_path: str, share_count: int, delay: int) -> Tuple[int, str]:
        """
        Perform the actual sharing operation.
        Returns tuple of (shares_completed, message).
        """
        headers = {
            **self.default_headers,
            "accept-encoding": "gzip, deflate",
            "host": "b-graph.facebook.com",
            "cookie": cookie
        }

        successful_shares = 0
        total_attempts = 0
        max_retries = 3
        error_count = 0

        print(f"{Fore.CYAN}Starting share operation...{Style.RESET_ALL}")

        while successful_shares < share_count and total_attempts < share_count * max_retries:
            try:
                # Check sharing limits
                can_share, remaining = await self.check_share_limit(session, token)
                if not can_share:
                    return successful_shares, f"Sharing limit reached. Try again later. Completed {successful_shares} shares."

                post_url = (f"{self.share_api_url}?link={self.mbasic_url}/{post_path}"
                           f"&published=0&access_token={token}")

                async with session.post(post_url, headers=headers, timeout=30) as response:
                    try:
                        data = await response.json()
                    except json.JSONDecodeError:
                        data = {"error": {"message": "Invalid JSON response"}}

                    if "id" in data:
                        successful_shares += 1
                        error_count = 0  # Reset error count on success
                        print(f"{Fore.GREEN}[{successful_shares}/{share_count}] "
                              f"Share successful{Style.RESET_ALL}")
                    else:
                        error_msg = data.get("error", {}).get("message", "Unknown error")
                        error_count += 1
                        print(f"{Fore.YELLOW}Share attempt failed: {error_msg}{Style.RESET_ALL}")
                        
                        if "spam" in error_msg.lower():
                            return successful_shares, "Spam detection triggered. Stopping."
                        elif error_count >= 3:
                            return successful_shares, f"Multiple errors occurred: {error_msg}"

                total_attempts += 1
                if successful_shares < share_count:
                    print(f"{Fore.CYAN}Waiting {delay} seconds before next share...{Style.RESET_ALL}")
                    await asyncio.sleep(delay)

            except asyncio.TimeoutError:
                error_count += 1
                print(f"{Fore.RED}Request timed out. Retrying...{Style.RESET_ALL}")
                await asyncio.sleep(delay)
            except Exception as e:
                error_count += 1
                print(f"{Fore.RED}Error during share: {str(e)}{Style.RESET_ALL}")
                if error_count >= 3:
                    return successful_shares, f"Multiple errors occurred: {str(e)}"
                await asyncio.sleep(delay)

        completion_message = (f"Completed {successful_shares} out of {share_count} shares "
                            f"({total_attempts} total attempts)")
        return successful_shares, completion_message

    def share_post(self, cookie: str, post_url: str, share_count: int, delay: int) -> Tuple[bool, str]:
        """
        Main method to handle post sharing.
        Returns tuple of (success, message).
        """
        async def share():
            async with aiohttp.ClientSession() as session:
                # Validate post URL
                valid, post_path = self.validate_post_url(post_url)
                if not valid:
                    return False, post_path

                # Get access token
                token, error = await self.get_token(session, cookie)
                if not token:
                    return False, error

                # Perform sharing
                shares_completed, message = await self.do_share(
                    session, token, cookie, post_path, share_count, delay
                )

                return shares_completed > 0, message

        try:
            return asyncio.run(share())
        except Exception as e:
            return False, f"Share operation failed: {str(e)}"

    def get_share_stats(self) -> Dict:
        """Get sharing statistics and limits."""
        return {
            "max_shares_per_hour": 30,
            "max_shares_per_day": 100,
            "recommended_delay": 5,
            "spam_detection_threshold": 50,
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
