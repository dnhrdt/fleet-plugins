# Edit Reminder Hook - Windows

Version: 2.00
Timestamp: 2026-01-21 14:30 CET

---

## No Script Needed

Windows uses cmd.exe for hooks. The command goes directly in settings.json.

## Installation

Add to `C:\Users\[USERNAME]\.claude\settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo {\"hookSpecificOutput\": {\"hookEventName\": \"PostToolUse\", \"additionalContext\": \"[CHECK] Time now: %date% %time% - Correct timestamp? English content? Version +0.01?\"}}"
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
[CHECK] Time now: 21.01.2026 14:30 - Correct timestamp? English content? Version +0.01?
```

Date format is locale-dependent (German Windows = DD.MM.YYYY).

## Important

- **NO bash, NO script** - cmd.exe doesn't understand `$(date ...)`!
- Changes only take effect in NEW sessions
- Uses `additionalContext` so Claude actually sees the message
