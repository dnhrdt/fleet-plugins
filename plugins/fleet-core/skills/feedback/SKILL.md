---
name: feedback
description: Create structured feedback issues on GitHub for template/plugin improvement. Conducts question-guided interview, generates standardized issue. Use when user says "feedback", "template feedback", at end of project milestones, or after significant rule violations/disasters.
---

# Feedback Skill

Version: 3.10
Timestamp: 2026-01-01 21:50 CET

## Purpose

Collect structured feedback from projects → Create GitHub Issue → Improve Fleet plugins/templates

## ⚠️ MIGRATION NOTICE

**Old system:** Local files in `claude-init/feedback-inbox/`
**New system:** GitHub Issues in `dnhrdt/fleet-plugins`

This skill now creates GitHub Issues instead of local files.

## Trigger

**Explicit (user says):**
- "feedback", "template feedback", "feedback für fleet-plugins"
- "create issue", "file issue", "GitHub issue"
- "we should document this", "this needs to be recorded"

**Situational (recognize yourself):**
- After significant error/problem/bug
- After rule violation (especially when Michael had to intervene)
- After "near-disaster"
- End of project milestone
- Pattern discovered worth sharing

**⚠️ SELF-CHECK (CRITICAL!):**
When you recognize an error/bug/problem in a skill/workflow:
→ **STOP** - Do NOT execute `gh issue create` directly!
→ Load this skill
→ Go through the interview process
→ The skill ensures all relevant information is captured

**Why?** You know the gh commands and the repo. Your training says "be efficient, do it directly". But the interview process captures structured information you would otherwise forget. COMPLIANCE > HELPFULNESS.

## Prerequisites

- GitHub CLI (`gh`) available
- Authenticated to GitHub (`gh auth status`)
- Repository: `dnhrdt/fleet-plugins`

## Collect Feedback

### Question-Guided Interview

Ask User sequentially, then create GitHub Issue:

**Project Context:**
- Project name?
- Duration (sessions/days)?
- Project type (WordPress/Python/Node/PHP/Other)?

**1. Setup & Init**
- Setup successful?
- Errors? Blockers?
- Missing tools/checks?

**2. Rules Effectiveness** ⭐
- Which rules used? (STOP, RTFM, DSGVO, Context Monitoring)
- Rule violations? (Which? Why? Consequences?)
- **Rule missing?** (What happened? What would prevent?)

**3. Lessons Learned** ⭐
- New pattern discovered?
- Disaster occurred/prevented?
- Workflow improvement found?

**4. Rule Evolution** ⭐⭐ CRITICAL
- What learned that must go into rules?
- Proposal for new rule/protocol?

**5. Plugin/Skill Usage**
- Skills used: [List]
- Skills ignored: [List] + Why?
- Problems: [Detail]
- Missing functionality?

**6. Priority**
- Blocker / High / Medium / Low?

## Create GitHub Issue

```bash
"/c/Program Files/GitHub CLI/gh.exe" issue create \
  --repo dnhrdt/fleet-plugins \
  --title "Feedback: [Project Name] - $(date +%Y-%m-%d)" \
  --label "feedback" \
  --label "pending" \
  --body "$(cat <<'BODY'
## Project Info

| Field | Value |
|-------|-------|
| Project | [Name] |
| Type | [WordPress/Python/Node/etc.] |
| Sessions | [Number] |
| Date | [YYYY-MM-DD] |

## Setup & Init

- Success: [Yes/No]
- Errors: [List or None]
- Blockers: [List or None]

## Rules Effectiveness

**Used:** [STOP, RTFM, etc.]
**Helpful:** [Examples]
**Violations:** [Detail + consequences]
**Missing Rule:** [What happened? Prevention?]

## Lessons Learned

- **Pattern:** [Description + evidence]
- **Disaster:** [What? Cause? Prevention?]
- **Workflow:** [Improvement]

## Rule Evolution ⭐

- **Learned:** [Critical insight]
- **Rule proposal:** [New rule/protocol]
- **Prevents:** [Future errors]

## Plugin/Skill Usage

- **Used:** [List]
- **Ignored:** [List + Why]
- **Problems:** [Detail]
- **Missing:** [Functionality]

## Priority

[Blocker | High | Medium | Low]

## Recommended Action

[What should change in fleet-plugins?]

---
*Created via Feedback Skill by Commander Pellaeon*
BODY
)"
```

## Confirm to User

```markdown
✅ Feedback Issue erstellt: [Issue URL]

Das Feedback wird bei der nächsten fleet-plugins Review berücksichtigt.
Labels: feedback, pending
```

## Priority Levels (for Labels)

| Priority | Label | Description |
|----------|-------|-------------|
| **Blocker** | `blocker` | Prevents usage completely |
| **High** | (default) | Significant issue, needs fix soon |
| **Medium** | (default) | Improvement, not urgent |
| **Low** | (default) | Nice to have, backlog |

Add `blocker` label if priority is Blocker:
```bash
gh issue edit [NUMBER] --add-label "blocker" --repo dnhrdt/fleet-plugins
```

## What Makes Good Feedback

**Most valuable:**
- Rule gaps (what rules didn't prevent)
- Disasters with prevention proposals
- Patterns causing recurring issues
- Plugin vs Reality discrepancies

**Example:**
"Complete rewrite ignored CHANGELOG → Bug reintroduced → Rule needed: Grep CHANGELOG before rewrite"

**Best feedback:** "This happened, rule would prevent, here's the rule."

## Viewing Existing Feedback

```bash
# List all feedback issues
gh issue list --repo dnhrdt/fleet-plugins --label "feedback"

# List pending feedback
gh issue list --repo dnhrdt/fleet-plugins --label "pending"

# View specific issue
gh issue view [NUMBER] --repo dnhrdt/fleet-plugins
```

## Processing Feedback (for Maintainer)

After processing feedback:
```bash
# Mark as processed
gh issue edit [NUMBER] --remove-label "pending" --add-label "processed" --repo dnhrdt/fleet-plugins

# Close if completed
gh issue close [NUMBER] --repo dnhrdt/fleet-plugins
```

---

*Part of fleet-dev plugin - Will move to fleet-core later*
