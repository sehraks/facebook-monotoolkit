#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: index.py
# Last Modified: 2025-05-13 17:03:46 UTC
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

# Initialize rich console
console = Console()

class FacebookMonoToolkit:
    def __init__(self):
        """Initialize the Facebook MonoToolkit."""
        self.VERSION = "3.50"
        self.ORIGINAL_AUTHOR = "Greegmon"
        self.MODIFIED_BY = "Cerax"
        self.LAST_UPDATED = "May 13, 2025 +8 GMT"
        self.CURRENT_TIME = "2025-05-13 17:03:46"
        self.CURRENT_USER = "sehraks"
        
        # Initialize components
        self.cookie_manager = CookieManager()
        self.spam_sharing = SpamSharing()
        self.current_account: Optional[Dict] = None
        
        # Create necessary directories
        self._init_directories()

    def _init_directories(self) -> None:
        """Initialize necessary directories."""
        directories = ['cookies-storage', 'logs']
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def clear_screen(self) -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self) -> None:
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

    def check_cookie_required(self) -> bool:
        """Check if cookie is available."""
        if not self.current_account:
            console.print(Panel(
                "[bold red]⚠️ Please login first using the Manage Cookies option.[/]",
                style="bold red"
            ))
            console.input("\n[bold blue]Press Enter to continue...[/]")
            return False
        return True

    def main_menu(self) -> None:
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
                "[bold red][3] 🚪 Exit[/]",
                title="[bold yellow]📋 Main Menu[/]",
                style="bold magenta"
            )
            console.print(menu_panel)

            choice = console.input("[bold yellow]Select an option (1-3): [/]").strip()

            if choice == "1":
                self.cookie_management_menu()
            elif choice == "2":
                if not self.check_cookie_required():
                    continue
                self.spam_sharing_menu()
            elif choice == "3":
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

    def cookie_management_menu(self) -> None:
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
            
            choice = console.input("[bold yellow]Select an option: [/]").strip()

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

    def add_new_cookie(self) -> None:
        """Handle adding a new cookie."""
        self.display_banner()
        console.print(Panel(
            "[bold cyan]📝 Add New Cookie[/]",
            style="bold cyan"
        ))
        
        console.print("\n[bold]Enter your Facebook cookie (JSON or semicolon-separated format):[/]")
        console.print("[bold yellow]Note: Cookie must contain c_user and xs values[/]\n")
        
        cookie = console.input("[bold green]Cookie: [/]").strip()
        
        if not cookie:
            console.print(Panel(
                "[bold red]❌ Cookie cannot be empty![/]",
                style="bold red"
            ))
            console.input("\n[bold blue]Press Enter to continue...[/]")
            return

        success, message = self.cookie_manager.add_cookie(cookie)
        
        if success:
            console.print(Panel(
                f"[bold green]✅ {message}[/]",
                style="bold green"
            ))
            if not self.current_account:
                self.current_account = self.cookie_manager.get_all_accounts()[-1]
        else:
            console.print(Panel(
                f"[bold red]❌ {message}[/]",
                style="bold red"
            ))
        
        Utils.log_activity("Add Cookie", success, message)
        console.input("\n[bold blue]Press Enter to continue...[/]")

    def cookie_settings_menu(self) -> None:
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
                console.print()

            console.print("[bold yellow][0] 🔙 Back[/]\n")

            choice = console.input("[bold yellow]Select an option: [/]").strip()
            
            if choice == "0":
                break
                
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
            
            console.input("\n[bold blue]Press Enter to continue...[/]")

    def spam_sharing_menu(self) -> None:
        """Handle spam sharing functionality."""
        self.display_banner()
        console.print(Panel(
            "[bold cyan]📢 Spam Sharing[/]",
            style="bold cyan"
        ))
        
        post_url = console.input("\n[bold green]📌 Enter the Facebook post URL: [/]").strip()
        
        if not Utils.validate_url(post_url):
            console.print(Panel(
                "[bold red]❌ Invalid Facebook URL![/]",
                style="bold red"
            ))
            console.input("\n[bold blue]Press Enter to continue...[/]")
            return

        success, share_count = Utils.validate_input(
            "[bold green]🔢 Number of shares: [/]",
            int,
            min_val=1,
            max_val=100
        )
        
        if not success:
            console.input("\n[bold blue]Press Enter to continue...[/]")
            return

        success, delay = Utils.validate_input(
            "[bold green]⏱️  Delay between shares (seconds): [/]",
            int,
            min_val=1,
            max_val=60
        )
        
        if not success:
            console.input("\n[bold blue]Press Enter to continue...[/]")
            return

        console.print(Panel(
            "[bold cyan]🚀 Starting share operation...[/]",
            style="bold cyan"
        ))
        
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
        console.input("\n[bold blue]Press Enter to continue...[/]")

def main():
    """Main entry point of the application."""
    try:
        tool = FacebookMonoToolkit()
        tool.main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]⚠️ Program interrupted by user.[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]❌ An unexpected error occurred: {str(e)}[/]")
        Utils.log_activity("System Error", False, str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
