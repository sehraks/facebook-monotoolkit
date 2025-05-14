#!/bin/bash

# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/bash

# Get current timestamp in UTC
CURRENT_DATE=$(date -u '+%Y-%m-%d %H:%M:%S')
CURRENT_DATE_GMT=$(date '+%b %d, %Y +8 GMT')

# Update the version and timestamp in index.py
sed -i "s/self\.VERSION = \".*\"/self.VERSION = \"3.51\"/" index.py
sed -i "s/self\.LAST_UPDATED = \".*\"/self.LAST_UPDATED = \"$CURRENT_DATE_GMT\"/" index.py
sed -i "s/self\.CURRENT_TIME = \".*\"/self.CURRENT_TIME = \"$CURRENT_DATE\"/" index.py
sed -i "s/self\.CURRENT_USER = \".*\"/self.CURRENT_USER = \"sehraks\"/" index.py

# Add change logs (Developer needs to edit this section)
CHANGELOG_FILE="changelogs.txt"
echo "- Version 3.51 ($CURRENT_DATE_GMT)" > $CHANGELOG_FILE
echo "  • Added new feature X" >> $CHANGELOG_FILE
echo "  • Fixed bug Y" >> $CHANGELOG_FILE
echo "  • Improved performance Z" >> $CHANGELOG_FILE

# Stage the modified files
git add index.py
git add $CHANGELOG_FILE
HOOK

# Make the hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed successfully!"
EOL
