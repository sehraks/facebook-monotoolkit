lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII, lllllllllllIlll, lllllllllllIllI, lllllllllllIlIl = bool, enumerate, Exception, str, IndexError, open, __name__, KeyboardInterrupt, len, ValueError, int

from os import makedirs as llIlIIIIIIlIIl, system as lllIlIIIIIlIIl, name as IIlllIIlIIllll, chmod as llllIlllllIIll
from time import sleep as IlIlIIllIlIIII
from requests import Timeout as IlllllIllllIIl, Session as lIIIIIlIIlIIIl
from re import search as llIIllIIllIIlI
from subprocess import Popen as lIIIlllIlIIIII, PIPE as lllIllIllIlllI
from sys import exit as IlllIlIlIlIIII
from datetime import datetime as llllIlIlIIIlII, timezone as IIIllIlIlllIll, timedelta as IIIllIIIlllIlI
from typing import Dict as IIIlIlIIIlIlIl, Optional as lIllIIIIIllIIl
from rich.console import Console as llllllIlIIIllI
from rich.panel import Panel as IllIllllIIlIIl
from rich.table import Table as lllIIIlIllIIIl
from modules.cookie_manager import CookieManager as lIIlIlllllIIll
from modules.spam_sharing import SpamSharing as IlIIIIIlllllII
from modules.utils import Utils as lIllIIIIlIIllI
from modules.update_settings import UpdateSettings as lIIIlIllIIIlIl
from modules.fb_login import FacebookLogin as IIIllIlllIlllI
from modules.cookie_database import CookieDatabase as IIllIIlIIlIIIl
from modules.fb_guard import FacebookGuard as IlllIIIIIllllI
lIIIlIlllllllllIIl = llllllIlIIIllI()

