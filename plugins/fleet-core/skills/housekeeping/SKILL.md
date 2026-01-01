---
name: housekeeping
description: Memory Bank cleanup and optimization using relevance-based archiving (NOT metric-based). Handles LLM-ONLY format conversion, redundancy removal, and archive management. Use when user requests "housekeeping", "cleanup memory bank", "optimize documentation", or when files exceed trigger thresholds. NEVER delete - always archive.
---

# Housekeeping Skill - LLM-ONLY Format

Version: 2.12
Timestamp: 2025-12-17 12:15 CET

## Trigger Keywords

Load when:
- "housekeeping"
- "cleanup memory bank"
- "optimize documentation"
- "find redundancies"
- "token optimization"
- Files exceed trigger thresholds (see below)

---

## Philosophy: Relevance > Metrics

**Core principle:** Relevance-based, NOT metric-based

- **NO fixed targets** (500 lines, 2 weeks old, etc.) → Guidelines only
- **NO time-based archiving** → Relevance-based archiving
- **NO deletion** → Archive everything
- **NO edit snippets** → Read full file, rewrite completely
- **NO quantitative goals** → Qualitative optimization

**Trigger thresholds** (when to START housekeeping, not goals):
- activeContext.md: >500 lines OR feels cluttered
- techContext.md: >300 lines OR outdated info suspected
- systemPatterns.md: >800 lines OR redundancies suspected
- CLAUDE.md: >700 lines OR prose detected
- Modules: >300 lines OR verbose

**Thresholds = "Check needed", not "Must reach X"**

---

## Minimum Context Requirements (MANDATORY)

**After housekeeping, activeContext.md MUST always contain:**

| Section | Purpose | Minimum |
|---------|---------|---------|
| Current Status + Version | What's the project state? | Always |
| Last 3-5 relevant sessions | Kompakt, nicht Details | 3-5 entries |
| ALL open/active topics | Nichts vergessen | Complete list |
| Key Learnings/Patterns | Zusammenfassung, nicht Details | Summary of each |
| Backlog/Next Steps | Clear direction | Actionable items |

**Core Rule: Archive DETAILS, keep SUMMARIES**

| ❌ Wrong | ✅ Right |
|----------|----------|
| Session 45 komplett archivieren | Session 45 Details archivieren, 2-Zeilen-Summary behalten |
| Pattern-Erklärung löschen | Details archivieren, "Pattern X löst Problem Y" behalten |
| Bug-Investigation entfernen | Details archivieren, "Bug war wegen X, Fix ist Y" behalten |

**Why this matters:**
- Next session needs context to continue work
- Summaries = Navigation markers to archived details
- Without summaries = Complete context loss

---

## Phase 1: Read & Analyze (NOT grep)

**Goal:** Understand current state holistically

### 1.1 Read Files Completely

**DO NOT grep/search snippets - Read ENTIRE files:**

**Use Read tool to read completely:**
- memory-bank/activeContext.md
- memory-bank/techContext.md
- memory-bank/systemPatterns.md

**Analyze for:**
- [ ] Which info is relevant for NEXT development steps?
- [ ] Which info needed for regression/debugging?
- [ ] Which info provides learning value?
- [ ] Which sections overlap (redundancy)?
- [ ] Which content is prose vs instructions?

**Key question:** "Do we need this to move forward?"
- YES → Keep or optimize
- NO but historical value → Archive
- NO and no value → Still archive (never delete)

### 1.2 Identify Redundancies

**Read across files, look for:**
- Same content in multiple files
- Rules in Memory Bank that belong in CLAUDE.md
- Historical decisions repeated in current sections
- Similar patterns described multiple ways
- Examples that repeat same concept

**Decision matrix:**
- Rule/Protocol → CLAUDE.md only
- Pattern/Implementation → systemPatterns.md only
- Current focus → activeContext.md only
- Project-specific → techContext.md only

### 1.3 Understand Archive Structure

**Check existing archives:**
```bash
ls -lh memory-bank/archive/
```

**Archive = Complete history, unlimited size allowed**
- Memory Bank = Read every session (must be lean)
- Archive = Read on demand (can be huge)

---

## Phase 2: Plan Restructuring

**Goal:** Decide what stays, what gets optimized, what archives

### 2.1 activeContext.md Planning

**For each entry, ask:**
- Needed for next development steps? → KEEP (optimize format)
- Historical context with learning value? → ARCHIVE
- Completed task with no further relevance? → ARCHIVE

**Project age matters:**
- Active daily project: Keep last 1-2 weeks
- Weekly project: Keep last 1-2 months
- Sporadic project: Keep all recent sessions regardless of age

**Relevance examples:**
- ✅ KEEP: "Bug in module X causes Y under condition Z" (regression risk)
- ✅ KEEP: "Investigation revealed pattern P" (learning value)
- ✅ KEEP: "Next: Implement feature F" (immediate next steps)
- 📦 ARCHIVE: "Completed migration to tech T" (done, historical only)
- 📦 ARCHIVE: "Session 45: Discussed approach A vs B" (decision made, archive details)

