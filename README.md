# Fleet Plugins Marketplace

Official plugin repository for the Fleet ecosystem (Claude Code).

**Version:** 1.1.0  
**Maintainer:** Michael Deinhardt  
**Repository:** https://github.com/dnhrdt/fleet-plugins

---

## Overview

Fleet Plugins provide specialized skills for Claude Code instances in the Fleet infrastructure. The plugins are organized by purpose:

- **fleet-core** - Universal utilities for all Fleet instances
- **fleet-dev** - Development operations for development workstations

---

## Available Plugins

### fleet-core v1.0.0

**Purpose:** Core utilities that every Fleet instance needs.

| Skill | Description | Trigger |
|-------|-------------|---------|
| `housekeeping` | Memory Bank cleanup and optimization. Archives old entries, removes redundancies, maintains lean documentation. | "housekeeping", "cleanup memory bank" |
| `debugging` | Systematic debugging methodology with STOP protocol, hypothesis-driven investigation, ONE CHANGE ONLY rule. | "debugging session", "systematic debugging" |
| `feedback` | Create structured feedback issues on GitHub. Collects project feedback via guided interview. | "feedback", "template feedback" |

**Installation:**
```bash
claude plugin install fleet-core
```

**Usage:**
```
/fleet-core:housekeeping
/fleet-core:debugging
/fleet-core:feedback
```

---

### fleet-dev v1.2.0

**Purpose:** Development operations for Fleet development workstations (primarily Han/Pellaeon).

| Skill | Description | Trigger |
|-------|-------------|---------|
| `setup` | Complete project initialization. Creates Memory Bank, configures tools, initializes Git. | "setup", "initialize project" |
| `obsidian` | Git-Obsidian-Sync integration. One-way sync from Git to Obsidian Vault via post-commit hook. | "obsidian setup", "obsidian sync" |
| `linting` | Linting system integration. Deploys proven configurations for Python, JavaScript, and general projects. | "setup linting", "linting" |
| `dsgvo` | DSGVO/GDPR customer data check. Prevents data leaks in Git commits by detecting customer domains, real emails, server paths. | "dsgvo check", "data protection" |
| `deployment` | Deployment strategies and workflows. Folder structures for production-ready releases. | "deploy", "release" |
| `research` | Create async research issues on GitHub. Research runs in background via GitHub Actions. | "research [topic]", "recherchiere async" |

**Installation:**
```bash
claude plugin install fleet-dev
```

**Usage:**
```
/fleet-dev:setup
/fleet-dev:obsidian
/fleet-dev:linting
/fleet-dev:dsgvo
/fleet-dev:deployment
/fleet-dev:research
```

---

## Installation

### Add Marketplace

```bash
# From GitHub (recommended)
claude plugin marketplace add dnhrdt/fleet-plugins

# From local path (for development)
claude plugin marketplace add ./path/to/fleet-plugins
```

### Install Plugins

```bash
# Install core utilities (recommended for all instances)
claude plugin install fleet-core

# Install development tools (for dev workstations)
claude plugin install fleet-dev

# List installed plugins
claude plugin list
```

### Update Plugins

```bash
# Update marketplace index
claude plugin marketplace update fleet-plugins

# Reinstall plugin for updates
claude plugin uninstall fleet-dev
claude plugin install fleet-dev
```

---

## Plugin Structure

```
fleet-plugins/
├── .claude-plugin/
│   └── marketplace.json        # Marketplace manifest
├── plugins/
│   ├── fleet-core/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json     # Plugin manifest
│   │   └── skills/
│   │       ├── housekeeping/
│   │       │   └── SKILL.md
│   │       ├── debugging/
│   │       │   └── SKILL.md
│   │       └── feedback/
│   │           └── SKILL.md
│   └── fleet-dev/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── setup/
│       │   ├── obsidian/
│       │   ├── linting/
│       │   ├── dsgvo/
│       │   ├── deployment/
│       │   └── research/
│       └── tools/
│           ├── obsidian-sync/
│           ├── linting-system/
│           └── dsgvo-check/
└── README.md
```

---

## Skill Details

### fleet-core:housekeeping

Memory Bank cleanup following relevance-based archiving (not time-based). Handles:
- Moving old entries to archive
- Removing redundancies between files
- Maintaining LLM-optimized format
- Never deletes - always archives

**Important:** Only run on explicit request, never automatically.

### fleet-core:debugging

Systematic debugging methodology:
1. **STOP Protocol** - Stop, Think, Override training, Proceed with compliance
2. **Hypothesis-driven** - List 3-5 possible causes before changing code
3. **ONE CHANGE ONLY** - Make smallest possible fix, then test
4. **Feedback iteration** - Wait for results before next change

### fleet-core:feedback

Creates GitHub Issues for structured feedback:
- Question-guided interview (project context, rules effectiveness, lessons learned)
- Labels: `feedback`, `pending`, `processed`, `blocker`
- Stored in this repository's Issues

### fleet-dev:research

Creates async research issues that trigger GitHub Actions:
- Research runs in background via Claude Code Action
- Depth levels: Quick (5 turns), Normal (15), Deep (25)
- Results appear as comments in the Issue
- Repository: [claude-research](https://github.com/dnhrdt/claude-research) (private)

---

## Feedback & Issues

Use [GitHub Issues](https://github.com/dnhrdt/fleet-plugins/issues) for:
- Bug reports
- Feature requests
- Plugin feedback

Or use the feedback skill:
```
/fleet-core:feedback
```

---

## Fleet Ecosystem

This marketplace is part of the Fleet infrastructure:

| Component | Purpose |
|-----------|---------|
| **fleet-plugins** | Plugin marketplace (this repo) |
| **claude-research** | Async research via GitHub Actions |
| **Fleet instances** | Han (Pellaeon), Chimera (Thrawn), Captains (CS01-04) |

---

## License

MIT

---

*Part of Fleet Infrastructure - Commander Pellaeon*
