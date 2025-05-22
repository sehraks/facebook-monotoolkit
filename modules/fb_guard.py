#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: modules/fb_guard.py

import json
import uuid
import requests
import time
from datetime import datetime, timezone, timedelta
from rich.console import Console
from rich.panel import Panel
from typing import Dict, Tuple

console = Console()

class FacebookGuard:
        def __init__(self):
                """Initialize FacebookGuard with necessary configurations."""
                # Get current UTC time
                self.last_update = "2025-05-22 13:40:33"
                self.current_user = "sehraks1"

        def toggle_profile_shield(self, account: Dict, enable: bool = True) -> Tuple[bool, str]:
                """Toggle Facebook profile shield."""
                try:
                        # Initial status message
                        console.print(Panel(
                                "[bold white]🔄 Initializing Profile Shield operation...[/]",
                                style="bold cyan",
                                border_style="cyan"
                        ))
                        time.sleep(1)

                        token = account.get('token')
                        if not token:
                                return False, "No valid token found for this account"

                        # Toggle shield
                        console.print(Panel(
                                f"[bold white]🔄 {'Activating' if enable else 'Deactivating'} Profile Shield...[/]",
                                style="bold cyan",
                                border_style="cyan"
                        ))
                        time.sleep(1)

                        headers = {
                                'Authorization': f'OAuth {token}',
                                'Content-Type': 'application/json'
                        }

                        data = {
                                'variables': json.dumps({
                                        'input': {
                                                'actor_id': account['user_id'],
                                                'client_mutation_id': str(uuid.uuid4()),
                                                'is_enabled': enable
                                        }
                                }),
                                'doc_id': '5014118178644909'
                        }

                        response = requests.post(
                                'https://graph.facebook.com/graphql',
                                json=data,
                                headers=headers
                        )

                        if response.status_code != 200:
                                return False, f"Request failed: {response.text}"

                        action = "turned on" if enable else "turned off"
                        return True, f"You {action} your Facebook Profile Shield"

                except Exception as e:
                        return False, f"Error: {str(e)}"
