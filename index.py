#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: index.py
# Author: sehraks

import os
import sys
import requests
import re
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import local modules
from modules.cookie_manager import CookieManager
from modules.spam_sharing import SpamSharing
from modules.utils import Utils
from modules.update_settings import UpdateSettings
from modules.fb_login import FacebookLogin
from modules.cookie_database import CookieDatabase
from modules.fb_guard import FacebookGuard

# Initialize rich console
console = Console()

class FacebookMonoToolkit:
    def __init__(self):
        """Initialize the Facebook MonoToolkit."""
        # Initialize account_data
        self.account_data = None
        self.current_account = None
        
        # Read version from changelogs.txt
        try:
            with open("changelogs.txt", "r") as f:
                first_line = f.readline().strip()
                self.VERSION = first_line.replace("Version ", "")
        except:
            self.VERSION = "X.XX"  # Fallback version if file read fails
            
        self.ORIGINAL_AUTHOR = "Greegmon"
        self.MODIFIED_BY = "Cerax"
        
        # Get current Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        self.LAST_UPDATED = philippines_time.strftime("%B %d, %Y")
        self.CURRENT_TIME = philippines_time.strftime("%I:%M %p")
        self.CURRENT_USER = "sehraks"  # Updated user login
        
        # Initialize components
        self.cookie_manager = CookieManager()
        self.spam_sharing = SpamSharing()
        self.update_settings = UpdateSettings(self.display_banner)
        self.fb_login = FacebookLogin()
        self.cookie_database = CookieDatabase(self.cookie_manager)
        self.fb_guard = FacebookGuard()
        
        # Create necessary directories
        self._init_directories()

        # Load the last active account
        self.current_account = self.cookie_manager.get_current_account()
        if self.current_account:
            self._load_account_data(self.current_account)

    
    def _load_account_data(self, account: Dict) -> None:
        """Load account data for the current account."""
        if account:
            self.account_data = {
                'name': account.get('name', 'Unknown User'),
                'user_id': account.get('user_id')
            }
        else:
            self.account_data = None
            
    def _init_directories(self):
        """Initialize necessary directories."""
        directories = ['cookies-storage', 'logs']
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                os.chmod(directory, 0o700)  # Secure permissions
            except Exception as e:
                console.print(f"[bold red]Error creating directory {directory}: {str(e)}[/]")

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        """Display the tool banner."""
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        current_time = philippines_time.strftime("%I:%M %p")
        current_date = philippines_time.strftime("%B %d, %Y")
        
        banner = Panel(
            f"[white]Original: {self.ORIGINAL_AUTHOR}[/]\n"
            f"[white]Modified by: {self.MODIFIED_BY}[/]\n"
            f"[white]Version: {self.VERSION}[/]\n"
            f"[white]Date: {current_date}[/]\n"
            f"[white]Time: {current_time} GMT+8[/]",
            style="bold magenta",
            title="[bold yellow]𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗠𝗢𝗡𝗢𝗧𝗢𝗢𝗟𝗞𝗜𝗧[/]",
            border_style="cyan"
        )
        console.print(banner)

    def check_cookie_required(self):
        """Check if cookie is available."""
        if not self.current_account:
            console.print(Panel(
                "[bold white]❕ Please login first using the Accounts Management option.[/]",
                style="bold indian_red",
                border_style="indian_red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return False
        return True

    def main(self):
        """Display and handle the main menu."""
        while True:
            self.clear_screen()
            self.display_banner()
            
            if self.current_account and self.account_data:
                console.print(Panel(
                    f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                    style="bold cyan",
                    border_style="cyan"
                ))

            menu_panel = Panel(
                "[bold white][1] Accounts Management[/]\n"
                "[bold white][2] Spam Sharing Post[/]\n"
                "[bold white][3] Profile Guard[/]\n"
                "[bold white][4] Settings[/]\n"
                "[bold red][5] Exit[/]",
                title="[bold white]𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨[/]",
                style="bold magenta",
                border_style="cyan"
            )
            console.print(menu_panel)

            choice = console.input("[bold yellow]Select an option (1-5): [/]")
            choice = choice.strip()

            if choice == "1":
                self.cookie_management_menu()
            elif choice == "2":
                if not self.check_cookie_required():
                    continue
                self.spam_sharing_menu()
            elif choice == "3":
                if not self.check_cookie_required():
                    continue
                self.handle_profile_guard()
            elif choice == "4":
                self.settings_menu()
            elif choice == "5":
                break
            else:
                console.print(Panel(
                    "[bold white]❕ Invalid choice! Please try again.[/]", 
                    style="bold indian_red",
                    border_style="indian_red"
                ))
                console.input("[bold white]Press Enter to continue...[/]")

    def settings_menu(self):
        """Handle settings menu."""
        self.update_settings.display_settings_menu()

    def cookie_management_menu(self):
        """Handle cookie management menu."""
        while True:
                self.clear_screen()
                self.display_banner()

                if self.current_account and self.account_data:
                        console.print(Panel(
                                f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                                style="bold cyan",
                                border_style="cyan"
                        ))

                console.print(Panel(
                        "[bold yellow]🔑 𝗔𝗖𝗖𝗢𝗨𝗡𝗧𝗦 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧[/]",
                        style="bold yellow",
                        border_style="yellow"
                ))

                menu_panel = Panel(
                        "[bold white][1] Enter your cookie[/]\n"
                        "[bold white][2] Login your Facebook account[/]\n"
                        "[bold white][3] Access your Facebook accounts[/]\n"
                        "[bold white][4] Cookies & Tokens Database[/]\n"
                        "[bold white][5] Back to Main Menu[/]",
                        title="[bold white]𝗦𝗘𝗟𝗘𝗖𝗧 𝗬𝗢𝗨𝗥 𝗖𝗛𝗢𝗜𝗖𝗘[/]",
                        style="bold yellow",
                        border_style="yellow"
                )
                console.print(menu_panel)

                choice = console.input("[bold yellow]Select an option: [/]")
                choice = choice.strip()

                if choice == "1":
                        self.add_new_cookie()
                elif choice == "2":
                        self.facebook_login()
                elif choice == "3":
                        if not self.cookie_manager.has_cookies():
                                console.print(Panel(
                                        "[bold white]❕ Add a cookie or login first.[/]",
                                        style="bold indian_red",
                                        border_style="indian_red"
                                ))
                                console.input("[bold white]Press Enter to continue...[/]")
                                continue
                        self.cookie_settings_menu()
                elif choice == "4":
                        if not self.cookie_manager.has_cookies():
                                console.print(Panel(
                                        "[bold white]❕ Add a cookie or login first.[/]",
                                        style="bold indian_red",
                                        border_style="indian_red"
                                ))
                                console.input("[bold white]Press Enter to continue...[/]")
                                continue
                        self.view_cookie_database()
                elif choice == "5":
                        break
                else:
                        console.print(Panel(
                                "[bold white]❕ Invalid choice! Please try again.[/]", 
                                style="bold indian_red",
                                border_style="indian_red"
                        ))
                        console.input("[bold white]Press Enter to continue...[/]")

    def facebook_login(self):
        """Handle Facebook login functionality."""
        self.clear_screen()
        self.display_banner()
        login_panel = Panel(
                "[bold yellow]Note:[/] [bold white]You can use either your email address or Facebook UID. Mobile numbers and usernames are currently not supported yet.[/]\n"
                "[bold indian_red]Caution:[/] [bold white]Refrain from using your main account, as doing so may cause lockout or suspension.[/]",
                title="[bold white]𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗟𝗢𝗚𝗜𝗡[/]",
                style="bold yellow",
                border_style="yellow"
        )
        console.print(login_panel)

        email = console.input("[bold yellow]🪪 Enter your credential: [/]")
        password = console.input("[bold yellow]🔑 Enter your password: [/]")

        # Attempt login with delay handling being managed by fb_login.py
        success, message, account_data = self.fb_login.login(email.strip(), password.strip())
            
        if success and account_data:
            # Store the account data before adding the cookie
            self.account_data = account_data
            
            # Pass both cookie and name to add_cookie
            success = self.cookie_manager.add_cookie(
                account_data['cookie'],
                account_data['name'],
                account_data['token']
            )[0]
            
            if success:
                self.current_account = None
                accounts = self.cookie_manager.get_all_accounts()
                for account in accounts:
                    if account['user_id'] == self.account_data['user_id']:
                        self.cookie_manager.set_current_account(account['id'])
                        self.current_account = account
                        break
        
        # Log the login attempt
        self.fb_login.log_login_attempt(email, success, message)
        console.input("[bold white]Press Enter to continue...[/]")

    def add_new_cookie(self):
        """Handle adding a new cookie."""
        self.clear_screen()
        self.display_banner()

        cookie_panel = Panel(
                "[bold yellow]Note:[/] [bold white]Use semi-colon separated format, cookie must contain c_user and xs values.[/]\n"
                "[bold indian_red]Caution:[/] [bold white]JSON format is not supported for some reason.[/]",
                title="[bold white]𝗔𝗗𝗗 𝗬𝗢𝗨𝗥 𝗖𝗢𝗢𝗞𝗜𝗘[/]",
                style="bold yellow",
                border_style="yellow"
        )
        console.print(cookie_panel)

        cookie = console.input("[bold yellow]🍪 Enter your cookie: [/]")
        cookie = cookie.strip()

        if not cookie:
            console.print(Panel(
                "[bold white]❕ Cookie cannot be empty![/]",
                style="bold indian_red",
                border_style="indian_red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return

        # Initial validation message with 1 second delay
        console.print(Panel(
            "[bold white]🔄 Validating cookie format...[/]",
            style="bold cyan",
            border_style="cyan"
        ))
        time.sleep(1)

        # Validate cookie format
        if "c_user=" not in cookie or "xs=" not in cookie:
            console.print(Panel(
                "[bold white]❕ Invalid cookie format! Cookie must contain c_user and xs values.[/]",
                style="bold indian_red",
                border_style="indian_red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return

        # Cookie validation success message with 1 second delay
        console.print(Panel(
            "[bold white]✅ Cookie format is valid![/]",
            style="bold green",
            border_style="green"
        ))
        time.sleep(1)

        # Get token before asking for name
        try:
            console.print(Panel(
                "[bold white]🔄 Getting account's token...[/]",
                style="bold cyan",
                border_style="cyan"
            ))
            time.sleep(1.5)  # Added delay before token extraction

            # Create a session to maintain cookies
            session = requests.Session()
            
            # Set the cookies in the session
            try:
                for cookie_item in cookie.split(';'):
                    if '=' in cookie_item:
                        name, value = cookie_item.strip().split('=', 1)
                        session.cookies.set(name, value)
            except Exception as e:
                console.print(Panel(
                    f"[bold white]❕ Error parsing cookie: {str(e)}[/]",
                    style="bold indian_red",
                    border_style="indian_red"
                ))
                time.sleep(1)

            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
                'Upgrade-Insecure-Requests': '1'
            }

            # Token extraction with multiple attempts
            access_token = None
            extraction_methods = [
                ('Ads Manager', 'https://adsmanager.facebook.com/adsmanager/', r'accessToken="(EAA[A-Za-z0-9]+)"'),
                ('Business Manager', 'https://business.facebook.com/content_management', r'"(EAA[A-Za-z0-9]+)"'),
                ('Feed Composer', 'https://www.facebook.com/composer/ocelot/async_loader/?publisher=feed', r'"accessToken":"(EAA[A-Za-z0-9]+)"')
            ]

            for method_name, url, pattern in extraction_methods:
                try:
                    console.print(Panel(
                        f"[bold white]🔄 Trying {method_name} method...[/]",
                        style="bold cyan",
                        border_style="cyan"
                    ))
                    time.sleep(1)  # Delay between attempts

                    response = session.get(url, headers=headers, timeout=30)
                    if response.ok:
                        token_match = re.search(pattern, response.text)
                        if token_match:
                            access_token = token_match.group(1)
                            console.print(Panel(
                                f"[bold white]✅ Token found using {method_name}![/]",
                                style="bold green",
                                border_style="green"
                            ))
                            time.sleep(1)
                            break
                except requests.Timeout:
                    console.print(Panel(
                        f"[bold white]❕ {method_name} request timed out[/]",
                        style="bold indian_red",
                        border_style="indian_red"
                    ))
                except Exception as e:
                    console.print(Panel(
                        f"[bold white]❕ Error with {method_name}: {str(e)}[/]",
                        style="bold indian_red",
                        border_style="indian_red"
                    ))

            if access_token:
                console.print(Panel(
                    "[bold green]✅ Successfully retrieved token![/]",
                    style="bold green",
                    border_style="green"
                ))
                time.sleep(1)
            else:
                console.print(Panel(
                    "[bold white]❕ Could not retrieve token. Continuing anyway...[/]",
                    style="bold indian_red",
                    border_style="indian_red"
                ))
                time.sleep(1)
                access_token = 'N/A'

        except Exception as e:
            console.print(Panel(
                f"[bold white]❕ Error during token extraction: {str(e)}. Continuing anyway...[/]",
                style="bold indian_red",
                border_style="indian_red"
            ))
            time.sleep(1)
            access_token = 'N/A'

        # Ask for account name if not in cookie
        account_name = None
        if "name=" not in cookie:
            account_name = console.input("[bold yellow]💳 Enter your name: [/]").strip()
            if not account_name:
                console.print(Panel(
                    "[bold white]❕ Please enter your Facebook account name[/]",
                    style="bold indian_red",
                    border_style="indian_red"
                ))
                console.input("[bold white]Press Enter to continue...[/]")
                return

        # Adding cookie to storage
        console.print(Panel(
            "[bold white]🔄 Saving account data...[/]",
            style="bold cyan",
            border_style="cyan"
        ))
        time.sleep(1)

        success, message = self.cookie_manager.add_cookie(cookie, account_name, access_token)

        if success:
            # Get the newly added account
            accounts = self.cookie_manager.get_all_accounts()
            new_account = accounts[-1]  # The newest account is the last one added

            # Set it as the current account
            self.current_account = new_account
            self.cookie_manager.set_current_account(new_account['id'])
            self._load_account_data(new_account)

            time.sleep(1)  # Delay before success message
            console.print(Panel(
                "[bold green]✅ Cookie added successfully!\n"
                f"👤 Account: {new_account['name']}\n"
                f"📩 UID: {new_account['user_id']}[/]",
                style="bold green",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[bold white]❕ {message}[/]",
                style="bold indian_red",
                border_style="indian_red"
            ))

        # Get Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        ph_timestamp = philippines_time.strftime("%B %d, %Y %I:%M %p")
        
        Utils.log_activity(f"Add Cookie (PH: {ph_timestamp}) by {self.CURRENT_USER}", success, message)
        console.input("[bold white]Press Enter to continue...[/]")

    def handle_profile_guard(self):
        """Handle Profile Guard operations."""
        if not self.current_account:
                console.print(Panel(
                        "[bold white]❕ Please select an account first[/]",
                        style="bold indian_red",
                        border_style="indian_red"
                ))
                console.input("[bold white]Press Enter to continue...[/]")
                return

        while True:
                self.clear_screen()
                self.display_banner()

                # Show current account
                console.print(Panel(
                        f"[bold white]Selected Account: {self.current_account['name']}[/]",
                        style="bold cyan",
                        border_style="cyan"
                ))

                # Show menu
                console.print(Panel(
                        "[bold yellow]Note:[/] [bold white]Make sure you turn off first your Facebook lock profile before proceeding to Facebook Profile Guard.[/]\n\n"
                        "[1] Activate your Facebook Profile Shield\n"
                        "[2] Deactivate your Facebook Profile Shield\n"
                        "[3] Back to Main Menu",
                        title="[bold white]🛡️ 𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 𝗚𝗨𝗔𝗥𝗗[/]",
                        style="bold cyan",
                        border_style="cyan"
                ))

                choice = console.input("[bold yellow]Enter your choice: [/]").strip()

                if choice == "1" or choice == "2":
                        enable = choice == "1"
                        success, message = self.fb_guard.toggle_profile_shield(self.current_account, enable)
                        
                        if success:
                                console.print(Panel(
                                        f"[bold white]✅ {message}\n"
                                        f"Name: {self.current_account['name']}\n"
                                        f"UID: {self.current_account['user_id']}[/]",
                                        style="bold green",
                                        border_style="green"
                                ))
                        else:
                                console.print(Panel(
                                        f"[bold white]❕ {message}[/]",
                                        style="bold indian_red",
                                        border_style="indian_red"
                                ))
                        
                        console.input("[bold white]Press Enter to continue...[/]")
                        
                elif choice == "3":
                        break
                else:
                        console.print(Panel(
                                "[bold white]❕ Invalid choice![/]",
                                style="bold indian_red",
                                border_style="indian_red"
                        ))
                        console.input("[bold white]Press Enter to continue...[/]")
    
    def cookie_settings_menu(self):
        """Handle cookie settings and storage menu."""
        while True:
            self.clear_screen()
            self.display_banner()
            
            if self.current_account and self.account_data:
                console.print(Panel(
                    f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                    style="bold cyan",
                    border_style="cyan"
                ))
            
            accounts = self.cookie_manager.get_all_accounts()
            for idx, account in enumerate(accounts, 1):
                status = "Logged in" if account == self.current_account else "Logged out"
                status_color = "green" if status == "Logged in" else "red"
                
                # Use the account's stored name directly
                display_name = account.get('name', 'Unknown User')
                
                account_panel = Panel(
                    f"[bold white]Name: {display_name}[/]\n"
                    f"[bold white]UID: {account['user_id']}[/]\n"
                    f"[bold {status_color}]Status: {status}[/]\n"
                    + (f"[bold yellow][{idx}] Select[/]\n" if account != self.current_account else "")
                    + f"[bold red][R{idx}] Remove[/]",
                    title=f"[bold yellow]📨 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 {idx}[/]",
                    style="bold yellow",
                    border_style="yellow"
                )
                console.print(account_panel)

            console.print("[bold white][0] Back[/]\n")

            choice = console.input("[bold yellow]Select an option: [/]")
            choice = choice.strip().upper()
            
            if choice == "0":
                break
                
            if choice.startswith('R'):
                try:
                    idx = int(choice[1:]) - 1
                    if 0 <= idx < len(accounts):
                        account_to_remove = accounts[idx]
                        if self.account_data and account_to_remove['user_id'] == self.account_data['user_id']:
                            display_name = self.account_data['name']
                        else:
                            display_name = "Unknown User"
                        confirm = console.input(f"[bold red]Are you sure you want to remove {display_name}? (y/N): [/]").strip().lower()
                        if confirm == 'y':
                            if account_to_remove == self.current_account:
                                self.current_account = None
                                self.account_data = None
                            success = self.cookie_manager.remove_cookie(account_to_remove)
                            if success:
                                console.print(Panel(
                                    f"[bold green]✅ Successfully removed account: {display_name}[/]",
                                    style="bold green",
                                    border_style="green"
                                ))
                            else:
                                console.print(Panel(
                                    "[bold white]❕ Failed to remove account![/]",
                                    style="bold indian_red",
                                    border_style="indian_red"
                                ))
                    else:
                        console.print(Panel(
                            "[bold white]❕ Invalid selection![/]",
                            style="bold indian_red",
                            border_style="indian_red"
                        ))
                except (ValueError, IndexError):
                    console.print(Panel(
                        "[bold white]❕ Invalid input![/]",
                        style="bold indian_red",
                        border_style="indian_red"
                    ))
            else:
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(accounts):
                        if accounts[choice_idx] != self.current_account:
                            self.current_account = accounts[choice_idx]
                            self.cookie_manager.set_current_account(self.current_account['id'])
                            self._load_account_data(self.current_account)
                            display_name = self.current_account['name']
                            console.print(Panel(
                                f"[bold green]✅ Successfully switched to account: {display_name}[/]",
                                style="bold green",
                                border_style="green"
                            ))
                        else:
                            console.print(Panel(
                                "[bold white]❕ This account is already selected.[/]",
                                style="bold indian_red",
                                border_style="indian_red"
                            ))
                    else:
                        console.print(Panel(
                            "[bold white]❕ Invalid selection![/]",
                            style="bold indian_red",
                            border_style="indian_red"
                        ))
                except ValueError:
                    console.print(Panel(
                        "[bold white]❕ Invalid input![/]",
                        style="bold indian_red",
                        border_style="indian_red"
                    ))
            
            console.input("[bold white]Press Enter to continue...[/]")

    def view_cookie_database(self):
        """Handle cookie database functionality."""
        self.clear_screen()
        self.display_banner()
        
        # Display selected account panel first
        if self.current_account and self.account_data:
                console.print(Panel(
                        f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                        style="bold cyan",
                        border_style="cyan"
                ))
        
        database_panel = Panel(
                "[bold yellow]Note:[/] [bold white]You can manage all your stored cookies and tokens here[/]\n"
                "[bold indian_red]Caution:[/] [bold white]Deleting cookies cannot be undone[/]",
                title="[bold white]𝗖𝗢𝗢𝗞𝗜𝗘𝗦 & 𝗧𝗢𝗞𝗘𝗡𝗦 𝗗𝗔𝗧𝗔𝗕𝗔𝗦𝗘[/]",
                style="bold cyan",
                border_style="cyan"
        )
        console.print(database_panel)

        menu_panel = Panel(
                "[bold white][1] View All Cookies & Tokens[/]\n"
                "[bold white][2] Back to Main Menu[/]",
                style="bold cyan",
                border_style="cyan"
        )
        console.print(menu_panel)

        choice = console.input("[bold cyan]Enter your choice: [/]")
        
        if choice == "1":
                self.clear_screen()
                self.display_banner()
                
                # Display selected account panel first
                if self.current_account and self.account_data:
                        console.print(Panel(
                                f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                                style="bold cyan",
                                border_style="cyan"
                        ))
                
                console.print(database_panel)
                
                accounts = self.cookie_manager.get_all_accounts()
                
                for idx, account in enumerate(accounts, 1):
                    # Format date and time
                    philippines_time = datetime.now(timezone(timedelta(hours=8)))
                    added_date = philippines_time.strftime("%B %d, %Y")
                    added_time = philippines_time.strftime("%I:%M %p +8 GMT (PH)")

                    # Mask cookie and token
                    cookie = account['cookie']
                    token = account.get('token', 'N/A')
                    masked_cookie = cookie[:20] + "..." + cookie[-10:] if len(cookie) > 30 else cookie
                    masked_token = token[:20] + "..." + token[-10:] if len(token) > 30 else token

                    cookie_panel = Panel(
                        f"[bold white]Name: {account.get('name', 'Unknown User')}[/]\n"
                        f"[bold white]Cookie: {masked_cookie}[/]\n"
                        f"[bold white]Token: {masked_token}[/]\n"
                        f"[bold white]Added Date: {added_date}[/]\n"
                        f"[bold white]Added Time: {added_time}[/]\n\n"
                        f"[bold yellow][C{idx}] Copy cookie[/]\n"
                        f"[bold yellow][T{idx}] Copy token[/]",
                        title=f"[bold yellow]📨 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 {idx}[/]",
                        style="bold yellow",
                        border_style="yellow"
                    )
                    console.print(cookie_panel)
                
                console.print("[bold white][0] Back[/]\n")

                while True:
                    copy_choice = console.input("[bold yellow]Select an option: [/]").strip().upper()
                    
                    if copy_choice == "0":  # If user enters 0
                        break
                        
                    if copy_choice.startswith(('C', 'T')):
                        try:
                            idx = int(copy_choice[1:]) - 1
                            if 0 <= idx < len(accounts):
                                try:
                                    import subprocess
                                    content = accounts[idx]['cookie'] if copy_choice.startswith('C') else accounts[idx].get('token', '')
                                    action = "Cookie" if copy_choice.startswith('C') else "Token"
                                    
                                    if not content and action == "Token":
                                        console.print(Panel(
                                            "[bold white]❕ No token available for this account![/]",
                                            style="bold indian_red",
                                            border_style="indian_red"
                                        ))
                                    else:
                                        process = subprocess.Popen(['termux-clipboard-set'], stdin=subprocess.PIPE)
                                        process.communicate(input=content.encode())
                                        console.print(Panel(
                                            f"[bold white]✅ {action} {idx + 1} copied to clipboard![/]",
                                            style="bold green",
                                            border_style="green"
                                        ))
                                except Exception as e:
                                    console.print(Panel(
                                        "[bold white]❕ Failed to copy to clipboard. Make sure Termux:API is installed.[/]",
                                        style="bold indian_red",
                                        border_style="indian_red"
                                    ))
                                console.input("[bold white]Press Enter to continue...[/]")
                                self.clear_screen()
                                self.display_banner()
                                if self.current_account and self.account_data:
                                    console.print(Panel(
                                        f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                                        style="bold cyan",
                                        border_style="cyan"
                                    ))
                                console.print(database_panel)
                                for idx, account in enumerate(accounts, 1):
                                    console.print(cookie_panel)
                                console.print("[bold white][0] Back[/]\n")
                                break
                            else:
                                console.print(Panel(
                                    "[bold white]❕ Invalid choice! Please try again.[/]",
                                    style="bold indian_red",
                                    border_style="indian_red"
                                ))
                                console.input("[bold white]Press Enter to continue...[/]")
                                self.clear_screen()
                                self.display_banner()
                                if self.current_account and self.account_data:
                                    console.print(Panel(
                                        f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                                        style="bold cyan",
                                        border_style="cyan"
                                    ))
                                console.print(database_panel)
                                for idx, account in enumerate(accounts, 1):
                                    console.print(cookie_panel)
                                console.print("[bold white][0] Back[/]\n")
                        except ValueError:
                            console.print(Panel(
                                "[bold white]❕ Invalid choice! Please try again.[/]",
                                style="bold indian_red",
                                border_style="indian_red"
                            ))
                            console.input("[bold white]Press Enter to continue...[/]")
                            self.clear_screen()
                            self.display_banner()
                            if self.current_account and self.account_data:
                                console.print(Panel(
                                    f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                                    style="bold cyan",
                                    border_style="cyan"
                                ))
                            console.print(database_panel)
                            for idx, account in enumerate(accounts, 1):
                                console.print(cookie_panel)
                            console.print("[bold white][0] Back[/]\n")
                    else:
                        console.print(Panel(
                            "[bold white]❕ Invalid choice! Please try again.[/]",
                            style="bold indian_red",
                            border_style="indian_red"
                        ))
                        console.input("[bold white]Press Enter to continue...[/]")
                        self.clear_screen()
                        self.display_banner()
                        if self.current_account and self.account_data:
                            console.print(Panel(
                                f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                                style="bold cyan",
                                border_style="cyan"
                            ))
                        console.print(database_panel)
                        for idx, account in enumerate(accounts, 1):
                            console.print(cookie_panel)
                        console.print("[bold white][0] Back[/]\n")
                return
        elif choice == "2":
                return
        else:
                console.print(Panel(
                        "[bold white]❕ Invalid choice! Please try again.[/]",
                        style="bold indian_red",
                        border_style="indian_red"
                ))
                console.input("[bold white]Press Enter to continue...[/]")
                self.view_cookie_database()
            
    def spam_sharing_menu(self):
        """Handle spam sharing functionality."""
        self.clear_screen()
        self.display_banner()

        if self.current_account and self.account_data:
                console.print(Panel(
                        f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {self.account_data['name']}[/]",
                        style="bold cyan",
                        border_style="cyan"
                ))

        share_panel = Panel(
                "[bold yellow]Note:[/] [bold white]This code does not use Facebook's API for fewer restrictions.[/]\n"
                "[bold indian_red]Caution:[/] [bold white]Do not turn off your internet while the process is ongoing.[/]",
                title="[bold white]𝗦𝗣𝗔𝗠 𝗣𝗢𝗦𝗧 𝗦𝗛𝗔𝗥𝗘𝗥[/]",
                style="bold cyan",
                border_style="cyan"
        )
        console.print(share_panel)

        post_url = console.input("[bold green]🔗 Enter the Facebook post URL: [/]")
        post_url = post_url.strip()

        if not Utils.validate_url(post_url):
            console.print(Panel(
                "[bold white]❕ Invalid Facebook URL![/]",
                style="bold indian_red",
                border_style="indian_red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return

        success, share_count = Utils.validate_input(
            "[bold green]Number of shares: [/]",
            int,
            min_val=1,
            max_val=100000
        )

        if not success:
            console.input("[bold white]Press Enter to continue...[/]")
            return

        success, delay = Utils.validate_input(
            "[bold green]Delay between shares (seconds): [/]",
            int,
            min_val=1,
            max_val=60
        )

        if not success:
            console.input("[bold white]Press Enter to continue...[/]")
            return

        success, message = self.spam_sharing.share_post(
            self.current_account['cookie'],
            post_url,
            share_count,
            delay
        )

        if success:
            console.print(Panel(
                f"[bold green]✅ {message}[/]",
                style="bold green",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[bold white]❕ {message}[/]",
                style="bold indian_red",
                border_style="indian_red"
            ))

        Utils.log_activity("Share Post", success, message)
        console.input("[bold white]Press Enter to continue...[/]")

def main():
    """Main entry point of the application."""
    try:
        tool = FacebookMonoToolkit()
        tool.main()
    except KeyboardInterrupt:
        # Changed: Wrapped error message in Panel and fixed markup
        console.print(Panel(
            "[bold white]❕ Program interrupted by user.[/]",
            style="bold indian_red",
            border_style="indian_red"
        ))
        sys.exit(0)
    except Exception as e:
        # Changed: Fixed markup error in exception handling
        console.print(Panel(
            f"[bold white]❕ An unexpected error occurred: {str(e)}[/]",
            style="bold indian_red",
            border_style="indian_red"
        ))
        # Current timestamp in UTC format
        current_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        Utils.log_activity(f"System Error (UTC: {current_utc}) by {sehraks1}", False, str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
