#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/utils.py
# Last Modified: 2025-05-16 14:32:46 +8 GMT
# Author: sehraks

import os
import re
from datetime import datetime, timezone, timedelta
from typing import Dict, Tuple, Any, Callable
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

class Utils:
    @staticmethod
    def print_banner(title: str, version: str, author: str, last_updated: str) -> None:
        """Print a stylized banner with tool information."""
        content = (
            f"[bold white]Version: {version}[/]\n"
            f"[bold white]Author: {author}[/]\n"
            f"[bold white]Last Updated: {last_updated}[/]"
        )
        
        console.print(Panel(
            content,
            title=f"[bold yellow]{title}[/]",
            style="bold magenta",
            border_style="cyan"
        ))

    @staticmethod
    def print_menu(options: Dict[str, str], title: str = "") -> None:
        """Print a menu with numbered options."""
        menu_content = ""
        if title:
            menu_content += f"[bold yellow]{title}[/]\n"
        
        # Create a table for better organization
        table = Table(show_header=False, box=None, pad_edge=False)
        table.add_column("Option", style="bold cyan", justify="right")
        table.add_column("Description", style="white")

        for key, value in options.items():
            table.add_row(f"[{key}]", value)

        menu_content += str(table)
        
        console.print(Panel(
            menu_content.strip(),
            title="[bold yellow]📋 Menu[/]",
            style="bold magenta",
            border_style="cyan"
        ))

    @staticmethod
    def get_menu_choice(options: Dict[str, str]) -> str:
        """Get user's menu choice with validation."""
        while True:
            choice = console.input("[bold yellow]Select an option: [/]").strip()
            if choice in options:
                return choice
            console.print(Panel(
                "[bold white]❌ Invalid option. Please try again.[/]",
                style="bold red",
                border_style="red"
            ))

    @staticmethod
    def print_status(message: str, status: str = "info") -> None:
        """Print a colored status message."""
        status_config = {
            "success": ("✅", "green", "Success"),
            "error": ("❌", "red", "Error"),
            "warning": ("⚠️", "yellow", "Warning"),
            "info": ("ℹ️", "cyan", "Info")
        }
        
        emoji, color, title = status_config.get(status.lower(), ("•", "white", "Status"))
        
        console.print(Panel(
            f"[bold white]{message}[/]",
            title=f"[bold {color}]{emoji} {title}[/]",
            style=f"bold {color}",
            border_style=color
        ))

    @staticmethod
    def validate_input(prompt: str, type_cast: Callable, min_val: Any = None, max_val: Any = None) -> Tuple[bool, Any]:
        """Validate user input with type casting and range checking."""
        try:
            value = type_cast(console.input(prompt).strip())
            if min_val is not None and value < min_val:
                Utils.print_status(f"Value must be at least {min_val}", "error")
                return False, None
            if max_val is not None and value > max_val:
                Utils.print_status(f"Value must be at most {max_val}", "error")
                return False, None
            return True, value
        except ValueError:
            Utils.print_status("Invalid input format", "error")
            return False, None

    @staticmethod
    def confirm_action(prompt: str) -> bool:
        """Get user confirmation for an action."""
        response = console.input(f"[bold yellow]{prompt} [y/n]: [/]").lower().strip()
        return response == 'y'

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate if a URL is properly formatted."""
        return bool(re.match(r'^https?://', url))

    @staticmethod
    def log_activity(activity: str, success: bool, message: str) -> None:
        """Log activity to a file."""
        # Get Philippines time (GMT+8)
        philippines_time = datetime.now(timezone(timedelta(hours=8)))
        timestamp = philippines_time.strftime('%Y-%m-%d %H:%M:%S')
        
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"activity_{philippines_time.strftime('%Y%m')}.log")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp} +8 GMT] {activity} | Success: {success} | Message: {message}\n")
        except Exception as e:
            console.print(Panel(
                f"[bold white]Failed to log activity: {str(e)}[/]",
                title="[bold red]❌ Error[/]",
                style="bold red",
                border_style="red"
            ))

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
