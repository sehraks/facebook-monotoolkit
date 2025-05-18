#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: index.py
# Last Modified: May 16, 2025 04:40 PM +8 GMT
# Author: sehraks

import os
import sys
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

# Initialize rich console
console = Console()

class FacebookMonoToolkit:
    def __init__(self):
        """Initialize the Facebook MonoToolkit."""
        # Read version from changelogs.txt
        try:
            with open("changelogs.txt", "r") as f:
                first_line = f.readline().strip()
                self.VERSION = first_line.replace("Version ", "")
        except:
            self.VERSION = "4.62"  # Fallback version if file read fails
            
        self.ORIGINAL_AUTHOR = "Greegmon"
        self.MODIFIED_BY = "Cerax"
        
        # Get current Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        self.LAST_UPDATED = philippines_time.strftime("%B %d, %Y")
        self.CURRENT_TIME = philippines_time.strftime("%I:%M %p")
        self.CURRENT_USER = "sehraks"
        
        # Initialize components
        self.cookie_manager = CookieManager()
        self.spam_sharing = SpamSharing()
        self.update_settings = UpdateSettings(self.display_banner)
        self.fb_login = FacebookLogin()  # New component
        self.current_account: Optional[Dict] = None
        
        # Create necessary directories
        self._init_directories()

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
        # Get current Philippines time for display
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
            title="[bold yellow]Facebook MonoToolkit[/]",
            border_style="cyan"
        )
        console.print(banner)

    def check_cookie_required(self):
        """Check if cookie is available."""
        if not self.current_account:
            console.print(Panel(
                "[bold white]❕ Please login first using the Manage Cookies option.[/]",
                style="bold red",
                border_style="red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return False
        return True

    def main(self):
        """Display and handle the main menu."""
        while True:
            self.clear_screen()
            self.display_banner()
            
            if self.current_account:
                console.print(Panel(
                    f"[bold cyan]💠 Current Account: {self.current_account['name']}[/]", 
                    style="bold cyan",
                    border_style="cyan"
                ))

            menu_panel = Panel(
                "[bold white][1] Manage Cookies[/]\n"
                "[bold white][2] Spam Sharing Post[/]\n"
                "[bold white][3] Settings[/]\n"
                "[bold red][4] Exit[/]",
                title="[bold white]Main Menu[/]",
                style="bold magenta",
                border_style="cyan"
            )
            console.print(menu_panel)

            choice = console.input("[bold yellow]Select an option (1-4): [/]")
            choice = choice.strip()

            if choice == "1":
                self.cookie_management_menu()
            elif choice == "2":
                if not self.check_cookie_required():
                    continue
                self.spam_sharing_menu()
            elif choice == "3":
                self.settings_menu()
            elif choice == "4":
                break
            else:
                console.print(Panel(
                    "[bold white]❌ Invalid choice! Please try again.[/]", 
                    style="bold red",
                    border_style="red"
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
            
            if self.current_account:
                console.print(Panel(
                    f"[bold cyan]💠 Current Account: {self.current_account['name']}[/]",
                    style="bold cyan",
                    border_style="cyan"
                ))

            console.print(Panel(
                "[bold yellow]🔑 Cookie Management[/]",
                style="bold yellow",
                border_style="yellow"
            ))
            
            menu_panel = Panel(
                "[bold white][1] Enter your cookie[/]\n"
                "[bold white][2] Login your Facebook account[/]\n"
                "[bold white][3] Cookie Settings and Storage[/]\n"
                "[bold white][4] Back to Main Menu[/]",
                title="[bold white]Cookie Management[/]",
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
                        "[bold red]❕ Add a cookie or login first.[/]",
                        style="bold yellow",
                        border_style="yellow"
                    ))
                    console.input("[bold white]Press Enter to continue...[/]")
                    continue
                self.cookie_settings_menu()
            elif choice == "4":
                break
            else:
                console.print(Panel(
                    "[bold white]❌ Invalid choice! Please try again.[/]", 
                    style="bold white",
                    border_style="red"
                ))
                console.input("[bold white]Press Enter to continue...[/]")

    def facebook_login(self):
        """Handle Facebook login functionality."""
        self.clear_screen()
        self.display_banner()
        console.print(Panel(
            "[bold yellow]Facebook Login[/]",
            style="bold yellow",
            border_style="yellow"
        ))
        
        console.print("[bold yellow]Login using Email/UID:[/]")
        console.print("[bold cyan]Note: You can use either your email address or Facebook UID[/]\n")
        
        email = console.input("[bold yellow]📧 Enter your email/UID: [/]")
        password = console.input("[bold yellow]🔑 Enter your password: [/]")
        
        # Validate credentials format
        valid, message = self.fb_login.validate_credentials(email.strip(), password.strip())
        if not valid:
            console.print(Panel(
                f"[bold white]❕ {message}[/]",
                style="bold red",
                border_style="red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return

        console.print(Panel(
            "[bold cyan]🔄 Logging in to Facebook...[/]",
            style="bold cyan",
            border_style="cyan"
        ))

        # Attempt login
        success, message, account_data = self.fb_login.login(email.strip(), password.strip())
        
        if success and account_data:
            # Add account to cookie manager
            success = self.cookie_manager.add_cookie(account_data['cookie'])[0]
            
            if success:
                # Set as current account immediately after successful login
                self.current_account = None  # Clear current selection first
                accounts = self.cookie_manager.get_all_accounts()
                for account in accounts:
                    if account['user_id'] == account_data['user_id']:
                        self.current_account = account
                        break
                
                console.print(Panel(
                    f"[bold green]✅ {message}[/]\n"
                    f"[bold green]👤 Account: {account_data['name']} / {account_data['user_id']}[/]\n"
                    "[bold green]✓ Account automatically selected[/]",
                    style="bold green",
                    border_style="green"
                ))
            else:
                console.print(Panel(
                    "[bold red]❌ Failed to save account data[/]",
                    style="bold red",
                    border_style="red"
                ))
        else:
            console.print(Panel(
                f"[bold red]❌ {message}[/]",
                style="bold red",
                border_style="red"
            ))
        
        # Log the login attempt
        self.fb_login.log_login_attempt(email, success, message)
        console.input("[bold white]Press Enter to continue...[/]")

    def add_new_cookie(self):
        """Handle adding a new cookie."""
        self.clear_screen()
        self.display_banner()
        console.print(Panel(
            "[bold yellow]Add New Cookie[/]",
            style="bold yellow",
            border_style="yellow"
        ))
        
        console.print("[bold]Enter your Facebook cookie (JSON or semicolon-separated format):[/]")
        console.print("[bold yellow]Note: Cookie must contain c_user and xs values[/]\n")
        
        cookie = console.input("[bold green]Cookie: [/]")
        cookie = cookie.strip()
        
        if not cookie:
            console.print(Panel(
                "[bold white]❕ Cookie cannot be empty![/]",
                style="bold red",
                border_style="red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return

        success, message = self.cookie_manager.add_cookie(cookie)
        
        if success:
            if not self.current_account:
                self.current_account = self.cookie_manager.get_all_accounts()[-1]
            console.print(Panel(
                "[bold green]✅ Cookie added successfully![/]",
                style="bold green",
                border_style="green"
            ))
        else:
            console.print(Panel(
                f"[bold white]❕ {message}[/]",
                style="bold red",
                border_style="red"
            ))
        
        Utils.log_activity("Add Cookie", success, message)
        console.input("[bold white]Press Enter to continue...[/]")

    def cookie_settings_menu(self):
        """Handle cookie settings and storage menu."""
        while True:
            self.clear_screen()
            self.display_banner()
            
            if self.current_account:
                console.print(Panel(
                    f"[bold cyan]💠 Current Account: {self.current_account['name'].split('Facebook_')[0].strip()}[/]",
                    style="bold cyan",
                    border_style="cyan"
                ))

            console.print(Panel(
                "[bold yellow]Cookie Settings and Storage[/]",
                style="bold yellow",
                border_style="yellow"
            ))
            
            accounts = self.cookie_manager.get_all_accounts()
            for idx, account in enumerate(accounts, 1):
                status = "Logged in" if account == self.current_account else "Logged out"
                status_color = "green" if status == "Logged in" else "red"
                
                # Clean up the name to remove Facebook_ prefix if it exists
                display_name = account['name']
                if 'Facebook_' in display_name:
                    display_name = display_name.split('Facebook_')[0].strip()
                if not display_name:  # If name becomes empty after cleanup
                    display_name = "Unknown User"
                
                account_panel = Panel(
                    f"[bold white]Name: {display_name}[/]\n"
                    f"[bold white]UID: {account['user_id']}[/]\n"
                    f"[bold {status_color}]Status: {status}[/]\n"
                    + (f"[bold yellow][{idx}] Select[/]\n" if account != self.current_account else "")
                    + f"[bold red][R{idx}] Remove[/]",
                    title=f"[bold yellow]📨 ACCOUNT {idx}[/]",
                    style="bold yellow",
                    border_style="yellow"
                )
                console.print(account_panel)
                console.print()  # Add space between accounts

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
                        display_name = account_to_remove['name'].split('Facebook_')[0].strip() or "Unknown User"
                        confirm = console.input(f"[bold red]Are you sure you want to remove {display_name}? (y/N): [/]").strip().lower()
                        if confirm == 'y':
                            if account_to_remove == self.current_account:
                                self.current_account = None
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
                                    style="bold yellow",
                                    border_style="yellow"
                                ))
                    else:
                        console.print(Panel(
                            "[bold white]❕ Invalid selection![/]",
                            style="bold red",
                            border_style="red"
                        ))
                except (ValueError, IndexError):
                    console.print(Panel(
                        "[bold white]❕ Invalid input![/]",
                        style="bold red",
                        border_style="red"
                    ))
            else:
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(accounts):
                        if accounts[choice_idx] != self.current_account:
                            self.current_account = accounts[choice_idx]
                            display_name = self.current_account['name'].split('Facebook_')[0].strip() or "Unknown User"
                            console.print(Panel(
                                f"[bold green]✅ Successfully switched to account: {display_name}[/]",
                                style="bold green",
                                border_style="green"
                            ))
                        else:
                            console.print(Panel(
                                "[bold white]❕ This account is already selected.[/]",
                                style="bold yellow",
                                border_style="yellow"
                            ))
                    else:
                        console.print(Panel(
                            "[bold white]❕ Invalid selection![/]",
                            style="bold red",
                            border_style="red"
                        ))
                except ValueError:
                    console.print(Panel(
                        "[bold white]❕ Invalid input![/]",
                        style="bold red",
                        border_style="red"
                    ))
            
            console.input("[bold white]Press Enter to continue...[/]")

    def spam_sharing_menu(self):
        """Handle spam sharing functionality."""
        self.clear_screen()
        self.display_banner()
        console.print(Panel(
            "[bold cyan]Spam Sharing[/]",
            style="bold white",
            border_style="cyan"
        ))
        
        post_url = console.input("[bold green]🔗 Enter the Facebook post URL: [/]")
        post_url = post_url.strip()
        
        if not Utils.validate_url(post_url):
            console.print(Panel(
                "[bold white]❕ Invalid Facebook URL![/]",
                style="bold red",
                border_style="red"
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
                f"[bold red]❕ {message}[/]",
                style="bold yellow",
                border_style="yellow"
            ))
        
        Utils.log_activity("Share Post", success, message)
        console.input("[bold white]Press Enter to continue...[/]")

def main():
    """Main entry point of the application."""
    try:
        tool = FacebookMonoToolkit()
        tool.main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]❕ Program interrupted by user.[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold yellow]❕ An unexpected error occurred: {str(e)}[/]")
        Utils.log_activity("System Error", False, str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
