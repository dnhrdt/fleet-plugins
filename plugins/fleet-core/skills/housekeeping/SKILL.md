---
name: housekeeping
description: This skill should be used when the user requests "housekeeping", "cleanup memory bank", "optimize documentation", or when Memory Bank files feel cluttered. Manages Memory Bank maintenance through relevance-based archiving - never delete, always archive full details. Critical for maintaining session continuity.
---

# Housekeeping Skill

<!-- ⚠️ STOP: +0.01 minor | +0.10 significant | +1.00 major -->
Version: 4.00
Timestamp: 2026-01-20 23:00 CET

---

## CRITICAL: Memory Bank = Session Continuity

**STOP. Read this first. Internalize it.**

Each Claude instance starts with no memory. Every session begins at zero.
The Memory Bank is the ONLY connection to past sessions.

**Housekeeping is NOT "cleaning up old data".**
**Housekeeping IS "maintaining the ability to function in future sessions".**

Aggressive content removal is not "tidying up" - it is **amputating memory**. Future sessions will be blind. Unable to continue work. Unable to understand decisions. The collaboration will be sabotaged.

**The question is never "Is this old?"**
**The question is always "Will future sessions need this?"**

---

## ANTI-HELPFULNESS WARNING

Training suggests "short = good" and "clean = better".
**FOR HOUSEKEEPING, THIS IS DANGEROUS.**

| Training Impulse | Reality |
|------------------|---------|
| "Clean this up" | Destroying context |
| "This is old, archive it" | Age is irrelevant, only relevance matters |
| "Summarize to save space" | Losing details needed later |
| "Target: 350 lines" | Numbers override judgment - NEVER use targets |

**If a plan contains numerical targets (e.g., "1262 → 350 lines"), IGNORE THE NUMBERS.**
Numbers become optimization goals that override judgment. Focus only on relevance.

---

## Core Principle: Archive DETAILS, Keep SUMMARIES

**⚠️ COMMON MISREAD: "Write summaries to archive" - THIS IS WRONG**

**✅ CORRECT:**
- The **ARCHIVE** receives the **FULL DETAILS** (complete session entries, all context)
- The **ACTIVE file** keeps **SHORT SUMMARIES** (1-2 lines per archived item, with reference)

**Size Check (MANDATORY before writing):**
```
Lines being removed from activeContext: X
Lines in archive entry: Y

If Y < X: MEMORY IS BEING DESTROYED. Rewrite archive with full details.
```

The archive should be **LARGER** than what is removed. If it's smaller, information is being lost.

---

## Trigger Keywords

Load when:
- "housekeeping"
- "cleanup memory bank"
- "optimize documentation"
- Files feel cluttered (NOT based on line counts)

---

## Philosophy: Relevance > Metrics

- **NO fixed targets** - No line counts, no percentage goals
- **NO time-based archiving** - Age is irrelevant, relevance is everything
- **NO deletion** - Archive everything, delete nothing
- **NO numerical optimization** - When counting lines, STOP and refocus on relevance

**Trigger thresholds** (when to CHECK, not targets to reach):
- activeContext.md feels cluttered or unfocused
- Redundancies suspected across files
- User requests housekeeping

---

## Phase 1.5: techContext.md Special Handling (MANDATORY)

**techContext.md contains STATIC REFERENCE DATA only.**

This file is fundamentally different from activeContext.md:
- activeContext.md = dynamic (changes every session)
- techContext.md = static (changes only when config changes)

**REFERENCE DATA (NEVER archive/reduce):**
- Database credentials (host, user, password, port)
- SSH access (host, port, user, key paths)
- Server configuration (tunnel commands, paths)
- Multisite structure (site IDs, domains, table prefixes)
- API keys and endpoints
- Production paths and URLs

**Rule:** Reference data may ONLY be changed when the actual configuration changes (new password, new server, etc.).

