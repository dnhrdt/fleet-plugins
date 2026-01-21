# Timestamp Hook - Linux/Mac

Version: 1.00
Timestamp: 2026-01-21 18:35 CET

---

## Option 1: Direkter Befehl (empfohlen)

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

## Output

```
2026-01-21 18:35:42 Edit
```

## Option 2: Via Script

Falls komplexere Logik nötig:

```json
{
  "command": "bash /path/to/timestamp-hook.sh"
}
```

Siehe `timestamp-hook.sh` in diesem Ordner.

## Wichtig

- Änderungen wirken erst in NEUER Session
- Timezone via `TZ="Europe/Berlin"` setzen falls nötig
