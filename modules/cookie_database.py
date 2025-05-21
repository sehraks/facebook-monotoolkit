# File: modules/cookie_database.py

from rich.console import Console
from rich.panel import Panel

console = Console()

class CookieDatabase:
    def __init__(self, cookie_manager):
        """Initialize the Cookie Database with a reference to CookieManager."""
        self.cookie_manager = cookie_manager

    def view_all_cookies(self):
        """Display all stored cookies."""
        accounts = self.cookie_manager.get_all_accounts()
        
        if not accounts:
            console.print(Panel(
                "[bold white]❕ No cookies found in the database![/]",
                style="bold indian_red",
                border_style="indian_red"
            ))
            console.input("[bold white]Press Enter to continue...[/]")
            return

        for idx, account in enumerate(accounts, 1):
            cookie_panel = Panel(
                f"[bold white]Name: {account.get('name', 'Unknown')}[/]\n"
                f"[bold white]Cookie: {account.get('cookie', 'N/A')}[/]",
                title=f"[bold white]𝗖𝗢𝗢𝗞𝗜𝗘 {idx}[/]",
                style="bold yellow",
                border_style="yellow"
            )
            console.print(cookie_panel)

        console.input("[bold white]Press Enter to continue...[/]")
