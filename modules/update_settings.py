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
            # Clear screen
            os.system('clear')
            
            # Display menu
            menu_panel = Panel(
                "[bold cyan][1] 🔄 Check updates[/]\n"
                "[bold yellow][2] 🔙 Back to Main Menu[/]",
                title="[bold yellow]⚙️  Settings[/]",
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
                    "[bold red]❌ Invalid choice! Please try again.[/]",
                    style="bold red"
                ))
                console.input("\nPress Enter to continue...")
                # After user presses enter, the while loop will start again
                # and clear the screen + show the menu

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
            "Current Date: 2025-05-14 07:57:18 UTC\n"
            "Current User: sehraks",
            style="bold green"
        ))
        console.print("\n[bold yellow]⚠️ The program will now exit. Please restart it.[/]")
        
        # Force exit to ensure clean restart
        os._exit(0)
        
        return True
    except Exception as e:
        console.print(f"Error during update: {str(e)}")
        return False

    def check_updates(self):
        """Check for updates using Git"""
        try:
            # Clear screen
            os.system('clear')

            # Check for updates
            console.print("📡 Checking for updates...")
            
            # Check for updates
            has_updates, update_count = self.check_for_updates()
            
            if has_updates:
                # Show changelog if available
                changelogs = self.show_changelogs()
                if changelogs:
                    console.print(Panel(
                        f"🆕 New updates available!\n\nChange Logs:\n{changelogs}",
                        style="bold green"
                    ))
                else:
                    console.print(Panel("🆕 New updates available!", style="bold green"))
                
                # Ask for user confirmation
                while True:
                    choice = input("\nDo you want to update it now? (y/n): ").lower()
                    if choice in ['y', 'n']:
                        break
                    console.print("Please enter 'y' for yes or 'n' for no.")
                
                if choice == 'y':
                    success = self.update_repository()
                    if success:
                        console.print(Panel(
                            "✅ Update completed! Please restart the tool to apply changes.\n\n"
                            "Current Date: 2025-05-14 07:49:59 UTC\n"
                            "Current User: sehraks",
                            style="bold green"
                        ))
                        console.print("\n[bold yellow]⚠️ The program will now exit. Please restart it.[/]")
                        os._exit(0)  # Force exit as the files have been replaced
                    else:
                        console.print(Panel("❌ Update failed! Please try again.", style="bold red"))
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
