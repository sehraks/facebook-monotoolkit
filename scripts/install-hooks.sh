#!/bin/bash

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash

# Version to update (change this when you want to update the version)
VERSION="4.66"

# Get current date and time in Philippines timezone (Asia/Manila)
CURRENT_DATE=$(TZ='Asia/Manila' date '+%B %d, %Y')
CURRENT_TIME=$(TZ='Asia/Manila' date '+%I:%M %p')

# Update the version and timestamp in index.py
sed -i "s/self\.VERSION = \".*\"/self.VERSION = \"$VERSION\"/" index.py
sed -i "s/self\.LAST_UPDATED = \".*\"/self.LAST_UPDATED = \"$CURRENT_DATE\"/" index.py
sed -i "s/self\.CURRENT_TIME = \".*\"/self.CURRENT_TIME = \"$CURRENT_TIME\"/" index.py
sed -i "s/self\.CURRENT_USER = \".*\"/self.CURRENT_USER = \"sehraks\"/" index.py
sed -i "s/# Last Modified: .*/# Last Modified: $CURRENT_DATE $CURRENT_TIME +8 GMT/" index.py

# Add change logs
CHANGELOG_FILE="changelogs.txt"
echo "Version $VERSION" > $CHANGELOG_FILE
echo "Date: $CURRENT_DATE" >> $CHANGELOG_FILE
echo "Time: $CURRENT_TIME" >> $CHANGELOG_FILE
echo "—————————————————————————————————" >> $CHANGELOG_FILE
echo "NEW CHANGES:" >> $CHANGELOG_FILE
echo "— fixed minor bugs and errors, and make minor changes." >> $CHANGELOG_FILE

# Stage the modified files
git add index.py
git add $CHANGELOG_FILE
HOOK

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed successfully!"