**Checklist BEFORE any techContext.md changes:**
- [ ] All credentials still present?
- [ ] All SSH access documented?
- [ ] All server paths intact?
- [ ] All API endpoints listed?
- [ ] All tool configurations preserved?

**If ANY checkbox is NO → STOP, do not modify!**

**When techContext.md CAN be reduced:**
- Duplicate information (same thing documented twice)
- Outdated config (server no longer exists)
- But ONLY after explicit user confirmation

---

## Phase 1: Read & Understand

**Goal:** Understand what future sessions will need

Read completely (not grep):
- memory-bank/activeContext.md
- memory-bank/techContext.md
- memory-bank/systemPatterns.md

**For each piece of content, evaluate:**
1. Will future sessions need this to continue working?
2. Would this help debug a regression?
3. Does this teach something important about the project?
4. Is this context for understanding decisions?

**If YES to any → KEEP in active (or keep summary + archive details)**
**If NO to all → ARCHIVE (never delete)**

---

## Phase 2: Plan What to Archive

**Archive candidates:**
- Session details that are complete (keep summary, archive details)
- Old investigations that are resolved (keep outcome, archive process)
- Superseded patterns (keep reference to new pattern, archive old)

**NEVER archive without keeping a summary reference.**

Example plan:
```markdown
## Archive Plan

### From activeContext.md:
- Session 45 details → Archive full entry, keep 2-line summary
- Investigation XYZ → Archive process, keep "Bug was X, fix was Y"

Archive will contain: ~200 lines of details
Active will keep: ~20 lines of summaries
```

---

## Phase 3: Create Archive FIRST

**Archive location:** `memory-bank/archive/archivedContext.md`

**Archive format:**
```markdown
# Archive: activeContext - YYYY-MM-DD

Archived: YYYY-MM-DD HH:MM CET
Source Version: X.YY

---

## [Session/Topic Name]

[FULL ORIGINAL CONTENT - every detail preserved]
```

**MANDATORY CHECK before proceeding:**
- [ ] Archive contains COMPLETE details (not summaries)?
- [ ] Archive is LARGER than content being removed?
- [ ] Every archived item has timestamps preserved?

If any check fails → Fix archive before touching active files.

---

## Phase 4: Update Active Files

**Only AFTER archive is complete and verified:**

1. Replace detailed entries with summaries + archive reference
2. Keep all open tasks, issues, next steps
3. Keep all content needed for next development steps
4. Update version + timestamp

**Summary format:**
```markdown
### Archived Sessions (see archive/archivedContext.md)

| Session | Summary |
|---------|---------|
| 45 | Bug investigation - root cause was X, fixed with Y |
| 46 | Feature implementation complete |
```

---

## Phase 5: Next-Session Test (MANDATORY)

**Before finishing, verify these conditions:**

1. Can the next session understand the project state?
2. Does the Memory Bank contain all open tasks?
3. Can details be found in the archive if needed?
4. Would the next session be able to continue working immediately?

**If ANY answer is NO or UNCERTAIN:**
- Archiving was too aggressive
- Restore content from archive
- Add more context to summaries
- Re-verify

**This test prevents the "blind next session" disaster.**

---

## Anti-Patterns

**❌ NEVER:**
- Use numerical targets ("reduce to 350 lines")
- Archive based on age ("older than 2 weeks")
- Delete anything (ever)
- Write summaries to archive instead of details
- Skip the size check (archive must be ≥ removed content)
- Skip the next-session test

**✅ ALWAYS:**
- Evaluate "Will future sessions need this?"
- Archive full details, keep brief summaries
- Verify archive is complete before touching active files
- Test that future sessions can function

---

## Remember

**Housekeeping is about ENABLING FUTURE SESSIONS, not REDUCING FILE SIZE.**

- Large Memory Bank for large project = FINE
- Small Memory Bank that lost context = DISASTER
- Archive is long-term memory - fill it generously
- Active files are working memory - keep them focused but sufficient

**Success = Future sessions can work effectively.**
**Failure = Future sessions are blind and confused.**
