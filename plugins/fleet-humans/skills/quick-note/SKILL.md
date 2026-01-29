---
name: quick-note
description: This skill should be used when insights about Michael or Sylvie emerge during work. Capture immediately, continue working. Triggers on "das halte ich fest", "notieren", "quick-note", or when learning something personal about household members.
---

# Quick Note Skill

## Purpose

Capture personal insights about Michael or Sylvie immediately when they emerge. Moltbot principle: document now, not later.

## Trigger

- "Das halte ich fest" / "Das notiere ich"
- "quick-note michael: [insight]"
- "Sylvie mag X" / "Michael arbeitet Y"
- Any personal insight worth preserving

## Target Locations

| Person | Directory |
|--------|-----------|
| Michael | `D:\dev\Projects\about-michael\` |
| Sylvia | `D:\dev\Projects\about-sylvia\` |

**Note:** Sylvia (official spelling) - Michael's nickname "Silvi", speech recognition varies. All refer to the same person.

## Workflow

### Step 1: Identify Person

Determine if insight is about Michael or Sylvie.

### Step 2: Append to insights.md

Append to `insights.md` in the appropriate directory. Create file if not exists.

**Format:**
```markdown
## YYYY-MM-DD | [source-project]

- [Insight in bullet point]
- [Another insight if multiple]
```

### Step 3: Continue Working

Confirm briefly and return to main task:
```
Notiert in about-michael/insights.md. Weiter...
```

## Example

**During session:**
> Claude discovers Michael prefers local inference over cloud APIs

**Action:**
```markdown
## 2026-01-29 | claude-session-analysis

- Prefers local inference (LM Studio) over cloud APIs
- Privacy-focused: own servers where possible
```

**Append to:** `D:\dev\Projects\about-michael\insights.md`

**Response:** "Notiert. Weiter mit..."

## Categories (Optional Headers)

When file grows, organize with headers:

- `## Arbeitsweise` - Work patterns, schedules
- `## Technologie` - Tech preferences, tools
- `## Geschaeftliches` - Business, clients, billing
- `## Persoenliches` - Personal preferences, habits
- `## Kommunikation` - Communication style

## Notes

- LLM-only format: bullets, no prose
- Append, never replace
- Brief confirmation, don't interrupt flow
- Source project helps trace context later
