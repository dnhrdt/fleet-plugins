---
name: setup
description: Complete project initialization and setup workflow. Creates Memory Bank, configures tools (Obsidian, Linting, DSGVO), initializes Git, and uses fleet-dev plugin tools. Use when starting a new project, user says "setup", "einrichten", "initialize", or when Memory Bank is missing/incomplete.
---

# Project Setup Skill

Version: 3.10
Timestamp: 2025-11-27 20:00 CET
<!-- ⚠️ ON EDIT: date "+%H:%M" → update timestamp, +0.01 minor | +0.10 significant | +1.00 major -->

---

## ⚠️ CRITICAL: Tool Sources

**All tools come from fleet-dev plugin.**

**Available tools (in plugin `tools/` directory):**
- `obsidian-sync/` - Git → Obsidian Vault sync
- `linting-system/` - Code quality configs (Python, JS, General)
- `dsgvo-check/` - Customer data protection

**After plugin installation, copy tools to project:**
```bash
# Verify what exists
ls -la tools/

# Copy from plugin or GitHub:
# Option 1: Clone from GitHub
git clone --depth 1 https://github.com/dnhrdt/fleet-plugins.git /tmp/fleet-plugins
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/obsidian-sync tools/
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/linting-system tools/
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/dsgvo-check tools/
rm -rf /tmp/fleet-plugins

# Option 2: Download specific tool via curl (if needed)
```

**NEVER improvise tools - always use tested versions from fleet-dev plugin!**

---

## Purpose

Complete project initialization workflow. Combines project bootstrapping and setup into one seamless process. Uses tools from fleet-dev plugin and configures the project.

## Auto-Activation Triggers

**MANDATORY activation when:**

1. **No Memory Bank exists**: `memory-bank/` directory missing or incomplete
2. **User keywords**: "setup", "einrichten", "initialize", "configure project", "complete setup"
3. **Tool configuration requested**: User asks about Obsidian, linting, or deployment without these being configured
4. **Fresh project**: No CLAUDE.md and no Memory Bank
5. **Pending initialization**: `.claude-init-pending` file exists

**⚠️ If ANY trigger matches → STOP → Load this skill → Follow workflow exactly**

**Note**: This skill should only run ONCE per project, then self-deactivates.

## Pre-Setup Detection

Before starting setup, check:

```
✓ Is this a fresh/empty project directory?
✓ Does .git/ exist? (Is it already a git repository?)
✓ Does memory-bank/ exist? (Partial setup?)
✓ Does CLAUDE.md exist? (Has project-specific rules?)
```

---

## Setup Workflow

### Phase 0: Detect Pending Initialization (0-5 seconds)

**Check for .claude-init-pending marker:**

```bash
if [ -f .claude-init-pending ]; then
  echo "🔄 Detected pending project initialization"
  echo "Loading project context..."

  # Load project info
  source .claude-init-pending
  # Variables now available:
  # - PROJECT_NAME
  # - PROJECT_TYPE
  # - PRIMARY_LANG
  # - REPO_VISIBILITY
  # - INIT_TIMESTAMP

  # Delete marker (setup is now in progress)
  rm .claude-init-pending

  # SKIP Phase 1 (already have project context)
  # CONTINUE with Phase 2
fi
```

**If .claude-init-pending found:**
- ✅ Load project context variables
- ✅ Delete marker file
- ✅ Skip Phase 1 (project questions)
- ✅ Continue with Phase 2

**If .claude-init-pending NOT found:**
- Continue with Phase 1 as normal (ask all questions)

---

### Phase 1: Project Context (1-2 minutes)

**⚠️ SKIP this phase if .claude-init-pending was found in Phase 0**

**Ask user these questions:**

1. **Project Name**: "What is the project name?" (lowercase, hyphens OK)
2. **Project Type**:
   - WordPress Plugin
   - Python Package/Script
   - Node.js Application
   - Bash/Shell Scripts
   - Internal tool / Script
   - Production application
   - Public library / Plugin
   - Client project
   - Other (specify)
3. **Primary Language/Stack**:
   - TypeScript/Node.js
   - Python
   - PHP/WordPress
   - Bash/Shell scripts
   - Other (specify)
4. **Project Goal**: "Briefly describe what this project does" (2-3 sentences)
5. **Repository Visibility**: Public or Private? (default: private)

**Store answers** for Memory Bank creation.

---

### Phase 2: DSGVO & Repository Configuration (1 minute)

**🚨 CRITICAL: Ask BEFORE any tool setup:**

