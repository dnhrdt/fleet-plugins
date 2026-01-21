# Timestamp Hook - Windows

Version: 1.00
Timestamp: 2026-01-21 18:35 CET

---

## Kein Script nötig!

Windows verwendet cmd.exe für Hooks. Der Timestamp-Befehl geht direkt in settings.json.

## Installation

Add to `C:\Users\[USERNAME]\.claude\settings.json`:

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

## Output

```
21.01.2026 18:35:42,17 Edit
```

Format ist locale-abhängig (deutsches Windows = DD.MM.YYYY).

## Wichtig

- **KEIN bash, KEIN Script** - cmd.exe versteht `$(date ...)` nicht!
- Änderungen wirken erst in NEUER Session
