#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: index.py
# Last Modified: 2025-05-14 16:02:40 UTC
# Author: sehraks

import os
import sys
from datetime import datetime
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Import local modules
from modules.cookie_manager import CookieManager
from modules.spam_sharing import SpamSharing
from modules.utils import Utils
from modules.update_settings import UpdateSettings

# Initialize rich console
console = Console()

class FacebookMonoToolkit:
    def __init__(self):
        """Initialize the Facebook MonoToolkit."""
        self.VERSION = "3.51"
        self.ORIGINAL_AUTHOR = "Greegmon"
        self.MODIFIED_BY = "Cerax"
        self.LAST_UPDATED = "May 14, 2025 +8 GMT"
        self.CURRENT_TIME = "2025-05-14 16:02:40"
        self.CURRENT_USER = "sehraks"
        
        # Initialize components
        self.cookie_manager = CookieManager()
        self.spam_sharing = SpamSharing()
        self.update_settings = UpdateSettings(self.display_banner)
        self.current_account: Optional[Dict] = None
        
        # Create necessary directories
        self._init_directories()

    def _init_directories(self):
        """Initialize necessary directories."""
        directories = ['cookies-storage', 'logs']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        """Display the tool banner."""
        banner = Panel(
            f"[white]Original: {self.ORIGINAL_AUTHOR}[/]\n"
            f"[white]Modified by: {self.MODIFIED_BY}[/]\n"
            f"[white]Version: {self.VERSION}[/]\n"
            f"[white]Last Updated: {self.LAST_UPDATED}[/]",
            style="bold magenta",
            title="[bold yellow]Facebook MonoToolkit[/]"
        )
        console.print(banner)

    def check_cookie_required(self):
        """Check if cookie is available."""
        if not self.current_account:
            console.print(Panel(
                "[bold white]❕ Please login first using the Manage Cookies option.[/]",
                style="bold red"
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
                    f"[bold green] Current Account: {self.current_account['name']}[/]", 
                    style="bold green"
                ))

            menu_panel = Panel(
                "[bold yellow][1] Manage Cookies[/]\n"
                "[bold cyan][2] Spam Sharing Post[/]\n"
                "[bold white][3] Settings[/]\n"
                "[bold red][4] Exit[/]",
                title="[bold white] Main Menu[/]",
                style="bold magenta"
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
                console.print(Panel(
                    "[bold white]👋 Thank you for using Facebook MonoToolkit![/]", 
                    style="bold cyan"
                ))
                sys.exit(0)
            else:
                console.print(Panel(
                    "[bold white]❕ Invalid choice! Please try again.[/]", 
                    style="bold red"
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
            console.print(Panel(
                "[bold yellow]🔑 Cookie Management[/]",
                style="bold yellow"
            ))
            
            # Always show all menu options
            menu_panel = Panel(
                "[bold white][1] Enter your cookie[/]\n"
                "[bold white][2] Cookie Settings and Storage[/]\n"
                "[bold white][3] Back to Main Menu[/]",
                title="[bold white]Cookie Management[/]",
                style="bold yellow"
            )
            console.print(menu_panel)
            
            choice = console.input("[bold yellow]Select an option: [/]")
            choice = choice.strip()

            if choice == "1":
                self.add_new_cookie()
            elif choice == "2":
                if not self.cookie_manager.has_cookies():
                    console.print(Panel(
                        "[bold red]❕ Enter your cookie first.[/]",
                        style="bold yellow"
                    ))
                    console.input("[bold white]Press Enter to continue...[/]")
                    continue
                self.cookie_settings_menu()
            elif choice == "3":
                break
            else:
                console.print(Panel(
                    "[bold white]❌ Invalid choice! Please try again.[/]", 
                    style="bold red"
                ))
                console.input("[bold white]Press Enter to continue...[/]")

    def add_new_cookie(self):
        """Handle adding a new cookie."""
        self.clear_screen()
        self.display_banner()
        console.print(Panel(
            "[bold yellow] Add New Cookie[/]",
            style="bold yellow"
        ))
        
        console.print("[bold]Enter your Facebook cookie (JSON or semicolon-separated format):[/]")
        console.print("[bold yellow]Note: Cookie must contain c_user and xs values[/]\n")
        
        cookie = console.input("[bold green]Cookie: [/]")
        cookie = cookie.strip()
        
        if not cookie:
            console.print(Panel(
                "[bold white]❕ Cookie cannot be empty![/]",
                style="bold red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return

        success, message = self.cookie_manager.add_cookie(cookie)
        
        if success:
            if not self.current_account:
                self.current_account = self.cookie_manager.get_all_accounts()[-1]
            console.print(Panel(
                "[bold green]✅ Cookie added successfully![/]",
                style="bold green"
            ))
        else:
            # Show error message only once
            console.print(Panel(
                f"[bold white]❕ {message}[/]",
                style="bold red"
            ))
        
        Utils.log_activity("Add Cookie", success, message)
        console.input("[bold white]Press Enter to continue...[/]")

    def cookie_settings_menu(self):
        """Handle cookie settings and storage menu."""
        while True:
            self.clear_screen()
            self.display_banner()
            console.print(Panel(
                "[bold yellow] Cookie Settings and Storage[/]",
                style="bold yellow"
            ))
            
            accounts = self.cookie_manager.get_all_accounts()
            for idx, account in enumerate(accounts, 1):
                status = "Logged in" if account == self.current_account else "Logged out"
                console.print(f"[bold yellow]— Account {idx}[/]")
                console.print(f"[bold white]Name: {account['name']}[/]")
                status_color = "green" if status == "Logged in" else "red"
                console.print(f"[bold {status_color}]Status: {status}[/]")
                if account != self.current_account:
                    console.print(f"[bold yellow][{idx}] Select[/]")
                console.print(f"[bold red][R{idx}] Remove[/]")
                console.print()

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
                        confirm = console.input(f"[bold red]Are you sure you want to remove {account_to_remove['name']}? (y/N): [/]").strip().lower()
                        if confirm == 'y':
                            if account_to_remove == self.current_account:
                                self.current_account = None
                            success = self.cookie_manager.remove_cookie(account_to_remove)
                            if success:
                                console.print(Panel(
                                    f"[bold green]✅ Successfully removed account: {account_to_remove['name']}[/]",
                                    style="bold green"
                                ))
                            else:
                                console.print(Panel(
                                    "[bold white]❕ Failed to remove account![/]",
                                    style="bold yellow"
                                ))
                    else:
                        console.print(Panel(
                            "[bold white]❕ Invalid selection![/]",
                            style="bold red"
                        ))
                except (ValueError, IndexError):
                    console.print(Panel(
                        "[bold white]❕ Invalid input![/]",
                        style="bold red"
                    ))
            else:
                try:
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(accounts):
                        if accounts[choice_idx] != self.current_account:
                            self.current_account = accounts[choice_idx]
                            console.print(Panel(
                                f"[bold green]✅ Successfully switched to account: {self.current_account['name']}[/]",
                                style="bold green"
                            ))
                        else:
                            console.print(Panel(
                                "[bold white]❕ This account is already selected.[/]",
                                style="bold yellow"
                            ))
                    else:
                        console.print(Panel(
                            "[bold white]❕ Invalid selection![/]",
                            style="bold red"
                        ))
                except ValueError:
                    console.print(Panel(
                        "[bold white]❕ Invalid input![/]",
                        style="bold red"
                    ))
            
            console.input("[bold white]Press Enter to continue...[/]")

    def spam_sharing_menu(self):
        """Handle spam sharing functionality."""
        self.clear_screen()
        self.display_banner()
        console.print(Panel(
            "[bold cyan] Spam Sharing[/]",
            style="bold white"
        ))
        
        post_url = console.input("[bold green]🔗 Enter the Facebook post URL: [/]")
        post_url = post_url.strip()
        
        if not Utils.validate_url(post_url):
            console.print(Panel(
                "[bold white]❕ Invalid Facebook URL![/]",
                style="bold red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return

        success, share_count = Utils.validate_input(
            "[bold green] Number of shares: [/]",
            int,
            min_val=1,
            max_val=100000
        )
        
        if not success:
            console.input("[bold white]Press Enter to continue...[/]")
            return

        success, delay = Utils.validate_input(
            "[bold green] Delay between shares (seconds): [/]",
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
                style="bold green"
            ))
        else:
            console.print(Panel(
                f"[bold red]❕ {message}[/]",
                style="bold yellow"
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
