---
name: review-issues
description: Review open feedback issues from fleet-plugins. Categorizes by type (skill/workflow/pattern) and proposes changes. Use when user says "review issues", "check feedback", or at session start to stay current.
---

# Review Issues Skill

Version: 1.00
Timestamp: 2025-01-01 19:15 CET

## Purpose

Read and process open feedback issues from fleet-plugins repository. Categorize by type and propose appropriate changes to Skills, CLAUDE.md, or Memory Bank.

## Trigger

- User: "review issues", "check feedback", "prüfe issues"
- Session start (optional routine)
- After completing major work

## Prerequisites

- GitHub CLI (`gh`) available
- Authenticated to GitHub (`gh auth status`)
- Repository: `dnhrdt/fleet-plugins`

## Workflow

### Step 1: Fetch Open Issues

```bash
# List all pending feedback issues
"/c/Program Files/GitHub CLI/gh.exe" issue list \
  --repo dnhrdt/fleet-plugins \
  --label "feedback" \
  --label "pending" \
  --json number,title,labels,createdAt \
  --jq '.[] | "Issue #\(.number): \(.title) [\(.labels | map(.name) | join(", "))]"'
```

### Step 2: Read Issue Details

For each issue:
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue view [NUMBER] \
  --repo dnhrdt/fleet-plugins
```

### Step 3: Categorize by Labels

| Label | Affects | Action |
|-------|---------|--------|
| `feedback:skill` | Plugin Skills | Modify SKILL.md in fleet-plugins |
| `feedback:workflow` | Work processes | Modify CLAUDE.md (global or local) |
| `feedback:pattern` | Learnings | Modify Memory Bank (systemPatterns.md) |
| (no sub-label) | Unknown | Analyze and suggest category |

### Step 4: Propose Changes

**For Skill Issues (`feedback:skill`):**
```markdown
## Skill Change Proposal

**Issue:** #[NUMBER] - [TITLE]
**Affected Skill:** fleet-[plugin]:[skill]
**File:** plugins/fleet-[plugin]/skills/[skill]/SKILL.md

**Proposed Change:**
[Description of what to change]

**Approval needed:** Yes/No
```

**For Workflow Issues (`feedback:workflow`):**
```markdown
## CLAUDE.md Change Proposal

**Issue:** #[NUMBER] - [TITLE]
**Affected File:** 
- [ ] D:\dev\CLAUDE.md (global)
- [ ] D:\dev\Claude\CLAUDE.md (Pellaeon)
- [ ] Project-specific CLAUDE.md

**Proposed Change:**
[Description of what to add/modify]

**Approval needed:** Yes
```

**For Pattern Issues (`feedback:pattern`):**
```markdown
## Memory Bank Change Proposal

**Issue:** #[NUMBER] - [TITLE]
**Affected File:** memory-bank/systemPatterns.md

**Proposed Change:**
[New pattern or modification]

**Approval needed:** Yes/No
```

### Step 5: After Approval - Mark as Processed

```bash
# After changes are made
"/c/Program Files/GitHub CLI/gh.exe" issue edit [NUMBER] \
  --repo dnhrdt/fleet-plugins \
  --remove-label "pending" \
  --add-label "processed"

# Add comment documenting the change
"/c/Program Files/GitHub CLI/gh.exe" issue comment [NUMBER] \
  --repo dnhrdt/fleet-plugins \
  --body "Changes applied in [commit/session]. Closing."

# Close the issue
"/c/Program Files/GitHub CLI/gh.exe" issue close [NUMBER] \
  --repo dnhrdt/fleet-plugins
```

## Label Management

### Adding Category Labels

If issue lacks category label, suggest one:
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue edit [NUMBER] \
  --repo dnhrdt/fleet-plugins \
  --add-label "feedback:skill"  # or workflow, pattern
```

### Available Labels

| Label | Color | Description |
|-------|-------|-------------|
| `feedback` | yellow | Base feedback label |
| `feedback:skill` | blue | Skill modification needed |
| `feedback:workflow` | purple | CLAUDE.md modification needed |
| `feedback:pattern` | green | Memory Bank modification needed |
| `pending` | orange | Awaiting review |
| `processed` | gray | Reviewed and acted upon |
| `blocker` | red | Critical issue |

## Quick Check (Session Start)

For a quick overview without full processing:
```bash
# Count pending issues
"/c/Program Files/GitHub CLI/gh.exe" issue list \
  --repo dnhrdt/fleet-plugins \
  --label "pending" \
  --json number \
  --jq 'length'
```

If count > 0, inform user: "Es gibt [N] offene Feedback-Issues. Soll ich sie durchgehen?"

## Output Format

```markdown
## Issue Review Summary

**Checked:** [TIMESTAMP]
**Pending Issues:** [N]

### Issues by Category:

**Skill Changes (feedback:skill):**
- #[N]: [Title] → [Affected Skill]

**Workflow Changes (feedback:workflow):**
- #[N]: [Title] → [Affected CLAUDE.md]

**Pattern Changes (feedback:pattern):**
- #[N]: [Title] → [Pattern to add]

**Uncategorized:**
- #[N]: [Title] → [Suggested category]

### Recommended Actions:

1. [First priority action]
2. [Second priority action]
```

## Notes

- This is a PULL mechanism - no automatic notifications
- Consider checking at session start or after major work
- Always get approval before modifying CLAUDE.md
- Document changes in issue comments before closing

---

*Part of fleet-core plugin*
