---
name: linting
description: Linting system integration for code quality enforcement. Deploys proven configurations (Code Quality Score 10.00/10) for Python, JavaScript, and general projects. Use when setting up a new project, user asks about linting, or for production/public code quality.
---

# Linting Integration Skill

Version: 2.10
Timestamp: 2025-11-27 19:00 CET

## ⚠️ CRITICAL: Glob and Hidden Files

**Glob tool does NOT find files starting with `.`!**

- ❌ `configs/javascript/*` → `.eslintrc.js` NOT found
- ❌ `Glob pattern: *.js` → `.eslintrc.js` NOT found
- ✅ `ls -la configs/javascript/` → shows ALL files

**ALWAYS use Bash `ls -la` to verify config files exist!**

## Overview

This skill explains how to deploy the proven Linting System (Code Quality Score: 10.00/10) across different projects. **No setup script required** - configurations can be applied flexibly and intelligently.

## Available Configurations

**Source Location**: In fleet-dev plugin under `tools/linting-system/configs/`

After copying tools to your project, configs are at: `tools/linting-system/configs/`

### 1. Python Projects
**Path**: `tools/linting-system/configs/python/`

**Verify files exist:**
```bash
ls -la tools/linting-system/configs/python/
```

**Files**:
- `.editorconfig` - Editor settings
- `.flake8` - Style checking configuration
- `.pylintrc` - Comprehensive code analysis
- `pyproject.toml` - Tool configurations (black, isort, mypy)
- `.pre-commit-config.yaml` - Git hook configuration

**Linting Tools**: black, isort, flake8, mypy, pylint, docformatter

**Dependencies (pip install):**
```bash
pip install black isort flake8 mypy pylint docformatter pre-commit
```

### 2. JavaScript/TypeScript Projects
**Path**: `tools/linting-system/configs/javascript/`

**Verify files exist:**
```bash
ls -la tools/linting-system/configs/javascript/
```

**Files**:
- `.editorconfig` - Editor settings
- `.eslintrc.js` - ESLint configuration (Legacy format, ESLint 8)
- `.prettierrc` - Prettier configuration

**⚠️ ESLint Version Notice:**
- **ESLint 8** (Legacy): Uses `.eslintrc.js` - configs provided here
- **ESLint 9** (Modern): Uses `eslint.config.js` (Flat Config) - migration required

**ASK USER:** "Welche ESLint-Version? ESLint 8 (vorhandene Configs) oder ESLint 9 (Migration nötig)?"

**Dependencies for ESLint 8 (npm install):**
```bash
npm install -D eslint@8 @typescript-eslint/parser @typescript-eslint/eslint-plugin \
  eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y \
  eslint-plugin-import eslint-import-resolver-typescript \
  eslint-plugin-prettier eslint-config-prettier prettier
```

**Dependencies for ESLint 9 (if migrating):**
```bash
npm install -D eslint @eslint/js typescript-eslint \
  eslint-plugin-react eslint-plugin-react-hooks \
  eslint-plugin-prettier eslint-config-prettier prettier
```

### 3. General Projects
**Path**: `tools/linting-system/configs/general/`
**Files**:
- `.editorconfig` - Universal editor settings

## Integration Workflow

### Step 1: Identify Project Type
```markdown
- Python: requirements.txt, setup.py, main.py, src/ with .py files
- JavaScript: package.json, node_modules/, src/ with .js/.ts files
- General: Markdown, documentation, mixed files
```

### Step 2: Verify Source Files Exist (MANDATORY)

**⚠️ STOP: Do NOT skip this step!**

```bash
# ALWAYS verify before copying - Glob won't find these!
ls -la tools/linting-system/configs/python/
ls -la tools/linting-system/configs/javascript/
ls -la tools/linting-system/configs/general/
```

**If "No such file or directory":**
1. STOP - Tools not copied yet
2. Copy from fleet-dev plugin first (see setup skill)
3. Never create configs from scratch without permission

### Step 3: Copy Configuration Files
```bash
# Example for Python project
cp tools/linting-system/configs/python/.* . 2>/dev/null
cp tools/linting-system/configs/python/* . 2>/dev/null

# Example for JavaScript project
cp tools/linting-system/configs/javascript/.* . 2>/dev/null
cp tools/linting-system/configs/javascript/* . 2>/dev/null

# Example for General project
cp tools/linting-system/configs/general/.* . 2>/dev/null
```

**Note:** Two cp commands needed - one for hidden files (`.*`), one for regular files (`*`).

### Step 4: Copy Linting Script
```bash
# Create scripts directory if not present
mkdir -p scripts

# Copy linting script
cp tools/linting-system/scripts/lint.sh scripts/
chmod +x scripts/lint.sh
```

### Step 5: Pre-commit Hooks (Recommended)

