#!/bin/bash
# File: update.sh
# Last Modified: 2025-05-14 05:20:02 UTC
# Author: sehraks

# Clear screen for cleaner output
clear

# Function to create a centered banner
create_banner() {
    local text="$1"
    local width=50
    local padding=$(( (width - ${#text}) / 2 ))
    
    echo "╭──$(printf '─%.0s' $(seq 1 $((width-4))))──╮"
    printf "│  %*s%s%*s  │\n" $padding "" "$text" $((width - ${#text} - padding)) ""
    echo "╰──$(printf '─%.0s' $(seq 1 $((width-4))))──╯"
}

# Display the main banner
create_banner "Facebook MonoToolkit Updater"
echo

# Check if git is installed
if ! command -v git &> /dev/null; then
    create_banner "❌ Error: Git is not installed!"
    echo
    echo "📦 Please install git first:"
    echo "pkg install git"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    create_banner "❌ Error: Not in a git repository!"
    echo
    echo "🔄 Please clone the repository first:"
    echo "git clone https://github.com/sehraks/facebook-monotoolkit.git"
    exit 1
fi

# Update process
create_banner "Starting Update Process"
echo

echo "📡 Checking for updates..."
if ! git fetch origin; then
    create_banner "❌ Failed to fetch updates!"
    exit 1
fi

echo "📥 Downloading latest changes..."
if ! git pull origin main; then
    create_banner "❌ Update failed!"
    echo
    echo "💡 Try: git reset --hard origin/main"
    exit 1
fi

# Update version and timestamp in index.py
echo "📝 Updating version information..."
CURRENT_DATE=$(date -u '+%Y-%m-%d %H:%M:%S')
CURRENT_DATE_GMT=$(date '+%b %d, %Y +8 GMT')
CURRENT_VERSION="3.51"  # You can modify this as needed

sed -i "s/self\.VERSION = \".*\"/self.VERSION = \"$CURRENT_VERSION\"/" index.py
sed -i "s/self\.LAST_UPDATED = \".*\"/self.LAST_UPDATED = \"$CURRENT_DATE_GMT\"/" index.py
sed -i "s/self\.CURRENT_TIME = \".*\"/self.CURRENT_TIME = \"$CURRENT_DATE\"/" index.py
sed -i "s/self\.CURRENT_USER = \".*\"/self.CURRENT_USER = \"sehraks\"/" index.py

# Make files executable
echo "🔧 Setting file permissions..."
chmod +x *.py
chmod +x modules/*.py

# Success message
echo
create_banner "✅ Update Completed Successfully!"
echo
echo "🕒 Last updated: $CURRENT_DATE UTC"
echo "📝 Please restart the tool to apply changes."
