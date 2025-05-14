#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: index.py
# Last Modified: 2025-05-14 03:56:52 UTC
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
        self.VERSION = "3.50"
        self.ORIGINAL_AUTHOR = "Greegmon"
        self.MODIFIED_BY = "Cerax"
        self.LAST_UPDATED = "May 14, 2025 +8 GMT"
        self.CURRENT_TIME = "2025-05-14 03:56:52"
        self.CURRENT_USER = "sehraks"
        
        # Initialize components
        self.cookie_manager = CookieManager()
        self.spam_sharing = SpamSharing()
        self.update_settings = UpdateSettings()
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
        self.clear_screen()
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
                "[bold red]⚠️ Please login first using the Manage Cookies option.[/]",
                style="bold red"
            ))
            console.input("[bold blue]Press Enter to continue...[/]")
            return False
        return True

    def main(self):
        """Display and handle the main menu."""
        while True:
            self.display_banner()
            
            if self.current_account:
                console.print(Panel(
                    f"[bold green]👤 Current Account: {self.current_account['name']}[/]", 
                    style="bold green"
                ))

            menu_panel = Panel(
                "[bold cyan][1] 🔑 Manage Cookies[/]\n"
                "[bold cyan][2] 📢 Spam Sharing Post[/]\n"
                "[bold cyan][3] ⚙️ Settings[/]\n"
                "[bold red][4] 🚪 Exit[/]",
                title="[bold yellow]📋 Main Menu[/]",
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
                    "[bold blue]👋 Thank you for using Facebook MonoToolkit![/]", 
                    style="bold blue"
                ))
                sys.exit(0)
            else:
                console.print(Panel(
                    "[bold red]❌ Invalid choice! Please try again.[/]", 
                    style="bold red"
                ))

    def settings_menu(self):
        """Handle settings menu."""
        self.display_banner()
        self.update_settings.display_settings_menu()

    def cookie_management_menu(self):
        """Handle cookie management menu."""
        while True:
            self.display_banner()
            console.print(Panel(
                "[bold cyan]🔑 Cookie Management[/]",
                style="bold cyan"
            ))
            
            options = [
                "[bold cyan][1] 📝 Enter your cookie[/]",
                "[bold cyan][2] ⚙️  Cookie Settings and Storage[/]" if self.cookie_manager.has_cookies() else None,
                "[bold yellow][3] 🔙 Back to Main Menu[/]"
            ]
            
            menu_panel = Panel(
                "\n".join([opt for opt in options if opt is not None]),
                title="[bold yellow]Cookie Management[/]",
                style="bold magenta"
            )
            console.print(menu_panel)
            
            choice = console.input("[bold yellow]Select an option: [/]")
            choice = choice.strip()

            if choice == "1":
                self.add_new_cookie()
            elif choice == "2" and self.cookie_manager.has_cookies():
                self.cookie_settings_menu()
            elif choice == "3":
                break
            else:
                console.print(Panel(
                    "[bold red]❌ Invalid choice! Please try again.[/]", 
                    style="bold red"
                ))

    def add_new_cookie(self):
        """Handle adding a new cookie."""
        self.display_banner()
        console.print(Panel(
            "[bold cyan]📝 Add New Cookie[/]",
            style="bold cyan"
        ))
        
        console.print("[bold]Enter your Facebook cookie (JSON or semicolon-separated format):[/]")
        console.print("[bold yellow]Note: Cookie must contain c_user and xs values[/]\n")
        
        cookie = console.input("[bold green]Cookie: [/]")
        cookie = cookie.strip()
        
        if not cookie:
            console.print(Panel(
                "[bold red]❌ Cookie cannot be empty![/]",
                style="bold red"
            ))
            console.input("[bold blue]Press Enter to continue...[/]")
            return

        success, message = self.cookie_manager.add_cookie(cookie)
        
        if success:
            if not self.current_account:
                self.current_account = self.cookie_manager.get_all_accounts()[-1]
        else:
            console.print(Panel(
                f"[bold red]❌ {message}[/]",
                style="bold red"
            ))
        
        Utils.log_activity("Add Cookie", success, message)
        console.input("[bold blue]Press Enter to continue...[/]")

    def cookie_settings_menu(self):
        """Handle cookie settings and storage menu."""
        while True:
            self.display_banner()
            console.print(Panel(
                "[bold cyan]⚙️  Cookie Settings and Storage[/]",
                style="bold cyan"
            ))
            
            accounts = self.cookie_manager.get_all_accounts()
            for idx, account in enumerate(accounts, 1):
                status = "Logged in" if account == self.current_account else "Logged out"
                console.print(f"[bold yellow]— Account {idx}[/]")
                console.print(f"[bold cyan]Name: {account['name']}[/]")
                status_color = "green" if status == "Logged in" else "red"
                console.print(f"[bold {status_color}]Status: {status}[/]")
                if account != self.current_account:
                    console.print(f"[bold yellow][{idx}] Select[/]")
                console.print(f"[bold red][R{idx}] Remove[/]")
                console.print()

            console.print("[bold yellow][0] 🔙 Back[/]\n")

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
                                    "[bold red]❌ Failed to remove account![/]",
                                    style="bold red"
                                ))
                    else:
                        console.print(Panel(
                            "[bold red]❌ Invalid selection![/]",
                            style="bold red"
                        ))
                except (ValueError, IndexError):
                    console.print(Panel(
                        "[bold red]❌ Invalid input![/]",
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
                                "[bold yellow]⚠️ This account is already selected.[/]",
                                style="bold yellow"
                            ))
                    else:
                        console.print(Panel(
                            "[bold red]❌ Invalid selection![/]",
                            style="bold red"
                        ))
                except ValueError:
                    console.print(Panel(
                        "[bold red]❌ Invalid input![/]",
                        style="bold red"
                    ))
            
            console.input("[bold blue]Press Enter to continue...[/]")

    def spam_sharing_menu(self):
        """Handle spam sharing functionality."""
        self.display_banner()
        console.print(Panel(
            "[bold cyan]📢 Spam Sharing[/]",
            style="bold cyan"
        ))
        
        post_url = console.input("[bold green]📌 Enter the Facebook post URL: [/]")
        post_url = post_url.strip()
        
        if not Utils.validate_url(post_url):
            console.print(Panel(
                "[bold red]❌ Invalid Facebook URL![/]",
                style="bold red"
            ))
            console.input("[bold blue]Press Enter to continue...[/]")
            return

        success, share_count = Utils.validate_input(
            "[bold green]🔢 Number of shares: [/]",
            int,
            min_val=1,
            max_val=100
        )
        
        if not success:
            console.input("[bold blue]Press Enter to continue...[/]")
            return

        success, delay = Utils.validate_input(
            "[bold green]⏱️  Delay between shares (seconds): [/]",
            int,
            min_val=1,
            max_val=60
        )
        
        if not success:
            console.input("[bold blue]Press Enter to continue...[/]")
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
                f"[bold red]❌ {message}[/]",
                style="bold red"
            ))
        
        Utils.log_activity("Share Post", success, message)
        console.input("[bold blue]Press Enter to continue...[/]")

def main():
    """Main entry point of the application."""
    try:
        tool = FacebookMonoToolkit()
        tool.main()  # Changed from main_menu to main
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⚠️ Program interrupted by user.[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ An unexpected error occurred: {str(e)}[/]")
        Utils.log_activity("System Error", False, str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
