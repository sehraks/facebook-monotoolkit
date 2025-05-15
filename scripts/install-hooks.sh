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
echo "- Version 4.53" > $CHANGELOG_FILE
echo "  Date: $CURRENT_DATE" >> $CHANGELOG_FILE
echo "  Time: $CURRENT_TIME" >> $CHANGELOG_FILE
echo "  • Make some changes on UI and colorings" >> $CHANGELOG_FILE
echo "  • Fixed duplicate messages" >> $CHANGELOG_FILE
echo "  • Improved the functionality and fixed minor bugs and errors" >> $CHANGELOG_FILE

# Stage the modified files
git add index.py
git add $CHANGELOG_FILE
HOOK

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed successfully!"
