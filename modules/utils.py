#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/utils.py
# Last Modified: 2025-05-13 15:40:35 UTC
# Author: sehraks

import os
import re
from datetime import datetime
from typing import Dict, Tuple, Any, Callable
from colorama import Fore, Style

class Utils:
    @staticmethod
    def print_banner(title: str, version: str, author: str, last_updated: str) -> None:
        """Print a stylized banner with tool information."""
        width = 50
        print(f"{Fore.CYAN}{'='*width}")
        print(f"{title} v{version}".center(width))
        print(f"By: {author}".center(width))
        print(f"Last Updated: {last_updated}".center(width))
        print(f"{'='*width}{Style.RESET_ALL}\n")

    @staticmethod
    def print_menu(options: Dict[str, str], title: str = "") -> None:
        """Print a menu with numbered options."""
        if title:
            print(f"{Fore.YELLOW}{title}:")
        for key, value in options.items():
            print(f"{Fore.YELLOW}[{key}] {Style.RESET_ALL}{value}")
        print()

    @staticmethod
    def get_menu_choice(options: Dict[str, str]) -> str:
        """Get user's menu choice with validation."""
        while True:
            choice = input(f"{Fore.YELLOW}Select an option: {Style.RESET_ALL}").strip()
            if choice in options:
                return choice
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")

    @staticmethod
    def print_status(message: str, status: str = "info") -> None:
        """Print a colored status message."""
        colors = {
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW,
            "info": Fore.CYAN
        }
        color = colors.get(status.lower(), Fore.WHITE)
        print(f"\n{color}{message}{Style.RESET_ALL}")

    @staticmethod
    def validate_input(prompt: str, type_cast: Callable, min_val: Any = None, max_val: Any = None) -> Tuple[bool, Any]:
        """Validate user input with type casting and range checking."""
        try:
            value = type_cast(input(prompt))
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
        response = input(f"{prompt}[y/n]: ").lower().strip()
        return response == 'y'

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate if a URL is properly formatted."""
        return bool(re.match(r'^https?://', url))

    @staticmethod
    def log_activity(activity: str, success: bool, message: str) -> None:
        """Log activity to a file."""
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_file = os.path.join(log_dir, f"activity_{datetime.now().strftime('%Y%m')}.log")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] {activity} | Success: {success} | Message: {message}\n")
        except Exception as e:
            print(f"{Fore.RED}Failed to log activity: {str(e)}{Style.RESET_ALL}")
