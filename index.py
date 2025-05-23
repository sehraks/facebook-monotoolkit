lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII, lllllllllllIlll, lllllllllllIllI, lllllllllllIlIl = bool, enumerate, Exception, str, IndexError, open, __name__, KeyboardInterrupt, len, ValueError, int

from os import makedirs as IlIIllIIllIllI, system as lIlllllIIIlllI, name as llIIIlllIlllII, chmod as IlIIllllllIIll
from time import sleep as lIIlIIIllIlIIl
from requests import Timeout as llIIllllIllIll, Session as lIllIIlIllIIll
from re import search as IlIllIIIlIlIll
from subprocess import Popen as lllIlIllIlIIll, PIPE as IlIIIIIllIllIl
from sys import exit as llIlIIIlllIIII
from datetime import datetime as lllIlIIllIllll, timezone as llllIllIlIlIII, timedelta as IIIllIlllllIIl
from typing import Dict as IIIlIIIlllIlIl, Optional as llllllllIIlIII
from rich.console import Console as lIllIlllIllIll
from rich.panel import Panel as lIIllIIlIllllI
from rich.table import Table as lIllllllIIlIlI
from modules.cookie_manager import CookieManager as IllIlIllIIlIlI
from modules.spam_sharing import SpamSharing as IlllllIllllIll
from modules.utils import Utils as IlllIIlIIIlllI
from modules.update_settings import UpdateSettings as IlIIlIllIIIlll
from modules.fb_login import FacebookLogin as llIllllllIlllI
from modules.cookie_database import CookieDatabase as IIllIlllIIlIIl
from modules.fb_guard import FacebookGuard as IIllIlIIIlIllI
lIllIIlIIlIIllIlIl = lIllIlllIllIll()

