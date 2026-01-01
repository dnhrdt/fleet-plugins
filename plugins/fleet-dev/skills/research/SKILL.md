---
name: research
description: Create async research issues on GitHub. Claude researches in background via GitHub Actions. Use when user says "research", "recherchiere async", or wants to delegate research to background processing.
---

# Research Skill

Version: 1.00
Timestamp: 2025-01-01 17:30 CET
<!-- ⚠️ ON EDIT: date "+%H:%M" → update timestamp, +0.01 minor | +0.10 significant | +1.00 major -->

## Purpose

Create GitHub Issues for async research via GitHub Actions. Research runs in background while user continues other work.

## Trigger

- User: "research [topic]", "recherchiere [thema] async"
- User: "erstelle research issue zu [frage]"
- User wants to delegate research to background processing

## Prerequisites

- GitHub CLI (`gh`) available
- Authenticated to GitHub (`gh auth status`)
- Repository: `dnhrdt/claude-research`

## Workflow

### Step 1: Clarify Research Question

Ask user if not clear:
- What exactly do you want to know?
- Why is this relevant? How will it be used?
- Depth: Quick (5 turns), Normal (15), Deep (25)?

### Step 2: Create GitHub Issue

```bash
"/c/Program Files/GitHub CLI/gh.exe" issue create \
  --repo dnhrdt/claude-research \
  --title "Research: [Topic]" \
  --label "research" \
  --body "$(cat <<'BODY'
## Research Question

[User's question here]

## Context

[Why relevant, how will be used]

## Research Depth

[Quick (5) | Normal (15) | Deep (25)]

---
*Created via Research Skill by Commander Pellaeon*
BODY
)"
```

### Step 3: Confirm to User

```markdown
✅ Research Issue erstellt: [Issue URL]

GitHub Actions wird automatisch Claude starten.
Ergebnis erscheint als Kommentar im Issue.
Du bekommst eine GitHub-Benachrichtigung wenn fertig.
```

## Research Depth Guide

| Depth | Max Turns | Use Case |
|-------|-----------|----------|
| **Quick (5)** | 5 | Fact-check, simple questions |
| **Normal (15)** | 15 | Standard research, multiple sources |
| **Deep (25)** | 25 | Complex topics, comprehensive analysis |

**Default:** Normal (15) unless user specifies otherwise.

## Example

**User:** "Recherchiere async was die neuesten Claude Code Hooks können"

**Action:**
```bash
gh issue create --repo dnhrdt/claude-research \
  --title "Research: Claude Code Hooks - Aktuelle Capabilities" \
  --label "research" \
  --body "## Research Question
Was sind die neuesten Claude Code Hooks Features und Best Practices?

## Context
Für Fleet-Plugins Hook-Integration. Brauche aktuelle Doku und Beispiele.

## Research Depth
Normal (15)

---
*Created via Research Skill by Commander Pellaeon*"
```

**Response:**
```
✅ Research Issue erstellt: https://github.com/dnhrdt/claude-research/issues/1

GitHub Actions startet automatisch. Benachrichtigung kommt wenn fertig.
```

## Notes

- Research runs async - user doesn't need to wait
- Results appear as comments in the Issue
- Can follow up with `@claude` in Issue comments
- Private repo - research topics not public

---

*Part of fleet-dev plugin - Will move to fleet-core later*
