#!/bin/bash
# File: update.sh
# Last Modified: 2025-05-14 04:01:47 UTC
# Author: sehraks

echo "╭─────────────────────────────╮"
echo "│   Facebook MonoToolkit Updater   │"
echo "╰─────────────────────────────╯"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed!"
    echo "📦 Please install git first:"
    echo "pkg install git"
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree &> /dev/null; then
    echo "❌ Error: Not a git repository!"
    echo "🔄 Please clone the repository first:"
    echo "git clone https://github.com/yourusername/facebook-monotoolkit.git"
    exit 1
fi

echo "🔄 Fetching updates..."
if ! git fetch origin; then
    echo "❌ Error: Failed to fetch updates!"
    exit 1
fi

echo "📥 Downloading latest changes..."
if ! git pull origin main; then
    echo "❌ Error: Failed to pull updates!"
    echo "💡 Try: git reset --hard origin/main"
    exit 1
fi

# Make sure Python files are executable
chmod +x *.py
chmod +x modules/*.py

echo "✅ Update completed successfully!"
echo "🕒 Last updated: $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
echo ""
echo "📝 Please restart the tool to apply changes."
