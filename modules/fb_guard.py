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
                self.last_update = datetime.now(timezone(timedelta(hours=8))).strftime("%B %d, %Y.")
                self.current_user = "sehraks"

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

                        data = {
                                'variables': json.dumps({
                                        '0': {
                                                'is_shielded': enable,
                                                'session_id': str(uuid.uuid4()),
                                                'actor_id': account['user_id'],
                                                'client_mutation_id': str(uuid.uuid4())
                                        }
                                }),
                                'method': 'post',
                                'doc_id': '1477043292367183'
                        }

                        headers = {
                                'Authorization': f"OAuth {token}"
                        }

                        response = requests.post(
                                'https://graph.facebook.com/graphql',
                                json=data,
                                headers=headers
                        )

                        if response.status_code != 200:
                                return False, f"Request failed: {response.text}"

                        response_text = response.text
                        if '"is_shielded":true' in response_text:
                                return True, "✅ Activated Profile Shield"
                        elif '"is_shielded":false' in response_text:
                                return True, "✅ Deactivated Profile Shield"
                        else:
                                return False, f"❕ Unexpected response: {response_text}"

                except Exception as e:
                        return False, f"Error: {str(e)}"
