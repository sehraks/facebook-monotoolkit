#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/update_settings.py
# Last Modified: May 17, 2025 11:33 AM +8 GMT
# Author: sehraks

import os
import subprocess
import re
import time
import shutil
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn

console = Console()

class UpdateSettings:
    def __init__(self, display_banner_func):
        """Initialize with the banner display function."""
        self.display_banner = display_banner_func
        # Get current Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        self.current_time = philippines_time.strftime("%I:%M %p")
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
                style="bold magenta",
                border_style="cyan"
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
                    style="bold red",
                    border_style="red"
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

    def backup_current_data(self):
        """Create backup of important data before update."""
        with Progress(
            TextColumn("⭘"),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[bold blue]{task.percentage:>3.0f}%")
        ) as progress:
            backup_task = progress.add_task("📦 Creating backup...", total=100)
            
            try:
                backup_dir = os.path.join(os.path.expanduser("~"), "facebook-monotoolkit-backup")
                os.makedirs(backup_dir, exist_ok=True)
                progress.update(backup_task, advance=30)

                # Backup cookies and logs
                for idx, directory in enumerate(['cookies-storage', 'logs']):
                    src = directory
                    dst = os.path.join(backup_dir, directory)
                    if os.path.exists(src):
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
                    progress.update(backup_task, advance=35)  # Split remaining progress

                progress.update(backup_task, completed=100)
                progress.update(backup_task, description="✅ Backup complete!")
                time.sleep(0.5)  # Small delay for visual feedback
                return True

            except Exception as e:
                progress.update(backup_task, description="❌ Backup failed!")
                console.print(Panel(
                    f"[bold red]Failed to create backup: {str(e)}[/]",
                    style="bold red",
                    border_style="red"
                ))
                return False

    def restore_backup(self):
        """Restore data from backup if update fails."""
        with Progress(
            TextColumn("⭘"),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[bold blue]{task.percentage:>3.0f}%")
        ) as progress:
            restore_task = progress.add_task("🔄 Restoring backup...", total=100)
            
            try:
                backup_dir = os.path.join(os.path.expanduser("~"), "facebook-monotoolkit-backup")
                if not os.path.exists(backup_dir):
                    progress.update(restore_task, description="❌ No backup found!")
                    return False

                for idx, directory in enumerate(['cookies-storage', 'logs']):
                    src = os.path.join(backup_dir, directory)
                    if os.path.exists(src):
                        dst = directory
                        if os.path.exists(dst):
                            shutil.rmtree(dst)
                        shutil.copytree(src, dst)
                    progress.update(restore_task, advance=50)  # Split progress in half

                progress.update(restore_task, completed=100)
                progress.update(restore_task, description="✅ Restore complete!")
                time.sleep(0.5)  # Small delay for visual feedback
                return True

            except Exception:
                progress.update(restore_task, description="❌ Restore failed!")
                return False

    def update_index_values(self):
        """Update version and timestamps in index.py"""
        with Progress(
            TextColumn("⭘"),
            TextColumn("[bold blue]{task.description}")
        ) as progress:
            update_task = progress.add_task("🔄 Updating index.py values...")
            
            try:
                # Wait for files to be available
                max_attempts = 5
                for attempt in range(max_attempts):
                    if os.path.exists("changelogs.txt"):
                        break
                    time.sleep(1)
                else:
                    progress.update(update_task, description="❌ Failed to find changelogs.txt")
                    return False

                # Read current version from changelogs.txt
                with open("changelogs.txt", "r") as f:
                    first_line = f.readline().strip()
                    version = first_line.replace("Version ", "")

                # Get current Philippines time (GMT+8)
                philippines_time = datetime.now(timezone(timedelta(hours=8)))
                current_date = philippines_time.strftime("%B %d, %Y")
                current_time = philippines_time.strftime("%I:%M %p")

                # Read and update index.py
                with open("index.py", "r") as f:
                    content = f.read()

                # Update the values using regex
                content = re.sub(
                    r'self\.VERSION = \".*\"',
                    f'self.VERSION = "{version}"',
                    content
                )
                content = re.sub(
                    r'self\.LAST_UPDATED = \".*\"',
                    f'self.LAST_UPDATED = "{current_date}"',
                    content
                )
                content = re.sub(
                    r'self\.CURRENT_TIME = \".*\"',
                    f'self.CURRENT_TIME = "{current_time}"',
                    content
                )
                content = re.sub(
                    r'self\.CURRENT_USER = \".*\"',
                    f'self.CURRENT_USER = "{self.current_user}"',
                    content
                )

                # Update file header
                content = re.sub(
                    r'# Last Modified: .*',
                    f'# Last Modified: {current_date} {current_time} +8 GMT',
                    content
                )

                # Write back to index.py
                with open("index.py", "w") as f:
                    f.write(content)

                progress.update(update_task, description="✅ Index.py updated successfully!")
                time.sleep(0.5)  # Small delay for visual feedback
                return True

            except Exception as e:
                progress.update(update_task, description=f"❌ Failed to update index.py: {str(e)}")
                return False

    def update_repository(self):
        """Update repository by re-cloning."""
        try:
            # Backup current data with progress
            if not self.backup_current_data():
                raise Exception("Failed to create backup")

            home = os.path.expanduser("~")
            repo_path = os.path.join(home, "facebook-monotoolkit")

            # Create a progress bar for the update process
            with Progress(
                TextColumn("⭘"),
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                TextColumn("[bold blue]{task.percentage:>3.0f}%")
            ) as progress:
                # Add tasks for each step
                download_task = progress.add_task("📥 Downloading latest changes...", total=100)
                
                # Prepare commands with proper directory handling
                commands = [
                    f"cd {home} && rm -rf facebook-monotoolkit",
                    f"cd {home} && git clone https://github.com/sehraks/facebook-monotoolkit.git",
                    f"cd {repo_path} && chmod +x index.py && chmod +x modules/*.py"
                ]

                # Execute commands with progress updates
                for i, cmd in enumerate(commands):
                    progress.update(download_task, advance=33)  # Split progress into thirds
                    status, output = self.run_command(cmd)
                    if not status:
                        progress.update(download_task, description="❌ Download failed!")
                        console.print(f"Command failed: {cmd}")
                        console.print(f"Error: {output}")
                        self.restore_backup()
                        raise Exception("Failed to update repository")
                    time.sleep(0.5)  # Small delay for visual feedback

                # Complete the progress bar
                progress.update(download_task, completed=100)
                progress.update(download_task, description="✅ Download complete!")
                time.sleep(0.5)  # Small delay for visual feedback

            # Wait for files to be ready
            time.sleep(1)

            # Check if we can access the new files
            if not os.path.exists(os.path.join(repo_path, "changelogs.txt")):
                console.print(Panel(
                    "[bold white]Update successful but requires restart.[/]\n"
                    "Please restart the tool manually.",
                    style="bold green",
                    border_style="green"
                ))
                os._exit(0)

            # Update index.py values after successful update
            if self.update_index_values():
                console.print("[bold green]✅ Successfully updated index.py values[/]")

            # Get current Philippines time
            philippines_time = datetime.now(timezone(timedelta(hours=8)))
            current_time = philippines_time.strftime("%I:%M %p")
            current_date = philippines_time.strftime("%B %d, %Y")

            # Update success message with current Philippines time
            console.print(Panel(
                "✅ Update completed! Please restart the tool to apply changes.\n\n"
                f"Date: {current_date}\n"
                f"Time: {current_time} GMT+8\n"
                f"Current User: {self.current_user}",
                style="bold green",
                border_style="green"
            ))
            console.print("\n[bold yellow]❕ The program will now exit. Please restart it.[/]")

            # Force exit to ensure clean restart
            os._exit(0)

            return True
        except Exception as e:
            console.print(Panel(
                f"[bold white]❌ Error during update: {str(e)}[/]",
                style="bold red",
                border_style="red"
            ))
            return False

    def check_updates(self):
        """Check for updates using Git"""
        try:
            # Clear screen and show banner
            os.system('clear')
            self.display_banner()

            # Check for updates with animated progress
            with Progress(
                TextColumn("⭘"),
                TextColumn("[bold blue]{task.description}")
            ) as progress:
                # Add task for checking updates
                check_task = progress.add_task("🔄 Checking for updates...")
                
                # Perform the actual update check
                has_updates, update_count = self.check_for_updates()
                
                # Complete the task without changing the message
                progress.update(check_task, completed=True)
                
                # Small delay for visual feedback
                time.sleep(0.5)

            if has_updates:
                # Show changelog if available
                changelogs = self.show_changelogs()
                if changelogs:
                    console.print(Panel(
                        f"[bold green]🆕 New updates available!\n\nChange Logs:\n{changelogs}[/]",
                        style="bold green",
                        border_style="green"
                    ))
                else:
                    console.print(Panel(
                        "[bold green]🆕 New updates available![/]",
                        style="bold green",
                        border_style="green"
                    ))

                # Ask for user confirmation
                while True:
                    choice = console.input("\n[bold yellow]Do you want to update it now? (y/n): [/]").lower()
                    if choice in ['y', 'n']:
                        break
                    console.print(Panel(
                        "[bold white]❕ Please enter 'y' for yes or 'n' for no.[/]",
                        style="bold yellow",
                        border_style="yellow"
                    ))

                if choice == 'y':
                    success = self.update_repository()
                    if not success:
                        console.print(Panel(
                            "[bold white]❕ Update failed! Please try again.[/]",
                            style="bold red",
                            border_style="red"
                        ))
                else:
                    console.print(Panel(
                        "[bold white]❕ Update cancelled by user.[/]",
                        style="bold yellow",
                        border_style="yellow"
                    ))
            else:
                # Only show no updates message when there are truly no updates
                console.print(Panel(
                    "[bold white]✨ No updates available.[/]", 
                    style="bold red",
                    border_style="red"
                ))

        except subprocess.CalledProcessError as e:
            console.print(Panel(
                f"[bold white]❌ Update failed: {str(e)}[/]",
                style="bold red",
                border_style="red"
            ))
        except Exception as e:
            console.print(Panel(
                f"[bold white]❌ Error: {str(e)}[/]",
                style="bold red",
                border_style="red"
            ))

        console.input("[bold white]Press Enter to continue...[/]")
