# Edit Reminder Hook - Integration Guide

Version: 2.0.0
Timestamp: 2026-01-21 14:25 CET

---

## Purpose

Post-edit reminder for Claude to self-check:
- Timestamp correct?
- Content in English?
- Version incremented (+0.01)?

Uses **PostToolUse** with `additionalContext` - Claude sees the reminder AFTER editing and can self-correct if needed.

---

## Critical: Platform Shell Differences

**Claude Code hooks use the SYSTEM SHELL, not bash!**

| Platform | Shell | Timestamp Syntax |
|----------|-------|------------------|
| Windows | cmd.exe | `%date% %time%` |
| Linux/Mac | bash | `$(date '+%H:%M %Z')` |

---

## Installation

### Windows (cmd.exe)

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
            "command": "echo {\"hookSpecificOutput\": {\"hookEventName\": \"PostToolUse\", \"additionalContext\": \"[CHECK] Time now: %date% %time% - Correct timestamp? English content? Version +0.01?\"}}"
          }
        ]
      }
    ]
  }
}
```

**Output:** Claude sees after each Edit/Write:
```
[CHECK] Time now: 21.01.2026 14:25 - Correct timestamp? English content? Version +0.01?
```

### Linux/Mac (bash)

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

---

## Testing

**Hook changes only take effect in NEW sessions!**

1. Edit settings.json
2. Start NEW Claude Code session
3. Make an Edit to any file
4. Claude should see `[CHECK] Time now: ...` after the edit

---

## Troubleshooting

### Hook not firing

1. Start a NEW session (hooks load at session start)
2. Check JSON syntax in settings.json
3. Verify matcher: `"Edit|Write"`

### "$(date ...)" appears literally (Windows)

cmd.exe doesn't understand bash command substitution.
Use `%date% %time%` instead.

### Wrong timezone (Linux/Mac)

```bash
export TZ="Europe/Berlin"
```

---

## Why PostToolUse?

**PreToolUse** fires BEFORE Claude sends the edit - but parameters are already fixed.
**PostToolUse** fires AFTER - Claude sees the current time and can self-correct.

Using `additionalContext` in JSON output makes the message visible to Claude.

---

## History

- v1.00 (2026-01-13): Initial version with bash script
- v1.50 (2026-01-17): Simplified to PreToolUse direct commands
- v2.00 (2026-01-21): Changed to PostToolUse with self-check reminders (Fixes #5)