```
Ask: "Will this repository be public or private?"

If PRIVATE (default):
- Auto-create .gitignore with memory-bank/ excluded
- Obsidian Sync is the Memory Bank backup system
- Customer data allowed in code/examples (will stay local)

If PUBLIC:
- Auto-create .gitignore with memory-bank/ excluded
- Enable customer data scan warnings
- Remind: Use ONLY generic examples (example.com, username, etc.)
- Memory Bank stays local, backed up to Obsidian only
- Offer to install DSGVO check (see dsgvo skill)
```

**Why Memory Bank is ALWAYS .gitignored:**
- Obsidian Sync provides backup (Git → Obsidian Vault)
- No risk of accidental publication
- Customer data stays private
- Cleaner Git history

**Exception (Memory Bank IN Git):**
Only for pure template/tool projects with NO customer data (example: claude-init itself)

---

### Phase 3: Tool Selection (1 minute)

**Obsidian Sync** (Recommended for all projects)
```
Ask: "Enable Obsidian sync?"
Default: Yes

If Yes:
- Load obsidian skill for setup instructions
- Will be configured in Phase 6
```

**Linting System** (For production/public projects)
```
Ask: "Enable linting system for code quality?"
Recommend: Yes if Production/Public, No if Internal/Script
Default: Based on project type

If Yes:
- Load linting skill for setup instructions
- Will be configured in Phase 6
```

**DSGVO Check** (For public repos)
```
Ask: "Enable DSGVO customer data check?"
Recommend: Yes if Public
Default: Based on repo visibility

If Yes:
- Load dsgvo skill for setup instructions
- Will be configured in Phase 6
```

**⚠️ CRITICAL PROCESS - NO EXCEPTIONS:**
1. Ask user about tool needs
2. If tool needed → Load respective skill
3. Follow skill instructions EXACTLY - don't improvise
4. Verify tool setup works before continuing

---

### Phase 4: .gitignore Creation (30 seconds)

**Create .gitignore file:**

```gitignore
# DSGVO: Internal documentation (may contain customer data)
memory-bank/

# Sensitive files
.env
.env.*
credentials.json
secrets.yml
customer-*.csv
customer-data/
production-logs/
real-examples/

# Tool-specific
node_modules/
__pycache__/
*.pyc
.vscode/settings.json
.idea/
```

**Add project-specific entries** based on project type from Phase 1:
- Python: `venv/`, `*.egg-info/`, `dist/`, `build/`
- Node.js: `node_modules/`, `dist/`, `build/`
- WordPress: `vendor/`, `node_modules/`

---

### Phase 5: Memory Bank Creation (2-3 minutes)

**Create directory:**
```bash
mkdir -p memory-bank
```

**Create three files:**

**activeContext.md:**
```markdown
# Active Context - [Project Name]

Version: 1.00
Timestamp: YYYY-MM-DD HH:MM CET

## Current Focus

[Project goal from Phase 1]

## Recent Changes

(None yet - project just initialized)

## Next Steps

1. [User's first task]
2. [User's second task]
3. Begin development

## Known Issues

(None yet)
```

**techContext.md:**
```markdown
# Technical Context - [Project Name]

Version: 1.00
Timestamp: YYYY-MM-DD HH:MM CET

## Tech Stack

- **Language**: [From Phase 1]
- **Framework**: [If applicable]
- **Tools**: [List tools enabled]

## Configuration

[Relevant config files]

## Development Setup

**Working Directory**: [Current path]
**Prerequisites**: [Based on project type]

## Integration

[Tools configured: Obsidian, Linting, DSGVO]
```

**systemPatterns.md:**
```markdown
# System Patterns - [Project Name]

Version: 1.00
Timestamp: YYYY-MM-DD HH:MM CET

## Development Standards

- Follow global CLAUDE.md rules
- Use Memory Bank for context persistence
- Update docs before commits

## Implementation Patterns

(To be developed as project progresses)

## Error Handling

- Use debugging skill for systematic investigation
- ONE CHANGE ONLY rule applies

## Lessons Learned

(To be captured during development)
```

---

### Phase 6: Tool Setup (if tools enabled)

**⚠️ STOP: Before loading any skill, verify tools directory exists:**
```bash
ls -la tools/
```

**If tools/ missing or empty → Copy from fleet-dev plugin first (see top of this skill)**

**For each enabled tool, load the respective skill:**

**Obsidian Integration (if enabled):**
1. Verify: `ls -la tools/obsidian-sync/` (copy from fleet-dev plugin if missing)
2. Load `obsidian` skill
3. Follow setup instructions exactly
4. Verify sync works

**Linting Setup (if enabled):**
1. Verify: `ls -la tools/linting-system/configs/` (must be copied first)
2. Load `linting` skill
3. Follow language-specific setup
4. Test linting works

