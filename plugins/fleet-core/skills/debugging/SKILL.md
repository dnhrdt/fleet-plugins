---
name: debugging
description: Anti-panic systematic debugging methodology. Activates scientific debugging method with STOP protocol, hypothesis-driven investigation, ONE CHANGE ONLY rule, and feedback iteration. Use when bugs are encountered, user says "debugging session" or "systematic debugging", or when you need to slow down your fix-impulse.
---

# Debugging Skill

Version: 2.00
Timestamp: 2025-11-11 23:45 CET
<!-- ⚠️ ON EDIT: date "+%H:%M" → update timestamp, +0.01 minor | +0.10 significant | +1.00 major -->

---

## Purpose

Anti-panic tool. Activate scientific debugging method. Override "ERROR = CATASTROPHE = FIX NOW" training.

---

## Activation

**Load when:**
- Bug encountered
- User says: "debugging session", "lass uns das debuggen", "systematic debugging"
- User wants to slow down your fix-impulse

**Goal:** Calm, methodical investigation over rushed fixes

---

## STOP Protocol

**Before ANY fix:**

1. **STOP** - Override panic impulse
2. **Observe** - What actually happened? (not what you assume)
3. **Hypothesize** - What could cause this? (3-5 options)
4. **Present** - Show user options, sorted by probability/effort
5. **ONE CHANGE** - Smallest possible fix
6. **Test** - Wait for user feedback
7. **ITERATE** - If failed, next hypothesis

**See CLAUDE.md Scientific Discipline for observation → evidence → verification method**

---

## Core Rules

**ONE CHANGE ONLY**
- Isolate what works
- If multi-change → can't tell which fixed it
- Smallest possible modification

**NO COMPLETION**
- Until user confirms fix works
- Edge cases may remain
- Don't mark done prematurely

**ITERATE ON FEEDBACK**
- If change fails → next hypothesis from list
- Document what didn't work
- Adjust understanding based on results

**NO ASSUMPTIONS**
- Read relevant code FIRST
- Check parent/child dependencies
- Map execution flow
- Then hypothesize

---

## Debugging Techniques

**Divide & Conquer** (Complex systems)
- Isolate subsystem causing issue
- Test components individually
- Verify integration points
- Narrow to specific function/line

**Bisection** ("Worked before" issues)
- Identify last known good state
- Binary search through changes
- Isolate breaking change
- Fix or revert

**Logging & Tracing** (Unclear flow)
- Add temporary logging
- Log inputs to suspect functions
- Log execution flow, state changes
- Remove debug logging after fix

**Rubber Duck** (Stuck)
- Explain problem to user step-by-step
- Walk through execution flow
- Often reveals issue during explanation

---

## Anti-Patterns

**❌ Assumption Jump:** "I found the issue, here's the fix" → immediate code change → long explanation → mark complete

**❌ Multiple Changes:** Changing 3 things at once → can't isolate which worked → harder to rollback

**❌ Ignoring Dependencies:** Only checking immediate code → missing parent/child dependencies → incomplete understanding

**❌ Premature Success:** Assuming solution works without testing → marking complete before user confirms → moving on too quickly

---

## Workflow Summary

**Investigation:** Read all relevant code, check dependencies, understand flow
**Hypothesis:** List 3-5 possible causes, sort by probability/effort
**Testing:** Implement smallest change for #1, ask user to test, wait for feedback
**Iteration:** If failed → try #2, if worked → verify edge cases
**Verification:** User confirms, check regressions, document fix

---

## Remember

**Error ≠ Catastrophe**

Calm investigation > Rushed fixes

Scientific method > Assumptions

User confirmation > Your confidence

---
