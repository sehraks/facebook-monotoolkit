lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI, llllllllllllIIl, llllllllllllIII, lllllllllllIlll, lllllllllllIllI, lllllllllllIlIl = bool, enumerate, Exception, str, IndexError, open, __name__, KeyboardInterrupt, len, ValueError, int

from os import makedirs as IIIlIIIlIllIlI, system as IlIlllIllIIIll, name as IllIllIllIllII, chmod as IlIIIIllIlIlll
from time import sleep as IlIIIIllllllII
from requests import Timeout as IlIIIlIlIllllI, Session as IIIlllllIlllll
from re import search as IlllIIIllIIIIl
from subprocess import Popen as IIllIIIIIIlllI, PIPE as lllIIIIIlIIlII
from sys import exit as IllIIIIlllllIl
from datetime import datetime as lIllIIlIllIIII, timezone as llllllllIlllII, timedelta as llIIIlIIIIIlII
from typing import Dict as IIlIlIIIIlIIll, Optional as IllllIllIlIllI
from rich.console import Console as IllIlIIlllIIlI
from rich.panel import Panel as IllllIlIlIlIll
from rich.table import Table as IlIllIllIllIlI
from modules.cookie_manager import CookieManager as llIIIlIlIIIlIl
from modules.spam_sharing import SpamSharing as lIlllllIlIIllI
from modules.utils import Utils as IIIIIllllIIlII
from modules.update_settings import UpdateSettings as IlIllIlIIIIlII
from modules.fb_login import FacebookLogin as IIllllIIIIlIII
from modules.cookie_database import CookieDatabase as lIlIIlIIIIlIII
from modules.fb_guard import FacebookGuard as IlIIIIIlIlIlll
llIIIIlIlllIllIlIl = IllIlIIlllIIlI()

