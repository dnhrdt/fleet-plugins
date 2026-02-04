---
name: feedback
description: This skill should be used when the user says "feedback", "template feedback", "create issue", at end of project milestones, or after significant rule violations/disasters. Creates structured feedback issues on GitHub. Supports multi-repo messaging with --repo parameter.
---

# Feedback Skill

## Purpose

**Two modes:**

1. **Fleet Feedback** (default): Structured interview → GitHub Issue in fleet-plugins
2. **Cross-Repo Message** (--repo): Quick message to any dnhrdt/* repo

## Quick Reference

```bash
# Fleet-plugins feedback (full interview)
/fleet-core:feedback

# Message to another repo (simple)
/fleet-core:feedback --repo claude-research
/fleet-core:feedback --repo maison-website-project
```

## Trigger

**Explicit (user says):**
- "feedback", "template feedback", "feedback für fleet-plugins"
- "create issue", "file issue", "GitHub issue"
- "notify [repo]", "message to [repo]"

**Situational (auto-recognize):**
- After significant error/problem/bug
- After rule violation (especially when Michael had to intervene)
- After "near-disaster"
- End of project milestone
- Pattern discovered worth sharing
- Need to leave a note for yourself in another repo

**SELF-CHECK (CRITICAL!):**
When recognizing an error/bug/problem in a skill/workflow:
→ **STOP** - Do NOT execute `gh issue create` directly!
→ Load this skill
→ The skill ensures proper routing and formatting

## Prerequisites

- GitHub CLI (`gh`) available
- Authenticated to GitHub (`gh auth status`)

---

## Mode 1: Cross-Repo Message (--repo)

**Use when:** You need to leave a note for yourself in another repo.

This is **not** a formal feedback process - just a message/reminder for when you next work in that repo.

**⚠️ All gh commands in this skill require the marker `# skill-approved-739`**

```bash
"/c/Program Files/GitHub CLI/gh.exe" issue create \
  --repo dnhrdt/[TARGET-REPO] \
  --title "[Brief descriptive title]" \
  --body "$(cat <<'BODY'
## Message

[What you want to communicate]

## Context

- **Source:** [Current project/repo]
- **Date:** [YYYY-MM-DD]
- **Reason:** [Why this is relevant for target repo]

---
*Cross-repo message via Feedback Skill*
BODY
)" # skill-approved-739
```

**No labels, no interview.** Just a simple issue as a note to yourself.

**Example:**
```bash
"/c/Program Files/GitHub CLI/gh.exe" issue create \
  --repo dnhrdt/claude-research \
  --title "Obsidian research results available in Tron Memory Bank" \
  --body "$(cat <<'BODY'
## Message

Tron completed Obsidian MCP research. Results are in fleet-plugins Memory Bank
under Session 178-179. Ready for integration into claude-research workflow.

## Context

- **Source:** fleet-plugins
- **Date:** 2026-02-04
- **Reason:** Research findings need to be processed here

---
*Cross-repo message via Feedback Skill*
BODY
)" # skill-approved-739
```

---

## Mode 2: Fleet Feedback (default)

**Use when:** Providing structured feedback about fleet-plugins itself.

**Repository:** `dnhrdt/fleet-plugins`

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

**⚠️ All gh commands in this skill require the marker `# skill-approved-739`**

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
)" # skill-approved-739
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
gh issue edit [NUMBER] --add-label "blocker" --repo dnhrdt/fleet-plugins # skill-approved-739
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
gh issue list --repo dnhrdt/fleet-plugins --label "feedback" # skill-approved-739

# List pending feedback
gh issue list --repo dnhrdt/fleet-plugins --label "pending" # skill-approved-739

# View specific issue
gh issue view [NUMBER] --repo dnhrdt/fleet-plugins # skill-approved-739
```

## Processing Feedback (for Maintainer)

After processing feedback:
```bash
# Mark as processed
gh issue edit [NUMBER] --remove-label "pending" --add-label "processed" --repo dnhrdt/fleet-plugins # skill-approved-739

# Close if completed
gh issue close [NUMBER] --repo dnhrdt/fleet-plugins # skill-approved-739
```

---

*Part of fleet-core plugin*
