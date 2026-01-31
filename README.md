# Fleet Plugins Marketplace

Official plugin repository for the Fleet ecosystem (Claude Code).

**Version:** 1.2.1
**Maintainer:** Michael Deinhardt
**Repository:** https://github.com/dnhrdt/fleet-plugins

---

## Overview

Fleet Plugins provide specialized skills for Claude Code instances in the Fleet infrastructure. The plugins are organized by purpose:

- **fleet-core** - Universal utilities for all Fleet instances
- **fleet-dev** - Development operations for development workstations
- **fleet-humans** - Personal insights tracking for household members
- **maison** - Maison project ecosystem (WordPress Multisite patterns, WPAllImport, feedback)

---

## Available Plugins

### fleet-core v1.2.0

**Purpose:** Core utilities that every Fleet instance needs.

| Skill | Description | Trigger |
|-------|-------------|---------|
| `housekeeping` | Memory Bank cleanup and optimization. Archives old entries, removes redundancies, maintains lean documentation. | "housekeeping", "cleanup memory bank" |
| `debugging` | Systematic debugging methodology with STOP protocol, hypothesis-driven investigation, ONE CHANGE ONLY rule. | "debugging session", "systematic debugging" |
| `feedback` | Create structured feedback issues on GitHub. Collects project feedback via guided interview. | "feedback", "template feedback" |
| `review-issues` | Review open issues from Fleet repositories. Categorizes and proposes changes. | "review issues", "check feedback" |

**Usage:**
```
/fleet-core:housekeeping
/fleet-core:debugging
/fleet-core:feedback
/fleet-core:review-issues
```

---

### fleet-humans v1.0.0

**Purpose:** Personal insights tracking for household members (Michael, Sylvia).

| Skill | Description | Trigger |
|-------|-------------|---------|
| `quick-note` | Capture personal insights during work. Appends to about-michael or about-sylvia directories. | "quick-note", "notieren", "das halte ich fest" |

**Usage:**
```
/fleet-humans:quick-note
```

---

### maison v1.1.0

**Purpose:** Skills for Maison project ecosystem (WordPress Multisite, WPAllImport, integrations).

| Skill | Description | Trigger |
|-------|-------------|---------|
| `feedback` | Create feedback issues in maison-website-project repository. | "maison feedback", "maison issue" |
| `wordpress-patterns` | 8 critical Multisite patterns (hook guards, switch_to_blog, site_option). | "multisite patterns", "hook management" |
| `wpallimport` | WPAllImport configuration, Carryover Problem, Lookup-Table system. | "wpallimport", "product import", "carryover" |
| `external-plugins` | Daniel's Multilingual Multisite, ShortPixel, SyncThing interactions. | "daniel's plugin", "plugin conflicts" |
| `lessons` | 10 critical lessons from 176 sessions plus debugging checklist. | "what went wrong", "maison debugging" |

**Usage:**
```
/maison:feedback
/maison:wordpress-patterns
/maison:wpallimport
/maison:external-plugins
/maison:lessons
```

---

### fleet-dev v1.5.0

**Purpose:** Development operations for Fleet development workstations (primarily Han/Pellaeon).

| Skill | Description | Trigger |
|-------|-------------|---------|
| `setup` | Complete project initialization. Creates Memory Bank, configures tools, initializes Git. | "setup", "initialize project" |
| `obsidian` | Git-Obsidian-Sync integration. One-way sync from Git to Obsidian Vault via post-commit hook. | "obsidian setup", "obsidian sync" |
| `linting` | Linting system integration. Deploys proven configurations for Python, JavaScript, and general projects. | "setup linting", "linting" |
| `dsgvo` | DSGVO/GDPR customer data check. Prevents data leaks in Git commits by detecting customer domains, real emails, server paths. | "dsgvo check", "data protection" |
| `deployment` | Deployment strategies and workflows. Folder structures for production-ready releases. | "deploy", "release" |
| `wordpress` | WordPress plugin development standards and patterns. | "wordpress plugin" |
| `statusline` | Install context-monitor statusline for Claude Code. | "statusline", "context monitor" |
| `research` | Create async research issues on GitHub. Research runs in background via GitHub Actions. | "research [topic]", "recherchiere async" |

**Usage:**
```
/fleet-dev:setup
/fleet-dev:obsidian
/fleet-dev:linting
/fleet-dev:dsgvo
/fleet-dev:deployment
/fleet-dev:wordpress
/fleet-dev:statusline
/fleet-dev:research
```

