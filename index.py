#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: index.py
# Last Modified: 2025-05-13 14:19:28 UTC
# Author: sehraks

import os
import sys
import json
import asyncio
from datetime import datetime
from typing import Dict, Optional
from colorama import init, Fore, Style

# Import local modules
from modules.cookie_manager import CookieManager
from modules.spam_sharing import SpamSharing
from modules.profile_guard import ProfileGuard
from modules.friend_scraper import FriendScraper
from modules.utils import Utils

# Initialize colorama
init(autoreset=True)

class FacebookMonoToolkit:
    def __init__(self):
        """Initialize the Facebook MonoToolkit."""
        self.VERSION = "1.0.0"
        self.AUTHOR = "sehraks"
        self.TOOL_NAME = "Facebook MonoToolkit"
        self.LAST_UPDATED = "2025-05-13 14:19:28 UTC"
        
        # Initialize components
        self.cookie_manager = CookieManager()
        self.spam_sharing = SpamSharing()
        self.profile_guard = ProfileGuard()
        self.friend_scraper = FriendScraper()
        self.current_account: Optional[Dict] = None
        
        # Create necessary directories
        self._init_directories()

    def _init_directories(self) -> None:
        """Initialize necessary directories."""
        directories = ['cookies-storage', 'logs', 'data']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def display_banner(self) -> None:
        """Display the tool banner."""
        Utils.print_banner(
            title=self.TOOL_NAME,
            version=self.VERSION,
            author=self.AUTHOR,
            last_updated=self.LAST_UPDATED
        )

    def check_cookie_required(self) -> bool:
        """Check if cookie is available."""
        if not self.current_account:
            Utils.print_status(
                "Please login first using the Manage Cookies option.", 
                "error"
            )
            input("\nPress Enter to continue...")
            return False
        return True

    async def main_menu(self) -> None:
        """Display and handle the main menu."""
        while True:
            self.display_banner()
            
            if self.current_account:
                print(f"{Fore.GREEN}Current Account: {self.current_account['name']}{Style.RESET_ALL}\n")

            options = {
                "1": "Manage Cookies",
                "2": "Spam Sharing Post",
                "3": "Activate Profile Picture Guard",
                "4": "Scrape your friend names and UIDs",
                "5": "Exit"
            }
            
            Utils.print_menu(options, "Main Menu")
            choice = Utils.get_menu_choice(options)

            if choice == "1":
                self.cookie_management_menu()
            elif choice == "2":
                if not self.check_cookie_required():
                    continue
                self.spam_sharing_menu()
            elif choice == "3":
                if not self.check_cookie_required():
                    continue
                self.profile_guard_menu()
            elif choice == "4":
                if not self.check_cookie_required():
                    continue
                await self.friend_scraper_menu()
            elif choice == "5":
                Utils.print_status(f"Thank you for using {self.TOOL_NAME}!", "success")
                sys.exit(0)

    def cookie_management_menu(self) -> None:
        """Handle cookie management menu."""
        while True:
            self.display_banner()
            print(f"{Fore.CYAN}=== Cookie Management ===\n")
            
            options = {
                "1": "Enter your cookie",
                "2": "Cookie Settings and Storage" if self.cookie_manager.has_cookies() else None,
                "3": "Back to Main Menu"
            }
            
            options = {k: v for k, v in options.items() if v is not None}
            
            Utils.print_menu(options, "Cookie Management")
            choice = Utils.get_menu_choice(options)

            if choice == "1":
                self.add_new_cookie()
            elif choice == "2" and self.cookie_manager.has_cookies():
                self.cookie_settings_menu()
            elif choice == "3":
                break

    def add_new_cookie(self) -> None:
        """Handle adding a new cookie."""
        self.display_banner()
        print(f"{Fore.CYAN}=== Add New Cookie ===\n")
        print("Enter your Facebook cookie (JSON or semicolon-separated format):")
        print(f"{Fore.YELLOW}Note: Cookie must contain c_user and xs values{Style.RESET_ALL}\n")
        
        cookie = input(f"{Fore.GREEN}Cookie: {Style.RESET_ALL}").strip()
        
        if not cookie:
            Utils.print_status("Cookie cannot be empty!", "error")
            input("\nPress Enter to continue...")
            return

        success, message = self.cookie_manager.add_cookie(cookie)
        
        if success:
            Utils.print_status(message, "success")
            if not self.current_account:
                self.current_account = self.cookie_manager.get_all_accounts()[-1]
        else:
            Utils.print_status(message, "error")
        
        Utils.log_activity("Add Cookie", success, message)
        input("\nPress Enter to continue...")

    def cookie_settings_menu(self) -> None:
        """Handle cookie settings and storage menu."""
        while True:
            self.display_banner()
            print(f"{Fore.CYAN}=== Cookie Settings and Storage ===\n")
            
            accounts = self.cookie_manager.get_all_accounts()
            for idx, account in enumerate(accounts, 1):
                status = "Logged in" if account == self.current_account else "Logged out"
                print(f"{Fore.YELLOW}— Account {idx}")
                print(f"{Fore.CYAN}Name: {account['name']}")
                print(f"Status: {Fore.GREEN if status == 'Logged in' else Fore.RED}{status}")
                if account != self.current_account:
                    print(f"{Fore.YELLOW}[{idx}] Select")
                print()

            print(f"{Fore.YELLOW}[0] Back\n")

            choice = input(f"{Fore.YELLOW}Select an option: {Style.RESET_ALL}")
            
            if choice == "0":
                break
                
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(accounts):
                    if accounts[choice_idx] != self.current_account:
                        self.current_account = accounts[choice_idx]
                        Utils.print_status(
                            f"Successfully switched to account: {self.current_account['name']}", 
                            "success"
                        )
                    else:
                        Utils.print_status("This account is already selected.", "warning")
                else:
                    Utils.print_status("Invalid selection!", "error")
            except ValueError:
                Utils.print_status("Invalid input!", "error")
            
            input("\nPress Enter to continue...")

    def spam_sharing_menu(self) -> None:
        """Handle spam sharing functionality."""
        self.display_banner()
        print(f"{Fore.CYAN}=== Spam Sharing ===\n")
        
        print("Enter the Facebook post URL:")
        post_url = input(f"{Fore.GREEN}URL: {Style.RESET_ALL}").strip()
        
        if not Utils.validate_url(post_url):
            Utils.print_status("Invalid Facebook URL!", "error")
            input("\nPress Enter to continue...")
            return

        success, share_count = Utils.validate_input(
            f"{Fore.GREEN}Number of shares: {Style.RESET_ALL}",
            int,
            min_val=1,
            max_val=100
        )
        
        if not success:
            input("\nPress Enter to continue...")
            return

        success, delay = Utils.validate_input(
            f"{Fore.GREEN}Delay between shares (seconds): {Style.RESET_ALL}",
            int,
            min_val=1,
            max_val=60
        )
        
        if not success:
            input("\nPress Enter to continue...")
            return

        print(f"\n{Fore.CYAN}Starting share operation...{Style.RESET_ALL}")
        
        success, message = self.spam_sharing.share_post(
            self.current_account['cookie'],
            post_url,
            share_count,
            delay
        )
        
        if success:
            Utils.print_status(message, "success")
        else:
            Utils.print_status(message, "error")
        
        Utils.log_activity("Share Post", success, message)
        input("\nPress Enter to continue...")

    def profile_guard_menu(self) -> None:
        """Handle profile guard functionality."""
        self.display_banner()
        print(f"{Fore.CYAN}=== Profile Picture Guard ===\n")

        print(f"{Fore.YELLOW}[!] Activate Profile Picture Guard? [y/n]")
        if not Utils.confirm_action(""):
            return
            
        print(f"\n{Fore.CYAN}Activating Profile Picture Guard...{Style.RESET_ALL}")
        
        success, message = self.profile_guard.activate_guard(
            self.current_account['cookie']
        )
        
        if success:
            Utils.print_status(message, "success")
        else:
            Utils.print_status(message, "error")
        
        Utils.log_activity("Profile Guard", success, message)
        input("\nPress Enter to continue...")

    async def friend_scraper_menu(self) -> None:
        """Handle friend scraping functionality."""
        self.display_banner()
        print(f"{Fore.CYAN}=== Friend Scraper ===\n")

        print(f"{Fore.YELLOW}[!] Scrape all of your friend names and UIDs [y/n]")
        if not Utils.confirm_action(""):
            return
            
        print(f"\n{Fore.CYAN}Starting friend data scraping...{Style.RESET_ALL}")
        
        success, message = await self.friend_scraper.scrape_friends(
            self.current_account['cookie']
        )
        
        if success:
            Utils.print_status(message, "success")
        else:
            Utils.print_status(message, "error")
        
        Utils.log_activity("Friend Scraper", success, message)
        input("\nPress Enter to continue...")

async def main():
    """Main entry point of the application."""
    try:
        tool = FacebookMonoToolkit()
        await tool.main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Program interrupted by user.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
        Utils.log_activity("System Error", False, str(e))
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
