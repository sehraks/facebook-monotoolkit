#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime, timezone
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

def run_command(command):
    try:
        process = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, process.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_for_updates():
    # Fetch latest changes
    console.print("📡 Checking for updates...")
    if not run_command("git fetch origin")[0]:
        return False, "Failed to fetch updates"
    
    # Check if we're behind origin
    status, output = run_command("git rev-list HEAD..origin/main --count")
    if not status:
        return False, "Failed to check update status"
    
    return int(output.strip()) > 0, output.strip()

def show_changelogs():
    try:
        with open("changelogs.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def main():
    # Clear screen
    os.system('clear')

    # Check for updates
    has_updates, update_count = check_for_updates()

    if has_updates:
        # Show changelog if available
        changelogs = show_changelogs()
        if changelogs:
            console.print(Panel(f"🆕 New updates available!\n\nChange Logs:\n{changelogs}", 
                              style="bold green"))
            
            # Download updates
            console.print("📥 Downloading latest changes...")
            run_command("git pull origin main")
            console.print("🔧 Setting file permissions...")
            run_command("chmod +x *.py")
            run_command("chmod +x modules/*.py")
            
            # Show success message only when updates were actually downloaded
            console.print(Panel("✅ Update completed! Please restart the tool to apply changes.", 
                              style="bold green"))
    else:
        # Only show "No updates available" message when there are no updates
        console.print(Panel("✨ No updates available", style="bold red"))

if __name__ == "__main__":
    main()
