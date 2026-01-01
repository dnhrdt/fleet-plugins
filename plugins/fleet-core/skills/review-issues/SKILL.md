---
name: review-issues
description: Review open issues from Fleet repositories (fleet-plugins, claude-research, and others). Categorizes by type (skill/workflow/pattern/context-request) and proposes changes. Use when user says "review issues", "check feedback", or at session start to stay current.
---

# Review Issues Skill

<!-- ⚠️ STOP: +0.01 minor | +0.10 significant | +1.00 major -->
Version: 2.10
<!-- ⚠️ STOP: Run `date "+%H:%M"` before changing! -->
Timestamp: 2026-01-01 22:27 CET

## Purpose

Read and process open issues from Fleet repositories. Handles:
- Feedback issues (fleet-plugins)
- Context requests from Research (claude-research)
- Issues from other Fleet projects

## Trigger

- User: "review issues", "check feedback", "prüfe issues"
- Session start (recommended routine)
- After completing major work

## Prerequisites

- GitHub CLI (`gh`) available
- Authenticated to GitHub (`gh auth status`)

## Repositories to Check

| Repo | What to look for |
|------|------------------|
| `dnhrdt/fleet-plugins` | Feedback (skill/workflow/pattern) |
| `dnhrdt/claude-research` | Context requests, research findings |
| Other projects | As needed |

---

## Workflow

### Step 1: Quick Status Check

```bash
echo "=== Fleet Issues Overview ==="
echo ""
echo "fleet-plugins (all open):"
"/c/Program Files/GitHub CLI/gh.exe" issue list --repo dnhrdt/fleet-plugins --state open --json number,title,labels --jq '.[] | "  #\(.number): \(.title) [\(.labels | map(.name) | join(", "))]"' 2>/dev/null || echo "  (none or error)"
echo ""
echo "claude-research (needs-context):"
"/c/Program Files/GitHub CLI/gh.exe" issue list --repo dnhrdt/claude-research --label "needs-context" --json number,title --jq '.[] | "  #\(.number): \(.title)"' 2>/dev/null || echo "  (none or error)"
echo ""
echo "claude-research (open research):"
"/c/Program Files/GitHub CLI/gh.exe" issue list --repo dnhrdt/claude-research --label "research" --state open --json number,title --jq '.[] | "  #\(.number): \(.title)"' 2>/dev/null || echo "  (none or error)"
```

**Note:** fleet-plugins shows ALL open issues regardless of label. Labels are shown for categorization.

### Step 2: Detailed Review (if issues found)

**⚠️ BEFORE reading any issue in detail:**
1. Add to your TodoWrite: `"Fixes #X - [brief description]"` (status: pending)
2. This ensures you remember to include `Fixes #X` in your commit message
3. GitHub will automatically close the issue when you push

**For fleet-plugins issues:**
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue view [NUMBER] --repo dnhrdt/fleet-plugins
```

**For claude-research issues:**
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue view [NUMBER] --repo dnhrdt/claude-research
```

### Step 3: Categorize and Act

| Issue Type | Source | Action |
|------------|--------|--------|
| `feedback:skill` | fleet-plugins | Modify SKILL.md |
| `feedback:workflow` | fleet-plugins | Modify CLAUDE.md |
| `feedback:pattern` | fleet-plugins | Modify Memory Bank |
| `needs-context` | claude-research | Provide context, then respond |
| `research` (completed) | claude-research | Review findings, extract patterns |

---

## Handling Context Requests

When Research-Claude creates `needs-context` issues:

1. **Read the issue** - What context is missing?
2. **Provide context** via comment:
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue comment [NUMBER] \
  --repo dnhrdt/claude-research \
  --body "## Context Provided

[Relevant information from Memory Bank, CLAUDE.md, or knowledge]

---
*Context provided by Commander Pellaeon*"
```
3. **Remove needs-context label:**
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue edit [NUMBER] \
  --repo dnhrdt/claude-research \
  --remove-label "needs-context"
```

---

## Handling Research Findings

When Research-Claude completes research:

1. **Review the findings** in the Issue
2. **If pattern discovered:**
   - Add to Memory Bank (systemPatterns.md)
   - Or create Issue in fleet-plugins if it needs discussion
3. **Mark as completed:**
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue edit [NUMBER] \
  --repo dnhrdt/claude-research \
  --add-label "completed"
"/c/Program Files/GitHub CLI/gh.exe" issue close [NUMBER] \
  --repo dnhrdt/claude-research
```

---

## Handling Fleet-Plugins Feedback

### Skill Changes (`feedback:skill`)

```markdown
## Skill Change Proposal

**Issue:** fleet-plugins#[NUMBER]
**Affected Skill:** fleet-[plugin]:[skill]
**File:** plugins/fleet-[plugin]/skills/[skill]/SKILL.md

**Proposed Change:**
[Description]
```

### Workflow Changes (`feedback:workflow`)

```markdown
## CLAUDE.md Change Proposal

**Issue:** fleet-plugins#[NUMBER]
**Affected File(s):**
- [ ] D:\dev\CLAUDE.md (global)
- [ ] D:\dev\Claude\CLAUDE.md (Pellaeon)
- [ ] Project-specific CLAUDE.md

**Proposed Change:**
[Description]
```

### Pattern Changes (`feedback:pattern`)

```markdown
## Memory Bank Change Proposal

**Issue:** fleet-plugins#[NUMBER]
**File:** memory-bank/systemPatterns.md

**Pattern to add:**
[Description]
```

---

## After Processing

**Commit with `Fixes #X` in the message:**
```bash
git commit -m "$(cat <<'EOF'
Fixes #X - Brief description of what was fixed

Details of changes...

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
git push
# → GitHub automatically closes Issue #X
```

**No manual closing needed!** The `Fixes #X` keyword does it automatically.

**If you forgot `Fixes #X` in your commit:**
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue close [NUMBER] \
  --repo dnhrdt/fleet-plugins \
  --comment "Fixed in commit [HASH]. Session [DATE]."
```

---

## Output Format

```markdown
## Issue Review Summary

**Checked:** [TIMESTAMP]

### fleet-plugins
- Pending: [N]
- By category: [skill: X, workflow: Y, pattern: Z]

### claude-research  
- Needs context: [N]
- Open research: [N]
- Completed (unreviewed): [N]

### Action Items

1. **[Priority]** [Issue] - [Action needed]
2. ...

### Recommendations

[What to do first]
```

---

## Session Start Routine (Optional)

Add to session start:

```
1. Check for .session-handoff.md
2. Read Memory Bank
3. **Quick issues check:** `/fleet-core:review-issues` (quick status only)
4. Ask for direction
```

If issues exist, inform user: "Es gibt [N] offene Issues. Soll ich sie durchgehen?"

---

*Part of fleet-core plugin*