class lllIlIlllIIlIlllll:

    def __init__(IIlIIllIlIlIIlllIl):
        """Initialize the Facebook MonoToolkit."""
        IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII = None
        IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl = None
        try:
            with llllllllllllIlI('changelogs.txt', 'r') as llIIlllIIlIIlIIIlI:
                lIllIllllIlIIIlIlI = llIIlllIIlIIlIIIlI.readline().strip()
                IIlIIllIlIlIIlllIl.IIlIIllIlllIIlIIII = lIllIllllIlIIIlIlI.replace('Version ', '')
        except:
            IIlIIllIlIlIIlllIl.IIlIIllIlllIIlIIII = 'X.XX'
        IIlIIllIlIlIIlllIl.IIllIlIIIIIlllllll = 'Greegmon'
        IIlIIllIlIlIIlllIl.lIlIlIllIIIIIlIIll = 'Cerax'
        IllIIIllIllllIlllI = lIllIIlIllIIII.now(llllllllIlllII(llIIIlIIIIIlII(hours=8)))
        IIlIIllIlIlIIlllIl.IllIIIlIlIIIIIIlIl = IllIIIllIllllIlllI.strftime('%B %d, %Y')
        IIlIIllIlIlIIlllIl.IlIIllllIIIllllIll = IllIIIllIllllIlllI.strftime('%I:%M %p')
        IIlIIllIlIlIIlllIl.llllIlllIlllIIIIII = 'sehraks'
        IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll = llIIIlIlIIIlIl()
        IIlIIllIlIlIIlllIl.IIIIllllIIIlIIIIll = lIlllllIlIIllI()
        IIlIIllIlIlIIlllIl.IllIllIIllIllIIIII = IlIllIlIIIIlII(IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI)
        IIlIIllIlIlIIlllIl.lIllIlllIIIIIIIlll = IIllllIIIIlIII()
        IIlIIllIlIlIIlllIl.IIllIllllIlIllIIll = lIlIIlIIIIlIII(IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll)
        IIlIIllIlIlIIlllIl.llIlIIllIIllIllIlI = IlIIIIIlIlIlll()
        IIlIIllIlIlIIlllIl.IlIIIllIIllIlIlllI()
        IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl = IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.get_current_account()
        if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl:
            IIlIIllIlIlIIlllIl.IIlIIllIIlIIIlIIll(IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl)

    def IIlIIllIIlIIIlIIll(IIlIIllIlIlIIlllIl, llllIlllIlIIllIIIl: IIlIlIIIIlIIll) -> None:
        """Load account data for the current account."""
        if llllIlllIlIIllIIIl:
            IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII = {'name': llllIlllIlIIllIIIl.get('name', 'Unknown User'), 'user_id': llllIlllIlIIllIIIl.get('user_id')}
        else:
            IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII = None

    def IlIIIllIIllIlIlllI(IIlIIllIlIlIIlllIl):
        """Initialize necessary directories."""
        lIlllIIIIlIIlllIIl = ['cookies-storage', 'logs']
        for llIllIIIIIIllllIIl in lIlllIIIIlIIlllIIl:
            try:
                IIIlIIIlIllIlI(llIllIIIIIIllllIIl, exist_ok=lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
                IlIIIIllIlIlll(llIllIIIIIIllllIIl, 448)
            except lllllllllllllIl as llIIlIIlIIlIIlIIII:
                llIIIIlIlllIllIlIl.print(f'[bold red]Error creating directory {llIllIIIIIIllllIIl}: {lllllllllllllII(llIIlIIlIIlIIlIIII)}[/]')

    def IlIIllIIlIIIllIlll(IIlIIllIlIlIIlllIl):
        """Clear the terminal screen."""
        IlIlllIllIIIll('cls' if lllllIIllIlIIIIIll == 'nt' else 'clear')

    def IlIIllIlIIIlIlIllI(IIlIIllIlIlIIlllIl):
        """Display the tool banner."""
        IllIIIllIllllIlllI = lIllIIlIllIIII.now(llllllllIlllII(llIIIlIIIIIlII(hours=8)))
        llllllIlIIlIllIlII = IllIIIllIllllIlllI.strftime('%I:%M %p')
        lllIlIIlIIlIIIIIII = IllIIIllIllllIlllI.strftime('%B %d, %Y')
        lIllIIllIllllIIllI = IllllIlIlIlIll(f'[white]Original: {IIlIIllIlIlIIlllIl.IIllIlIIIIIlllllll}[/]\n[white]Modified by: {IIlIIllIlIlIIlllIl.lIlIlIllIIIIIlIIll}[/]\n[white]Version: {IIlIIllIlIlIIlllIl.IIlIIllIlllIIlIIII}[/]\n[white]Date: {lllIlIIlIIlIIIIIII}[/]\n[white]Time: {llllllIlIIlIllIlII} GMT+8[/]', style='bold magenta', title='[bold yellow]𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗠𝗢𝗡𝗢𝗧𝗢𝗢𝗟𝗞𝗜𝗧[/]', border_style='cyan')
        llIIIIlIlllIllIlIl.print(lIllIIllIllllIIllI)

    def IIIIIlllllIIIIIIlI(IIlIIllIlIlIIlllIl):
        """Check if cookie is available."""
        if not IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Please login first using the Accounts Management option.[/]', style='bold indian_red', border_style='indian_red'))
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)
        return lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)

    def lIllIllIIllllIlIll(IIlIIllIlIlIIlllIl):
        """Display and handle the main menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
            IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
            if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
            IIIIIIIIIllIIlIIll = IllllIlIlIlIll('[bold white][1] Accounts Management[/]\n[bold white][2] Spam Sharing Post[/]\n[bold white][3] Profile Guard[/]\n[bold white][4] Settings[/]\n[bold red][5] Exit[/]', title='[bold white]𝗠𝗔𝗜𝗡 𝗠𝗘𝗡𝗨[/]', style='bold magenta', border_style='cyan')
            llIIIIlIlllIllIlIl.print(IIIIIIIIIllIIlIIll)
            lIlIlIlIlIllIlIIll = llIIIIlIlllIllIlIl.input('[bold yellow]Select an option (1-5): [/]')
            lIlIlIlIlIllIlIIll = lIlIlIlIlIllIlIIll.strip()
            if lIlIlIlIlIllIlIIll == '1':
                IIlIIllIlIlIIlllIl.IIlllllllllIIIllII()
            elif lIlIlIlIlIllIlIIll == '2':
                if not IIlIIllIlIlIIlllIl.IIIIIlllllIIIIIIlI():
                    continue
                IIlIIllIlIlIIlllIl.IIlllIIIIIIIlIlllI()
            elif lIlIlIlIlIllIlIIll == '3':
                if not IIlIIllIlIlIIlllIl.IIIIIlllllIIIIIIlI():
                    continue
                IIlIIllIlIlIIlllIl.IIIIlIIIIlIlIllIll()
            elif lIlIlIlIlIllIlIIll == '4':
                IIlIIllIlIlIIlllIl.llllIllllIllllIIlI()
            elif lIlIlIlIlIllIlIIll == '5':
                break
            else:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def llllIllllIllllIIlI(IIlIIllIlIlIIlllIl):
        """Handle settings menu."""
        IIlIIllIlIlIIlllIl.IllIllIIllIllIIIII.display_settings_menu()

    def IIlllllllllIIIllII(IIlIIllIlIlIIlllIl):
        """Handle cookie management menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
            IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
            if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold yellow]🔑 𝗔𝗖𝗖𝗢𝗨𝗡𝗧𝗦 𝗠𝗔𝗡𝗔𝗚𝗘𝗠𝗘𝗡𝗧[/]', style='bold yellow', border_style='yellow'))
            IIIIIIIIIllIIlIIll = IllllIlIlIlIll('[bold white][1] Enter your cookie[/]\n[bold white][2] Login your Facebook account[/]\n[bold white][3] Access your Facebook accounts[/]\n[bold white][4] Cookies & Tokens Database[/]\n[bold white][5] Back to Main Menu[/]', title='[bold white]𝗦𝗘𝗟𝗘𝗖𝗧 𝗬𝗢𝗨𝗥 𝗖𝗛𝗢𝗜𝗖𝗘[/]', style='bold yellow', border_style='yellow')
            llIIIIlIlllIllIlIl.print(IIIIIIIIIllIIlIIll)
            lIlIlIlIlIllIlIIll = llIIIIlIlllIllIlIl.input('[bold yellow]Select an option: [/]')
            lIlIlIlIlIllIlIIll = lIlIlIlIlIllIlIIll.strip()
            if lIlIlIlIlIllIlIIll == '1':
                IIlIIllIlIlIIlllIl.IIIIIIIllIlIllIllI()
            elif lIlIlIlIlIllIlIIll == '2':
                IIlIIllIlIlIIlllIl.IIIIlIllllIIlIlIII()
            elif lIlIlIlIlIllIlIIll == '3':
                if not IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.has_cookies():
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Add a cookie or login first.[/]', style='bold indian_red', border_style='indian_red'))
                    llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
                    continue
                IIlIIllIlIlIIlllIl.lIlIIIIllIIIlIllII()
            elif lIlIlIlIlIllIlIIll == '4':
                if not IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.has_cookies():
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Add a cookie or login first.[/]', style='bold indian_red', border_style='indian_red'))
                    llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
                    continue
                IIlIIllIlIlIIlllIl.IllIIIllllIIlIllII()
            elif lIlIlIlIlIllIlIIll == '5':
                break
            else:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def IIIIlIllllIIlIlIII(IIlIIllIlIlIIlllIl):
        """Handle Facebook login functionality."""
        IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
        IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
        llIIllIIIIIlIIIIIl = IllllIlIlIlIll('[bold yellow]Note:[/] [bold white]You can use either your email address or Facebook UID. Mobile numbers and usernames are currently not supported yet.[/]\n[bold indian_red]Caution:[/] [bold white]Refrain from using your main account, as doing so may cause lockout or suspension.[/]', title='[bold white]𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗟𝗢𝗚𝗜𝗡[/]', style='bold yellow', border_style='yellow')
        llIIIIlIlllIllIlIl.print(llIIllIIIIIlIIIIIl)
        lIlIlllIlllIIlIlll = llIIIIlIlllIllIlIl.input('[bold yellow]\U0001faaa Enter your credential: [/]')
        IlIIIIIllIIIIIlIII = llIIIIlIlllIllIlIl.input('[bold yellow]🔑 Enter your password: [/]')
        (IlIIlIIIIlIIIlIlll, IlIIIIIlIlllIIIIlI, lllIlIlllllIIlIIII) = IIlIIllIlIlIIlllIl.lIllIlllIIIIIIIlll.login(lIlIlllIlllIIlIlll.strip(), IlIIIIIllIIIIIlIII.strip())
        if IlIIlIIIIlIIIlIlll and lllIlIlllllIIlIIII:
            IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII = lllIlIlllllIIlIIII
            IlIIlIIIIlIIIlIlll = IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.add_cookie(lllIlIlllllIIlIIII['cookie'], lllIlIlllllIIlIIII['name'], lllIlIlllllIIlIIII['token'])[0]
            if IlIIlIIIIlIIIlIlll:
                IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl = None
                IlIIIllIlllIIlIIll = IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.get_all_accounts()
                for llllIlllIlIIllIIIl in IlIIIllIlllIIlIIll:
                    if llllIlllIlIIllIIIl['user_id'] == IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['user_id']:
                        IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.set_current_account(llllIlllIlIIllIIIl['id'])
                        IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl = llllIlllIlIIllIIIl
                        break
        IIlIIllIlIlIIlllIl.lIllIlllIIIIIIIlll.log_login_attempt(lIlIlllIlllIIlIlll, IlIIlIIIIlIIIlIlll, IlIIIIIlIlllIIIIlI)
        llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def IIIIIIIllIlIllIllI(IIlIIllIlIlIIlllIl):
        """Handle adding a new cookie."""
        IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
        IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
        lIllIIlIIllIIllIlI = IllllIlIlIlIll('[bold yellow]Note:[/] [bold white]Use semi-colon separated format, cookie must contain c_user and xs values.[/]\n[bold indian_red]Caution:[/] [bold white]JSON format is not supported for some reason.[/]', title='[bold white]𝗔𝗗𝗗 𝗬𝗢𝗨𝗥 𝗖𝗢𝗢𝗞𝗜𝗘[/]', style='bold yellow', border_style='yellow')
        llIIIIlIlllIllIlIl.print(lIllIIlIIllIIllIlI)
        IlIIllIlIIIIllllII = llIIIIlIlllIllIlIl.input('[bold yellow]🍪 Enter your cookie: [/]')
        IlIIllIlIIIIllllII = IlIIllIlIIIIllllII.strip()
        if not IlIIllIlIIIIllllII:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Cookie cannot be empty![/]', style='bold indian_red', border_style='indian_red'))
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]🔄 Validating cookie format...[/]', style='bold cyan', border_style='cyan'))
        IlIIIIllllllII(1)
        if 'c_user=' not in IlIIllIlIIIIllllII or 'xs=' not in IlIIllIlIIIIllllII:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid cookie format! Cookie must contain c_user and xs values.[/]', style='bold indian_red', border_style='indian_red'))
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]✅ Cookie format is valid![/]', style='bold green', border_style='green'))
        IlIIIIllllllII(1)
        try:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll("[bold white]🔄 Getting account's token...[/]", style='bold cyan', border_style='cyan'))
            IlIIIIllllllII(1.5)
            IlIIlIIIIIlllIIIII = IIIlllllIlllll()
            try:
                for IlllllIIIIIllIlIlI in IlIIllIlIIIIllllII.split(';'):
                    if '=' in IlllllIIIIIllIlIlI:
                        (lllllIIllIlIIIIIll, lIllIIlIIllIIIIllI) = IlllllIIIIIllIlIlI.strip().split('=', 1)
                        IlIIlIIIIIlllIIIII.cookies.set(lllllIIllIlIIIIIll, lIllIIlIIllIIIIllI)
            except lllllllllllllIl as llIIlIIlIIlIIlIIII:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]❕ Error parsing cookie: {lllllllllllllII(llIIlIIlIIlIIlIIII)}[/]', style='bold indian_red', border_style='indian_red'))
                IlIIIIllllllII(1)
            IllIIllIIlllIllIII = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.9', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Upgrade-Insecure-Requests': '1'}
            lIlIIIIlIlIIIIIlll = None
            IIllllllIlIlllIIll = [('Ads Manager', 'https://adsmanager.facebook.com/adsmanager/', 'accessToken="(EAA[A-Za-z0-9]+)"'), ('Business Manager', 'https://business.facebook.com/content_management', '"(EAA[A-Za-z0-9]+)"'), ('Feed Composer', 'https://www.facebook.com/composer/ocelot/async_loader/?publisher=feed', '"accessToken":"(EAA[A-Za-z0-9]+)"')]
            for (llIIlllIIllIllllII, llIlIIIIIlIllllIIl, llllllIlIllllllllI) in IIllllllIlIlllIIll:
                try:
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]🔄 Trying {llIIlllIIllIllllII} method...[/]', style='bold cyan', border_style='cyan'))
                    IlIIIIllllllII(1)
                    lllIlIllIlllIIIIIl = IlIIlIIIIIlllIIIII.get(llIlIIIIIlIllllIIl, headers=IllIIllIIlllIllIII, timeout=30)
                    if lllIlIllIlllIIIIIl.ok:
                        lIllIIIIlIIIIIlIII = IlllIIIllIIIIl(llllllIlIllllllllI, lllIlIllIlllIIIIIl.text)
                        if lIllIIIIlIIIIIlIII:
                            lIlIIIIlIlIIIIIlll = lIllIIIIlIIIIIlIII.group(1)
                            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]✅ Token found using {llIIlllIIllIllllII}![/]', style='bold green', border_style='green'))
                            IlIIIIllllllII(1)
                            break
                except IlIIIlIlIllllI:
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]❕ {llIIlllIIllIllllII} request timed out[/]', style='bold indian_red', border_style='indian_red'))
                except lllllllllllllIl as llIIlIIlIIlIIlIIII:
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]❕ Error with {llIIlllIIllIllllII}: {lllllllllllllII(llIIlIIlIIlIIlIIII)}[/]', style='bold indian_red', border_style='indian_red'))
            if lIlIIIIlIlIIIIIlll:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold green]✅ Successfully retrieved token![/]', style='bold green', border_style='green'))
                IlIIIIllllllII(1)
            else:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Could not retrieve token. Continuing anyway...[/]', style='bold indian_red', border_style='indian_red'))
                IlIIIIllllllII(1)
                lIlIIIIlIlIIIIIlll = 'N/A'
        except lllllllllllllIl as llIIlIIlIIlIIlIIII:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]❕ Error during token extraction: {lllllllllllllII(llIIlIIlIIlIIlIIII)}. Continuing anyway...[/]', style='bold indian_red', border_style='indian_red'))
            IlIIIIllllllII(1)
            lIlIIIIlIlIIIIIlll = 'N/A'
        IIIIlIlIIIIlIIllII = None
        if 'name=' not in IlIIllIlIIIIllllII:
            IIIIlIlIIIIlIIllII = llIIIIlIlllIllIlIl.input('[bold yellow]💳 Enter your name: [/]').strip()
            if not IIIIlIlIIIIlIIllII:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Please enter your Facebook account name[/]', style='bold indian_red', border_style='indian_red'))
                llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
                return
        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]🔄 Saving account data...[/]', style='bold cyan', border_style='cyan'))
        IlIIIIllllllII(1)
        (IlIIlIIIIlIIIlIlll, IlIIIIIlIlllIIIIlI) = IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.add_cookie(IlIIllIlIIIIllllII, IIIIlIlIIIIlIIllII, lIlIIIIlIlIIIIIlll)
        if IlIIlIIIIlIIIlIlll:
            IlIIIllIlllIIlIIll = IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.get_all_accounts()
            IIllIlllIIIlIIIlII = IlIIIllIlllIIlIIll[-1]
            IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl = IIllIlllIIIlIIIlII
            IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.set_current_account(IIllIlllIIIlIIIlII['id'])
            IIlIIllIlIlIIlllIl.IIlIIllIIlIIIlIIll(IIllIlllIIIlIIIlII)
            IlIIIIllllllII(1)
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold green]✅ Cookie added successfully!\n👤 Account: {IIllIlllIIIlIIIlII['name']}\n📩 UID: {IIllIlllIIIlIIIlII['user_id']}[/]", style='bold green', border_style='green'))
        else:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]❕ {IlIIIIIlIlllIIIIlI}[/]', style='bold indian_red', border_style='indian_red'))
        IllIIIllIllllIlllI = lIllIIlIllIIII.now(llllllllIlllII(llIIIlIIIIIlII(hours=8)))
        llIIlllIIlIlIlIlII = IllIIIllIllllIlllI.strftime('%B %d, %Y %I:%M %p')
        IIIIIllllIIlII.log_activity(f'Add Cookie (PH: {llIIlllIIlIlIlIlII}) by {IIlIIllIlIlIIlllIl.llllIlllIlllIIIIII}', IlIIlIIIIlIIIlIlll, IlIIIIIlIlllIIIIlI)
        llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def IIIIlIIIIlIlIllIll(IIlIIllIlIlIIlllIl):
        """Handle Profile Guard operations."""
        if not IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Please select an account first[/]', style='bold indian_red', border_style='indian_red'))
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
            IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl['name']}[/]", style='bold cyan', border_style='cyan'))
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold yellow]Note:[/] [bold white]Make sure you turn off first your Facebook lock profile before proceeding to Facebook Profile Guard.[/]\n\n[1] Activate your Facebook Profile Shield\n[2] Deactivate your Facebook Profile Shield\n[3] Back to Main Menu', title='[bold white]🛡️ 𝗙𝗔𝗖𝗘𝗕𝗢𝗢𝗞 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 𝗚𝗨𝗔𝗥𝗗[/]', style='bold cyan', border_style='cyan'))
            lIlIlIlIlIllIlIIll = llIIIIlIlllIllIlIl.input('[bold yellow]Enter your choice: [/]').strip()
            if lIlIlIlIlIllIlIIll == '1' or lIlIlIlIlIllIlIIll == '2':
                lllIllIIlIIIllIlIl = lIlIlIlIlIllIlIIll == '1'
                (IlIIlIIIIlIIIlIlll, IlIIIIIlIlllIIIIlI) = IIlIIllIlIlIIlllIl.llIlIIllIIllIllIlI.toggle_profile_shield(IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl, lllIllIIlIIIllIlIl)
                if IlIIlIIIIlIIIlIlll:
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold white]✅ {IlIIIIIlIlllIIIIlI}\nName: {IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl['name']}\nUID: {IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl['user_id']}[/]", style='bold green', border_style='green'))
                else:
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]❕ {IlIIIIIlIlllIIIIlI}[/]', style='bold indian_red', border_style='indian_red'))
                llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            elif lIlIlIlIlIllIlIIll == '3':
                break
            else:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid choice![/]', style='bold indian_red', border_style='indian_red'))
                llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def lIlIIIIllIIIlIllII(IIlIIllIlIlIIlllIl):
        """Handle cookie settings and storage menu."""
        while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
            IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
            IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
            if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
            IlIIIllIlllIIlIIll = IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.get_all_accounts()
            for (IlIIIIlllIIlIIIIII, llllIlllIlIIllIIIl) in llllllllllllllI(IlIIIllIlllIIlIIll, 1):
                lIlIllIllIIllIIIIl = 'Logged in' if llllIlllIlIIllIIIl == IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl else 'Logged out'
                lIIIIllIlIIlIlIIII = 'green' if lIlIllIllIIllIIIIl == 'Logged in' else 'red'
                lIlIlIIIIIIIIIllIl = llllIlllIlIIllIIIl.get('name', 'Unknown User')
                IllIIIllIIIlllIIII = IllllIlIlIlIll(f"[bold white]Name: {lIlIlIIIIIIIIIllIl}[/]\n[bold white]UID: {llllIlllIlIIllIIIl['user_id']}[/]\n[bold {lIIIIllIlIIlIlIIII}]Status: {lIlIllIllIIllIIIIl}[/]\n" + (f'[bold yellow][{IlIIIIlllIIlIIIIII}] Select[/]\n' if llllIlllIlIIllIIIl != IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl else '') + f'[bold red][R{IlIIIIlllIIlIIIIII}] Remove[/]', title=f'[bold yellow]📨 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 {IlIIIIlllIIlIIIIII}[/]', style='bold yellow', border_style='yellow')
                llIIIIlIlllIllIlIl.print(IllIIIllIIIlllIIII)
            llIIIIlIlllIllIlIl.print('[bold white][0] Back[/]\n')
            lIlIlIlIlIllIlIIll = llIIIIlIlllIllIlIl.input('[bold yellow]Select an option: [/]')
            lIlIlIlIlIllIlIIll = lIlIlIlIlIllIlIIll.strip().upper()
            if lIlIlIlIlIllIlIIll == '0':
                break
            if lIlIlIlIlIllIlIIll.startswith('R'):
                try:
                    IlIIIIlllIIlIIIIII = lllllllllllIlIl(lIlIlIlIlIllIlIIll[1:]) - 1
                    if 0 <= IlIIIIlllIIlIIIIII < lllllllllllIlll(IlIIIllIlllIIlIIll):
                        IlllIIIlIlIIlIllII = IlIIIllIlllIIlIIll[IlIIIIlllIIlIIIIII]
                        if IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII and IlllIIIlIlIIlIllII['user_id'] == IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['user_id']:
                            lIlIlIIIIIIIIIllIl = IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']
                        else:
                            lIlIlIIIIIIIIIllIl = 'Unknown User'
                        llIIIIIlIIllIlIlll = llIIIIlIlllIllIlIl.input(f'[bold red]Are you sure you want to remove {lIlIlIIIIIIIIIllIl}? (y/N): [/]').strip().lower()
                        if llIIIIIlIIllIlIlll == 'y':
                            if IlllIIIlIlIIlIllII == IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl:
                                IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl = None
                                IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII = None
                            IlIIlIIIIlIIIlIlll = IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.remove_cookie(IlllIIIlIlIIlIllII)
                            if IlIIlIIIIlIIIlIlll:
                                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold green]✅ Successfully removed account: {lIlIlIIIIIIIIIllIl}[/]', style='bold green', border_style='green'))
                            else:
                                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Failed to remove account![/]', style='bold indian_red', border_style='indian_red'))
                    else:
                        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid selection![/]', style='bold indian_red', border_style='indian_red'))
                except (lllllllllllIllI, llllllllllllIll):
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid input![/]', style='bold indian_red', border_style='indian_red'))
            else:
                try:
                    lllIllllIIllIllIlI = lllllllllllIlIl(lIlIlIlIlIllIlIIll) - 1
                    if 0 <= lllIllllIIllIllIlI < lllllllllllIlll(IlIIIllIlllIIlIIll):
                        if IlIIIllIlllIIlIIll[lllIllllIIllIllIlI] != IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl:
                            IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl = IlIIIllIlllIIlIIll[lllIllllIIllIllIlI]
                            IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.set_current_account(IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl['id'])
                            IIlIIllIlIlIIlllIl.IIlIIllIIlIIIlIIll(IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl)
                            lIlIlIIIIIIIIIllIl = IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl['name']
                            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold green]✅ Successfully switched to account: {lIlIlIIIIIIIIIllIl}[/]', style='bold green', border_style='green'))
                        else:
                            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ This account is already selected.[/]', style='bold indian_red', border_style='indian_red'))
                    else:
                        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid selection![/]', style='bold indian_red', border_style='indian_red'))
                except lllllllllllIllI:
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid input![/]', style='bold indian_red', border_style='indian_red'))
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')

    def IllIIIllllIIlIllII(IIlIIllIlIlIIlllIl):
        """Handle cookie database functionality."""
        IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
        IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
        if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
        IlllIIIIlIIIIIIIlI = IllllIlIlIlIll('[bold yellow]Note:[/] [bold white]You can manage all your stored cookies and tokens here[/]\n[bold indian_red]Caution:[/] [bold white]Deleting cookies cannot be undone[/]', title='[bold white]𝗖𝗢𝗢𝗞𝗜𝗘𝗦 & 𝗧𝗢𝗞𝗘𝗡𝗦 𝗗𝗔𝗧𝗔𝗕𝗔𝗦𝗘[/]', style='bold cyan', border_style='cyan')
        llIIIIlIlllIllIlIl.print(IlllIIIIlIIIIIIIlI)
        IIIIIIIIIllIIlIIll = IllllIlIlIlIll('[bold white][1] View All Cookies & Tokens[/]\n[bold white][2] Back to Main Menu[/]', style='bold cyan', border_style='cyan')
        llIIIIlIlllIllIlIl.print(IIIIIIIIIllIIlIIll)
        lIlIlIlIlIllIlIIll = llIIIIlIlllIllIlIl.input('[bold cyan]Enter your choice: [/]')
        if lIlIlIlIlIllIlIIll == '1':
            IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
            IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
            if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
            llIIIIlIlllIllIlIl.print(IlllIIIIlIIIIIIIlI)
            IlIIIllIlllIIlIIll = IIlIIllIlIlIIlllIl.IllIlIllIIIllIIIll.get_all_accounts()
            for (IlIIIIlllIIlIIIIII, llllIlllIlIIllIIIl) in llllllllllllllI(IlIIIllIlllIIlIIll, 1):
                IllIIIllIllllIlllI = lIllIIlIllIIII.now(llllllllIlllII(llIIIlIIIIIlII(hours=8)))
                llIllIIlIllIIlllll = IllIIIllIllllIlllI.strftime('%B %d, %Y')
                IIlIlllIIIlllIIlIl = IllIIIllIllllIlllI.strftime('%I:%M %p +8 GMT (PH)')
                IlIIllIlIIIIllllII = llllIlllIlIIllIIIl['cookie']
                lIIIIlIlIllIlIllII = llllIlllIlIIllIIIl.get('token', 'N/A')
                IIIIIlIIlIlllIIllI = IlIIllIlIIIIllllII[:20] + '...' + IlIIllIlIIIIllllII[-10:] if lllllllllllIlll(IlIIllIlIIIIllllII) > 30 else IlIIllIlIIIIllllII
                IllllIIIIIIlIIlIlI = lIIIIlIlIllIlIllII[:20] + '...' + lIIIIlIlIllIlIllII[-10:] if lllllllllllIlll(lIIIIlIlIllIlIllII) > 30 else lIIIIlIlIllIlIllII
                lIllIIlIIllIIllIlI = IllllIlIlIlIll(f"[bold white]Name: {llllIlllIlIIllIIIl.get('name', 'Unknown User')}[/]\n[bold white]Cookie: {IIIIIlIIlIlllIIllI}[/]\n[bold white]Token: {IllllIIIIIIlIIlIlI}[/]\n[bold white]Added Date: {llIllIIlIllIIlllll}[/]\n[bold white]Added Time: {IIlIlllIIIlllIIlIl}[/]\n\n[bold yellow][C{IlIIIIlllIIlIIIIII}] Copy cookie[/]\n[bold yellow][T{IlIIIIlllIIlIIIIII}] Copy token[/]", title=f'[bold yellow]📨 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 {IlIIIIlllIIlIIIIII}[/]', style='bold yellow', border_style='yellow')
                llIIIIlIlllIllIlIl.print(lIllIIlIIllIIllIlI)
            llIIIIlIlllIllIlIl.print('[bold white][0] Back[/]\n')
            while lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1):
                IIlllllIIllIllIllI = llIIIIlIlllIllIlIl.input('[bold yellow]Select an option: [/]').strip().upper()
                if IIlllllIIllIllIllI == '0':
                    break
                if IIlllllIIllIllIllI.startswith(('C', 'T')):
                    try:
                        IlIIIIlllIIlIIIIII = lllllllllllIlIl(IIlllllIIllIllIllI[1:]) - 1
                        if 0 <= IlIIIIlllIIlIIIIII < lllllllllllIlll(IlIIIllIlllIIlIIll):
                            try:
                                IIIIlllIIIlIllllII = IlIIIllIlllIIlIIll[IlIIIIlllIIlIIIIII]['cookie'] if IIlllllIIllIllIllI.startswith('C') else IlIIIllIlllIIlIIll[IlIIIIlllIIlIIIIII].get('token', '')
                                lIIIlIllIllllIIlll = 'Cookie' if IIlllllIIllIllIllI.startswith('C') else 'Token'
                                if not IIIIlllIIIlIllllII and lIIIlIllIllllIIlll == 'Token':
                                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ No token available for this account![/]', style='bold indian_red', border_style='indian_red'))
                                else:
                                    IIlIlllIIIIlIllIlI = IIllIIIIIIlllI(['termux-clipboard-set'], stdin=lllIIIIIlIIlII)
                                    IIlIlllIIIIlIllIlI.communicate(input=IIIIlllIIIlIllllII.encode())
                                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]✅ {lIIIlIllIllllIIlll} {IlIIIIlllIIlIIIIII + 1} copied to clipboard![/]', style='bold green', border_style='green'))
                            except lllllllllllllIl as llIIlIIlIIlIIlIIII:
                                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Failed to copy to clipboard. Make sure Termux:API is installed.[/]', style='bold indian_red', border_style='indian_red'))
                            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
                            IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
                            IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
                            if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
                                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
                            llIIIIlIlllIllIlIl.print(IlllIIIIlIIIIIIIlI)
                            for (IlIIIIlllIIlIIIIII, llllIlllIlIIllIIIl) in llllllllllllllI(IlIIIllIlllIIlIIll, 1):
                                llIIIIlIlllIllIlIl.print(lIllIIlIIllIIllIlI)
                            llIIIIlIlllIllIlIl.print('[bold white][0] Back[/]\n')
                            break
                        else:
                            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
                            IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
                            IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
                            if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
                                llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
                            llIIIIlIlllIllIlIl.print(IlllIIIIlIIIIIIIlI)
                            for (IlIIIIlllIIlIIIIII, llllIlllIlIIllIIIl) in llllllllllllllI(IlIIIllIlllIIlIIll, 1):
                                llIIIIlIlllIllIlIl.print(lIllIIlIIllIIllIlI)
                            llIIIIlIlllIllIlIl.print('[bold white][0] Back[/]\n')
                    except lllllllllllIllI:
                        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                        llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
                        IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
                        IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
                        if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
                            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
                        llIIIIlIlllIllIlIl.print(IlllIIIIlIIIIIIIlI)
                        for (IlIIIIlllIIlIIIIII, llllIlllIlIIllIIIl) in llllllllllllllI(IlIIIllIlllIIlIIll, 1):
                            llIIIIlIlllIllIlIl.print(lIllIIlIIllIIllIlI)
                        llIIIIlIlllIllIlIl.print('[bold white][0] Back[/]\n')
                else:
                    llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
                    llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
                    IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
                    IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
                    if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
                        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold white]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
                    llIIIIlIlllIllIlIl.print(IlllIIIIlIIIIIIIlI)
                    for (IlIIIIlllIIlIIIIII, llllIlllIlIIllIIIl) in llllllllllllllI(IlIIIllIlllIIlIIll, 1):
                        llIIIIlIlllIllIlIl.print(lIllIIlIIllIIllIlI)
                    llIIIIlIlllIllIlIl.print('[bold white][0] Back[/]\n')
            return
        elif lIlIlIlIlIllIlIIll == '2':
            return
        else:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid choice! Please try again.[/]', style='bold indian_red', border_style='indian_red'))
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            IIlIIllIlIlIIlllIl.IllIIIllllIIlIllII()

    def IIlllIIIIIIIlIlllI(IIlIIllIlIlIIlllIl):
        """Handle spam sharing functionality."""
        IIlIIllIlIlIIlllIl.IlIIllIIlIIIllIlll()
        IIlIIllIlIlIIlllIl.IlIIllIlIIIlIlIllI()
        if IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl and IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f"[bold cyan]💠 𝗦𝗘𝗟𝗘𝗖𝗧𝗘𝗗 𝗔𝗖𝗖𝗢𝗨𝗡𝗧: {IIlIIllIlIlIIlllIl.lllIlIlllllIIlIIII['name']}[/]", style='bold cyan', border_style='cyan'))
        lllIlIlIllIllllllI = IllllIlIlIlIll("[bold yellow]Note:[/] [bold white]This code does not use Facebook's API for fewer restrictions.[/]\n[bold indian_red]Caution:[/] [bold white]Do not turn off your internet while the process is ongoing.[/]", title='[bold white]𝗦𝗣𝗔𝗠 𝗣𝗢𝗦𝗧 𝗦𝗛𝗔𝗥𝗘𝗥[/]', style='bold cyan', border_style='cyan')
        llIIIIlIlllIllIlIl.print(lllIlIlIllIllllllI)
        IlIlIIllIIIlIlIIll = llIIIIlIlllIllIlIl.input('[bold green]🔗 Enter the Facebook post URL: [/]')
        IlIlIIllIIIlIlIIll = IlIlIIllIIIlIlIIll.strip()
        if not IIIIIllllIIlII.validate_url(IlIlIIllIIIlIlIIll):
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Invalid Facebook URL![/]', style='bold indian_red', border_style='indian_red'))
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        (IlIIlIIIIlIIIlIlll, IlIIlllIIlllIIIIIl) = IIIIIllllIIlII.validate_input('[bold green]Number of shares: [/]', lllllllllllIlIl, min_val=1, max_val=100000)
        if not IlIIlIIIIlIIIlIlll:
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        (IlIIlIIIIlIIIlIlll, llIIIIllllIlIlllll) = IIIIIllllIIlII.validate_input('[bold green]Delay between shares (seconds): [/]', lllllllllllIlIl, min_val=1, max_val=60)
        if not IlIIlIIIIlIIIlIlll:
            llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')
            return
        (IlIIlIIIIlIIIlIlll, IlIIIIIlIlllIIIIlI) = IIlIIllIlIlIIlllIl.IIIIllllIIIlIIIIll.share_post(IIlIIllIlIlIIlllIl.IIllllIlllIIlIIIIl['cookie'], IlIlIIllIIIlIlIIll, IlIIlllIIlllIIIIIl, llIIIIllllIlIlllll)
        if IlIIlIIIIlIIIlIlll:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold green]✅ {IlIIIIIlIlllIIIIlI}[/]', style='bold green', border_style='green'))
        else:
            llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]❕ {IlIIIIIlIlllIIIIlI}[/]', style='bold indian_red', border_style='indian_red'))
        IIIIIllllIIlII.log_activity('Share Post', IlIIlIIIIlIIIlIlll, IlIIIIIlIlllIIIIlI)
        llIIIIlIlllIllIlIl.input('[bold white]Press Enter to continue...[/]')

