#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/update_settings.py
# Last Modified: May 17, 2025 02:48 AM +8 GMT
# Author: sehraks

import os
import subprocess
import re
import time
import shutil
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.panel import Panel

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

    def read_version_from_install_hook(self):
        """Read version and other details from install-hook.sh."""
        try:
            with open("install-hooks.sh", "r") as f:
                content = f.read()
                
                # Look for VERSION="X.XX" pattern
                version_match = re.search(r'VERSION="([0-9.]+)"', content)
                if not version_match:
                    raise Exception("Version not found in install-hook.sh")
                    
                version = version_match.group(1)
                
                # Extract changelog entries
                changelog_start = content.find('echo "Version')
                changelog_end = content.find('HOOK', changelog_start)
                if changelog_start == -1 or changelog_end == -1:
                    raise Exception("Changelog content not found in install-hooks.sh")
                    
                changelog_content = content[changelog_start:changelog_end]
                changelog_lines = [line.strip() for line in changelog_content.split('echo "')[1:]]
                changelog_text = '\n'.join(line.strip('"') for line in changelog_lines)
                
                return True, version, changelog_text
        except FileNotFoundError:
            return False, None, "install-hooks.sh not found"
        except Exception as e:
            return False, None, str(e)

    def sync_changelogs(self):
        """Synchronize changelogs.txt with install-hook.sh content."""
        success, version, changelog_content = self.read_version_from_install_hook()
        if not success:
            return False, changelog_content
            
        try:
            with open("changelogs.txt", "w") as f:
                f.write(changelog_content)
            return True, "Changelog synchronized successfully"
        except Exception as e:
            return False, f"Failed to update changelogs.txt: {str(e)}"

    def backup_current_data(self):
        """Create backup of important data before update."""
        try:
            backup_dir = os.path.join(os.path.expanduser("~"), "facebook-monotoolkit-backup")
            os.makedirs(backup_dir, exist_ok=True)
            
            # Backup cookies and logs
            for directory in ['cookies-storage', 'logs']:
                src = directory
                dst = os.path.join(backup_dir, directory)
                if os.path.exists(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
            
            return True
        except Exception as e:
            console.print(Panel(
                f"[bold red]Failed to create backup: {str(e)}[/]",
                style="bold red",
                border_style="red"
            ))
            return False

    def restore_backup(self):
        """Restore data from backup if update fails."""
        try:
            backup_dir = os.path.join(os.path.expanduser("~"), "facebook-monotoolkit-backup")
            if not os.path.exists(backup_dir):
                return False
                
            for directory in ['cookies-storage', 'logs']:
                src = os.path.join(backup_dir, directory)
                if os.path.exists(src):
                    dst = directory
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
            
            return True
        except Exception:
            return False

    def update_repository(self):
        """Update repository by re-cloning."""
        try:
            # Backup current data
            if not self.backup_current_data():
                raise Exception("Failed to create backup")

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
                    self.restore_backup()
                    raise Exception("Failed to update repository")

            # Wait for files to be ready
            time.sleep(2)

            # Check if install-hook.sh exists
            if not os.path.exists(os.path.join(repo_path, "install-hook.sh")):
                console.print(Panel(
                    "[bold red]Error: install-hook.sh not found![/]",
                    style="bold red",
                    border_style="red"
                ))
                self.restore_backup()
                return False

            # Sync changelogs with install-hook.sh
            sync_success, sync_message = self.sync_changelogs()
            if not sync_success:
                console.print(Panel(
                    f"[bold yellow]Warning: {sync_message}[/]",
                    style="bold yellow",
                    border_style="yellow"
                ))

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

            # Check for updates
            console.print("🔄 Checking for updates...")
            
            # Check for updates
            has_updates, update_count = self.check_for_updates()
            
            if has_updates:
                # Get version and changelog from install-hook.sh
                success, version, changelog_content = self.read_version_from_install_hook()
                if success:
                    console.print(Panel(
                        f"[bold green]🆕 New updates available!\n\nLatest Version: {version}\n\nChange Logs:\n{changelog_content}[/]",
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
                    style="bold cyan",
                    border_style="cyan"
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