class lIIlIIllllllllIlll:

    def __init__(IIIIIIIIlIllIlllll):
        """Initialize the Facebook MonoToolkit."""
        IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll = None
        IIIIIIIIlIllIlllll.lllllIIIIlllIIllll = None
        try:
            with llllllllllllIlI('changelogs.txt', 'r') as lIllllIIlIIlIIlIlI:
                llIIlIIllIIIlllIII = lIllllIIlIIlIIlIlI.readline().strip()
                IIIIIIIIlIllIlllll.lIllIIIIlIlllIIlII = llIIlIIllIIIlllIII.replace('Version ', '')
        except:
            IIIIIIIIlIllIlllll.lIllIIIIlIlllIIlII = 'X.XX'
        IIIIIIIIlIllIlllll.lIllIlIIllIllllIlI = 'Greegmon'
        IIIIIIIIlIllIlllll.IIIIIIIIIlIlllIIll = 'Cerax'
        lIllIIIllIlIlllIll = llllIlIlIIIlII.now(IIIllIlIlllIll(IIIllIIIlllIlI(hours=8)))
        IIIIIIIIlIllIlllll.IIlllIIlIlIlIlIIll = lIllIIIllIlIlllIll.strftime('%B %d, %Y')
        IIIIIIIIlIllIlllll.IllIllIIIIIIlIlIll = lIllIIIllIlIlllIll.strftime('%I:%M %p')
        IIIIIIIIlIllIlllll.lIIIIlIIIIIllllIIl = 'sehraks'
        IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI = lIIlIlllllIIll()
        IIIIIIIIlIllIlllll.lIIIlIllIlIIIIIIll = IlIIIIIlllllII()
        IIIIIIIIlIllIlllll.lIIllIIIIIlIIllIII = lIIIlIllIIIlIl(IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI)
        IIIIIIIIlIllIlllll.llIIIllIlllIllIIll = IIIllIlllIlllI()
        IIIIIIIIlIllIlllll.IIIIIIllIIlllIllll = IIllIIlIIlIIIl(IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI)
        IIIIIIIIlIllIlllll.llIlIIlIlllIlllllI = IlllIIIIIllllI()
        IIIIIIIIlIllIlllll.IlIIIIIllIIIlllIII()
        IIIIIIIIlIllIlllll.lllllIIIIlllIIllll = IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.get_current_account()
        if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll:
            IIIIIIIIlIllIlllll.lIllIIIIlIIIIlllll(IIIIIIIIlIllIlllll.lllllIIIIlllIIllll)

    def lIllIIIIlIIIIlllll(IIIIIIIIlIllIlllll, IllllllIlllIIllIlI: IIIlIlIIIlIlIl) -> None:
        """Load account data for the current account."""
        if IllllllIlllIIllIlI:
            IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll = {'name': IllllllIlllIIllIlI.get('name', 'Unknown User'), 'user_id': IllllllIlllIIllIlI.get('user_id')}
        else:
            IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll = None

    def IlIIIIIllIIIlllIII(IIIIIIIIlIllIlllll):
        """Initialize necessary directories."""
        IIllIlIIllIlIIlllI = ['cookies-storage', 'logs']
        for lllllIIIllIlllIlll in IIllIlIIllIlIIlllI:
            try:
                llIlIIIIIIlIIl(lllllIIIllIlllIlll, exist_ok=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                llllIlllllIIll(lllllIIIllIlllIlll, 448)
            except lllllllllllllIl as IIllIlllIIIIIIllll:
                lIIIlIlllllllllIIl.print(f'[bold red]Error creating directory {lllllIIIllIlllIlll}: {lllllllllllllII(IIllIlllIIIIIIllll)}[/]')

    def lllIllllllIlIlllIl(IIIIIIIIlIllIlllll):
        """Clear the terminal screen."""
        lllIlIIIIIlIIl('cls' if lIllIlIIlIIIIIIlIl == 'nt' else 'clear')

    def IllIIIlIIlIIIlIIlI(IIIIIIIIlIllIlllll):
        """Display the tool banner."""
        lIllIIIllIlIlllIll = llllIlIlIIIlII.now(IIIllIlIlllIll(IIIllIIIlllIlI(hours=8)))
        IlIlIlllllIlIIIIII = lIllIIIllIlIlllIll.strftime('%I:%M %p')
        lIllIlIIllIIIlllll = lIllIIIllIlIlllIll.strftime('%B %d, %Y')
        llllllIllIIIIlllIl = IllIllllIIlIIl(f'[white]Original: {IIIIIIIIlIllIlllll.lIllIlIIllIllllIlI}[/]\n[white]Modified by: {IIIIIIIIlIllIlllll.IIIIIIIIIlIlllIIll}[/]\n[white]Version: {IIIIIIIIlIllIlllll.lIllIIIIlIlllIIlII}[/]\n[white]Date: {lIllIlIIllIIIlllll}[/]\n[white]Time: {IlIlIlllllIlIIIIII} GMT+8[/]', style='bold magenta', title='[bold yellow]𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗠𝗢𝗡𝗢𝗧𝗢𝗢𝗟𝗞𝗜𝗧[/]', border_style='cyan')
        lIIIlIlllllllllIIl.print(llllllIllIIIIlllIl)

    def IllllIlIIIIIIlIlII(IIIIIIIIlIllIlllll):
        """Check if cookie is available."""
        if not IIIIIIIIlIllIlllll.lllllIIIIlllIIllll:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Please login first using the Accounts Management option.[/]', style='bold indian_red', border_style='indian_red'))
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            return lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        return lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)

    def llIlIlIlIllIIllIlI(IIIIIIIIlIllIlllll):
        """Display and handle the main menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
            IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
            if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
            lIIlllIlIlllIllIIl = IllIllllIIlIIl('[bold white][1] Accounts Management[/]\n[bold white][2] Spam Sharing Post[/]\n[bold white][3] Profile Guard[/]\n[bold white][4] Settings[/]\n[bold red][5] Exit[/]', title='[bold white]𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨[/]', style='bold magenta', border_style='cyan')
            lIIIlIlllllllllIIl.print(lIIlllIlIlllIllIIl)
            lllIIIIllIIlIIlllI = lIIIlIlllllllllIIl.input('[bold yellow]Select an option (1-5): [/]')
            lllIIIIllIIlIIlllI = lllIIIIllIIlIIlllI.strip()
            if lllIIIIllIIlIIlllI == '1':
                IIIIIIIIlIllIlllll.IIlllIllIlIIlllIlI()
            elif lllIIIIllIIlIIlllI == '2':
                if not IIIIIIIIlIllIlllll.IllllIlIIIIIIlIlII():
                    continue
                IIIIIIIIlIllIlllll.llllIlIIlIIllllllI()
            elif lllIIIIllIIlIIlllI == '3':
                if not IIIIIIIIlIllIlllll.IllllIlIIIIIIlIlII():
                    continue
                IIIIIIIIlIllIlllll.IlIIIIIllllllllIIl()
            elif lllIIIIllIIlIIlllI == '4':
                IIIIIIIIlIllIlllll.lIlllIllIIIllIIIll()
            elif lllIIIIllIIlIIlllI == '5':
                break
            else:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')

    def lIlllIllIIIllIIIll(IIIIIIIIlIllIlllll):
        """Handle settings menu."""
        IIIIIIIIlIllIlllll.lIIllIIIIIlIIllIII.display_settings_menu()

    def IIlllIllIlIIlllIlI(IIIIIIIIlIllIlllll):
        """Handle cookie management menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
            IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
            if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold yellow]🔑 𝗔𝗖𝗖𝗢𝗨𝗡𝗧𝗦 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧[/]', style='bold yellow', border_style='yellow'))
            lIIlllIlIlllIllIIl = IllIllllIIlIIl('[bold white][1] Enter your cookie[/]\n[bold white][2] Login your Facebook account[/]\n[bold white][3] Access your Facebook accounts[/]\n[bold white][4] Cookies & Tokens Database[/]\n[bold white][5] Back to Main Menu[/]', title='[bold white]𝗦𝗘𝗟𝗘𝗖𝗧 𝗬𝗢𝗨𝗥 𝗖𝗛𝗢𝗜𝗖𝗘[/]', style='bold yellow', border_style='yellow')
            lIIIlIlllllllllIIl.print(lIIlllIlIlllIllIIl)
            lllIIIIllIIlIIlllI = lIIIlIlllllllllIIl.input('[bold yellow]Select an option: [/]')
            lllIIIIllIIlIIlllI = lllIIIIllIIlIIlllI.strip()
            if lllIIIIllIIlIIlllI == '1':
                IIIIIIIIlIllIlllll.lllIllIllIlIlIIIlI()
            elif lllIIIIllIIlIIlllI == '2':
                IIIIIIIIlIllIlllll.IlIlIIlllIIlIIllll()
            elif lllIIIIllIIlIIlllI == '3':
                if not IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.has_cookies():
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Add a cookie or login first.[/]', style='bold indian_red', border_style='indian_red'))
                    lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
                    continue
                IIIIIIIIlIllIlllll.IlIlllIlIlllIlIIII()
            elif lllIIIIllIIlIIlllI == '4':
                if not IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.has_cookies():
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Add a cookie or login first.[/]', style='bold indian_red', border_style='indian_red'))
                    lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
                    continue
                IIIIIIIIlIllIlllll.IIIIIIIIlllllllIll()
            elif lllIIIIllIIlIIlllI == '5':
                break
            else:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')

    def IlIlIIlllIIlIIllll(IIIIIIIIlIllIlllll):
        """Handle Facebook login functionality."""
        IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
        IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
        IIIlIIIlIlIIllIlII = IllIllllIIlIIl('[bold yellow]Note:[/] [bold white]You can use either your email address or Facebook UID. Mobile numbers and usernames are currently not supported yet.[/]\n[bold indian_red]Caution:[/] [bold white]Refrain from using your main account, as doing so may cause lockout or suspension.[/]', title='[bold white]𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗟𝗢𝗚𝗜𝗡[/]', style='bold yellow', border_style='yellow')
        lIIIlIlllllllllIIl.print(IIIlIIIlIlIIllIlII)
        llIlIIlIIllIIllIII = lIIIlIlllllllllIIl.input('[bold yellow]\U0001faaa Enter your credential: [/]')
        IlllIIlIIlIlIIIlIl = lIIIlIlllllllllIIl.input('[bold yellow]🔑 Enter your password: [/]')
        (lllIlllIIIlIllIIIl, lIllIIllIllIllIlll, IlIlllIIIlllIIIlll) = IIIIIIIIlIllIlllll.llIIIllIlllIllIIll.login(llIlIIlIIllIIllIII.strip(), IlllIIlIIlIlIIIlIl.strip())
        if lllIlllIIIlIllIIIl and IlIlllIIIlllIIIlll:
            IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll = IlIlllIIIlllIIIlll
            lllIlllIIIlIllIIIl = IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.add_cookie(IlIlllIIIlllIIIlll['cookie'], IlIlllIIIlllIIIlll['name'], IlIlllIIIlllIIIlll['token'])[0]
            if lllIlllIIIlIllIIIl:
                IIIIIIIIlIllIlllll.lllllIIIIlllIIllll = None
                IIllIIllIlIllIlIlI = IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.get_all_accounts()
                for IllllllIlllIIllIlI in IIllIIllIlIllIlIlI:
                    if IllllllIlllIIllIlI['user_id'] == IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['user_id']:
                        IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.set_current_account(IllllllIlllIIllIlI['id'])
                        IIIIIIIIlIllIlllll.lllllIIIIlllIIllll = IllllllIlllIIllIlI
                        break
        IIIIIIIIlIllIlllll.llIIIllIlllIllIIll.log_login_attempt(llIlIIlIIllIIllIII, lllIlllIIIlIllIIIl, lIllIIllIllIllIlll)
        lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')

    def lllIllIllIlIlIIIlI(IIIIIIIIlIllIlllll):
        """Handle adding a new cookie."""
        IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
        IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
        IIIIIIlIIlIIIlllll = IllIllllIIlIIl('[bold yellow]Note:[/] [bold white]Use semi-colon separated format, cookie must contain c_user and xs values.[/]\n[bold indian_red]Caution:[/] [bold white]JSON format is not supported for some reason.[/]', title='[bold white]𝗔𝗗𝗗 𝗬𝗢𝗨𝗥 𝗖𝗢𝗢𝗞𝗜𝗘[/]', style='bold yellow', border_style='yellow')
        lIIIlIlllllllllIIl.print(IIIIIIlIIlIIIlllll)
        lIIIIIIIIIIIIlIlIl = lIIIlIlllllllllIIl.input('[bold yellow]🍪 Enter your cookie: [/]')
        lIIIIIIIIIIIIlIlIl = lIIIIIIIIIIIIlIlIl.strip()
        if not lIIIIIIIIIIIIlIlIl:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Cookie cannot be empty![/]', style='bold indian_red', border_style='indian_red'))
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            return
        lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]🔄 Validating cookie format...[/]', style='bold cyan', border_style='cyan'))
        IlIlIIllIlIIII(1)
        if 'c_user=' not in lIIIIIIIIIIIIlIlIl or 'xs=' not in lIIIIIIIIIIIIlIlIl:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid cookie format! Cookie must contain c_user and xs values.[/]', style='bold indian_red', border_style='indian_red'))
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            return
        lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]✅ Cookie format is valid![/]', style='bold green', border_style='green'))
        IlIlIIllIlIIII(1)
        try:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl("[bold white]🔄 Getting account's token...[/]", style='bold cyan', border_style='cyan'))
            IlIlIIllIlIIII(1.5)
            lIIIllllIIlIlllIll = lIIIIIlIIlIIIl()
            try:
                for IlIlIIlllllllIIIII in lIIIIIIIIIIIIlIlIl.split(';'):
                    if '=' in IlIlIIlllllllIIIII:
                        (lIllIlIIlIIIIIIlIl, IllIllllllIlIIIIll) = IlIlIIlllllllIIIII.strip().split('=', 1)
                        lIIIllllIIlIlllIll.cookies.set(lIllIlIIlIIIIIIlIl, IllIllllllIlIIIIll)
            except lllllllllllllIl as IIllIlllIIIIIIllll:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]❕ Error parsing cookie: {lllllllllllllII(IIllIlllIIIIIIllll)}[/]', style='bold indian_red', border_style='indian_red'))
                IlIlIIllIlIIII(1)
            IIlIlIlIIIIllIlIII = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Upgrade-Insecure-Requests': '1'}
            IlIIlIllIllIIIIIll = None
            lllIIlIIIlllIIIllI = [('Ads Manager', 'https://adsmanager.facebook.com/adsmanager/', 'accessToken="(EAA[A-Za-z0-9]+)"'), ('Business Manager', 'https://business.facebook.com/content_management', '"(EAA[A-Za-z0-9]+)"'), ('Feed Composer', 'https://www.facebook.com/composer/ocelot/async_loader/?publisher=feed', '"accessToken":"(EAA[A-Za-z0-9]+)"')]
            for (lIlIllIlIIIIIlIIII, IlIlIIIlIIIIIlIIll, llIIllIlIllllIIIII) in lllIIlIIIlllIIIllI:
                try:
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]🔄 Trying {lIlIllIlIIIIIlIIII} method...[/]', style='bold cyan', border_style='cyan'))
                    IlIlIIllIlIIII(1)
                    IIIlIllIIIlIlIIIIl = lIIIllllIIlIlllIll.get(IlIlIIIlIIIIIlIIll, headers=IIlIlIlIIIIllIlIII, timeout=30)
                    if IIIlIllIIIlIlIIIIl.ok:
                        lIlIIlllllllIlIlIl = llIIllIIllIIlI(llIIllIlIllllIIIII, IIIlIllIIIlIlIIIIl.text)
                        if lIlIIlllllllIlIlIl:
                            IlIIlIllIllIIIIIll = lIlIIlllllllIlIlIl.group(1)
                            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]✅ Token found using {lIlIllIlIIIIIlIIII}![/]', style='bold green', border_style='green'))
                            IlIlIIllIlIIII(1)
                            break
                except IlllllIllllIIl:
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]❕ {lIlIllIlIIIIIlIIII} request timed out[/]', style='bold indian_red', border_style='indian_red'))
                except lllllllllllllIl as IIllIlllIIIIIIllll:
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]❕ Error with {lIlIllIlIIIIIlIIII}: {lllllllllllllII(IIllIlllIIIIIIllll)}[/]', style='bold indian_red', border_style='indian_red'))
            if IlIIlIllIllIIIIIll:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold green]✅ Successfully retrieved token![/]', style='bold green', border_style='green'))
                IlIlIIllIlIIII(1)
            else:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Could not retrieve token. Continuing anyway...[/]', style='bold indian_red', border_style='indian_red'))
                IlIlIIllIlIIII(1)
                IlIIlIllIllIIIIIll = 'N/A'
        except lllllllllllllIl as IIllIlllIIIIIIllll:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]❕ Error during token extraction: {lllllllllllllII(IIllIlllIIIIIIllll)}. Continuing anyway...[/]', style='bold indian_red', border_style='indian_red'))
            IlIlIIllIlIIII(1)
            IlIIlIllIllIIIIIll = 'N/A'
        lIIllllIIlIIIllIlI = None
        if 'name=' not in lIIIIIIIIIIIIlIlIl:
            lIIllllIIlIIIllIlI = lIIIlIlllllllllIIl.input('[bold yellow]💳 Enter your name: [/]').strip()
            if not lIIllllIIlIIIllIlI:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Please enter your Facebook account name[/]', style='bold indian_red', border_style='indian_red'))
                lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
                return
        lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]🔄 Saving account data...[/]', style='bold cyan', border_style='cyan'))
        IlIlIIllIlIIII(1)
        (lllIlllIIIlIllIIIl, lIllIIllIllIllIlll) = IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.add_cookie(lIIIIIIIIIIIIlIlIl, lIIllllIIlIIIllIlI, IlIIlIllIllIIIIIll)
        if lllIlllIIIlIllIIIl:
            IIllIIllIlIllIlIlI = IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.get_all_accounts()
            IIIllllIIIIllIlIII = IIllIIllIlIllIlIlI[-1]
            IIIIIIIIlIllIlllll.lllllIIIIlllIIllll = IIIllllIIIIllIlIII
            IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.set_current_account(IIIllllIIIIllIlIII['id'])
            IIIIIIIIlIllIlllll.lIllIIIIlIIIIlllll(IIIllllIIIIllIlIII)
            IlIlIIllIlIIII(1)
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold green]✅ Cookie added successfully!\n👤 Account: {IIIllllIIIIllIlIII['name']}\n📩 UID: {IIIllllIIIIllIlIII['user_id']}[/]", style='bold green', border_style='green'))
        else:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]❕ {lIllIIllIllIllIlll}[/]', style='bold indian_red', border_style='indian_red'))
        lIllIIIllIlIlllIll = llllIlIlIIIlII.now(IIIllIlIlllIll(IIIllIIIlllIlI(hours=8)))
        lIllIlIIIlIllIIIIl = lIllIIIllIlIlllIll.strftime('%B %d, %Y %I:%M %p')
        lIllIIIIlIIllI.log_activity(f'Add Cookie (PH: {lIllIlIIIlIllIIIIl}) by {IIIIIIIIlIllIlllll.lIIIIlIIIIIllllIIl}', lllIlllIIIlIllIIIl, lIllIIllIllIllIlll)
        lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')

    def IlIIIIIllllllllIIl(IIIIIIIIlIllIlllll):
        """Handle Profile Guard operations."""
        if not IIIIIIIIlIllIlllll.lllllIIIIlllIIllll:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Please select an account first[/]', style='bold indian_red', border_style='indian_red'))
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            return
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
            IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.lllllIIIIlllIIllll['name']}[/]", style='bold cyan', border_style='cyan'))
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold yellow]Note:[/] [bold white]Make sure you turn off first your Facebook lock profile before proceeding to Facebook Profile Guard.[/]\n\n[1] Activate your Facebook Profile Shield\n[2] Deactivate your Facebook Profile Shield\n[3] Back to Main Menu', title='[bold white]🛡️ 𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 𝗚𝗨𝗔𝗥𝗗[/]', style='bold cyan', border_style='cyan'))
            lllIIIIllIIlIIlllI = lIIIlIlllllllllIIl.input('[bold yellow]Enter your choice: [/]').strip()
            if lllIIIIllIIlIIlllI == '1' or lllIIIIllIIlIIlllI == '2':
                llIllllIIIIllIIlll = lllIIIIllIIlIIlllI == '1'
                (lllIlllIIIlIllIIIl, lIllIIllIllIllIlll) = IIIIIIIIlIllIlllll.llIlIIlIlllIlllllI.toggle_profile_shield(IIIIIIIIlIllIlllll.lllllIIIIlllIIllll, llIllllIIIIllIIlll)
                if lllIlllIIIlIllIIIl:
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold white]✅ {lIllIIllIllIllIlll}\nName: {IIIIIIIIlIllIlllll.lllllIIIIlllIIllll['name']}\nUID: {IIIIIIIIlIllIlllll.lllllIIIIlllIIllll['user_id']}[/]", style='bold green', border_style='green'))
                else:
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]❕ {lIllIIllIllIllIlll}[/]', style='bold indian_red', border_style='indian_red'))
                lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            elif lllIIIIllIIlIIlllI == '3':
                break
            else:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid choice![/]', style='bold indian_red', border_style='indian_red'))
                lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')

    def IlIlllIlIlllIlIIII(IIIIIIIIlIllIlllll):
        """Handle cookie settings and storage menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
            IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
            if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
            IIllIIllIlIllIlIlI = IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.get_all_accounts()
            for (llIIIIIllIlllllllI, IllllllIlllIIllIlI) in llllllllllllllI(IIllIIllIlIllIlIlI, 1):
                IIIIIlIIlIlIIlllIl = 'Logged in' if IllllllIlllIIllIlI == IIIIIIIIlIllIlllll.lllllIIIIlllIIllll else 'Logged out'
                IIIllIlllIIIIIlIIl = 'green' if IIIIIlIIlIlIIlllIl == 'Logged in' else 'red'
                llIIlllIllIIIlllll = IllllllIlllIIllIlI.get('name', 'Unknown User')
                IlIllIlIlIlllIlIII = IllIllllIIlIIl(f"[bold white]Name: {llIIlllIllIIIlllll}[/]\n[bold white]UID: {IllllllIlllIIllIlI['user_id']}[/]\n[bold {IIIllIlllIIIIIlIIl}]Status: {IIIIIlIIlIlIIlllIl}[/]\n" + (f'[bold yellow][{llIIIIIllIlllllllI}] Select[/]\n' if IllllllIlllIIllIlI != IIIIIIIIlIllIlllll.lllllIIIIlllIIllll else '') + f'[bold red][R{llIIIIIllIlllllllI}] Remove[/]', title=f'[bold yellow]📨 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 {llIIIIIllIlllllllI}[/]', style='bold yellow', border_style='yellow')
                lIIIlIlllllllllIIl.print(IlIllIlIlIlllIlIII)
            lIIIlIlllllllllIIl.print('[bold white][0] Back[/]\n')
            lllIIIIllIIlIIlllI = lIIIlIlllllllllIIl.input('[bold yellow]Select an option: [/]')
            lllIIIIllIIlIIlllI = lllIIIIllIIlIIlllI.strip().upper()
            if lllIIIIllIIlIIlllI == '0':
                break
            if lllIIIIllIIlIIlllI.startswith('R'):
                try:
                    llIIIIIllIlllllllI = lllllllllllIlIl(lllIIIIllIIlIIlllI[1:]) - 1
                    if 0 <= llIIIIIllIlllllllI < lllllllllllIlll(IIllIIllIlIllIlIlI):
                        lIllllIIIIIIIIllII = IIllIIllIlIllIlIlI[llIIIIIllIlllllllI]
                        if IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll and lIllllIIIIIIIIllII['user_id'] == IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['user_id']:
                            llIIlllIllIIIlllll = IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']
                        else:
                            llIIlllIllIIIlllll = 'Unknown User'
                        llIllIlIIIIllIIIIl = lIIIlIlllllllllIIl.input(f'[bold red]Are you sure you want to remove {llIIlllIllIIIlllll}? (y/N): [/]').strip().lower()
                        if llIllIlIIIIllIIIIl == 'y':
                            if lIllllIIIIIIIIllII == IIIIIIIIlIllIlllll.lllllIIIIlllIIllll:
                                IIIIIIIIlIllIlllll.lllllIIIIlllIIllll = None
                                IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll = None
                            lllIlllIIIlIllIIIl = IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.remove_cookie(lIllllIIIIIIIIllII)
                            if lllIlllIIIlIllIIIl:
                                lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold green]✅ Successfully removed account: {llIIlllIllIIIlllll}[/]', style='bold green', border_style='green'))
                            else:
                                lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Failed to remove account![/]', style='bold indian_red', border_style='indian_red'))
                    else:
                        lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid selection![/]', style='bold indian_red', border_style='indian_red'))
                except (lllllllllllIllI, llllllllllllIll):
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid input![/]', style='bold indian_red', border_style='indian_red'))
            else:
                try:
                    IIllIlIIlIlllIllll = lllllllllllIlIl(lllIIIIllIIlIIlllI) - 1
                    if 0 <= IIllIlIIlIlllIllll < lllllllllllIlll(IIllIIllIlIllIlIlI):
                        if IIllIIllIlIllIlIlI[IIllIlIIlIlllIllll] != IIIIIIIIlIllIlllll.lllllIIIIlllIIllll:
                            IIIIIIIIlIllIlllll.lllllIIIIlllIIllll = IIllIIllIlIllIlIlI[IIllIlIIlIlllIllll]
                            IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.set_current_account(IIIIIIIIlIllIlllll.lllllIIIIlllIIllll['id'])
                            IIIIIIIIlIllIlllll.lIllIIIIlIIIIlllll(IIIIIIIIlIllIlllll.lllllIIIIlllIIllll)
                            llIIlllIllIIIlllll = IIIIIIIIlIllIlllll.lllllIIIIlllIIllll['name']
                            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold green]✅ Successfully switched to account: {llIIlllIllIIIlllll}[/]', style='bold green', border_style='green'))
                        else:
                            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ This account is already selected.[/]', style='bold indian_red', border_style='indian_red'))
                    else:
                        lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid selection![/]', style='bold indian_red', border_style='indian_red'))
                except lllllllllllIllI:
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid input![/]', style='bold indian_red', border_style='indian_red'))
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')

    def IIIIIIIIlllllllIll(IIIIIIIIlIllIlllll):
        """Handle cookie database functionality."""
        IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
        IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
        if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
        lllIIlIllllIIIIIII = IllIllllIIlIIl('[bold yellow]Note:[/] [bold white]You can manage all your stored cookies and tokens here[/]\n[bold indian_red]Caution:[/] [bold white]Deleting cookies cannot be undone[/]', title='[bold white]𝗖𝗢𝗢𝗞𝗜𝗘𝗦 & 𝗧𝗢𝗞𝗘𝗡𝗦 𝗗𝗔𝗧𝗔𝗕𝗔𝗦𝗘[/]', style='bold cyan', border_style='cyan')
        lIIIlIlllllllllIIl.print(lllIIlIllllIIIIIII)
        lIIlllIlIlllIllIIl = IllIllllIIlIIl('[bold white][1] View All Cookies & Tokens[/]\n[bold white][2] Back to Main Menu[/]', style='bold cyan', border_style='cyan')
        lIIIlIlllllllllIIl.print(lIIlllIlIlllIllIIl)
        lllIIIIllIIlIIlllI = lIIIlIlllllllllIIl.input('[bold cyan]Enter your choice: [/]')
        if lllIIIIllIIlIIlllI == '1':
            IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
            IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
            if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
                lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
            lIIIlIlllllllllIIl.print(lllIIlIllllIIIIIII)
            IIllIIllIlIllIlIlI = IIIIIIIIlIllIlllll.lIllllIlIIIIlIlllI.get_all_accounts()
            for (llIIIIIllIlllllllI, IllllllIlllIIllIlI) in llllllllllllllI(IIllIIllIlIllIlIlI, 1):
                lIllIIIllIlIlllIll = llllIlIlIIIlII.now(IIIllIlIlllIll(IIIllIIIlllIlI(hours=8)))
                IIIllIlIlIlIIlIIlI = lIllIIIllIlIlllIll.strftime('%B %d, %Y')
                llllIIlIIIIIlIlIlI = lIllIIIllIlIlllIll.strftime('%I:%M %p +8 GMT (PH)')
                lIIIIIIIIIIIIlIlIl = IllllllIlllIIllIlI['cookie']
                lIIIIIIIIIIlIIIIll = IllllllIlllIIllIlI.get('token', 'N/A')
                llllIllIIIIIIlIIIl = lIIIIIIIIIIIIlIlIl[:20] + '...' + lIIIIIIIIIIIIlIlIl[-10:] if lllllllllllIlll(lIIIIIIIIIIIIlIlIl) > 30 else lIIIIIIIIIIIIlIlIl
                IlIlIIllIIlIlIllIl = lIIIIIIIIIIlIIIIll[:20] + '...' + lIIIIIIIIIIlIIIIll[-10:] if lllllllllllIlll(lIIIIIIIIIIlIIIIll) > 30 else lIIIIIIIIIIlIIIIll
                IIIIIIlIIlIIIlllll = IllIllllIIlIIl(f"[bold white]Name: {IllllllIlllIIllIlI.get('name', 'Unknown User')}[/]\n[bold white]Cookie: {llllIllIIIIIIlIIIl}[/]\n[bold white]Token: {IlIlIIllIIlIlIllIl}[/]\n[bold white]Added Date: {IIIllIlIlIlIIlIIlI}[/]\n[bold white]Added Time: {llllIIlIIIIIlIlIlI}[/]\n\n[bold yellow][C{llIIIIIllIlllllllI}] Copy cookie[/]\n[bold yellow][T{llIIIIIllIlllllllI}] Copy token[/]", title=f'[bold yellow]📨 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 {llIIIIIllIlllllllI}[/]', style='bold yellow', border_style='yellow')
                lIIIlIlllllllllIIl.print(IIIIIIlIIlIIIlllll)
            lIIIlIlllllllllIIl.print('[bold white][0] Back[/]\n')
            while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
                IIlllIIIlIIllIIllI = lIIIlIlllllllllIIl.input('[bold yellow]Select an option: [/]').strip().upper()
                if IIlllIIIlIIllIIllI == '0':
                    break
                if IIlllIIIlIIllIIllI.startswith(('C', 'T')):
                    try:
                        llIIIIIllIlllllllI = lllllllllllIlIl(IIlllIIIlIIllIIllI[1:]) - 1
                        if 0 <= llIIIIIllIlllllllI < lllllllllllIlll(IIllIIllIlIllIlIlI):
                            try:
                                IIIIIIlIIlIlIIIllI = IIllIIllIlIllIlIlI[llIIIIIllIlllllllI]['cookie'] if IIlllIIIlIIllIIllI.startswith('C') else IIllIIllIlIllIlIlI[llIIIIIllIlllllllI].get('token', '')
                                lIIIlIIlllIIllIIll = 'Cookie' if IIlllIIIlIIllIIllI.startswith('C') else 'Token'
                                if not IIIIIIlIIlIlIIIllI and lIIIlIIlllIIllIIll == 'Token':
                                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ No token available for this account![/]', style='bold indian_red', border_style='indian_red'))
                                else:
                                    IlIIlIlIIIIIIIlIIl = lIIIlllIlIIIII(['termux-clipboard-set'], stdin=lllIllIllIlllI)
                                    IlIIlIlIIIIIIIlIIl.communicate(input=IIIIIIlIIlIlIIIllI.encode())
                                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]✅ {lIIIlIIlllIIllIIll} {llIIIIIllIlllllllI + 1} copied to clipboard![/]', style='bold green', border_style='green'))
                            except lllllllllllllIl as IIllIlllIIIIIIllll:
                                lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Failed to copy to clipboard. Make sure Termux:API is installed.[/]', style='bold indian_red', border_style='indian_red'))
                            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
                            IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
                            IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
                            if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
                                lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
                            lIIIlIlllllllllIIl.print(lllIIlIllllIIIIIII)
                            for (llIIIIIllIlllllllI, IllllllIlllIIllIlI) in llllllllllllllI(IIllIIllIlIllIlIlI, 1):
                                lIIIlIlllllllllIIl.print(IIIIIIlIIlIIIlllll)
                            lIIIlIlllllllllIIl.print('[bold white][0] Back[/]\n')
                            break
                        else:
                            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
                            IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
                            IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
                            if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
                                lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
                            lIIIlIlllllllllIIl.print(lllIIlIllllIIIIIII)
                            for (llIIIIIllIlllllllI, IllllllIlllIIllIlI) in llllllllllllllI(IIllIIllIlIllIlIlI, 1):
                                lIIIlIlllllllllIIl.print(IIIIIIlIIlIIIlllll)
                            lIIIlIlllllllllIIl.print('[bold white][0] Back[/]\n')
                    except lllllllllllIllI:
                        lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                        lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
                        IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
                        IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
                        if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
                            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
                        lIIIlIlllllllllIIl.print(lllIIlIllllIIIIIII)
                        for (llIIIIIllIlllllllI, IllllllIlllIIllIlI) in llllllllllllllI(IIllIIllIlIllIlIlI, 1):
                            lIIIlIlllllllllIIl.print(IIIIIIlIIlIIIlllll)
                        lIIIlIlllllllllIIl.print('[bold white][0] Back[/]\n')
                else:
                    lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                    lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
                    IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
                    IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
                    if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
                        lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
                    lIIIlIlllllllllIIl.print(lllIIlIllllIIIIIII)
                    for (llIIIIIllIlllllllI, IllllllIlllIIllIlI) in llllllllllllllI(IIllIIllIlIllIlIlI, 1):
                        lIIIlIlllllllllIIl.print(IIIIIIlIIlIIIlllll)
                    lIIIlIlllllllllIIl.print('[bold white][0] Back[/]\n')
            return
        elif lllIIIIllIIlIIlllI == '2':
            return
        else:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            IIIIIIIIlIllIlllll.IIIIIIIIlllllllIll()

    def llllIlIIlIIllllllI(IIIIIIIIlIllIlllll):
        """Handle spam sharing functionality."""
        IIIIIIIIlIllIlllll.lllIllllllIlIlllIl()
        IIIIIIIIlIllIlllll.IllIIIlIIlIIIlIIlI()
        if IIIIIIIIlIllIlllll.lllllIIIIlllIIllll and IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIIIIIIIlIllIlllll.IlIlllIIIlllIIIlll['name']}[/]", style='bold cyan', border_style='cyan'))
        IlllIlIlllIIIlllIl = IllIllllIIlIIl("[bold yellow]Note:[/] [bold white]This code does not use Facebook's API for fewer restrictions.[/]\n[bold indian_red]Caution:[/] [bold white]Do not turn off your internet while the process is ongoing.[/]", title='[bold white]𝗦𝗣𝗔𝗠 𝗣𝗢𝗦𝗧 𝗦𝗛𝗔𝗥𝗘𝗥[/]', style='bold cyan', border_style='cyan')
        lIIIlIlllllllllIIl.print(IlllIlIlllIIIlllIl)
        lIllIlIIlIIIIlllIl = lIIIlIlllllllllIIl.input('[bold green]🔗 Enter the Facebook post URL: [/]')
        lIllIlIIlIIIIlllIl = lIllIlIIlIIIIlllIl.strip()
        if not lIllIIIIlIIllI.validate_url(lIllIlIIlIIIIlllIl):
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Invalid Facebook URL![/]', style='bold indian_red', border_style='indian_red'))
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            return
        (lllIlllIIIlIllIIIl, IIlIIlllllIIlIlIll) = lIllIIIIlIIllI.validate_input('[bold green]Number of shares: [/]', lllllllllllIlIl, min_val=1, max_val=100000)
        if not lllIlllIIIlIllIIIl:
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            return
        (lllIlllIIIlIllIIIl, llIIlIIllllIlIIIII) = lIllIIIIlIIllI.validate_input('[bold green]Delay between shares (seconds): [/]', lllllllllllIlIl, min_val=1, max_val=60)
        if not lllIlllIIIlIllIIIl:
            lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')
            return
        (lllIlllIIIlIllIIIl, lIllIIllIllIllIlll) = IIIIIIIIlIllIlllll.lIIIlIllIlIIIIIIll.share_post(IIIIIIIIlIllIlllll.lllllIIIIlllIIllll['cookie'], lIllIlIIlIIIIlllIl, IIlIIlllllIIlIlIll, llIIlIIllllIlIIIII)
        if lllIlllIIIlIllIIIl:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold green]✅ {lIllIIllIllIllIlll}[/]', style='bold green', border_style='green'))
        else:
            lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]❕ {lIllIIllIllIllIlll}[/]', style='bold indian_red', border_style='indian_red'))
        lIllIIIIlIIllI.log_activity('Share Post', lllIlllIIIlIllIIIl, lIllIIllIllIllIlll)
        lIIIlIlllllllllIIl.input('[bold white]Press Enter to continue...[/]')

def llIlIlIlIllIIllIlI():
    """Main entry point of the application."""
    try:
        IIIlllllllIIIllIII = lIIlIIllllllllIlll()
        IIIlllllllIIIllIII.llIlIlIlIllIIllIlI()
    except llllllllllllIII:
        lIIIlIlllllllllIIl.print(IllIllllIIlIIl('[bold white]❕ Program interrupted by user.[/]', style='bold indian_red', border_style='indian_red'))
        IlllIlIlIlIIII(0)
    except lllllllllllllIl as IIllIlllIIIIIIllll:
        lIIIlIlllllllllIIl.print(IllIllllIIlIIl(f'[bold white]❕ An unexpected error occurred: {lllllllllllllII(IIllIlllIIIIIIllll)}[/]', style='bold indian_red', border_style='indian_red'))
        IIIIlIlIlIlIIlIIII = llllIlIlIIIlII.now(IIIllIlIlllIll.utc).strftime('%Y-%m-%d %H:%M:%S')
        lIllIIIIlIIllI.log_activity(f'System Error (UTC: {IIIIlIlIlIlIIlIIII}) by {sehraks}', lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), lllllllllllllII(IIllIlllIIIIIIllll))
        IlllIlIlIlIIII(1)
if llllllllllllIIl == '__main__':
    llIlIlIlIllIIllIlI()
