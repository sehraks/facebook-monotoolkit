#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/friend_scraper.py
# Last Modified: 2025-05-13 14:21:33 UTC
# Author: sehraks
# Description: Advanced friend scraper for Facebook MonoToolkit

import os
import sys
import json
import re
import asyncio
import aiohttp
from typing import List, Dict, Tuple, Optional, Set
from datetime import datetime
from bs4 import BeautifulSoup
from colorama import Fore, Style
from .utils import Utils

class FriendScraper:
    def __init__(self) -> None:
        """Initialize FriendScraper with advanced configuration."""
        # Base configuration
        self.base_url = 'https://mbasic.facebook.com'
        self.friends_url = f"{self.base_url}/friends/center/friends"
        self.output_dir = "data/friends"
        self.max_retries = 3
        self.delay = 2
        
        # State tracking
        self.friends_data: List[Dict] = []
        self.processed_uids: Set[str] = set()
        self.error_count = 0
        self.success_count = 0
        self.start_time = None
        
        # Initialize directory
        os.makedirs(self.output_dir, exist_ok=True)
        
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

    async def _make_request(self, session: aiohttp.ClientSession, url: str, retry_count: int = 0) -> Optional[str]:
        """
        Make HTTP request with retry mechanism.
        
        Args:
            session (aiohttp.ClientSession): Active session
            url (str): Target URL
            retry_count (int): Current retry attempt
            
        Returns:
            Optional[str]: HTML content if successful, None otherwise
        """
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                elif response.status == 404:
                    return None
                elif retry_count < self.max_retries:
                    await asyncio.sleep(self.delay * (retry_count + 1))
                    return await self._make_request(session, url, retry_count + 1)
                return None
        except Exception as e:
            Utils.log_activity("HTTP Request", False, f"Error: {str(e)}")
            return None

    async def _extract_friend_data(self, html_content: str) -> List[Dict]:
        """
        Extract friend information from HTML content.
        
        Args:
            html_content (str): HTML content from Facebook page
            
        Returns:
            List[Dict]: List of friend data dictionaries
        """
        friends = []
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            friend_elements = soup.find_all(['table', 'div'], {'role': 'presentation'})

            for element in friend_elements:
                try:
                    # Find friend link
                    link = element.find('a')
                    if not link:
                        continue

                    href = link.get('href', '')
                    if not href:
                        continue

                    # Extract name
                    name = link.text.strip()
                    if not name:
                        continue

                    # Extract UID or username
                    uid = None
                    profile_url = None

                    # Try numeric ID first
                    uid_match = re.search(r'(?:profile\.php\?id=|/profile/|\/?)(\d{6,})(?:\?|$|\/)', href)
                    if uid_match:
                        uid = uid_match.group(1)
                        profile_url = f"https://facebook.com/profile.php?id={uid}"
                    else:
                        # Try username
                        username_match = re.search(r'(?:\/|\?)([a-zA-Z0-9\._]+)(?:\?|$|\/)', href)
                        if username_match:
                            username = username_match.group(1)
                            if username not in ['profile.php', 'friends', 'center']:
                                uid = username
                                profile_url = f"https://facebook.com/{uid}"

                    if uid and uid not in self.processed_uids:
                        self.processed_uids.add(uid)
                        self.success_count += 1
                        friends.append({
                            'uid': uid,
                            'name': name,
                            'profile_url': profile_url,
                            'scraped_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
                        })

                except Exception as e:
                    self.error_count += 1
                    Utils.log_activity("Friend Data Extraction", False, str(e))
                    continue

        except Exception as e:
            self.error_count += 1
            Utils.log_activity("HTML Parsing", False, str(e))

        return friends

    async def _get_next_page(self, html_content: str) -> Optional[str]:
        """
        Get URL for the next page of friends.
        
        Args:
            html_content (str): Current page HTML content
            
        Returns:
            Optional[str]: Next page URL or None if no more pages
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Try multiple possible next page patterns
            patterns = [
                re.compile(r'See More|Show more|View more|Next|More', re.I),
                re.compile(r'Lihat Teman Lainnya|Lihat Selengkapnya', re.I),
                re.compile(r'Tampilkan lainnya', re.I)
            ]
            
            for pattern in patterns:
                next_link = soup.find('a', string=pattern)
                if next_link and 'href' in next_link.attrs:
                    return self.base_url + next_link['href']
            
            return None
        except Exception:
            return None

    async def scrape_friends(self, cookie: str) -> Tuple[bool, str]:
        """
        Main method to scrape friend data.
        
        Args:
            cookie (str): Facebook cookie
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            self.start_time = datetime.utcnow()
            self.friends_data = []
            self.processed_uids.clear()
            self.error_count = 0
            self.success_count = 0

            headers = self.headers.copy()
            headers['cookie'] = cookie

            async with aiohttp.ClientSession(headers=headers) as session:
                current_url = self.friends_url
                page = 1

                while current_url:
                    # Add delay between requests
                    if page > 1:
                        await asyncio.sleep(self.delay)

                    Utils.print_status(f"Scanning page {page}...", "info")
                    
                    html_content = await self._make_request(session, current_url)
                    if not html_content:
                        break

                    new_friends = await self._extract_friend_data(html_content)
                    if new_friends:
                        self.friends_data.extend(new_friends)
                        Utils.print_status(
                            f"Found {len(self.friends_data)} friends so far...",
                            "info"
                        )

                    current_url = await self._get_next_page(html_content)
                    page += 1

                if not self.friends_data:
                    return False, "No friends found. Please check your cookie."

                # Save the scraped data
                if self.save_friends_data():
                    duration = (datetime.utcnow() - self.start_time).total_seconds()
                    return True, (
                        f"Successfully scraped {len(self.friends_data)} friends "
                        f"in {duration:.1f} seconds"
                    )
                return False, "Failed to save friend data"

        except Exception as e:
            return False, f"Scraping error: {str(e)}"

    def save_friends_data(self) -> bool:
        """Save scraped friend data to JSON file."""
        try:
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"friends_data_{timestamp}.json"
            filepath = os.path.join(self.output_dir, filename)

            data = {
                "metadata": {
                    "scraped_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'),
                    "total_friends": len(self.friends_data),
                    "success_count": self.success_count,
                    "error_count": self.error_count,
                    "duration_seconds": (datetime.utcnow() - self.start_time).total_seconds()
                },
                "friends": self.friends_data
            }

            return Utils.save_json(data, filepath)
        except Exception as e:
            Utils.log_activity("Save Data", False, str(e))
            return False

    def get_friends_data(self) -> List[Dict]:
        """Get the scraped friends data."""
        return self.friends_data.copy()
