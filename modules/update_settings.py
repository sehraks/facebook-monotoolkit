#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/update_settings.py
# Last Modified: 2025-05-15 05:37:04 UTC
# Author: sehraks

import os
import subprocess
from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel

console = Console()

class UpdateSettings:
    def __init__(self, display_banner_func):
        """Initialize with the banner display function."""
        self.display_banner = display_banner_func
        self.current_time = "2025-05-15 05:37:04"
        self.current_user = "sehraks"

    def display_settings_menu(self):
        """Display and handle settings menu."""
        while True:
            # Clear screen and show banner
            os.system('clear')
            self.display_banner()
            
            # Display menu
            menu_panel = Panel(
                "[bold green][1] Check updates[/]\n"
                "[bold white][2] Back to Main Menu[/]",
                title="[bold white]Settings[/]",
                style="bold magenta"
            )
            console.print(menu_panel)

            # Get user choice
            choice = console.input("[bold yellow]Select an option (1-2): [/]")
            
            # Handle user choice
            if choice == "1":
                self.check_updates()
            elif choice == "2":
                break
            else:
                console.print(Panel(
                    "[bold white]❕ Invalid choice! Please try again.[/]",
                    style="bold red"
                ))
                console.input("[bold white]Press Enter to continue...[/]")

    def run_command(self, command):
        """Run a shell command and return its status and output."""
        try:
            process = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            return True, process.stdout
        except subprocess.CalledProcessError as e:
            return False, e.stderr

    def check_for_updates(self):
        """Check if updates are available."""
        if not self.run_command("git fetch origin")[0]:
            return False, "Failed to fetch updates"
        
        status, output = self.run_command("git rev-list HEAD..origin/main --count")
        if not status:
            return False, "Failed to check update status"
        
        return int(output.strip()) > 0, output.strip()

    def show_changelogs(self):
        """Show changelog content if available."""
        try:
            with open("changelogs.txt", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            return None

    def update_repository(self):
        """Update repository by re-cloning."""
        try:
            home = os.path.expanduser("~")
            repo_path = os.path.join(home, "facebook-monotoolkit")
            
            # Prepare commands with proper directory handling
            commands = [
                f"cd {home} && rm -rf facebook-monotoolkit",
                f"cd {home} && git clone https://github.com/sehraks/facebook-monotoolkit.git",
                f"cd {repo_path} && chmod +x index.py && chmod +x modules/*.py"
            ]
            
            console.print("\n📥 Downloading latest changes...")
            for cmd in commands:
                status, output = self.run_command(cmd)
                if not status:
                    console.print(f"Command failed: {cmd}")
                    console.print(f"Error: {output}")
                    raise Exception("Failed to update repository")
            
            # Update success message with current time
            console.print(Panel(
                "✅ Update completed! Please restart the tool to apply changes.\n\n"
                f"Current Date: {self.current_time} UTC\n"
                f"Current User: {self.current_user}",
                style="bold green"
            ))
            console.print("\n[bold yellow]❕ The program will now exit. Please restart it.[/]")
            
            # Force exit to ensure clean restart
            os._exit(0)
            
            return True
        except Exception as e:
            console.print(Panel(
                f"[bold white]❌ Error during update: {str(e)}[/]",
                style="bold red"
            ))
            return False

    def check_updates(self):
        """Check for updates using Git"""
        try:
            # Clear screen and show banner
            os.system('clear')
            self.display_banner()

            # Check for updates
            console.print("🔄 Checking for updates...")
            
            # Check for updates
            has_updates, update_count = self.check_for_updates()
            
            if has_updates:
                # Show changelog if available
                changelogs = self.show_changelogs()
                if changelogs:
                    console.print(Panel(
                        f"[bold green]🆕 New updates available!\n\nChange Logs:\n{changelogs}[/]",
                        style="bold green"
                    ))
                else:
                    console.print(Panel(
                        "[bold green]🆕 New updates available![/]",
                        style="bold green"
                    ))
                
                # Ask for user confirmation
                while True:
                    choice = console.input("\n[bold yellow]Do you want to update it now? (y/n): [/]").lower()
                    if choice in ['y', 'n']:
                        break
                    console.print(Panel(
                        "[bold white]❕ Please enter 'y' for yes or 'n' for no.[/]",
                        style="bold yellow"
                    ))
                
                if choice == 'y':
                    success = self.update_repository()
                    if not success:
                        console.print(Panel(
                            "[bold white]❕ Update failed! Please try again.[/]",
                            style="bold red"
                        ))
                else:
                    console.print(Panel(
                        "[bold white]❕ Update cancelled by user.[/]",
                        style="bold yellow"
                    ))
            else:
                # Only show no updates message when there are truly no updates
                console.print(Panel(
                    "[bold white]✨ No updates available.[/]", 
                    style="bold red"
                ))

        except subprocess.CalledProcessError as e:
            console.print(Panel(
                f"[bold white]❌ Update failed: {str(e)}[/]",
                style="bold red"
            ))
        except Exception as e:
            console.print(Panel(
                f"[bold white]❌ Error: {str(e)}[/]",
                style="bold red"
            ))

        console.input("[bold white]Press Enter to continue...[/]")