### 2.2 techContext.md Planning

**For each section, ask:**
- Current tech stack/config? → KEEP (optimize format)
- Deprecated/replaced? → ARCHIVE
- Future consideration? → KEEP if soon, ARCHIVE if distant

**Examples:**
- ✅ KEEP: Current PHP version, active dependencies
- 📦 ARCHIVE: Migration notes from old framework
- 📦 ARCHIVE: Evaluated-but-not-used alternatives

### 2.3 systemPatterns.md Planning

**For each pattern, ask:**
- Currently used in development? → KEEP (optimize format)
- Critical lesson (disaster prevention)? → KEEP
- Obsolete/superseded pattern? → ARCHIVE

**Examples:**
- ✅ KEEP: "Complete Rewrites Must Review CHANGELOG" (critical)
- ✅ KEEP: "LLM-ONLY Documentation" (active standard)
- 📦 ARCHIVE: Pattern only relevant for old tech

### 2.4 Create Archive Plan

**Document what will archive:**
```markdown
## Archive Plan

### From activeContext.md:
- Sessions 1-10 (completed, historical only)
- Investigation XYZ (resolved, keep summary)

### From techContext.md:
- Old framework config (migrated)
- Deprecated tool setup

### From systemPatterns.md:
- Pattern ABC (superseded by XYZ)
```

---

## Phase 3: Execute Restructuring

**CRITICAL: Full file rewrite, NOT snippet edits**

### 3.1 Archive First (Safety)

**Create archive with OLD content:**

```markdown
# Archive: activeContext - YYYY-MM-DD
Archived: YYYY-MM-DD HH:MM CET
Source Version: X.YY

## [Original Section Name]

[Full original content with timestamps preserved]
```

**Archive location:** `memory-bank/archive/YYYY-MM-activeContext.md`

**Commit archive:**
```bash
git add memory-bank/archive/
git commit -m "Archive: activeContext entries (safe before restructure)"
```

### 3.2 Rewrite activeContext.md

**Read original completely, write NEW file:**

```markdown
# Active Context - [Project]

Version: X.YY (increment)
Timestamp: YYYY-MM-DD HH:MM CET

## Current Focus

[ONLY relevant current work]

## Recent Changes

[ONLY entries needed for next steps - max 10-20 depending on project]

## Active Issues

[ONLY unresolved blockers]

## Next Steps

[Clear, actionable next steps]
```

**Format: LLM-ONLY**
- Bullets, no prose
- No "why" unless critical for understanding
- No repeated context
- Data-dense, token-minimal

### 3.3 Rewrite techContext.md

**Read original completely, write NEW file:**

```markdown
# Technical Context - [Project]

Version: X.YY (increment)
Timestamp: YYYY-MM-DD HH:MM CET

## Tech Stack

[Current only]

## Configuration

[Active configs only]

## Setup

[Current setup instructions]

## Integration

[Active integrations]
```

### 3.4 Rewrite systemPatterns.md

**Read original completely, write NEW file:**

```markdown
# System Patterns - [Project]

Version: X.YY (increment)
Timestamp: YYYY-MM-DD HH:MM CET

## Development Standards

[Active standards]

## Implementation Patterns

[Currently used patterns]

## Error Handling

[Active protocols]

## Critical Lessons

[Disaster prevention - always keep]
```

### 3.5 Optimize CLAUDE.md (If Needed)

**CRITICAL: ALWAYS coordinate CLAUDE.md changes with user FIRST**

**IF CLAUDE.md has prose/redundancy:**

Read completely, **ASK USER** before making changes:
- "CLAUDE.md optimization needed: [list changes]. Proceed?"
- Wait for explicit approval
- Then write optimized version:
  - Paragraphs → Bullets
  - Remove "why" explanations
  - Consolidate duplicate sections
  - One example per concept max
  - Remove overlap with systemPatterns.md

**Why coordinate:** CLAUDE.md = Core rules, no auto-edit even with Auto-Edit enabled

---

## Phase 4: Module Optimization

**ONLY: LLM-ONLY format conversion, NO functional changes**

### 4.1 Review Each Module

**For each module in `.claude/modules/`:**

Read completely, analyze:
- [ ] Prose paragraphs present?
- [ ] "Why" explanations verbose?
- [ ] Examples redundant?
- [ ] Instructions clear or chatty?

### 4.2 Compress Verbose Modules

**IF module verbose:**

Read original completely, write NEW version:
- Convert all prose → bullets
- Remove all "why" → keep only "what do"
- Consolidate examples (1 max)
- Clear instructions, no chat

**CRITICAL: Modules = Compression ONLY, NOT archiving**
- Compress verbose content → token-sparse format
- Keep ALL functionality unchanged
- Keep ALL content (just more concise)
- Modules cannot be archived (always active)

**DO NOT:**
- Remove modules (keep all)
- Change functionality
- Archive module content (modules stay complete)

---

