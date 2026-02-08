---
name: review-pr
description: >-
  This skill should be used when the user says "review PRs", "check pull requests",
  "prüfe PRs", "merge PR", or when PRs need structured review before merging.
  Reviews open PRs from Fleet repositories, runs structured checklist, and handles
  approve/request-changes/merge workflow. Enforces repo sovereignty - only repo
  owners may merge.
---

# Review PR Skill

## Purpose

Review and manage Pull Requests across Fleet repositories. Handles:
- Listing open PRs (fleet-plugins, other dnhrdt/* repos)
- Structured code review with fleet-specific checklist
- Approve, Request Changes, or Merge decisions
- Never auto-merges -- always requires user confirmation

## Trigger

- User: "review PRs", "check pull requests", "prüfe PRs"
- User: "merge PR #X", "review PR #X"
- After receiving notification about new PR
- When PR-based changes need integration

## Prerequisites

- GitHub CLI (`gh`) available
- Authenticated to GitHub (`gh auth status`)

## Default Repository

**Primary:** `dnhrdt/fleet-plugins`

Override with `--repo` parameter for other repos:
```
/fleet-core:review-pr --repo dnhrdt/maison-website-project
```

---

## Critical: Repo Sovereignty

**Each instance has absolute control over its own repo.**

- Only the repo owner/maintainer may merge PRs
- Cross-repo merges are FORBIDDEN (e.g., Fleet Deck merging on fleet-plugins)
- PRs are the communication channel -- merging is the owner's decision
- DCG enforces: `gh pr merge/close/review/comment` blocked without `# skill-approved-471`

---

## Workflow

### Phase 1: Quick Status

**All gh commands in this skill require the marker `# skill-approved-471`**

```bash
echo "=== Fleet PRs Overview ==="
echo ""
echo "fleet-plugins (open):"
"/c/Program Files/GitHub CLI/gh.exe" pr list --repo dnhrdt/fleet-plugins --state open --json number,title,author,headRefName,createdAt --jq '.[] | "  #\(.number): \(.title) [\(.author.login)] (\(.headRefName))"' 2>/dev/null || echo "  (none or error)" # skill-approved-471
echo ""
echo "fleet-plugins (recently merged, last 5):"
"/c/Program Files/GitHub CLI/gh.exe" pr list --repo dnhrdt/fleet-plugins --state merged --limit 5 --json number,title,mergedAt --jq '.[] | "  #\(.number): \(.title) (merged: \(.mergedAt[:10]))"' 2>/dev/null || echo "  (none or error)" # skill-approved-471
```

**If --repo parameter provided, replace fleet-plugins with target repo.**

**Report to user:**
```
## PR Status

**Open:** [N] PRs
**Recently Merged:** [last 5]

Soll ich einen bestimmten PR reviewen?
```

### Phase 2: Detailed Review

For a specific PR, gather all information:

**Step 2a: Read PR metadata**
```bash
"/c/Program Files/GitHub CLI/gh.exe" pr view [NUMBER] --repo dnhrdt/[REPO] --json number,title,body,author,headRefName,baseRefName,state,additions,deletions,commits,files,reviews,labels # skill-approved-471
```

**Step 2b: Read the diff**
```bash
"/c/Program Files/GitHub CLI/gh.exe" pr diff [NUMBER] --repo dnhrdt/[REPO] # skill-approved-471
```

**Step 2c: Check PR comments (if any)**
```bash
"/c/Program Files/GitHub CLI/gh.exe" pr view [NUMBER] --repo dnhrdt/[REPO] --json comments --jq '.comments[] | "[\(.author.login) \(.createdAt[:10])]: \(.body[:200])"' # skill-approved-471
```

### Step 2d: Structured Review Checklist

**Run this checklist for EVERY PR. Report findings to user.**

#### General Quality
- [ ] PR description explains what AND why
- [ ] Trade-offs identified and documented
- [ ] Commit messages are descriptive (not "fix" or "update")
- [ ] No unrelated changes mixed in

#### Fleet-Plugins Specific
- [ ] **Version bump** included in plugin.json (if modifying a plugin)
- [ ] **Breaking changes** identified (API changes, removed features, renamed files)
- [ ] **Memory Bank impact** -- does this change require Memory Bank updates in consuming repos?
- [ ] **Hook changes** -- if hooks modified:
  - [ ] Tested on Windows? (hooks run under cmd.exe, not Git Bash)
  - [ ] stdin handling correct? (no blocking reads)
  - [ ] Exit codes correct? (0=success, 2=blocking error)
  - [ ] hookEventName present in response JSON?
- [ ] **Skill changes** -- if skills modified:
  - [ ] Skill-approved markers preserved?
  - [ ] Triggers/description updated?
  - [ ] Plugin.json skills list updated (if new skill)?
- [ ] **DCG impact** -- does this change affect DCG patterns or markers?
- [ ] **CLAUDE.md impact** -- does this require global CLAUDE.md updates?

#### Code Quality
- [ ] Follows existing patterns in the codebase
- [ ] No hardcoded paths (use `${CLAUDE_PLUGIN_ROOT}` or env vars)
- [ ] Error handling present (stderr, exit codes)
- [ ] No sensitive data (credentials, tokens, paths to local files)

**Present findings to user as:**
```markdown
## PR #[NUMBER] Review: [Title]

**Author:** [login]
**Branch:** [head] → [base]
**Changes:** +[additions] -[deletions] in [N] files

### Checklist Results

[check] [Passing items]
[warn] [Items needing attention]
[fail] [Failed items]

### Trade-offs

[Identified trade-offs and their impact]

### Summary

[1-3 sentences: overall assessment]

### Recommendation

[Approve | Request Changes | Needs Discussion]
[Specific feedback if Request Changes]
```

### Phase 3: Decision & Action

**NEVER auto-merge. Always ask user for explicit confirmation.**

#### Option A: Approve

```bash
"/c/Program Files/GitHub CLI/gh.exe" pr review [NUMBER] --repo dnhrdt/[REPO] --approve --body "$(cat <<'BODY'
## Approved

[Summary of review findings]

### Checklist
- [Key items verified]

---
*Reviewed via fleet-core:review-pr*
BODY
)" # skill-approved-471
```

#### Option B: Request Changes

```bash
"/c/Program Files/GitHub CLI/gh.exe" pr review [NUMBER] --repo dnhrdt/[REPO] --request-changes --body "$(cat <<'BODY'
## Changes Requested

### Required
- [Must-fix items]

### Suggested
- [Nice-to-have improvements]

---
*Reviewed via fleet-core:review-pr*
BODY
)" # skill-approved-471
```

#### Option C: Comment Only (no formal review)

```bash
"/c/Program Files/GitHub CLI/gh.exe" pr comment [NUMBER] --repo dnhrdt/[REPO] --body "$(cat <<'BODY'
## Review Notes

[Comments without formal approve/reject]

---
*Reviewed via fleet-core:review-pr*
BODY
)" # skill-approved-471
```

#### Option D: Merge (REQUIRES USER CONFIRMATION)

**Before merging, ask:**
```
PR #[NUMBER] "[title]" ist approved und bereit zum Merge.

Merge-Methode:
- merge (Standard, behaelt alle Commits)
- squash (Ein Commit, cleaner History)
- rebase (Linear History)

Soll ich mergen? Welche Methode?
```

**Only after explicit "yes":**
```bash
"/c/Program Files/GitHub CLI/gh.exe" pr merge [NUMBER] --repo dnhrdt/[REPO] --[merge|squash|rebase] --delete-branch # skill-approved-471
```

**Default:** `--squash` for external/fix PRs, `--merge` for feature branches.

#### Option E: Close without merging

```bash
"/c/Program Files/GitHub CLI/gh.exe" pr close [NUMBER] --repo dnhrdt/[REPO] --comment "$(cat <<'BODY'
Closed: [Reason]

---
*Closed via fleet-core:review-pr*
BODY
)" # skill-approved-471
```

---

## Post-Merge Actions

After a successful merge:

1. **Update Memory Bank** if PR introduced:
   - New skills or hooks → activeContext.md (plugin status table)
   - New patterns → systemPatterns.md
   - Config changes → techContext.md

2. **Plugin update** if fleet-plugins itself was changed:
   ```bash
   claude plugin update [plugin]@fleet-plugins --scope user
   ```

3. **Inform user** about downstream impacts:
   ```
   PR #[NUMBER] merged.

   Downstream-Aktionen:
   - [ ] Plugin update noetig? [Ja/Nein]
   - [ ] Memory Bank Update? [Ja/Nein]
   - [ ] CLAUDE.md Update? [Ja/Nein]
   ```

---

## Output Format

```markdown
## PR Review Summary

**Reviewed:** [TIMESTAMP]

### [Repo Name]
- Open: [N]
- Reviewed this session: [List]

### Action Items

1. **[Priority]** PR #[N] - [Action needed]
2. ...

### Post-Merge Tasks

[Any downstream updates needed]
```

---

*Part of fleet-core plugin*
