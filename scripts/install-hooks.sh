#!/bin/bash

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash

# Get current date and time in Philippines timezone (Asia/Manila)
CURRENT_DATE=$(TZ='Asia/Manila' date '+%B %d, %Y')
CURRENT_TIME=$(TZ='Asia/Manila' date '+%I:%M %p')

# Update the version and timestamp in index.py
sed -i "s/self\.VERSION = \".*\"/self.VERSION = \"3.51\"/" index.py
sed -i "s/self\.LAST_UPDATED = \".*\"/self.LAST_UPDATED = \"$CURRENT_DATE\"/" index.py
sed -i "s/self\.CURRENT_TIME = \".*\"/self.CURRENT_TIME = \"$CURRENT_TIME\"/" index.py
sed -i "s/self\.CURRENT_USER = \".*\"/self.CURRENT_USER = \"Cerax\"/" index.py

# Add change logs
CHANGELOG_FILE="changelogs.txt"
echo "  ℹ️ Version 4.55" > $CHANGELOG_FILE
echo "  🗓️ Date: $CURRENT_DATE" >> $CHANGELOG_FILE
echo "  🕓 Time: $CURRENT_TIME" >> $CHANGELOG_FILE
echo "  ADDED NEW FEATURE(S):" >> $CHANGELOG_FILE
echo "  — Cookie Management (support log-in & log-out method. It can also remove you stored cookies" >> $CHANGELOG_FILE
echo "  — Spam Sharing (without Facebook's API, for less Facebook restriction" >> $CHANGELOG_FILE
echo "  — Facebook log-in (API support, soon)" >> $CHANGELOG_FILE
echo "  — Profile Picture Guard (soon)" >> $CHANGELOG_FILE
echo "  NEW CHANGES:" >> $CHANGELOG_FILE
echo "  — fixed minor bugs and errors." >> $CHANGELOG_FILE

# Stage the modified files
git add index.py
git add $CHANGELOG_FILE
HOOK

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed successfully!"
