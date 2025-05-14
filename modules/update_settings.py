def check_updates(self):
    """Check for updates using Git"""
    try:
        # Clear screen
        os.system('clear')

        # Check for updates
        console.print("📡 Checking for updates...")
        
        # Fetch latest changes
        subprocess.run(["git", "fetch", "origin"], check=True, capture_output=True)
        
        # Check if we're behind origin
        result = subprocess.run(
            ["git", "rev-list", "HEAD..origin/main", "--count"],
            check=True,
            capture_output=True,
            text=True
        )
        
        update_count = int(result.stdout.strip())
        
        if update_count > 0:
            # Show changelog if available
            try:
                with open("changelogs.txt", "r") as f:
                    changelogs = f.read().strip()
                    console.print(Panel(
                        f"🆕 New updates available!\n\nChange Logs:\n{changelogs}",
                        style="bold green"
                    ))
            except FileNotFoundError:
                console.print(Panel("🆕 New updates available!", style="bold green"))
            
            # Ask for user confirmation
            while True:
                choice = input("\nDo you want to update it now? (y/n): ").lower()
                if choice in ['y', 'n']:
                    break
                console.print("Please enter 'y' for yes or 'n' for no.")
            
            if choice == 'y':
                # Download updates
                console.print("\n📥 Downloading latest changes...")
                subprocess.run(["git", "pull", "origin", "main"], check=True)
                console.print("🔧 Setting file permissions...")
                subprocess.run(["chmod", "+x", "*.py"], check=True)
                subprocess.run(["chmod", "+x", "modules/*.py"], check=True)
                
                # Show single success message with current time and user
                current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                console.print(Panel(
                    "✅ Update completed! Please restart the tool to apply changes.\n\n"
                    f"Current Date: {current_time} UTC\n"
                    "Current User: sehraks",
                    style="bold green"
                ))
                # No need for input here as it's at the end
            else:
                console.print(Panel("Update cancelled by user.", style="bold yellow"))
        else:
            # Only show no updates message when there are truly no updates
            console.print(Panel("✨ No updates available", style="bold red"))

    except subprocess.CalledProcessError as e:
        console.print(Panel(f"❌ Update failed: {str(e)}", style="bold red"))
    except Exception as e:
        console.print(Panel(f"❌ Error: {str(e)}", style="bold red"))

    console.input("\nPress Enter to continue...")
