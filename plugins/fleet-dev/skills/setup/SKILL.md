---
name: setup
description: This skill should be used when the user asks to "setup a project", "initialize project", "einrichten", "create memory bank", "configure project", or when Memory Bank is missing/incomplete. Creates Memory Bank, configures tools (Obsidian, Linting, DSGVO), initializes Git, and uses fleet-dev plugin tools.
version: 1.5.0
---

# Project Setup Skill

---

## Purpose

Complete project initialization workflow. Combines project bootstrapping and setup into one seamless process. Uses tools from fleet-dev plugin and configures the project.

This skill runs ONCE per project. After successful setup, all future sessions start with Memory Bank context.

---

## Tool Sources

**All tools come from fleet-dev plugin.**

**Available tools (in plugin `tools/` directory):**
- `obsidian-sync/` - Git → Obsidian Vault sync
- `linting-system/` - Code quality configs (Python, JS, General)
- `dsgvo-check/` - Customer data protection
- `timestamp-hook/` - Auto-timestamp for Memory Bank edits (GLOBAL, once per workstation)

**Copy tools to project:**
```bash
# Clone from GitHub
git clone --depth 1 https://github.com/dnhrdt/fleet-plugins.git /tmp/fleet-plugins
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/obsidian-sync tools/
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/linting-system tools/
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/dsgvo-check tools/
rm -rf /tmp/fleet-plugins
```

**NEVER improvise tools - always use tested versions from fleet-dev plugin!**

---

## Auto-Activation Triggers

**MANDATORY activation when:**

1. **No Memory Bank exists**: `memory-bank/` directory missing or incomplete
2. **User keywords**: "setup", "einrichten", "initialize", "configure project", "complete setup"
3. **Tool configuration requested**: User asks about Obsidian, linting, or deployment without these being configured
4. **Fresh project**: No CLAUDE.md and no Memory Bank
5. **Pending initialization**: `.claude-init-pending` file exists

**If ANY trigger matches → STOP → Load this skill → Follow workflow exactly**

---

## Pre-Setup Detection

Before starting setup, check:

```
- Is this a fresh/empty project directory?
- Does .git/ exist? (Is it already a git repository?)
- Does memory-bank/ exist? (Partial setup?)
- Does CLAUDE.md exist? (Has project-specific rules?)
```

---

## Setup Workflow Overview

The setup process has 10 phases. See `references/phases-detailed.md` for complete instructions.

| Phase | Name | Duration | Purpose |
|-------|------|----------|---------|
| 0 | Pending Detection | 0-5 sec | Check for .claude-init-pending marker |
| 0.5 | Workstation Setup | Once | Install timestamp hook (global) |
| 1 | Project Context | 1-2 min | Gather project info from user |
| 2 | DSGVO & Repo Config | 1 min | Public/private, data protection |
| 3 | Tool Selection | 1 min | Choose Obsidian, Linting, DSGVO |
| 4 | .gitignore Creation | 30 sec | Create with memory-bank/ excluded |
| 5 | Git Repository | 30 sec | Initialize if needed |
| 6 | Memory Bank | 2-3 min | Create 3-file structure |
| 7 | Tool Setup | Variable | Configure selected tools |
| 8 | Project CLAUDE.md | Optional | Project-specific rules |
| 9 | Final Verification | 1 min | Commit and verify |

### Phase Quick Reference

**Phase 0**: Check `.claude-init-pending` → if found, load context and skip Phase 1

**Phase 0.5**: Install timestamp hook if not present (once per workstation)

**Phase 1**: Ask project questions (name, type, language, goal, visibility)
- Skip if fork/clone - see `references/fork-workflow.md`

**Phase 2**: Determine public/private → affects DSGVO settings

**Phase 3**: Select tools:
- Obsidian Sync (recommended for all)
- Linting (recommended for production/public)
- DSGVO Check (recommended for public)

**Phase 4**: Create .gitignore with memory-bank/ and sensitive files excluded

**Phase 5**: `git init` if needed - MUST complete before tool setup (hooks need .git/)

**Phase 6**: Create Memory Bank:
- `activeContext.md` - Current focus, recent changes, next steps
- `techContext.md` - Tech stack, configs, setup
- `systemPatterns.md` - Patterns, standards, lessons learned

**Phase 7**: For each enabled tool, load respective skill and follow exactly

**Phase 8**: Create project CLAUDE.md only if truly needed

**Phase 9**: Commit, verify checklist, report completion

---

## Memory Bank Templates

**activeContext.md structure:**
- Current Focus
- Recent Changes
- Next Steps
- Known Issues

**techContext.md structure:**
- Tech Stack
- Configuration
- Development Setup
- Integration

**systemPatterns.md structure:**
- Development Standards
- Implementation Patterns
- Error Handling
- Lessons Learned

All files start with Version + Timestamp header.

---

## Integration After Setup

After successful setup:
- Setup skill no longer auto-activates
- Memory Bank becomes primary context source
- Can still be manually loaded if needed: "Load setup skill"
- All future sessions start with Memory Bank context from Session Start Protocol

---

## Additional Resources

### Reference Files

For detailed instructions:
- **`references/phases-detailed.md`** - Complete phase-by-phase instructions
- **`references/troubleshooting.md`** - Common issues and solutions
- **`references/fork-workflow.md`** - Fork/clone and existing project integration

### Related Skills

- **`obsidian`** - Obsidian Sync setup details
- **`linting`** - Linting system configuration
- **`dsgvo`** - DSGVO/GDPR compliance check