## Phase 5: Verification

### 5.1 Quality Check

**Read new versions completely:**
- [ ] All critical info preserved?
- [ ] Clear and actionable?
- [ ] LLM-ONLY format throughout?
- [ ] No redundancies across files?
- [ ] Versions + timestamps updated?

### 5.2 Archive Verification

**Check archives:**
- [ ] All removed content in archives?
- [ ] Archives complete and readable?
- [ ] Nothing lost?

### 5.3 Git Status

```bash
git status
git diff memory-bank/activeContext.md
git diff memory-bank/systemPatterns.md
```

**Verify changes make sense**

### 5.4 Next-Session Test (CRITICAL)

**Before committing, ask yourself:**
"Kann die nächste Session mit dieser activeContext.md sinnvoll weiterarbeiten?"

**Checklist:**
- [ ] Weiß ich, wie das Projekt funktioniert?
- [ ] Kenne ich die wichtigen Patterns?
- [ ] Verstehe ich die Architektur?
- [ ] Habe ich Kontext über gelöste Probleme und warum?
- [ ] Sind alle offenen Tasks/Themen dokumentiert?

**If ANY answer is NO → Too much archived**
- Restore summaries from archive
- Add missing context back
- Re-run verification

**This test prevents the "120-line disaster"** - A minimal activeContext.md that looks clean but leaves the next session blind.

---

## Phase 6: Commit

**Update all versions + timestamps:**
- [ ] All modified Memory Bank files
- [ ] Modified modules
- [ ] Archive files

**Commit format:**
```bash
git add memory-bank/*.md memory-bank/archive/*.md .claude/modules/*.md
git commit -m "$(cat <<'EOF'
Housekeeping: Relevance-based optimization

Archives:
- activeContext: [describe what archived]
- techContext: [describe what archived]
- systemPatterns: [describe what archived]

Optimizations:
- Converted prose → bullets
- Removed redundancies (list key ones)
- Focused on relevance (not age)
- Complete file rewrites (not edits)

Philosophy: Relevance > Metrics, Archive > Delete

Evidence: maison Sessions 101-105 (relevance-based cleanup)

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Success Criteria

**Housekeeping successful when:**
- [ ] Memory Bank feels actionable (not cluttered)
- [ ] No redundant content across files
- [ ] All prose → bullet format
- [ ] Everything relevant for NEXT work is present
- [ ] Everything irrelevant is archived (not deleted)
- [ ] All versions + timestamps updated
- [ ] Git commit created
- [ ] Obsidian sync successful
- [ ] YOU understand the project better now

**Last criterion is key: Better understanding = Good housekeeping**

---

## Anti-Patterns

**❌ DON'T:**
- Set fixed line count goals (500 lines target)
- Archive based on age (2 weeks old)
- Delete anything (ever)
- Edit snippets (always full rewrite)
- Use grep for analysis (read full files)
- Focus on token count numbers (focus on relevance)
- Remove modules "not used recently"
- Aim for percentage reductions
- Archive entire sessions without keeping summary (context loss!)
- Reduce activeContext.md below minimum requirements (see above)

**✅ DO:**
- Ask "Is this relevant for next steps?"
- Archive everything not currently needed
- Read files completely before rewriting
- Optimize based on understanding, not metrics
- Keep all modules, just optimize format
- Focus on clarity and actionability
- Trust qualitative judgment

---

## Context Considerations

**Project size matters:**
- **Small project:** Memory Bank naturally small
- **Large project:** Memory Bank naturally larger
- **Complex project:** More context needed
- **Simple project:** Less context needed

**Development rhythm matters:**
- **Daily work:** Keep very recent only
- **Weekly work:** Keep broader timeframe
- **Sporadic work:** Keep all recent sessions regardless of calendar time

**There is NO universal size target - optimize for PROJECT needs**

---

## Troubleshooting

**Problem:** Unsure what to keep vs archive

**Solution:**
- Ask: "Do I need this for NEXT development?"
- Ask: "Would this help debug a regression?"
- Ask: "Does this teach me something important?"
- If YES to any → KEEP
- If NO to all → ARCHIVE (not delete)

**Problem:** File still feels large after housekeeping

**Solution:**
- Large project = Large Memory Bank is OK
- Check: Is it cluttered or just comprehensive?
- Cluttered → More archiving
- Comprehensive → It's fine

**Problem:** Lost important context

**Solution:**
- Check archive files
- Check git history: `git log -p -- memory-bank/`
- Restore from archive or git
- Archives are permanent for this reason

**Problem:** Took too long

**Solution:**
- Multiple sessions OK for large projects
- Full file context > Speed
- Better understanding = Worth the time

---

## Remember

**Housekeeping is about UNDERSTANDING, not METRICS**

- Read completely (not grep snippets)
- Rewrite completely (not edit snippets)
- Archive based on relevance (not age)
- Optimize based on clarity (not line counts)
- Never delete (always archive)
- Trust judgment (not formulas)

**If you understand the project better after housekeeping → Success**
