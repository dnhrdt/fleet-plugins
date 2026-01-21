---
name: feedback
description: This skill should be used when working on Maison projects and encountering bugs, discovering patterns, learning new mechanisms, or gaining insights that should be documented. Creates GitHub Issues in the maison-website-project hub for tracking across all Maison-related work.
---

# Maison Feedback Skill

## Purpose

Collect structured feedback from Maison projects → Create GitHub Issue → Track learnings across all Maison work

## Target Repository

**GitHub:** `dnhrdt/maison-website-project`

This is the central hub for all Maison-related development.

## Trigger

**Explicit (user says):**
- "maison feedback", "maison issue"
- "create issue for maison"
- "document this for maison"

**Situational (auto-recognize when working on Maison projects):**
- Bug discovered
- Important insight or pattern learned
- New mechanism understood (belongs in techContext or systemPatterns)
- Server-related discovery
- WooCommerce/Integration learning
- Cross-project pattern

**Scope:** Everything Maison - websites, hosting, integrations, Warenwirtschaft, all sites, all subprojects.

## Prerequisites

- GitHub CLI (`gh`) available
- Authenticated to GitHub (`gh auth status`)
- Repository: `dnhrdt/maison-website-project`

## Collect Feedback

### Quick Interview

Ask User briefly:

1. **What happened?** (Bug / Pattern / Learning / Feature Request)
2. **Which area?** (Website / Server / Integration / WooCommerce / Other)
3. **Which subproject?** (media-manager / helpdesk / quick-order / core / other)
4. **Priority?** (Blocker / High / Medium / Low)

Keep it lean - details go in the issue body.

## Create GitHub Issue

```bash
"/c/Program Files/GitHub CLI/gh.exe" issue create \
  --repo dnhrdt/maison-website-project \
  --title "[Area] Brief description" \
  --label "feedback" \
  --label "pending" \
  --body "$(cat <<'BODY'
## Summary

[Brief description of what was discovered/learned/broken]

## Context

| Field | Value |
|-------|-------|
| Type | [Bug / Pattern / Learning / Feature Request] |
| Area | [Website / Server / Integration / WooCommerce / Other] |
| Subproject | [media-manager / helpdesk / quick-order / core / N/A] |
| Session | [Number if known] |
| Date | [YYYY-MM-DD] |

## Details

[Full description with evidence, steps to reproduce, or explanation]

## Impact

[What does this affect? Which sites/projects?]

## Recommended Action

[What should be done? Add to techContext? New pattern? Fix needed?]

## Priority

[Blocker / High / Medium / Low]

---
*Created via maison:feedback Skill*
BODY
)"
```

## Confirm to User

```markdown
Issue erstellt: [Issue URL]

Das Feedback wird im Maison Project Hub getrackt.
```

## Labels

Keep minimal:
- `feedback` - Standard for all feedback
- `pending` - Awaiting processing

Project name and area are in the issue title/body - no need for extra labels.

## Viewing Existing Feedback

```bash
# List all feedback
gh issue list --repo dnhrdt/maison-website-project --label "feedback"

# List pending
gh issue list --repo dnhrdt/maison-website-project --label "pending"
```

## Processing Feedback

After implementing:
```bash
# Mark as processed
gh issue edit [NUMBER] --remove-label "pending" --add-label "processed" --repo dnhrdt/maison-website-project

# Close
gh issue close [NUMBER] --repo dnhrdt/maison-website-project
```

---

*Part of maison plugin for Fleet ecosystem*
