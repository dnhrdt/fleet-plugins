# Session ID Konzept - Analyse aus fleet-plugins Perspektive

Version: 1.00
Timestamp: 2026-02-06 21:20 CET
Author: Tron (Session 185, fleet-plugins)

## Kernfund: Claude Code liefert bereits `session_id`

Alle Hook-Events bekommen via stdin-JSON ein `session_id` Feld.
Kein eigener Generator nötig.

### Gemeinsame Felder in JEDEM Hook-Event

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

### Zusatzfelder je Event-Typ

| Event | Zusatzfelder |
|-------|-------------|
| SessionStart | `source`, `model`, `agent_type` |
| UserPromptSubmit | `prompt` |
| PreToolUse | `tool_name`, `tool_input`, `tool_use_id` |
| PermissionRequest | `tool_name`, `tool_input`, `permission_suggestions` |
| PostToolUse | `tool_name`, `tool_input`, `tool_response`, `tool_use_id` |
| PostToolUseFailure | `tool_name`, `tool_input`, `tool_use_id`, `error`, `is_interrupt` |
| Notification | `message`, `title`, `notification_type` |
| SubagentStart | `agent_id`, `agent_type` |
| SubagentStop | `agent_id`, `agent_type`, `agent_transcript_path`, `stop_hook_active` |
| Stop | `stop_hook_active` |
| PreCompact | `trigger`, `custom_instructions` |
| SessionEnd | `reason` |

Quelle: https://docs.anthropic.com/en/docs/claude-code/hooks

---

## Auswirkung auf die offenen Fragen

### 1. Zentral vs. Dezentral? - Weder noch

Claude Code selbst ist der Generator. Jeder Hook bekommt die ID automatisch.
Kein fleet-plugins-Generator, kein dezentrales Generieren.

Einzige Aufgabe: `session_id` aus stdin auslesen und in Status-Datei schreiben.

### 2. Format? - Von Anthropic vorgegeben

Wir kontrollieren das Format nicht. Aus Doku-Beispiel: `"abc123"`.
Tatsaechliches Format muss einmal verifiziert werden (kurzer Test-Hook).

**Option fuer Fleet-eigene Display-ID:**
- `session_id` = Anthropics ID (autoritativ, fuer Korrelation)
- `display_id` = Menschenlesbares Alias, z.B. `tron-20260206-2115` (nur UI)

Empfehlung: Erstmal nur native ID nutzen, Display-ID nur bei Bedarf.

### 3. Speicherort? - Bereits abgedeckt

| Ort | Zugriff |
|-----|---------|
| Hook stdin (jeder Hook) | Automatisch, kein Setup |
| `.fleet-deck-status.json` | Fuer Fleet Deck + externe Tools |
| `transcript_path` (im Hook-Input) | Pfad zur vollen Session-JSONL |

Env-Variable nicht noetig - Hooks bekommen ID via stdin, andere Tools lesen Status-Datei.

### 4. Session-Typen? - Ueberall wo Hooks feuern

| Typ | Hooks? | Session-ID? |
|-----|--------|-------------|
| Terminal CLI (Windows Terminal) | Ja | Ja |
| VS Code Extension | Ja (stabil seit ~2.1.31) | Ja |
| Remote SSH (Yoda, CS-Server) | Ja (lokal auf Server) | Ja |
| Claude Desktop | Nein (kein Claude Code) | Nein |
| Headless/API | Keine Hooks | N/A |

### 5. Nicht ueber Stream Deck gestartet? - Kein Problem

Session-ID kommt von Claude Code, nicht vom Start-Mechanismus.
Manuell gestartete Sessions bekommen die gleiche ID wie Stream-Deck-Sessions.

### 6. Hook-Event fuer Generierung? - Entfaellt

Kein "Generieren" - nur Auslesen. Jedes Event liefert dieselbe `session_id`.
Kein "bereits generiert"-Check noetig: Einfach bei jedem Event in Status-Datei schreiben (idempotent).

Auf Windows: Erster UserPromptSubmit schreibt die ID (SessionStart haengt, Issue #9542).

### 7. Cross-Projekt Nutzung? - Sofort moeglich

| Consumer | Nutzen |
|----------|--------|
| Fleet Deck | Window Focus, Status-Zuordnung |
| DCG Decision Logger | Session-ID pro Entscheidung |
| Permission Logger | Session-ID pro Request |
| Session Analysis | Sessions eindeutig korrelieren |
| Event Log | Session-Grenzen erkennen |

---

## Bestehender Code: Erweiterungsbedarf

### fleet-deck-status.js (fleet-plugins)

Aktuell: Liest stdin, nutzt `session_id` nicht.
Erweiterung: Eine Zeile im `updateStatus()`:

```javascript
status.session_id = hookData.session_id || status.session_id;
```

### permission-logger.js (~/.claude/scripts/)

Aktuell: Loggt `ts`, `project`, `tool`, `detail`.
Erweiterung: `session_id` aus Hook-Input mitspeichern.

### DCG Decision Logger (geplant, docs/specs/dcg-decision-logger.md)

Sollte `session_id` von Anfang an mit aufnehmen.

---

## Offene Punkte

1. **Format verifizieren** - Tatsaechliches `session_id` Format von Claude Code capturen (Test-Hook)
2. **Stabilitaet pruefen** - Bleibt `session_id` ueber die gesamte Session gleich? (Erwartung: Ja)
3. **Eindeutigkeit pruefen** - Globale Eindeutigkeit oder nur pro Installation?
4. **transcript_path** - Kann Fleet Deck diesen Pfad nutzen um Session-Daten zu lesen?

---

## Bekannte Eigenschaft

Die session_id aendert sich bei `--resume` (GitHub Issue #12235).
Fuer Fleet Deck kein Problem - es geht um "welche Session laeuft jetzt", nicht um Konversations-Historie.
Fuer langfristige Korrelation ist `transcript_path` der stabilere Anker.

---

## Zusammenfassung

Das Session-ID-Problem ist bereits von Claude Code geloest.
Unsere Aufgabe reduziert sich auf: **Auslesen, Durchreichen, Nutzen.**
