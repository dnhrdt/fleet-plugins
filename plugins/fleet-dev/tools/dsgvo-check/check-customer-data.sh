#!/bin/bash
# DSGVO Check - Pre-commit hook for customer data detection
# Version: 1.00
#
# This script scans staged Git files for customer data before committing.
# Install as pre-commit hook or run manually before pushing to public repos.

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration file (optional)
CONFIG_FILE=".dsgvo-check.conf"

# Default patterns (can be overridden in config)
CUSTOMER_DOMAINS=""
CUSTOMER_NAMES=""

# Load configuration if exists
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

echo -e "${YELLOW}🔍 DSGVO Check: Scanning for customer data...${NC}"

# Get staged files
STAGED_FILES=$(git diff --cached --name-only)

if [ -z "$STAGED_FILES" ]; then
    echo -e "${GREEN}✅ No staged files to check${NC}"
    exit 0
fi

# Initialize violation counter
VIOLATIONS=0

# Check each staged file
for file in $STAGED_FILES; do
    # Skip binary files
    if git diff --cached --numstat "$file" | grep -qE '^-\s+-'; then
        continue
    fi

    # Get diff content for this file
    DIFF=$(git diff --cached "$file")

    # Check 1: Customer domains (if configured)
    if [ -n "$CUSTOMER_DOMAINS" ]; then
        if echo "$DIFF" | grep -iE "$CUSTOMER_DOMAINS" > /dev/null; then
            echo -e "${RED}❌ Customer domain found in: $file${NC}"
            echo "$DIFF" | grep -iE "$CUSTOMER_DOMAINS" --color=always
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi

    # Check 2: Customer names (if configured)
    if [ -n "$CUSTOMER_NAMES" ]; then
        if echo "$DIFF" | grep -iE "$CUSTOMER_NAMES" > /dev/null; then
            echo -e "${RED}❌ Customer name found in: $file${NC}"
            echo "$DIFF" | grep -iE "$CUSTOMER_NAMES" --color=always
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi

    # Check 3: Real email addresses (exclude example.com, test.com, etc.)
    if echo "$DIFF" | grep -E '\+.*[a-z0-9._%+-]+@(?!example\.com|test\.com|domain\.com|localhost)[a-z0-9.-]+\.[a-z]{2,}' > /dev/null; then
        MATCHES=$(echo "$DIFF" | grep -oE '[a-z0-9._%+-]+@(?!example\.com|test\.com|domain\.com|localhost)[a-z0-9.-]+\.[a-z]{2,}')
        if [ -n "$MATCHES" ]; then
            echo -e "${RED}❌ Real email address found in: $file${NC}"
            echo "$MATCHES" | while read -r email; do
                echo -e "  ${YELLOW}→ $email${NC}"
            done
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi

    # Check 4: Specific user paths (exclude generic /home/username/)
    if echo "$DIFF" | grep -E '\+.*/home/[^/]+/' | grep -v '/home/username/' | grep -v '/home/user/' > /dev/null; then
        PATHS=$(echo "$DIFF" | grep -oE '/home/[^/]+/' | grep -v '/home/username/' | grep -v '/home/user/' | sort -u)
        if [ -n "$PATHS" ]; then
            echo -e "${RED}❌ Specific user path found in: $file${NC}"
            echo "$PATHS" | while read -r path; do
                echo -e "  ${YELLOW}→ $path${NC}"
            done
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    fi

    # Check 5: Memory Bank files (should never be committed to public repos)
    if echo "$file" | grep -E '^memory-bank/' > /dev/null; then
        echo -e "${RED}❌ Memory Bank file should be .gitignored: $file${NC}"
        echo -e "  ${YELLOW}Memory Bank may contain customer data and should stay local${NC}"
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done

# Summary
echo ""
if [ $VIOLATIONS -eq 0 ]; then
    echo -e "${GREEN}✅ DSGVO Check passed - No customer data detected${NC}"
    exit 0
else
    echo -e "${RED}❌ DSGVO Check FAILED - $VIOLATIONS violation(s) found${NC}"
    echo ""
    echo -e "${YELLOW}Action required:${NC}"
    echo "  1. Review flagged content above"
    echo "  2. Replace customer data with generic examples:"
    echo "     • Domains: example.com, test.com, domain.com"
    echo "     • Names: username, user, account1, account2"
    echo "     • Paths: /home/username/, ~/projects/"
    echo "  3. Add memory-bank/ to .gitignore if not already"
    echo "  4. Run 'git add' again after fixes"
    echo "  5. Commit again"
    echo ""
    exit 1
fi
