#!/bin/bash
# Edit Reminder Hook for Claude Code (Linux/Mac)
# Version: 2.00
# Outputs JSON with additionalContext for Claude visibility

CURRENT_TIME=$(date '+%Y-%m-%d %H:%M')

echo "{\"hookSpecificOutput\": {\"hookEventName\": \"PostToolUse\", \"additionalContext\": \"[CHECK] Time now: ${CURRENT_TIME} - Correct timestamp? English content? Version +0.01?\"}}"

exit 0