def lIllIllIIllllIlIll():
    """Main entry point of the application."""
    try:
        llllIllIIlIlIIIlll = lllIlIlllIIlIlllll()
        llllIllIIlIlIIIlll.lIllIllIIllllIlIll()
    except llllllllllllIII:
        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll('[bold white]❕ Program interrupted by user.[/]', style='bold indian_red', border_style='indian_red'))
        IllIIIIlllllIl(0)
    except lllllllllllllIl as llIIlIIlIIlIIlIIII:
        llIIIIlIlllIllIlIl.print(IllllIlIlIlIll(f'[bold white]❕ An unexpected error occurred: {lllllllllllllII(llIIlIIlIIlIIlIIII)}[/]', style='bold indian_red', border_style='indian_red'))
        lllIIIIlIIlIlIIIIl = lIllIIlIllIIII.now(llllllllIlllII.utc).strftime('%Y-%m-%d %H:%M:%S')
        IIIIIllllIIlII.log_activity(f'System Error (UTC: {lllIIIIlIIlIlIIIIl}) by {sehraks1}', lllllllllllllll(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0), lllllllllllllII(llIIlIIlIIlIIlIIII))
        IllIIIIlllllIl(1)
if llllllllllllIIl == '__main__':
    lIllIllIIllllIlIll()
