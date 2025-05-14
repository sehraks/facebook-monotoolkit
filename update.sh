#!/usr/bin/env python3

import os
import subprocess
import re
from datetime import datetime
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

def main():
    # Clear screen
    os.system('clear')

    # Initialize console
    console = Console()

    # Show updating message
    console.print(Panel("🔄 Updating Facebook MonoToolkit...", style="bold blue"))

    # Check if git is installed
    if not run_command("command -v git")[0]:
        console.print(Panel("❌ Error: Git is not installed!", style="bold red"))
        console.print("\n📦 Please install git first:")
        console.print("pkg install git")
        return

    # Check for updates
    console.print("📡 Checking for updates...")
    if not run_command("git fetch origin")[0]:
        console.print(Panel("❌ Failed to fetch updates!", style="bold red"))
        return

    # Download updates
    console.print("📥 Downloading latest changes...")
    if not run_command("git pull origin main")[0]:
        console.print(Panel("❌ Update failed!", style="bold red"))
        console.print("\n💡 Try: git reset --hard origin/main")
        return

    # Get current version from index.py
    with open("index.py", "r") as f:
        content = f.read()
        current_version = re.search(r'self\.VERSION = "([^"]+)"', content).group(1)
        major, minor = map(int, current_version.split('.'))
        new_version = f"{major}.{minor + 1}"

    # Update timestamps and version
    current_date_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    current_date_gmt = datetime.now().strftime('%b %d, %Y +8 GMT')

    # Update index.py
    with open("index.py", "r") as f:
        content = f.read()

    content = re.sub(r'self\.VERSION = ".*"', f'self.VERSION = "{new_version}"', content)
    content = re.sub(r'self\.LAST_UPDATED = ".*"', f'self.LAST_UPDATED = "{current_date_gmt}"', content)
    content = re.sub(r'self\.CURRENT_TIME = ".*"', f'self.CURRENT_TIME = "{current_date_utc}"', content)
    content = re.sub(r'self\.CURRENT_USER = ".*"', f'self.CURRENT_USER = "sehraks"', content)

    with open("index.py", "w") as f:
        f.write(content)

    # Make files executable
    console.print("🔧 Setting file permissions...")
    run_command("chmod +x *.py")
    run_command("chmod +x modules/*.py")

    # Create success table
    table = Table(show_header=False, box=box.ROUNDED)
    table.add_row("✅ Update Completed Successfully!")
    table.add_row(f"🕒 Last updated: {current_date_utc} UTC")
    table.add_row(f"📈 Version updated to: {new_version}")
    table.add_row("📝 Please restart the tool to apply changes.")

    # Show success message
    console.print("\n")
    console.print(Panel(table, style="bold green"))

if __name__ == "__main__":
    main()
