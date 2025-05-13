#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/utils.py
# Last Modified: 2025-05-13 14:09:08 UTC
# Author: sehraks

import os
import sys
import json
import re
import uuid
import time
from typing import Tuple, Any, Dict, Optional, List, Union
from datetime import datetime
from colorama import init, Fore, Style, Back

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class Utils:
    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def validate_input(prompt: str, input_type: type, 
                      min_val: Optional[Any] = None,
                      max_val: Optional[Any] = None) -> Tuple[bool, Any]:
        """
        Validate user input for a specific type and range.
        
        Args:
            prompt (str): The prompt to display to the user
            input_type (type): The expected type of input (int, str, etc.)
            min_val (Any, optional): Minimum allowed value
            max_val (Any, optional): Maximum allowed value
            
        Returns:
            Tuple[bool, Any]: (success, value) pair
        """
        try:
            value = input_type(input(prompt))
            
            if min_val is not None and value < min_val:
                print(f"{Fore.RED}Value must be at least {min_val}{Style.RESET_ALL}")
                return False, None
                
            if max_val is not None and value > max_val:
                print(f"{Fore.RED}Value must be at most {max_val}{Style.RESET_ALL}")
                return False, None
                
            return True, value
        except ValueError:
            print(f"{Fore.RED}Invalid input. Expected {input_type.__name__}{Style.RESET_ALL}")
            return False, None

    @staticmethod
    def print_banner(title: str, version: str = "1.0", 
                    author: str = "sehraks",
                    last_updated: Optional[str] = None) -> None:
        """
        Print a formatted banner with tool information.
        
        Args:
            title (str): The title to display
            version (str): Version number
            author (str): Author name
            last_updated (str, optional): Last update timestamp
        """
        Utils.clear_screen()
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}{title.center(50)}")
        print(f"{Fore.CYAN}{'-'*50}")
        print(f"{Fore.GREEN}Version: {version}")
        print(f"{Fore.BLUE}Author: {author}")
        if last_updated:
            print(f"{Fore.MAGENTA}Last Updated: {last_updated}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")

    @staticmethod
    def print_menu(options: Dict[str, Optional[str]], title: str = "") -> None:
        """
        Print a menu with numbered options in order.
        
        Args:
            options (Dict[str, Optional[str]]): Dictionary of menu options
            title (str): Menu title
        """
        if title:
            print(f"{Fore.CYAN}{title}:\n")
        
        for key, value in sorted(options.items()):
            if value is not None:  # Only print non-None options
                print(f"{Fore.YELLOW}[{key}]{Fore.CYAN} {value}")
        print()

    @staticmethod
    def get_menu_choice(options: Dict[str, Optional[str]]) -> str:
        """
        Get user's menu choice with validation.
        
        Args:
            options (Dict[str, Optional[str]]): Dictionary of valid options
            
        Returns:
            str: Selected option key
        """
        while True:
            choice = input(f"{Fore.YELLOW}Select an option: {Style.RESET_ALL}")
            if choice in options and options[choice] is not None:
                return choice
            print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")

    @staticmethod
    def format_cookie(cookie: str, mask: bool = True) -> str:
        """
        Format cookie string for display or storage.
        
        Args:
            cookie (str): The cookie string to format
            mask (bool): Whether to mask sensitive parts
            
        Returns:
            str: Formatted cookie string
        """
        if not cookie:
            return ""
            
        if not mask:
            return cookie
            
        # Keep first 10 and last 5 characters visible
        if len(cookie) > 20:
            return f"{cookie[:10]}...{cookie[-5:]}"
        return "*" * len(cookie)

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate if a URL is a valid Facebook URL.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid Facebook URL
        """
        # Clean URL first
        cleaned_url = Utils.clean_facebook_url(url)
        
        # Facebook URL patterns
        patterns = [
            r'^https?:\/\/(www\.|m\.|mbasic\.)?facebook\.com\/',
            r'^https?:\/\/(web\.|touch\.)?facebook\.com\/'
        ]
        
        return any(bool(re.match(pattern, cleaned_url)) for pattern in patterns)

    @staticmethod
    def clean_facebook_url(url: str) -> str:
        """
        Clean a Facebook URL by removing unnecessary parameters.
        
        Args:
            url (str): The Facebook URL to clean
            
        Returns:
            str: Cleaned Facebook URL
        """
        try:
            # Remove tracking parameters
            base_url = url.split('?')[0]
            
            # Remove trailing slashes
            base_url = base_url.rstrip('/')
            
            # Handle mobile URLs
            if any(domain in base_url for domain in ['m.facebook.com', 'mbasic.facebook.com']):
                base_url = base_url.replace('m.facebook.com', 'www.facebook.com')
                base_url = base_url.replace('mbasic.facebook.com', 'www.facebook.com')
                
            return base_url
        except Exception:
            return url

    @staticmethod
    def log_activity(action: str, status: bool, details: str) -> None:
        """
        Log activity to a file with timestamp.
        
        Args:
            action (str): The action being performed
            status (bool): Success/failure status
            details (str): Additional details
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        status_str = "SUCCESS" if status else "FAILURE"
        
        log_dir = "logs"
        if not os.makedirs(log_dir, exist_ok=True):
            return
            
        log_file = os.path.join(log_dir, f"activity_{datetime.utcnow().strftime('%Y%m')}.log")
        
        log_entry = f"[{timestamp}] {action} - {status_str}: {details}\n"
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"{Fore.RED}Failed to log activity: {str(e)}{Style.RESET_ALL}")

    @staticmethod
    def print_status(message: str, status: str = "info") -> None:
        """
        Print a formatted status message.
        
        Args:
            message (str): Message to display
            status (str): Status type (info, success, error, warning)
        """
        status_colors = {
            "info": Fore.BLUE,
            "success": Fore.GREEN,
            "error": Fore.RED,
            "warning": Fore.YELLOW
        }
        color = status_colors.get(status.lower(), Fore.WHITE)
        print(f"{color}{message}{Style.RESET_ALL}")

    @staticmethod
    def confirm_action(prompt: str = "Are you sure?") -> bool:
        """
        Ask for user confirmation.
        
        Args:
            prompt (str): Confirmation prompt
            
        Returns:
            bool: True if confirmed
        """
        response = input(f"{Fore.YELLOW}{prompt} (y/n): {Style.RESET_ALL}").lower()
        return response in ['y', 'yes']

    @staticmethod
    def save_json(data: Any, filepath: str) -> bool:
        """
        Save data to a JSON file.
        
        Args:
            data (Any): Data to save
            filepath (str): Path to save file
            
        Returns:
            bool: True if successful
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            Utils.print_status(f"Error saving file: {str(e)}", "error")
            return False

    @staticmethod
    def load_json(filepath: str) -> Tuple[bool, Any]:
        """
        Load data from a JSON file.
        
        Args:
            filepath (str): Path to load file
            
        Returns:
            Tuple[bool, Any]: (success, data) pair
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return True, json.load(f)
        except Exception as e:
            Utils.print_status(f"Error loading file: {str(e)}", "error")
            return False, None

    @staticmethod
    def create_progress_bar(current: int, total: int, 
                          width: int = 30) -> str:
        """
        Create a progress bar string.
        
        Args:
            current (int): Current progress
            total (int): Total value
            width (int): Width of progress bar
            
        Returns:
            str: Formatted progress bar
        """
        percentage = (current / total) if total > 0 else 0
        filled = int(width * percentage)
        bar = '█' * filled + '░' * (width - filled)
        percent_str = f'{percentage:>3.0%}'
        return f'{bar} {percent_str}'

    @staticmethod
    def generate_mutation_id() -> str:
        """
        Generate a mutation ID for Facebook requests.
        
        Returns:
            str: UUID version 4 string
        """
        return str(uuid.uuid4())

    @staticmethod
    def format_time_ago(timestamp: Union[str, datetime]) -> str:
        """
        Convert timestamp to "time ago" format.
        
        Args:
            timestamp (Union[str, datetime]): Timestamp to format
            
        Returns:
            str: Formatted time ago string
        """
        try:
            if isinstance(timestamp, str):
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                dt = timestamp
                
            now = datetime.utcnow()
            diff = now - dt

            if diff.days > 365:
                return f"{diff.days // 365}y ago"
            if diff.days > 30:
                return f"{diff.days // 30}mo ago"
            if diff.days > 0:
                return f"{diff.days}d ago"
            if diff.seconds > 3600:
                return f"{diff.seconds // 3600}h ago"
            if diff.seconds > 60:
                return f"{diff.seconds // 60}m ago"
            return f"{diff.seconds}s ago"
        except Exception:
            return str(timestamp)
