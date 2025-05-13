import os
import json
import asyncio
from colorama import init, Fore, Style
from modules.cookie_manager import CookieManager
from modules.spam_sharing import SpamSharing
from modules.utils import clear_screen, validate_input

init(autoreset=True)

class FacebookMonoToolkit:
    def __init__(self):
        self.cookie_manager = CookieManager()
        self.spam_sharing = SpamSharing()
        self.current_account = None

    def display_banner(self):
        clear_screen()
        print(Fore.CYAN + "=" * 40)
        print(Fore.YELLOW + Style.BRIGHT + "Facebook MonoToolkit")
        print(Fore.CYAN + "-" * 40)
        print(Fore.GREEN + "Version: 1.0")
        print(Fore.CYAN + "=" * 40 + "\n")

    def main_menu(self):
        while True:
            self.display_banner()
            print(f"{Fore.CYAN}[1] Manage Cookies")
            print(f"{Fore.CYAN}[2] Spam Sharing Post")
            print(f"{Fore.CYAN}[3] Quit\n")

            choice = input(f"{Fore.YELLOW}Select an option (1-3): {Fore.RESET}")
            
            if choice == "1":
                self.cookie_management_menu()
            elif choice == "2":
                if not self.current_account:
                    print(f"{Fore.RED}Please login first using the Manage Cookies option.{Fore.RESET}")
                    input("Press Enter to continue...")
                    continue
                self.spam_sharing_menu()
            elif choice == "3":
                print(f"{Fore.GREEN}Thank you for using Facebook MonoToolkit!{Fore.RESET}")
                break
            else:
                print(f"{Fore.RED}Invalid option!{Fore.RESET}")
                input("Press Enter to continue...")

    def cookie_management_menu(self):
        while True:
            self.display_banner()
            print(f"{Fore.CYAN}=== Cookie Management ===")
            print(f"{Fore.CYAN}[1] Enter new cookie")
            
            if self.cookie_manager.has_cookies():
                print(f"{Fore.CYAN}[2] Cookie Settings and Storage")
            
            print(f"{Fore.CYAN}[3] Back to Main Menu\n")

            choice = input(f"{Fore.YELLOW}Select an option: {Fore.RESET}")

            if choice == "1":
                self.add_new_cookie()
            elif choice == "2" and self.cookie_manager.has_cookies():
                self.cookie_settings_menu()
            elif choice == "3":
                break
            else:
                print(f"{Fore.RED}Invalid option!{Fore.RESET}")
                input("Press Enter to continue...")

    def add_new_cookie(self):
        print(f"{Fore.CYAN}Enter your Facebook cookie (JSON or semicolon-separated format):{Fore.RESET}")
        cookie = input().strip()
        
        success, message = self.cookie_manager.add_cookie(cookie)
        if success:
            print(f"{Fore.GREEN}{message}{Fore.RESET}")
        else:
            print(f"{Fore.RED}{message}{Fore.RESET}")
        
        input("Press Enter to continue...")

    def cookie_settings_menu(self):
        while True:
            self.display_banner()
            print(f"{Fore.CYAN}=== Cookie Settings and Storage ===\n")
            
            accounts = self.cookie_manager.get_all_accounts()
            for idx, account in enumerate(accounts, 1):
                status = "Logged in" if account == self.current_account else "Logged out"
                print(f"— Account {idx}")
                print(f"Name: {account['name']}")
                print(f"Status: {status}")
                if account != self.current_account:
                    print(f"[{idx}] Select")
                print()

            print(f"[0] Back\n")

            choice = input(f"{Fore.YELLOW}Select an option: {Fore.RESET}")
            
            if choice == "0":
                break
            try:
                choice = int(choice)
                if 1 <= choice <= len(accounts):
                    if accounts[choice-1] != self.current_account:
                        self.current_account = accounts[choice-1]
                        print(f"{Fore.GREEN}Successfully switched to account: {self.current_account['name']}{Fore.RESET}")
                    else:
                        print(f"{Fore.YELLOW}This account is already selected.{Fore.RESET}")
                else:
                    print(f"{Fore.RED}Invalid option!{Fore.RESET}")
            except ValueError:
                print(f"{Fore.RED}Invalid input!{Fore.RESET}")
            
            input("Press Enter to continue...")

    def spam_sharing_menu(self):
        self.display_banner()
        print(f"{Fore.CYAN}=== Spam Sharing ===\n")
        
        post_url = input(f"{Fore.YELLOW}Enter post URL: {Fore.RESET}")
        try:
            share_count = int(input(f"{Fore.YELLOW}Enter number of shares: {Fore.RESET}"))
            delay = int(input(f"{Fore.YELLOW}Enter delay between shares (seconds): {Fore.RESET}"))
        except ValueError:
            print(f"{Fore.RED}Invalid input! Share count and delay must be numbers.{Fore.RESET}")
            input("Press Enter to continue...")
            return

        success, message = self.spam_sharing.share_post(
            self.current_account['cookie'],
            post_url,
            share_count,
            delay
        )
        
        if success:
            print(f"{Fore.GREEN}{message}{Fore.RESET}")
        else:
            print(f"{Fore.RED}{message}{Fore.RESET}")
        
        input("Press Enter to continue...")

if __name__ == "__main__":
    tool = FacebookMonoToolkit()
    tool.main_menu()
