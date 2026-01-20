# Setup Phases - Detailed Instructions

This document contains the detailed step-by-step instructions for each setup phase.

---

## Phase 0: Detect Pending Initialization (0-5 seconds)

**Check for .claude-init-pending marker:**

```bash
if [ -f .claude-init-pending ]; then
  echo "Detected pending project initialization"
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
- Load project context variables
- Delete marker file
- Skip Phase 1 (project questions)
- Continue with Phase 2

**If .claude-init-pending NOT found:**
- Continue with Phase 0.5, then Phase 1 as normal

---

## Phase 0.5: Global Workstation Setup (Once per workstation)

**Check and install timestamp hook (GLOBAL - not project-specific):**

```bash
# Check if timestamp hook is already installed
if grep -q "memory-bank" ~/.claude/settings.local.json 2>/dev/null; then
    echo "Timestamp hook already installed"
else
    echo "Installing timestamp hook for Memory Bank edits..."
    # Run installer from fleet-dev plugin
    bash tools/timestamp-hook/install-timestamp-hook.sh
fi
```

**What the hook does:**
- Displays current time before Edit/Write on `**/memory-bank/**` files
- Prevents guessing timestamps in version headers
- Installed ONCE per workstation, applies to ALL projects

**If tools/timestamp-hook/ missing:**
```bash
# Copy from fleet-dev plugin
git clone --depth 1 https://github.com/dnhrdt/fleet-plugins.git /tmp/fleet-plugins
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/timestamp-hook tools/
bash tools/timestamp-hook/install-timestamp-hook.sh
rm -rf /tmp/fleet-plugins
```

**Verification:**
- Edit any Memory Bank file
- Timestamp output should appear before the edit
- Example: `21:45 CET`

---

## Phase 1: Project Context (1-2 minutes)

**SKIP this phase if .claude-init-pending was found in Phase 0**

**First, determine project origin:**

```
Ask: "Is this a new project or a fork/clone of an existing repository?"

If NEW PROJECT:
- Continue with questions below
- Full tool configuration in Phase 3

If FORK/CLONE:
- Clone/fork the repository FIRST
- Analyze existing configs (package.json, pyproject.toml, etc.)
- Skip linting questions - analyze what's already there
- Only offer to EXTEND existing tooling, not replace
```

**For new projects, ask user these questions:**

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

## Phase 2: DSGVO & Repository Configuration (1 minute)

**CRITICAL: Ask BEFORE any tool setup:**

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

## Phase 3: Tool Selection (1 minute)

**Obsidian Sync** (Recommended for all projects)
```
Ask: "Enable Obsidian sync?"
Default: Yes

If Yes:
- Load obsidian skill for setup instructions
- Will be configured in Phase 7
```

**Linting System** (For production/public projects)
```
Ask: "Enable linting system for code quality?"
Recommend: Yes if Production/Public, No if Internal/Script
Default: Based on project type

If Yes:
- Load linting skill for setup instructions
- Will be configured in Phase 7
```

**DSGVO Check** (For public repos)
```
Ask: "Enable DSGVO customer data check?"
Recommend: Yes if Public
Default: Based on repo visibility

If Yes:
- Load dsgvo skill for setup instructions
- Will be configured in Phase 7
```

**CRITICAL PROCESS - NO EXCEPTIONS:**
1. Ask user about tool needs
2. If tool needed → Load respective skill
3. Follow skill instructions EXACTLY - don't improvise
4. Verify tool setup works before continuing

---

## Phase 4: .gitignore Creation (30 seconds)

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

## Phase 5: Git Repository Setup

**CRITICAL: Git must be initialized BEFORE tool setup (hooks need .git/ directory)**

**If .git/ already exists:**
- Skip initialization
- Continue with Phase 6

**If .git/ missing:**
```bash
# Initialize repository
git init
git branch -M main

# Add initial files
git add .gitignore
git commit -m "$(cat <<'EOF'
Initial project structure

- Created .gitignore (DSGVO compliant)

Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Why Git init comes before tools:**
- Obsidian sync requires `.git/hooks/` directory for post-commit hook
- DSGVO check uses pre-commit hooks
- All hook-based tools need `.git/` to exist first

---

## Phase 6: Memory Bank Creation (2-3 minutes)

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

## Phase 7: Tool Setup (if tools enabled)

**STOP: Before loading any skill, verify tools directory exists:**
```bash
ls -la tools/
```

**If tools/ missing or empty → Copy from fleet-dev plugin first (see Tool Sources section)**

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

## Phase 8: Project-Specific CLAUDE.md (Optional)

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

## Phase 9: Final Commit & Verification

**Commit all setup files:**
```bash
git add .gitignore .git-obsidian-sync.json CLAUDE.md
git commit -m "$(cat <<'EOF'
Complete project setup

- Created Memory Bank (3-file lean system)
- Configured .gitignore (DSGVO compliant)
- [Configured Obsidian sync]
- [Configured linting system]
- [Installed DSGVO check]

Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**If Obsidian sync enabled:**
- Verify commit triggered sync
- Check Obsidian Vault for new project folder

**Verify checklist:**
- [ ] .gitignore created with memory-bank/ excluded
- [ ] Git repository initialized
- [ ] Memory Bank created with all 3 files (local only)
- [ ] All headers have Version + Timestamp
- [ ] Memory Bank content matches project context
- [ ] Initial commit completed (memory-bank/ NOT in git)
- [ ] Obsidian sync configured and tested (if enabled)
- [ ] Linting system ready (if enabled)
- [ ] DSGVO check installed (if enabled)

**Report to user:**
```
Project setup complete!

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