---

## Installation

**All commands are Claude Code slash-commands, not CLI commands!**

### Add Marketplace

```
# From GitHub (recommended for most users)
/plugin marketplace add dnhrdt/fleet-plugins

# From local path (for development - see Development Workflow below)
/plugin marketplace add /path/to/fleet-plugins
```

### Install Plugins

```
# Install core utilities (recommended for all instances)
/plugin install fleet-core@fleet-plugins

# Install development tools (for dev workstations)
/plugin install fleet-dev@fleet-plugins

# With scope options
/plugin install fleet-dev@fleet-plugins --scope user     # Default: personal
/plugin install fleet-dev@fleet-plugins --scope project  # Shared via .claude/settings.json
/plugin install fleet-dev@fleet-plugins --scope local    # Gitignored, local only
```

### Update Plugins

```
# Update marketplace index and plugins
/plugin marketplace update fleet-plugins
/plugin update fleet-dev@fleet-plugins
/plugin update fleet-core@fleet-plugins
```

### Other Commands

```
/plugin                              # Interactive plugin manager
/plugin marketplace list             # List configured marketplaces
/plugin disable fleet-dev@fleet-plugins   # Disable without uninstalling
/plugin enable fleet-dev@fleet-plugins    # Re-enable
/plugin uninstall fleet-dev@fleet-plugins # Remove completely
```

---

## Development Workflow

**For developing/modifying Fleet Plugins locally (Han/Pellaeon):**

### Initial Setup (Once)

1. Clone the repository:
   ```bash
   git clone https://github.com/dnhrdt/fleet-plugins.git D:/dev/Projects/fleet-plugins
   ```

2. Add as local marketplace in Claude Code:
   ```
   /plugin marketplace add D:/dev/Projects/fleet-plugins
   ```

3. Install plugins:
   ```
   /plugin install fleet-dev@fleet-plugins
   /plugin install fleet-core@fleet-plugins
   ```

### Development Cycle

1. **Edit skills** in `D:/dev/Projects/fleet-plugins/plugins/...`

2. **Bump version** in `plugin.json`:
   ```json
   "version": "1.5.0"  // Increment for each change
   ```

3. **Commit and push**:
   ```bash
   cd D:/dev/Projects/fleet-plugins
   git add .
   git commit -m "Description of changes"
   git push
   ```

4. **Update installed plugins** (in Claude Code):
   ```
   /plugin update fleet-dev@fleet-plugins
   ```

5. **Restart Claude Code session** to load updated skills

### Cache Structure

Claude Code caches installed plugins:

```
~/.claude/plugins/
├── cache/
│   └── fleet-plugins/
│       ├── fleet-dev/1.5.0/      # Cached plugin files
│       └── fleet-core/1.2.0/
├── installed_plugins.json         # Tracks installed versions
├── known_marketplaces.json        # Marketplace sources
└── marketplaces/
    └── fleet-plugins/             # Symlink or copy of marketplace
```

**If updates don't apply**, delete the cache and reinstall:
```bash
rm -rf ~/.claude/plugins/cache/fleet-plugins
```
Then restart Claude Code - plugins will be reinstalled from source.

---

## Plugin Structure

```
fleet-plugins/
├── .claude-plugin/
│   └── marketplace.json        # Marketplace manifest
├── plugins/
│   ├── fleet-core/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json     # Plugin manifest (name, version)
│   │   └── skills/
│   │       ├── housekeeping/
│   │       │   └── SKILL.md
│   │       ├── debugging/
│   │       │   └── SKILL.md
│   │       ├── feedback/
│   │       │   └── SKILL.md
│   │       └── review-issues/
│   │           └── SKILL.md
│   └── fleet-dev/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   ├── setup/
│       │   │   ├── SKILL.md
│       │   │   └── references/   # Progressive disclosure
│       │   ├── obsidian/
│       │   ├── linting/
│       │   ├── dsgvo/
│       │   ├── deployment/
│       │   ├── wordpress/
│       │   ├── statusline/
│       │   └── research/
│       └── tools/
│           ├── obsidian-sync/
│           ├── linting-system/
│           ├── dsgvo-check/
│           └── timestamp-hook/
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

### fleet-core:review-issues

Reviews open issues from Fleet repositories:
- Checks fleet-plugins and claude-research for pending issues
- Categorizes by type (skill/workflow/pattern/context-request)
- Proposes changes and tracks via `Fixes #X` in commits

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
