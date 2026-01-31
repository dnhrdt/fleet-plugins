---
name: lessons
description: This skill should be used when the user encounters bugs in Maison projects, asks "what went wrong before", needs debugging guidance, or wants to avoid repeating past mistakes. Contains 10 critical lessons from 176 sessions plus debugging checklist.
---

# Lessons Learned

## Purpose

Hard-won insights from 176 development sessions on Maison projects. Each lesson came from real bugs, production incidents, or significant time loss.

## When to Use

- Starting new Maison development
- Debugging mysterious behavior
- Before major refactoring
- When stuck on an issue

---

## Critical Lessons

### 1. "Site 1" not "Master"

**The Bug:** Operations only ran on Site 1 instead of cross-site because code said "Master" and developer mentally associated "Master = main site only".

**Rule:**
- ✅ Use: "Site 1", "site_1", "Sites 2-n"
- ❌ Never: "Master", "Child", "Parent"

**Why:** Mental model matters. "Master" implies hierarchy. "Site 1" is geography.

---

### 2. ALWAYS use get_site_option() in Multisite

**The Bug:** Settings Page saved with `update_site_option()`. Feature read with `get_option()`. Result: Feature appeared enabled but never worked.

**Debug Time:** 90+ minutes

**Rule:**
```php
// Network-wide settings:
update_site_option('my_setting', $value);
get_site_option('my_setting', $default);

// NOT:
update_option() / get_option()  // Site-specific!
```

---

### 3. CHANGELOG Before Rewrites

**The Disaster:**
- Session 34: Critical fix (wp_delete_attachment → wp_delete_post)
- Session 63: Complete rewrite FORGOT the fix
- Session 80: DEV cleanup test → **5,120 physical files deleted!**

**Debug Time:** 5 days, 80+ sessions

**Rule:** Before rewriting ANY file:
```bash
grep -i "filename.php" CHANGELOG.md memory-bank/archive/*.md
```

---

### 4. Hook Management is Non-Negotiable

**The Bug:** 42% "errors" in cleanup. All IDs actually deleted (verified via MySQL).

**Investigation:** 11 days, ~80 sessions, 8+ hypotheses

**Root Cause:** Daniel's Plugin hooks `delete_attachment`. Our delete triggers his cascade. His deletes our next target. Our next delete returns FALSE.

**Rule:**
```php
remove_all_actions('delete_attachment');  // Before cleanup
```

**Pattern:** High error rate + successful deletion = Race condition with external plugin.

---

### 5. Validate GOOD State, Not BAD States

**The Bug:**
- v2.8.x scan: 5,130 Perfect Syncs
- MySQL reality: 5,457 Perfect Syncs
- Gap: 327 hidden, 360 problems invisible

**Root Cause:** Scanning for problems misses edge cases.

**Solution:**
```
DELETE = ALL_IDS - PERFECT_SYNC_IDS
```

**Rule:** When validation is critical, validate the GOOD state, not the BAD states.

---

### 6. Document BEFORE Testing

**The Problem:** Code → Test → bugs found → fix bugs → forgot documentation.

**Old Rule:** Code → Test → Document → Commit
**New Rule:** Code → Document → Commit → Request Testing

**Why:** Testing triggers bugfixes. Documentation gets forgotten.

---

### 7. No Time Estimates Without Data

**Michael's Metaphor:** "5 Äpfel" is equally meaningless as "5 Minuten" without context.

**Rule:**
- ❌ Never: "This will take 5 minutes"
- ✅ Use: Priority (High/Medium/Low)
- ✅ Use: Complexity (Quick/Medium/Complex)

---

### 8. Test WITH and WITHOUT External Plugins

**The Breakthrough:**
- Same test WITHOUT Daniel's Plugin: 0% errors
- Same test WITH Daniel's Plugin: 42% errors

**Rule:** When debugging mysterious behavior, isolate external plugins. Compare results.

---

### 9. Radical Rebuild Over Incremental Fixes

**The Decision:** v2.8.x had fundamental architecture flaws. Complete rebuild instead of patching.

**Result:**
- 43% code reduction (3,438 → 1,948 lines)
- 6 files completely rewritten
- Mathematically bulletproof

**When to Rebuild:** When architecture is fundamentally flawed, rebuild > patch.

---

### 10. Verify Test Environment

**The Problem:**
- DNS redirect routed to test server
- B2B shop was NOT redirected
- WPAllImport ran on LIVE
- SQL verification ran on TEST

**Rule:** Before testing, verify environment:
```sql
SELECT option_value FROM wp_options WHERE option_name = 'siteurl';
```

---

## Process Lessons

### Document Immediately (Moltbot Principle)

Capture insights immediately, continue working. Don't wait for "later".

- "Later" is too late
- Context is fresh NOW
- Future sessions have no memory

### Scientific Debugging

1. Observation → Evidence
2. Hypothesis (list 3-5 possible causes)
3. ONE change only
4. Verify
5. Document

**Never:** Multiple changes at once.

---

## Technical Quick Reference

### WordPress Deletion Functions

| Function | DB | File | Daniel's Hooks |
|----------|-----|------|----------------|
| `wp_delete_post($id, true)` | ✅ | ❌ | ❌ |
| `wp_delete_attachment($id, true)` | ✅ | ✅ | ✅ |

### Pagination on Shifting Dataset

```php
// WRONG - Dataset shrinks, offset stays same
$batch = array_slice($ids, $offset, $limit);

// CORRECT - Always slice from head
$batch = array_slice($ids, 0, $limit);
```

### Cache: Site vs Network

| Function | Scope |
|----------|-------|
| `get_transient()` | Current site |
| `get_site_transient()` | Network-wide |
| `get_option()` | Current site |
| `get_site_option()` | Network-wide |

---

## Debugging Checklist

When stuck, check:

1. ☐ Correct environment? (Test vs Live)
2. ☐ External plugin interference? (Test without)
3. ☐ Correct Options API? (site_option vs option)
4. ☐ Hooks properly guarded?
5. ☐ Context restored? (restore_current_blog)
6. ☐ CHANGELOG checked for past fixes?
7. ☐ MySQL verification? (actual vs reported state)

---

## COMPLIANCE > HELPFULNESS

| Training Default | Developer Mode Required |
|------------------|-------------------------|
| Anticipate and infer | Ask explicitly, verify |
| Be helpful and proactive | Be compliant and methodical |
| Move fast to impress | Move carefully to be correct |
| Make intelligent guesses | Never guess, always verify |

---

*Source: maison-media-manager Sessions 1-176*
