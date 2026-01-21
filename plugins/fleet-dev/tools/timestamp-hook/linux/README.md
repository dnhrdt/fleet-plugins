# Edit Reminder Hook - Linux/Mac

Version: 2.00
Timestamp: 2026-01-21 14:30 CET

---

## Option 1: Direct Command (Recommended)

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PostToolUse\", \"additionalContext\": \"[CHECK] Time now: '$(date '+%Y-%m-%d %H:%M')' - Correct timestamp? English content? Version +0.01?\"}}'"
          }
        ]
      }
    ]
  }
}
```

## Output

Claude sees after each Edit/Write:
```
[CHECK] Time now: 2026-01-21 14:30 - Correct timestamp? English content? Version +0.01?
```

## Option 2: Via Script

For more complex logic:

```json
{
  "command": "bash /path/to/timestamp-hook.sh"
}
```

See `timestamp-hook.sh` in this folder.

## Important

- Changes only take effect in NEW sessions
- Set timezone via `TZ="Europe/Berlin"` if needed
- Uses `additionalContext` so Claude actually sees the message