#### Option A: Git Hook Installation (Recommended)
```bash
# Install pre-commit hook that blocks commits with linting issues
echo '#!/bin/bash
./scripts/lint.sh --shellcheck --bash-lint --files "scripts tools"
LINT_EXIT_CODE=$?

if [[ "$LINT_ALLOW_COMMIT" == "1" ]]; then
    echo "LINT_ALLOW_COMMIT=1 set - allowing commit despite linting issues"
    exit 0
else
    exit $LINT_EXIT_CODE
fi' > .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

**Usage**:
- **Normal commits**: Blocked if linting issues found (production-safe)
- **Emergency bypass**: `LINT_ALLOW_COMMIT=1 git commit -m "message"`

#### Option B: Pre-commit Framework (Alternative)
```bash
# Only if pre-commit framework is preferred
pre-commit install
```

**Note**: Git hooks provide more direct control and don't require additional dependencies.

### Step 6: VS Code Extensions (Recommended)

Install these extensions for real-time linting feedback:

```bash
# Install VS Code extensions (if using VS Code)
code --install-extension timonwong.shellcheck
code --install-extension foxundermoon.shell-format
code --install-extension davidanson.vscode-markdownlint
```

**Extensions provide**:
- **Real-time feedback**: Immediate error highlighting
- **Auto-formatting**: Format on save capabilities
- **Integrated linting**: No need to run scripts manually during development

### Step 7: Shellcheck Installation (For Bash Projects)

#### Windows (Git Bash)
```bash
# Direct download approach (no package manager required)
cd ~
mkdir -p bin
curl -L https://github.com/koalaman/shellcheck/releases/download/v0.10.0/shellcheck-v0.10.0.zip -o shellcheck.zip
unzip shellcheck.zip
cp shellcheck-v0.10.0/shellcheck.exe bin/
rm -rf shellcheck.zip shellcheck-v0.10.0/

# Add to PATH (add to ~/.bashrc for persistence)
export PATH="$HOME/bin:$PATH"
```

#### Linux/macOS
```bash
# Package manager installation
# Ubuntu/Debian
sudo apt-get install shellcheck

# macOS
brew install shellcheck
```

## Practical Application

### For New Projects
1. Identify project type
2. Copy corresponding configuration files
3. Install linting script
4. Ready to use immediately!

### For Existing Projects
1. Check existing linting configuration
2. Replace with proven configuration if needed
3. Add linting script
4. First linting run with `./scripts/lint.sh --all`

## Customizations

### Project-Specific Adjustments
- **Path adjustments**: Adapt paths in pyproject.toml or .flake8 to project structure
- **Add exclusions**: Exclude special folders or files
- **Tool versions**: Update tool versions in pyproject.toml if needed

### Common Adjustments
```toml
# pyproject.toml - Path adjustments
[tool.black]
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
  | your_specific_folder
)/
'''

# .flake8 - Additional exclusions
[flake8]
exclude =
    .git,
    __pycache__,
    .venv,
    your_specific_folder
```

## Advantages of This Method

### ✅ **Flexibility**
- No rigid scripts that fail in unexpected situations
- Can intelligently react to project specifics
- Easy adaptation to special requirements

### ✅ **Proven Quality**
- Configurations from project with 10.00/10 Code Quality Score
- All tools are coordinated
- Windows-optimized and tested

### ✅ **Easy Maintenance**
- Central configurations in fleet-dev plugin
- Updates can be easily transferred to all projects
- No duplication of configuration files

## Troubleshooting

### "No files found" / Empty directory
1. **NEVER assume directory is empty**
2. Verify with `ls -la [path]` (shows hidden files)
3. Glob tool limitation: does NOT find files starting with `.`
4. If really missing: ASK USER, do not improvise

### Config files not copying
```bash
# Hidden files need explicit pattern
cp "source/."* destination/  # Copies .eslintrc.js, .prettierrc, etc.
cp "source/"* destination/   # Copies regular files

# Or use:
cp -r source/. destination/  # Copies everything including hidden
```

### ESLint "Flat config" error
- **Symptom**: "ESLint couldn't find the config"
- **Cause**: ESLint 9 doesn't read `.eslintrc.js`
- **Fix**: Either downgrade to ESLint 8 OR migrate to `eslint.config.js`

### npm install fails
1. Check Node.js version: `node --version` (need ≥18)
2. Try with legacy peer deps: `npm install --legacy-peer-deps`
3. Clear cache: `npm cache clean --force`

### Python tool not found
```bash
pip install black isort flake8 mypy pylint docformatter
```

### Pre-commit errors
```bash
pip install pre-commit
pre-commit install
```

### Path problems
- Adapt paths in configuration files to project structure
- Check `.flake8` and `pyproject.toml` for hardcoded paths

### Obsidian-Sync Integration
Based on WhisperClient feedback:
```yaml
# .pre-commit-config.yaml - Correct configuration
-   repo: local
    hooks:
    -   id: obsidian-sync
        name: Sync Memory Bank to Obsidian
        entry: python tools/obsidian_sync.py
        language: system  # IMPORTANT: system, not python!
        files: ^memory-bank/
        pass_filenames: false
        always_run: false
```

## Memory Bank Integration

### Quality Tracking
```markdown
# activeContext.md - Example entry
## Recent Changes
- **Linting System**: Integrated with Code Quality Score 10.00/10
- **Tools**: black, isort, flake8, mypy, pylint configured
- **Pre-commit**: Automatic quality checks on commits
```

### Development Standards
```markdown
# systemPatterns.md - Example entry
## Code Quality Standards
- **Linting**: All commits must pass linting checks
- **Formatting**: Automatic formatting with black/prettier
- **Type Checking**: mypy for Python, TypeScript for JS projects
```

---

**Conclusion**: This method gives maximum flexibility when integrating the proven linting system, without the constraints of rigid setup scripts.
