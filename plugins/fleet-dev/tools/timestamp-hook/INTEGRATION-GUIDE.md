# Timestamp Hook - Integration Guide

Version: 1.5.0

---

## Purpose

Displays current timestamp before Edit/Write operations.
Prevents Claude from guessing timestamps in version headers.

---

## Critical: Platform Shell Differences

**Claude Code hooks use the SYSTEM SHELL, not bash!**

| Platform | Shell | Timestamp Syntax |
|----------|-------|------------------|
| Windows | cmd.exe | `%date% %time%` |
| Linux/Mac | bash | `$(date '+%H:%M %Z')` |

**Session 158 Discovery:** `$(date ...)` wird auf Windows LITERAL geschrieben, nicht ausgeführt - weil cmd.exe keine Command Substitution kennt.

---

## Installation

### Windows (cmd.exe)

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo %date% %time% Edit"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo %date% %time% Write"
          }
        ]
      }
    ]
  }
}
```

**Output format:** `21.01.2026 18:30:45,27 Edit`

### Linux/Mac (bash)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "echo $(date '+%Y-%m-%d %H:%M:%S') Edit"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "echo $(date '+%Y-%m-%d %H:%M:%S') Write"
          }
        ]
      }
    ]
  }
}
```

**Output format:** `2026-01-21 18:30:45 Edit`

---

## Testing Hooks

**Problem:** Hook changes only take effect in NEW sessions!

**Test Protocol:**
1. Edit settings.json
2. Start NEW Claude Code session
3. Make an Edit to any file
4. Check if timestamp appears in output

**If timestamp doesn't appear:**
- Verify JSON syntax is valid
- Check you're in a NEW session (not old one)
- On Windows: Don't use bash syntax like `$(date ...)`

---

## Troubleshooting

### Zuerst prüfen: settings.local.json Konflikt?

Ältere Versionen dieser Anleitung verwendeten fälschlich `settings.local.json`.
Falls dort Hooks eingetragen sind, überschreiben sie möglicherweise die globale Config!

**Check:**
```bash
# Windows
type "%USERPROFILE%\.claude\settings.local.json" 2>nul | findstr hook

# Linux/Mac
grep -i hook ~/.claude/settings.local.json 2>/dev/null
```

**Falls Hooks dort gefunden:** Entfernen und nur in `settings.json` (global) eintragen.

---

### "$(date ...)" appears literally (Windows)

**Cause:** cmd.exe doesn't understand bash command substitution.
**Fix:** Use `%date% %time%` instead.

### Hook not firing

1. Start a NEW session (hooks load at session start)
2. Check JSON syntax in settings.json
3. Verify matcher matches tool name exactly ("Edit", "Write")

### Wrong timezone (Linux/Mac)

```bash
export TZ="Europe/Berlin"
```

---

## Why No File Filtering?

Earlier versions filtered for `**/memory-bank/**` files only.

**Current approach:** Fire on ALL Edit/Write operations.

Reason: Almost all project files have version headers that need timestamps.
Simpler config, no filtering logic needed.

---

## History

- v1.00 (2026-01-13): Initial version with bash script
- v2.00 (2026-01-21): Simplified to direct commands, documented Windows cmd.exe requirement
