#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/update_settings.py
# Last Modified: 2025-05-14 03:56:00 UTC
# Author: sehraks

import os
import sys
from rich.console import Console
from rich.panel import Panel

# Initialize rich console
console = Console()

class UpdateSettings:
    def __init__(self):
        """Initialize the Update Settings."""
        self.VERSION = "3.50"
        self.LAST_UPDATED = "May 14, 2025 +8 GMT"
        self.CURRENT_TIME = "2025-05-14 03:56:00"
        self.CURRENT_USER = "sehraks"

    def display_settings_menu(self):
        """Display and handle settings menu."""
        while True:
            console.print(Panel(
                "[bold cyan]⚙️ Settings[/]",
                style="bold cyan"
            ))

            menu_panel = Panel(
                "[bold cyan][1] 🔄 Update Facebook MonoToolkit[/]\n"
                "[bold yellow][2] 🔙 Back to Main Menu[/]",
                title="[bold yellow]Settings Menu[/]",
                style="bold magenta"
            )
            console.print(menu_panel)

            choice = console.input("[bold yellow]Select an option: [/]")
            choice = choice.strip()

            if choice == "1":
                self.update_tool()
            elif choice == "2":
                break
            else:
                console.print(Panel(
                    "[bold red]❌ Invalid choice! Please try again.[/]", 
                    style="bold red"
                ))
            
            if choice == "1":
                break
            else:
                console.input("[bold blue]Press Enter to continue...[/]")

    def update_tool(self):
        """Handle tool update process."""
        console.print(Panel(
            "[bold cyan]🔄 Updating Facebook MonoToolkit...[/]",
            style="bold cyan"
        ))
        try:
            os.system('chmod +x update.sh && ./update.sh')
            console.print(Panel(
                "[bold green]✅ Update completed! Please restart the tool to apply changes.[/]",
                style="bold green"
            ))
            sys.exit(0)
        except Exception as e:
            console.print(Panel(
                f"[bold red]❌ Update failed: {str(e)}[/]",
                style="bold red"
            ))
            console.input("[bold blue]Press Enter to continue...[/]")