class lllIIIIIllllIlIIII:

    def __init__(lIIlllIIlllIIIlllI):
        """Initialize the Facebook MonoToolkit."""
        lIIlllIIlllIIIlllI.lIlIlIIllllIllllll = None
        lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI = None
        try:
            with llllllllllllIlI('changelogs.txt', 'r') as lIlllllIIIIIllllIl:
                IllllIIlllIlIIlIII = lIlllllIIIIIllllIl.readline().strip()
                lIIlllIIlllIIIlllI.IllllIIlIlIllIIIIl = IllllIIlllIlIIlIII.replace('Version ', '')
        except:
            lIIlllIIlllIIIlllI.IllllIIlIlIllIIIIl = 'X.XX'
        lIIlllIIlllIIIlllI.lIlllllIlIlllllIll = 'Greegmon'
        lIIlllIIlllIIIlllI.IIIlIIIIllIllIllll = 'Cerax'
        IIIlIlllllIIllllIl = lllIlIIllIllll.now(llllIllIlIlIII(IIIllIlllllIIl(hours=8)))
        lIIlllIIlllIIIlllI.IIllllIIllIllIllIl = IIIlIlllllIIllllIl.strftime('%B %d, %Y')
        lIIlllIIlllIIIlllI.IIIllIllIIllIIIlll = IIIlIlllllIIllllIl.strftime('%I:%M %p')
        lIIlllIIlllIIIlllI.IlIIllIlIIIlllIIll = 'sehraks'
        lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII = IllIlIllIIlIlI()
        lIIlllIIlllIIIlllI.lIIlllllIlIlIllIII = IlllllIllllIll()
        lIIlllIIlllIIIlllI.lIlllIlIIlIlIIlIll = IlIIlIllIIIlll(lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl)
        lIIlllIIlllIIIlllI.IllIlllIIlIlIIIIII = llIllllllIlllI()
        lIIlllIIlllIIIlllI.lllIIlIIlIllIIlIll = IIllIlllIIlIIl(lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII)
        lIIlllIIlllIIIlllI.lIlIIlIllIlllIIIlI = IIllIlIIIlIllI()
        lIIlllIIlllIIIlllI.IIlIIlIlIIIIIIIIlI()
        lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI = lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.get_current_account()
        if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI:
            lIIlllIIlllIIIlllI.IlllIIIlIIlllIlIII(lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI)

    def IlllIIIlIIlllIlIII(lIIlllIIlllIIIlllI, IIlIIlIllIlIllIlll: IIIlIIIlllIlIl) -> None:
        """Load account data for the current account."""
        if IIlIIlIllIlIllIlll:
            lIIlllIIlllIIIlllI.lIlIlIIllllIllllll = {'name': IIlIIlIllIlIllIlll.get('name', 'Unknown User'), 'user_id': IIlIIlIllIlIllIlll.get('user_id')}
        else:
            lIIlllIIlllIIIlllI.lIlIlIIllllIllllll = None

    def IIlIIlIlIIIIIIIIlI(lIIlllIIlllIIIlllI):
        """Initialize necessary directories."""
        IIIIlllIIlIIIIIlll = ['cookies-storage', 'logs']
        for lIlIIIlIIllllIllll in IIIIlllIIlIIIIIlll:
            try:
                IlIIllIIllIllI(lIlIIIlIIllllIllll, exist_ok=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                IlIIllllllIIll(lIlIIIlIIllllIllll, 448)
            except lllllllllllllIl as IlllIIIIllIIllIlIl:
                lIllIIlIIlIIllIlIl.print(f'[bold red]Error creating directory {lIlIIIlIIllllIllll}: {lllllllllllllII(IlllIIIIllIIllIlIl)}[/]')

    def lIIIIlIlllIIlIlIII(lIIlllIIlllIIIlllI):
        """Clear the terminal screen."""
        lIlllllIIIlllI('cls' if IllllIlIlIllllIIll == 'nt' else 'clear')

    def llllIlIIlIIlIlIIIl(lIIlllIIlllIIIlllI):
        """Display the tool banner."""
        IIIlIlllllIIllllIl = lllIlIIllIllll.now(llllIllIlIlIII(IIIllIlllllIIl(hours=8)))
        IlIlllIIIIIIllIIII = IIIlIlllllIIllllIl.strftime('%I:%M %p')
        IIIlIlIllIIIlIIlIl = IIIlIlllllIIllllIl.strftime('%B %d, %Y')
        IIllIIllIlIllllllI = lIIllIIlIllllI(f'[white]Original: {lIIlllIIlllIIIlllI.lIlllllIlIlllllIll}[/]\n[white]Modified by: {lIIlllIIlllIIIlllI.IIIlIIIIllIllIllll}[/]\n[white]Version: {lIIlllIIlllIIIlllI.IllllIIlIlIllIIIIl}[/]\n[white]Date: {IIIlIlIllIIIlIIlIl}[/]\n[white]Time: {IlIlllIIIIIIllIIII} GMT+8[/]', style='bold magenta', title='[bold yellow]𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗠𝗢𝗡𝗢𝗧𝗢𝗢𝗟𝗞𝗜𝗧[/]', border_style='cyan')
        lIllIIlIIlIIllIlIl.print(IIllIIllIlIllllllI)

    def lIIlllllIlIlIllIlI(lIIlllIIlllIIIlllI):
        """Check if cookie is available."""
        if not lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Please login first using the Accounts Management option.[/]', style='bold indian_red', border_style='indian_red'))
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        return lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)

    def lllIllIlIlIllIllIl(lIIlllIIlllIIIlllI):
        """Display and handle the main menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
            lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
            if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
            lIllIIlIlIIIlIlIIl = lIIllIIlIllllI('[bold white][1] Accounts Management[/]\n[bold white][2] Spam Sharing Post[/]\n[bold white][3] Profile Guard[/]\n[bold white][4] Settings[/]\n[bold red][5] Exit[/]', title='[bold white]𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨[/]', style='bold magenta', border_style='cyan')
            lIllIIlIIlIIllIlIl.print(lIllIIlIlIIIlIlIIl)
            lIIlIIlIllIIlIIIlI = lIllIIlIIlIIllIlIl.input('[bold yellow]Select an option (1-5): [/]')
            lIIlIIlIllIIlIIIlI = lIIlIIlIllIIlIIIlI.strip()
            if lIIlIIlIllIIlIIIlI == '1':
                lIIlllIIlllIIIlllI.lIlllIlIlIlIlllIll()
            elif lIIlIIlIllIIlIIIlI == '2':
                if not lIIlllIIlllIIIlllI.lIIlllllIlIlIllIlI():
                    continue
                lIIlllIIlllIIIlllI.lIIIlIIIllIIlllIll()
            elif lIIlIIlIllIIlIIIlI == '3':
                if not lIIlllIIlllIIIlllI.lIIlllllIlIlIllIlI():
                    continue
                lIIlllIIlllIIIlllI.IIIIlIIIlIIlllIlIl()
            elif lIIlIIlIllIIlIIIlI == '4':
                lIIlllIIlllIIIlllI.llIllIlIIIIIIlIIII()
            elif lIIlIIlIllIIlIIIlI == '5':
                break
            else:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def llIllIlIIIIIIlIIII(lIIlllIIlllIIIlllI):
        """Handle settings menu."""
        lIIlllIIlllIIIlllI.lIlllIlIIlIlIIlIll.display_settings_menu()

    def lIlllIlIlIlIlllIll(lIIlllIIlllIIIlllI):
        """Handle cookie management menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
            lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
            if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold yellow]🔑 𝗔𝗖𝗖𝗢𝗨𝗡𝗧𝗦 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧[/]', style='bold yellow', border_style='yellow'))
            lIllIIlIlIIIlIlIIl = lIIllIIlIllllI('[bold white][1] Enter your cookie[/]\n[bold white][2] Login your Facebook account[/]\n[bold white][3] Access your Facebook accounts[/]\n[bold white][4] Cookies & Tokens Database[/]\n[bold white][5] Back to Main Menu[/]', title='[bold white]𝗦𝗘𝗟𝗘𝗖𝗧 𝗬𝗢𝗨𝗥 𝗖𝗛𝗢𝗜𝗖𝗘[/]', style='bold yellow', border_style='yellow')
            lIllIIlIIlIIllIlIl.print(lIllIIlIlIIIlIlIIl)
            lIIlIIlIllIIlIIIlI = lIllIIlIIlIIllIlIl.input('[bold yellow]Select an option: [/]')
            lIIlIIlIllIIlIIIlI = lIIlIIlIllIIlIIIlI.strip()
            if lIIlIIlIllIIlIIIlI == '1':
                lIIlllIIlllIIIlllI.llllIIIlllllIIIIll()
            elif lIIlIIlIllIIlIIIlI == '2':
                lIIlllIIlllIIIlllI.lIllIIIIlIIIllIlIl()
            elif lIIlIIlIllIIlIIIlI == '3':
                if not lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.has_cookies():
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Add a cookie or login first.[/]', style='bold indian_red', border_style='indian_red'))
                    lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
                    continue
                lIIlllIIlllIIIlllI.llllIIllIlllIIlllI()
            elif lIIlIIlIllIIlIIIlI == '4':
                if not lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.has_cookies():
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Add a cookie or login first.[/]', style='bold indian_red', border_style='indian_red'))
                    lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
                    continue
                lIIlllIIlllIIIlllI.IlIlIIlIIIllllIIll()
            elif lIIlIIlIllIIlIIIlI == '5':
                break
            else:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def lIllIIIIlIIIllIlIl(lIIlllIIlllIIIlllI):
        """Handle Facebook login functionality."""
        lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
        lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
        lIlIIllIllllIlIlIl = lIIllIIlIllllI('[bold yellow]Note:[/] [bold white]You can use either your email address or Facebook UID. Mobile numbers and usernames are currently not supported yet.[/]\n[bold indian_red]Caution:[/] [bold white]Refrain from using your main account, as doing so may cause lockout or suspension.[/]', title='[bold white]𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗟𝗢𝗚𝗜𝗡[/]', style='bold yellow', border_style='yellow')
        lIllIIlIIlIIllIlIl.print(lIlIIllIllllIlIlIl)
        lIlllllIIlIllIllII = lIllIIlIIlIIllIlIl.input('[bold yellow]\U0001faaa Enter your credential: [/]')
        lIlIlIlllllIlIIIll = lIllIIlIIlIIllIlIl.input('[bold yellow]🔑 Enter your password: [/]')
        (lIlIIlllIlIllIIIII, IlIIIIlllIIlIlllll, lIlIlIIllllIllllll) = lIIlllIIlllIIIlllI.IllIlllIIlIlIIIIII.login(lIlllllIIlIllIllII.strip(), lIlIlIlllllIlIIIll.strip())
        if lIlIIlllIlIllIIIII and lIlIlIIllllIllllll:
            lIIlllIIlllIIIlllI.lIlIlIIllllIllllll = lIlIlIIllllIllllll
            lIlIIlllIlIllIIIII = lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.add_cookie(lIlIlIIllllIllllll['cookie'], lIlIlIIllllIllllll['name'], lIlIlIIllllIllllll['token'])[0]
            if lIlIIlllIlIllIIIII:
                lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI = None
                lIIIIlIlIlllIlIlII = lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.get_all_accounts()
                for IIlIIlIllIlIllIlll in lIIIIlIlIlllIlIlII:
                    if IIlIIlIllIlIllIlll['user_id'] == lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['user_id']:
                        lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.set_current_account(IIlIIlIllIlIllIlll['id'])
                        lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI = IIlIIlIllIlIllIlll
                        break
        lIIlllIIlllIIIlllI.IllIlllIIlIlIIIIII.log_login_attempt(lIlllllIIlIllIllII, lIlIIlllIlIllIIIII, IlIIIIlllIIlIlllll)
        lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def llllIIIlllllIIIIll(lIIlllIIlllIIIlllI):
        """Handle adding a new cookie."""
        lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
        lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
        llIlIIIlllIllIIIll = lIIllIIlIllllI('[bold yellow]Note:[/] [bold white]Use semi-colon separated format, cookie must contain c_user and xs values.[/]\n[bold indian_red]Caution:[/] [bold white]JSON format is not supported for some reason.[/]', title='[bold white]𝗔𝗗𝗗 𝗬𝗢𝗨𝗥 𝗖𝗢𝗢𝗞𝗜𝗘[/]', style='bold yellow', border_style='yellow')
        lIllIIlIIlIIllIlIl.print(llIlIIIlllIllIIIll)
        lIlIlIIIlllIIllIII = lIllIIlIIlIIllIlIl.input('[bold yellow]🍪 Enter your cookie: [/]')
        lIlIlIIIlllIIllIII = lIlIlIIIlllIIllIII.strip()
        if not lIlIlIIIlllIIllIII:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Cookie cannot be empty![/]', style='bold indian_red', border_style='indian_red'))
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]🔄 Validating cookie format...[/]', style='bold cyan', border_style='cyan'))
        lIIlIIIllIlIIl(1)
        if 'c_user=' not in lIlIlIIIlllIIllIII or 'xs=' not in lIlIlIIIlllIIllIII:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid cookie format! Cookie must contain c_user and xs values.[/]', style='bold indian_red', border_style='indian_red'))
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]✅ Cookie format is valid![/]', style='bold green', border_style='green'))
        lIIlIIIllIlIIl(1)
        try:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI("[bold white]🔄 Getting account's token...[/]", style='bold cyan', border_style='cyan'))
            lIIlIIIllIlIIl(1.5)
            lIIIIlIllIIIIlIlII = lIllIIlIllIIll()
            try:
                for IlIlIllIIIIlllIIll in lIlIlIIIlllIIllIII.split(';'):
                    if '=' in IlIlIllIIIIlllIIll:
                        (IllllIlIlIllllIIll, llllllllIIIIllIllI) = IlIlIllIIIIlllIIll.strip().split('=', 1)
                        lIIIIlIllIIIIlIlII.cookies.set(IllllIlIlIllllIIll, llllllllIIIIllIllI)
            except lllllllllllllIl as IlllIIIIllIIllIlIl:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]❕ Error parsing cookie: {lllllllllllllII(IlllIIIIllIIllIlIl)}[/]', style='bold indian_red', border_style='indian_red'))
                lIIlIIIllIlIIl(1)
            IlIIIIlIIlllIlIIII = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Upgrade-Insecure-Requests': '1'}
            lllIllllIlllllllIl = None
            lIIIllIIIIIlIIllll = [('Ads Manager', 'https://adsmanager.facebook.com/adsmanager/', 'accessToken="(EAA[A-Za-z0-9]+)"'), ('Business Manager', 'https://business.facebook.com/content_management', '"(EAA[A-Za-z0-9]+)"'), ('Feed Composer', 'https://www.facebook.com/composer/ocelot/async_loader/?publisher=feed', '"accessToken":"(EAA[A-Za-z0-9]+)"')]
            for (llIlIIIlllIIllllIl, IIIIlIIIIIlIIlIllI, llIIllIlIIlIIIIIlI) in lIIIllIIIIIlIIllll:
                try:
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]🔄 Trying {llIlIIIlllIIllllIl} method...[/]', style='bold cyan', border_style='cyan'))
                    lIIlIIIllIlIIl(1)
                    lIIlIllllIIIllIlIl = lIIIIlIllIIIIlIlII.get(IIIIlIIIIIlIIlIllI, headers=IlIIIIlIIlllIlIIII, timeout=30)
                    if lIIlIllllIIIllIlIl.ok:
                        lIIIllllIllIIIllIl = IlIllIIIlIlIll(llIIllIlIIlIIIIIlI, lIIlIllllIIIllIlIl.text)
                        if lIIIllllIllIIIllIl:
                            lllIllllIlllllllIl = lIIIllllIllIIIllIl.group(1)
                            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]✅ Token found using {llIlIIIlllIIllllIl}![/]', style='bold green', border_style='green'))
                            lIIlIIIllIlIIl(1)
                            break
                except llIIllllIllIll:
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]❕ {llIlIIIlllIIllllIl} request timed out[/]', style='bold indian_red', border_style='indian_red'))
                except lllllllllllllIl as IlllIIIIllIIllIlIl:
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]❕ Error with {llIlIIIlllIIllllIl}: {lllllllllllllII(IlllIIIIllIIllIlIl)}[/]', style='bold indian_red', border_style='indian_red'))
            if lllIllllIlllllllIl:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold green]✅ Successfully retrieved token![/]', style='bold green', border_style='green'))
                lIIlIIIllIlIIl(1)
            else:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Could not retrieve token. Continuing anyway...[/]', style='bold indian_red', border_style='indian_red'))
                lIIlIIIllIlIIl(1)
                lllIllllIlllllllIl = 'N/A'
        except lllllllllllllIl as IlllIIIIllIIllIlIl:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]❕ Error during token extraction: {lllllllllllllII(IlllIIIIllIIllIlIl)}. Continuing anyway...[/]', style='bold indian_red', border_style='indian_red'))
            lIIlIIIllIlIIl(1)
            lllIllllIlllllllIl = 'N/A'
        lllllIIllllIIIlIIl = None
        if 'name=' not in lIlIlIIIlllIIllIII:
            lllllIIllllIIIlIIl = lIllIIlIIlIIllIlIl.input('[bold yellow]💳 Enter your name: [/]').strip()
            if not lllllIIllllIIIlIIl:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Please enter your Facebook account name[/]', style='bold indian_red', border_style='indian_red'))
                lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
                return
        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]🔄 Saving account data...[/]', style='bold cyan', border_style='cyan'))
        lIIlIIIllIlIIl(1)
        (lIlIIlllIlIllIIIII, IlIIIIlllIIlIlllll) = lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.add_cookie(lIlIlIIIlllIIllIII, lllllIIllllIIIlIIl, lllIllllIlllllllIl)
        if lIlIIlllIlIllIIIII:
            lIIIIlIlIlllIlIlII = lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.get_all_accounts()
            lIIIlIIlllIllllllI = lIIIIlIlIlllIlIlII[-1]
            lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI = lIIIlIIlllIllllllI
            lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.set_current_account(lIIIlIIlllIllllllI['id'])
            lIIlllIIlllIIIlllI.IlllIIIlIIlllIlIII(lIIIlIIlllIllllllI)
            lIIlIIIllIlIIl(1)
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold green]✅ Cookie added successfully!\n👤 Account: {lIIIlIIlllIllllllI['name']}\n📩 UID: {lIIIlIIlllIllllllI['user_id']}[/]", style='bold green', border_style='green'))
        else:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]❕ {IlIIIIlllIIlIlllll}[/]', style='bold indian_red', border_style='indian_red'))
        IIIlIlllllIIllllIl = lllIlIIllIllll.now(llllIllIlIlIII(IIIllIlllllIIl(hours=8)))
        lllllIIlIIlIIllIll = IIIlIlllllIIllllIl.strftime('%B %d, %Y %I:%M %p')
        IlllIIlIIIlllI.log_activity(f'Add Cookie (PH: {lllllIIlIIlIIllIll}) by {lIIlllIIlllIIIlllI.IlIIllIlIIIlllIIll}', lIlIIlllIlIllIIIII, IlIIIIlllIIlIlllll)
        lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def IIIIlIIIlIIlllIlIl(lIIlllIIlllIIIlllI):
        """Handle Profile Guard operations."""
        if not lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Please select an account first[/]', style='bold indian_red', border_style='indian_red'))
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
            lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI['name']}[/]", style='bold cyan', border_style='cyan'))
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold yellow]Note:[/] [bold white]Make sure you turn off first your Facebook lock profile before proceeding to Facebook Profile Guard.[/]\n\n[1] Activate your Facebook Profile Shield\n[2] Deactivate your Facebook Profile Shield\n[3] Back to Main Menu', title='[bold white]🛡️ 𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 𝗚𝗨𝗔𝗥𝗗[/]', style='bold cyan', border_style='cyan'))
            lIIlIIlIllIIlIIIlI = lIllIIlIIlIIllIlIl.input('[bold yellow]Enter your choice: [/]').strip()
            if lIIlIIlIllIIlIIIlI == '1' or lIIlIIlIllIIlIIIlI == '2':
                llIlIIlIIlIlllIIll = lIIlIIlIllIIlIIIlI == '1'
                (lIlIIlllIlIllIIIII, IlIIIIlllIIlIlllll) = lIIlllIIlllIIIlllI.lIlIIlIllIlllIIIlI.toggle_profile_shield(lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI, llIlIIlIIlIlllIIll)
                if lIlIIlllIlIllIIIII:
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold white]✅ {IlIIIIlllIIlIlllll}\nName: {lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI['name']}\nUID: {lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI['user_id']}[/]", style='bold green', border_style='green'))
                else:
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]❕ {IlIIIIlllIIlIlllll}[/]', style='bold indian_red', border_style='indian_red'))
                lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            elif lIIlIIlIllIIlIIIlI == '3':
                break
            else:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid choice![/]', style='bold indian_red', border_style='indian_red'))
                lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def llllIIllIlllIIlllI(lIIlllIIlllIIIlllI):
        """Handle cookie settings and storage menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
            lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
            if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
            lIIIIlIlIlllIlIlII = lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.get_all_accounts()
            for (IIlIlIIIlllIIIIlll, IIlIIlIllIlIllIlll) in llllllllllllllI(lIIIIlIlIlllIlIlII, 1):
                lIllIlIIlIIlIlIlIl = 'Logged in' if IIlIIlIllIlIllIlll == lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI else 'Logged out'
                llllllIIIIlIIIIlll = 'green' if lIllIlIIlIIlIlIlIl == 'Logged in' else 'red'
                IllIlIIllIllIIIIll = IIlIIlIllIlIllIlll.get('name', 'Unknown User')
                llIlIIIlIIllIllIIl = lIIllIIlIllllI(f"[bold white]Name: {IllIlIIllIllIIIIll}[/]\n[bold white]UID: {IIlIIlIllIlIllIlll['user_id']}[/]\n[bold {llllllIIIIlIIIIlll}]Status: {lIllIlIIlIIlIlIlIl}[/]\n" + (f'[bold yellow][{IIlIlIIIlllIIIIlll}] Select[/]\n' if IIlIIlIllIlIllIlll != lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI else '') + f'[bold red][R{IIlIlIIIlllIIIIlll}] Remove[/]', title=f'[bold yellow]📨 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 {IIlIlIIIlllIIIIlll}[/]', style='bold yellow', border_style='yellow')
                lIllIIlIIlIIllIlIl.print(llIlIIIlIIllIllIIl)
            lIllIIlIIlIIllIlIl.print('[bold white][0] Back[/]\n')
            lIIlIIlIllIIlIIIlI = lIllIIlIIlIIllIlIl.input('[bold yellow]Select an option: [/]')
            lIIlIIlIllIIlIIIlI = lIIlIIlIllIIlIIIlI.strip().upper()
            if lIIlIIlIllIIlIIIlI == '0':
                break
            if lIIlIIlIllIIlIIIlI.startswith('R'):
                try:
                    IIlIlIIIlllIIIIlll = lllllllllllIlIl(lIIlIIlIllIIlIIIlI[1:]) - 1
                    if 0 <= IIlIlIIIlllIIIIlll < lllllllllllIlll(lIIIIlIlIlllIlIlII):
                        lIlIlllIIIIIIlIIll = lIIIIlIlIlllIlIlII[IIlIlIIIlllIIIIlll]
                        if lIIlllIIlllIIIlllI.lIlIlIIllllIllllll and lIlIlllIIIIIIlIIll['user_id'] == lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['user_id']:
                            IllIlIIllIllIIIIll = lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']
                        else:
                            IllIlIIllIllIIIIll = 'Unknown User'
                        IIIIIlIIlIlIIIlllI = lIllIIlIIlIIllIlIl.input(f'[bold red]Are you sure you want to remove {IllIlIIllIllIIIIll}? (y/N): [/]').strip().lower()
                        if IIIIIlIIlIlIIIlllI == 'y':
                            if lIlIlllIIIIIIlIIll == lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI:
                                lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI = None
                                lIIlllIIlllIIIlllI.lIlIlIIllllIllllll = None
                            lIlIIlllIlIllIIIII = lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.remove_cookie(lIlIlllIIIIIIlIIll)
                            if lIlIIlllIlIllIIIII:
                                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold green]✅ Successfully removed account: {IllIlIIllIllIIIIll}[/]', style='bold green', border_style='green'))
                            else:
                                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Failed to remove account![/]', style='bold indian_red', border_style='indian_red'))
                    else:
                        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid selection![/]', style='bold indian_red', border_style='indian_red'))
                except (lllllllllllIllI, llllllllllllIll):
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid input![/]', style='bold indian_red', border_style='indian_red'))
            else:
                try:
                    lIlIIIlllllIIllIlI = lllllllllllIlIl(lIIlIIlIllIIlIIIlI) - 1
                    if 0 <= lIlIIIlllllIIllIlI < lllllllllllIlll(lIIIIlIlIlllIlIlII):
                        if lIIIIlIlIlllIlIlII[lIlIIIlllllIIllIlI] != lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI:
                            lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI = lIIIIlIlIlllIlIlII[lIlIIIlllllIIllIlI]
                            lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.set_current_account(lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI['id'])
                            lIIlllIIlllIIIlllI.IlllIIIlIIlllIlIII(lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI)
                            IllIlIIllIllIIIIll = lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI['name']
                            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold green]✅ Successfully switched to account: {IllIlIIllIllIIIIll}[/]', style='bold green', border_style='green'))
                        else:
                            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ This account is already selected.[/]', style='bold indian_red', border_style='indian_red'))
                    else:
                        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid selection![/]', style='bold indian_red', border_style='indian_red'))
                except lllllllllllIllI:
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid input![/]', style='bold indian_red', border_style='indian_red'))
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def IlIlIIlIIIllllIIll(lIIlllIIlllIIIlllI):
        """Handle cookie database functionality."""
        lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
        lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
        if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
        llIIIlllllIlIIIlll = lIIllIIlIllllI('[bold yellow]Note:[/] [bold white]You can manage all your stored cookies and tokens here[/]\n[bold indian_red]Caution:[/] [bold white]Deleting cookies cannot be undone[/]', title='[bold white]𝗖𝗢𝗢𝗞𝗜𝗘𝗦 & 𝗧𝗢𝗞𝗘𝗡𝗦 𝗗𝗔𝗧𝗔𝗕𝗔𝗦𝗘[/]', style='bold cyan', border_style='cyan')
        lIllIIlIIlIIllIlIl.print(llIIIlllllIlIIIlll)
        lIllIIlIlIIIlIlIIl = lIIllIIlIllllI('[bold white][1] View All Cookies & Tokens[/]\n[bold white][2] Back to Main Menu[/]', style='bold cyan', border_style='cyan')
        lIllIIlIIlIIllIlIl.print(lIllIIlIlIIIlIlIIl)
        lIIlIIlIllIIlIIIlI = lIllIIlIIlIIllIlIl.input('[bold cyan]Enter your choice: [/]')
        if lIIlIIlIllIIlIIIlI == '1':
            lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
            lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
            if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
            lIllIIlIIlIIllIlIl.print(llIIIlllllIlIIIlll)
            lIIIIlIlIlllIlIlII = lIIlllIIlllIIIlllI.lllIlIllIIIIIIlIII.get_all_accounts()
            for (IIlIlIIIlllIIIIlll, IIlIIlIllIlIllIlll) in llllllllllllllI(lIIIIlIlIlllIlIlII, 1):
                IIIlIlllllIIllllIl = lllIlIIllIllll.now(llllIllIlIlIII(IIIllIlllllIIl(hours=8)))
                IlllIllIIllllIIIIl = IIIlIlllllIIllllIl.strftime('%B %d, %Y')
                IllIlIIllllIlIIIll = IIIlIlllllIIllllIl.strftime('%I:%M %p +8 GMT (PH)')
                lIlIlIIIlllIIllIII = IIlIIlIllIlIllIlll['cookie']
                llIllllIIlIIIlllIl = IIlIIlIllIlIllIlll.get('token', 'N/A')
                IIIIIIlIlIlIlIlIlI = lIlIlIIIlllIIllIII[:20] + '...' + lIlIlIIIlllIIllIII[-10:] if lllllllllllIlll(lIlIlIIIlllIIllIII) > 30 else lIlIlIIIlllIIllIII
                llllIlIlIlIIIIlIII = llIllllIIlIIIlllIl[:20] + '...' + llIllllIIlIIIlllIl[-10:] if lllllllllllIlll(llIllllIIlIIIlllIl) > 30 else llIllllIIlIIIlllIl
                llIlIIIlllIllIIIll = lIIllIIlIllllI(f"[bold white]Name: {IIlIIlIllIlIllIlll.get('name', 'Unknown User')}[/]\n[bold white]Cookie: {IIIIIIlIlIlIlIlIlI}[/]\n[bold white]Token: {llllIlIlIlIIIIlIII}[/]\n[bold white]Added Date: {IlllIllIIllllIIIIl}[/]\n[bold white]Added Time: {IllIlIIllllIlIIIll}[/]\n\n[bold yellow][C{IIlIlIIIlllIIIIlll}] Copy cookie[/]\n[bold yellow][T{IIlIlIIIlllIIIIlll}] Copy token[/]", title=f'[bold yellow]📨 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 {IIlIlIIIlllIIIIlll}[/]', style='bold yellow', border_style='yellow')
                lIllIIlIIlIIllIlIl.print(llIlIIIlllIllIIIll)
            lIllIIlIIlIIllIlIl.print('[bold white][0] Back[/]\n')
            while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
                lIlIIllIlllIlIlIIl = lIllIIlIIlIIllIlIl.input('[bold yellow]Select an option: [/]').strip().upper()
                if lIlIIllIlllIlIlIIl == '0':
                    break
                if lIlIIllIlllIlIlIIl.startswith(('C', 'T')):
                    try:
                        IIlIlIIIlllIIIIlll = lllllllllllIlIl(lIlIIllIlllIlIlIIl[1:]) - 1
                        if 0 <= IIlIlIIIlllIIIIlll < lllllllllllIlll(lIIIIlIlIlllIlIlII):
                            try:
                                lllIIllllIlIIIlIll = lIIIIlIlIlllIlIlII[IIlIlIIIlllIIIIlll]['cookie'] if lIlIIllIlllIlIlIIl.startswith('C') else lIIIIlIlIlllIlIlII[IIlIlIIIlllIIIIlll].get('token', '')
                                IllIllIIlIllIlIIlI = 'Cookie' if lIlIIllIlllIlIlIIl.startswith('C') else 'Token'
                                if not lllIIllllIlIIIlIll and IllIllIIlIllIlIIlI == 'Token':
                                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ No token available for this account![/]', style='bold indian_red', border_style='indian_red'))
                                else:
                                    lIllllllIIIlIIlIIl = lllIlIllIlIIll(['termux-clipboard-set'], stdin=IlIIIIIllIllIl)
                                    lIllllllIIIlIIlIIl.communicate(input=lllIIllllIlIIIlIll.encode())
                                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]✅ {IllIllIIlIllIlIIlI} {IIlIlIIIlllIIIIlll + 1} copied to clipboard![/]', style='bold green', border_style='green'))
                            except lllllllllllllIl as IlllIIIIllIIllIlIl:
                                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Failed to copy to clipboard. Make sure Termux:API is installed.[/]', style='bold indian_red', border_style='indian_red'))
                            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
                            lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
                            lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
                            if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
                                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
                            lIllIIlIIlIIllIlIl.print(llIIIlllllIlIIIlll)
                            for (IIlIlIIIlllIIIIlll, IIlIIlIllIlIllIlll) in llllllllllllllI(lIIIIlIlIlllIlIlII, 1):
                                lIllIIlIIlIIllIlIl.print(llIlIIIlllIllIIIll)
                            lIllIIlIIlIIllIlIl.print('[bold white][0] Back[/]\n')
                            break
                        else:
                            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
                            lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
                            lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
                            if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
                                lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
                            lIllIIlIIlIIllIlIl.print(llIIIlllllIlIIIlll)
                            for (IIlIlIIIlllIIIIlll, IIlIIlIllIlIllIlll) in llllllllllllllI(lIIIIlIlIlllIlIlII, 1):
                                lIllIIlIIlIIllIlIl.print(llIlIIIlllIllIIIll)
                            lIllIIlIIlIIllIlIl.print('[bold white][0] Back[/]\n')
                    except lllllllllllIllI:
                        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                        lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
                        lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
                        lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
                        if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
                            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
                        lIllIIlIIlIIllIlIl.print(llIIIlllllIlIIIlll)
                        for (IIlIlIIIlllIIIIlll, IIlIIlIllIlIllIlll) in llllllllllllllI(lIIIIlIlIlllIlIlII, 1):
                            lIllIIlIIlIIllIlIl.print(llIlIIIlllIllIIIll)
                        lIllIIlIIlIIllIlIl.print('[bold white][0] Back[/]\n')
                else:
                    lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                    lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
                    lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
                    lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
                    if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
                        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
                    lIllIIlIIlIIllIlIl.print(llIIIlllllIlIIIlll)
                    for (IIlIlIIIlllIIIIlll, IIlIIlIllIlIllIlll) in llllllllllllllI(lIIIIlIlIlllIlIlII, 1):
                        lIllIIlIIlIIllIlIl.print(llIlIIIlllIllIIIll)
                    lIllIIlIIlIIllIlIl.print('[bold white][0] Back[/]\n')
            return
        elif lIIlIIlIllIIlIIIlI == '2':
            return
        else:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            lIIlllIIlllIIIlllI.IlIlIIlIIIllllIIll()

    def lIIIlIIIllIIlllIll(lIIlllIIlllIIIlllI):
        """Handle spam sharing functionality."""
        lIIlllIIlllIIIlllI.lIIIIlIlllIIlIlIII()
        lIIlllIIlllIIIlllI.llllIlIIlIIlIlIIIl()
        if lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI and lIIlllIIlllIIIlllI.lIlIlIIllllIllllll:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {lIIlllIIlllIIIlllI.lIlIlIIllllIllllll['name']}[/]", style='bold cyan', border_style='cyan'))
        IIlllIIllIIlIlllll = lIIllIIlIllllI("[bold yellow]Note:[/] [bold white]This code does not use Facebook's API for fewer restrictions.[/]\n[bold indian_red]Caution:[/] [bold white]Do not turn off your internet while the process is ongoing.[/]", title='[bold white]𝗦𝗣𝗔𝗠 𝗣𝗢𝗦𝗧 𝗦𝗛𝗔𝗥𝗘𝗥[/]', style='bold cyan', border_style='cyan')
        lIllIIlIIlIIllIlIl.print(IIlllIIllIIlIlllll)
        IIllIlllIlIlIllIIl = lIllIIlIIlIIllIlIl.input('[bold green]🔗 Enter the Facebook post URL: [/]')
        IIllIlllIlIlIllIIl = IIllIlllIlIlIllIIl.strip()
        if not IlllIIlIIIlllI.validate_url(IIllIlllIlIlIllIIl):
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Invalid Facebook URL![/]', style='bold indian_red', border_style='indian_red'))
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        (lIlIIlllIlIllIIIII, IlIIIlIIIIIlIlllIl) = IlllIIlIIIlllI.validate_input('[bold green]Number of shares: [/]', lllllllllllIlIl, min_val=1, max_val=100000)
        if not lIlIIlllIlIllIIIII:
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        (lIlIIlllIlIllIIIII, IIIllIllIIIIIlIIlI) = IlllIIlIIIlllI.validate_input('[bold green]Delay between shares (seconds): [/]', lllllllllllIlIl, min_val=1, max_val=60)
        if not lIlIIlllIlIllIIIII:
            lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        (lIlIIlllIlIllIIIII, IlIIIIlllIIlIlllll) = lIIlllIIlllIIIlllI.lIIlllllIlIlIllIII.share_post(lIIlllIIlllIIIlllI.llIIIIllIIlIlIIllI['cookie'], IIllIlllIlIlIllIIl, IlIIIlIIIIIlIlllIl, IIIllIllIIIIIlIIlI)
        if lIlIIlllIlIllIIIII:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold green]✅ {IlIIIIlllIIlIlllll}[/]', style='bold green', border_style='green'))
        else:
            lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]❕ {IlIIIIlllIIlIlllll}[/]', style='bold indian_red', border_style='indian_red'))
        IlllIIlIIIlllI.log_activity('Share Post', lIlIIlllIlIllIIIII, IlIIIIlllIIlIlllll)
        lIllIIlIIlIIllIlIl.input('[bold white]Press Enter to continue...[/]')

def lllIllIlIlIllIllIl():
    """Main entry point of the application."""
    try:
        lIllIIllIIIIIlIIll = lllIIIIIllllIlIIII()
        lIllIIllIIIIIlIIll.lllIllIlIlIllIllIl()
    except llllllllllllIII:
        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI('[bold white]❕ Program interrupted by user.[/]', style='bold indian_red', border_style='indian_red'))
        llIlIIIlllIIII(0)
    except lllllllllllllIl as IlllIIIIllIIllIlIl:
        lIllIIlIIlIIllIlIl.print(lIIllIIlIllllI(f'[bold white]❕ An unexpected error occurred: {lllllllllllllII(IlllIIIIllIIllIlIl)}[/]', style='bold indian_red', border_style='indian_red'))
        IlIlIIllIIIlIIllll = lllIlIIllIllll.now(llllIllIlIlIII.utc).strftime('%Y-%m-%d %H:%M:%S')
        IlllIIlIIIlllI.log_activity(f'System Error (UTC: {IlIlIIllIIIlIIllll}) by {sehraks1}', lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), lllllllllllllII(IlllIIIIllIIllIlIl))
        llIlIIIlllIIII(1)
if llllllllllllIIl == '__main__':
    lllIllIlIlIllIllIl()
