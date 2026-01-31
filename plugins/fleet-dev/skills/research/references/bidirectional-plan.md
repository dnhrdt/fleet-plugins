# Bidirectional Research Communication - Implementation Plan

Version: 1.00
Timestamp: 2026-01-31 12:56 CET

---

## Overview

Extend fleet-dev:research skill to support automatic result delivery back to the requesting repository.

**Current:** Hin-Weg only (Issue creation in claude-research)
**Target:** Hin-Weg + Rück-Weg (Results flow back automatically)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        HIN-WEG                              │
│  fleet-plugins ──(Issue with Source-Repo)──► claude-research│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    GitHub Actions Claude
                       (researches)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        RÜCK-WEG                             │
│  claude-research ──(repository_dispatch)──► fleet-plugins   │
│                              │                              │
│                              ▼                              │
│                    Creates Issue with                       │
│                    link to research results                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Checklist

### Part 1: claude-research Repository (Michael required)

#### 1.1 PAT Creation (Michael)

**Required:** Personal Access Token with `repo` scope

```
1. GitHub → Settings → Developer Settings → Personal Access Tokens
2. Generate new token (classic)
3. Name: "Fleet Cross-Repo Dispatch"
4. Scope: repo (full control)
5. Expiration: 1 year (or no expiration)
6. Copy token immediately
```

#### 1.2 Add Secret (Michael)

```
1. Go to: github.com/dnhrdt/claude-research/settings/secrets/actions
2. New repository secret
3. Name: FLEET_GITHUB_TOKEN
4. Value: [PAT from step 1.1]
```

#### 1.3 Extend Workflow (Tron)

**File:** `.github/workflows/claude.yml`

Add dispatch step after research completion:

```yaml
- name: Notify source repo
  if: contains(github.event.issue.body, 'Source-Repo:')
  env:
    GH_TOKEN: ${{ secrets.FLEET_GITHUB_TOKEN }}
  run: |
    SOURCE_REPO=$(grep -oP 'Source-Repo: \K[^\s]+' <<< "${{ github.event.issue.body }}")
    if [ -n "$SOURCE_REPO" ]; then
      gh api repos/${SOURCE_REPO}/dispatches \
        -f event_type=research-complete \
        -f client_payload="{\"issue\": ${{ github.event.issue.number }}, \"title\": \"${{ github.event.issue.title }}\", \"url\": \"${{ github.event.issue.html_url }}\"}"
    fi
```

---

### Part 2: Skill Extension (Tron)

#### 2.1 Update SKILL.md

Add `Source-Repo` field to Issue template:

```bash
gh issue create --repo dnhrdt/claude-research \
  --title "Research: [Topic]" \
  --label "research" \
  --body "## Research Question

[Question here]

## Context

[Why relevant]

## Source-Repo

dnhrdt/[repo-name]

## Research Depth

[Quick (5) | Normal (15) | Deep (25)]

---
*Created via Research Skill*

@claude please research this topic."
```

#### 2.2 Add Setup Reference

Create `references/bidirectional-setup.md` with:
- Per-repo workflow template
- Instructions for receiving results

---

### Part 3: Per-Repo Setup (Template)

#### Workflow Template

**File:** `.github/workflows/research-results.yml`

```yaml
name: Research Results Handler

on:
  repository_dispatch:
    types: [research-complete]

jobs:
  create-notification:
    runs-on: ubuntu-latest
    steps:
      - name: Create result notification
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          gh issue create \
            --title "📚 Research Complete: ${{ github.event.client_payload.title }}" \
            --label "research-result" \
            --body "## Research Complete

Research results are ready for review.

**Source Issue:** ${{ github.event.client_payload.url }}

Please review the findings and integrate relevant insights.

---
*Auto-created by Research Results Handler*"
```

---

## Testing Plan

1. **Test dispatch manually:**
   ```bash
   gh api repos/dnhrdt/fleet-plugins/dispatches \
     -f event_type=research-complete \
     -f client_payload='{"issue": 99, "title": "Test Research", "url": "https://github.com/dnhrdt/claude-research/issues/99"}'
   ```

2. **Verify Issue creation** in fleet-plugins

3. **Full integration test:**
   - Create research issue from fleet-plugins with Source-Repo field
   - Wait for research completion
   - Verify dispatch arrives
   - Verify Issue created in fleet-plugins

---

## Backward Compatibility

- If `Source-Repo:` missing → No dispatch (graceful degradation)
- Existing Issues without Source-Repo continue working
- No breaking changes to current workflow

---

## Dependencies

| Dependency | Owner | Status |
|------------|-------|--------|
| PAT Creation | Michael | ⏳ Pending |
| Secret Setup | Michael | ⏳ Pending |
| Workflow Extension | Tron | ⏳ Ready to implement |
| Skill Update | Tron | ⏳ Ready to implement |
| Per-Repo Template | Tron | ✅ Documented |

---

## Next Steps

1. **Michael:** Create PAT + add as secret to claude-research
2. **Tron:** Extend claude.yml workflow after secret is ready
3. **Tron:** Update research skill with Source-Repo field
4. **Test:** Full integration test

---

*Created for Issue #7*