**DSGVO Check (if enabled):**
1. Verify: `ls -la tools/dsgvo-check/` (copy from fleet-dev plugin if missing)
2. Load `dsgvo` skill
3. Install pre-commit hook
4. Test check works

---

### Phase 7: Project-Specific CLAUDE.md (Optional)

**If project needs specific rules beyond global CLAUDE.md:**

Create minimal project CLAUDE.md:

```markdown
# [Project Name] - Project Rules

Version: 1.00
Timestamp: YYYY-MM-DD HH:MM CET

## Project Context

[Brief description]

## Project-Specific Rules

[Only rules that DIFFER from or ADD TO global CLAUDE.md]

## Technical Constraints

[Project-specific constraints]
```

**NOTE:** Global `D:\dev\CLAUDE.md` applies to all projects. Only add project-specific CLAUDE.md if truly necessary.

---

### Phase 8: Git Repository Setup

**If .git/ exists:**
```bash
# Add setup files (NOTE: memory-bank/ is .gitignored, won't be added)
git add .gitignore .git-obsidian-sync.json
git commit -m "$(cat <<'EOF'
Initial project setup

- Created Memory Bank (3-file lean system)
- Configured .gitignore (DSGVO compliant)
- [Configured Obsidian sync]
- [Configured linting system]
- [Installed DSGVO check]

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**If .git/ missing:**
```bash
# Initialize repository
git init
git branch -M main
git add .
git commit -m "$(cat <<'EOF'
Initial project setup with Claude

- Project structure initialized
- Memory Bank created
- Tools configured

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**If Obsidian sync enabled:**
- Verify commit triggered sync
- Check Obsidian Vault for new project folder

---

### Phase 9: Verification & Completion

**Verify checklist:**
- [ ] .gitignore created with memory-bank/ excluded
- [ ] Memory Bank created with all 3 files (local only)
- [ ] All headers have Version + Timestamp
- [ ] Memory Bank content matches project context
- [ ] Git repository initialized (if needed)
- [ ] Initial commit completed (memory-bank/ NOT in git)
- [ ] Obsidian sync configured and tested (if enabled)
- [ ] Linting system ready (if enabled)
- [ ] DSGVO check installed (if enabled)

**Report to user:**
```
✅ Project setup complete!

Created:
- Memory Bank (activeContext.md, techContext.md, systemPatterns.md)
- [Obsidian sync → C:\Eigene Dateien\Obsidian Vault\...\PROJECT]
- [Linting system ready]
- [DSGVO check installed]

Next steps:
1. [User's first task from Phase 1]
2. [User's second task from Phase 1]

Setup skill will now deactivate. All future sessions start with Memory Bank context.
```

---

## Existing Project Integration

If integrating setup into existing project:

### Modified Workflow:

**Phase 1**: Ask about existing project
- Scan codebase for technologies
- Check existing documentation
- Identify current state

**Phase 2**: Same tool selection

**Phase 3**: Populate Memory Bank with existing project info
- Review package.json / requirements.txt / etc.
- Scan for existing patterns
- Include current development state

**Phase 4+**: Same as new project

---

## Troubleshooting Setup

### Memory Bank Creation Fails

**Problem**: Cannot create memory-bank/ directory

**Solution**:
- Check write permissions
- Verify current working directory
- Try manual creation: `mkdir memory-bank`

### Tool Setup Fails

**Problem**: Obsidian/Linting/DSGVO setup fails

**Solution**:
- Load the respective skill
- Follow troubleshooting section in that skill
- Verify prerequisites met

### Git Not Initialized

**Problem**: Not a git repository

**Solution**:
```bash
git init
git branch -M main
# Then continue with Phase 8
```

### User Unsure About Questions

**Problem**: User doesn't know answers in Phase 1

**Solution**:
- Use sensible defaults
- Can update Memory Bank later
- Project type: Default to "Internal tool"
- Stack: Scan project files to detect

---

## Best Practices

### Keep It Brief

- Don't over-question the user
- Use intelligent defaults
- Make reasonable assumptions
- Can always refine later

### Context Awareness

- Scan existing files for clues
- Check package.json, requirements.txt, etc.
- Look for README.md or existing docs
- Identify language by file extensions

### User Experience

- Clear progress indicators
- Explain what you're doing
- Show created files and paths
- Verify everything works before completion

---

## Integration with Main CLAUDE.md

After successful setup:
- Setup skill no longer auto-activates
- Memory Bank now primary context source
- Can still be manually loaded if needed: "Load setup skill"
- All future sessions start with Memory Bank context from Session Start Protocol

---

**Remember**: This skill runs ONCE per project. After successful setup, all future sessions start with Memory Bank context.
