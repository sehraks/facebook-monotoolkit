#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel

console = Console()

class UpdateSettings:
    def display_settings_menu(self):
        """Display and handle settings menu."""
        while True:
            menu_panel = Panel(
                "[bold cyan][1] 🔄 Check updates[/]\n"
                "[bold yellow][2] 🔙 Back to Main Menu[/]",
                title="[bold yellow]⚙️  Settings[/]",
                style="bold magenta"
            )
            console.print(menu_panel)

            choice = console.input("[bold yellow]Select an option (1-2): [/]")
            choice = choice.strip()

            if choice == "1":
                self.check_updates()
            elif choice == "2":
                break
            else:
                console.print(Panel(
                    "[bold red]❌ Invalid choice! Please try again.[/]",
                    style="bold red"
                ))

    def check_updates(self):
        """Check for updates using Git"""
        try:
            # Clear screen
            os.system('clear')

            # Check for updates
            console.print("📡 Checking for updates...")
            
            # Fetch latest changes
            subprocess.run(["git", "fetch", "origin"], check=True, capture_output=True)
            
            # Check if we're behind origin
            result = subprocess.run(
                ["git", "rev-list", "HEAD..origin/main", "--count"],
                check=True,
                capture_output=True,
                text=True
            )
            
            update_count = int(result.stdout.strip())
            
            if update_count > 0:
                # Show changelog if available
                try:
                    with open("changelogs.txt", "r") as f:
                        changelogs = f.read().strip()
                        console.print(Panel(
                            f"🆕 New updates available!\n\nChange Logs:\n{changelogs}",
                            style="bold green"
                        ))
                except FileNotFoundError:
                    console.print(Panel("🆕 New updates available!", style="bold green"))
                
                # Ask for user confirmation
                while True:
                    choice = input("\nDo you want to update it now? (y/n): ").lower()
                    if choice in ['y', 'n']:
                        break
                    console.print("Please enter 'y' for yes or 'n' for no.")
                
                if choice == 'y':
                    # Download updates
                    console.print("\n📥 Downloading latest changes...")
                    subprocess.run(["git", "pull", "origin", "main"], check=True)
                    console.print("🔧 Setting file permissions...")
                    subprocess.run(["chmod", "+x", "*.py"], check=True)
                    subprocess.run(["chmod", "+x", "modules/*.py"], check=True)
                    
                    # Show success message only when updates were downloaded
                    console.print(Panel(
                        "✅ Update completed! Please restart the tool to apply changes.",
                        style="bold green"
                    ))
                else:
                    console.print(Panel("Update cancelled by user.", style="bold yellow"))
            else:
                # Only show no updates message when there are truly no updates
                console.print(Panel("✨ No updates available", style="bold red"))

        except subprocess.CalledProcessError as e:
            console.print(Panel(f"❌ Update failed: {str(e)}", style="bold red"))
        except Exception as e:
            console.print(Panel(f"❌ Error: {str(e)}", style="bold red"))

        console.input("\nPress Enter to continue...")
