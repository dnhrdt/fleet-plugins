---
name: statusline
description: Install context-monitor statusline for Claude Code. Shows context usage, model, session metrics. Use when setting up a new workstation or when statusline is missing.
---

# Statusline Setup Skill

<!-- ⚠️ STOP: +0.01 minor | +0.10 significant | +1.00 major -->
Version: 1.00
<!-- ⚠️ STOP: Run `date "+%H:%M"` before changing! -->
Timestamp: 2026-01-02 01:07 CET

---

## What This Does

Installs a custom statusline for Claude Code that shows:
- 🧠 Context usage (percentage + visual bar)
- Model name (color-coded by context usage)
- 📁 Current directory
- 💰 Session cost
- ⏱️ Duration
- 📝 Lines changed

---

## Installation Steps

### Step 1: Create scripts directory

```bash
mkdir -p ~/.claude/scripts
```

### Step 2: Copy the script

**Source:** `tools/statusline/context-monitor.py` in fleet-dev plugin

```bash
# Find plugin location and copy
cp "$(dirname "$(dirname "$(pwd)")")/tools/statusline/context-monitor.py" ~/.claude/scripts/
```

**If that fails, copy manually from fleet-plugins repo:**
```bash
cp "D:/dev/Projects/fleet-plugins/plugins/fleet-dev/tools/statusline/context-monitor.py" ~/.claude/scripts/
```

### Step 3: Update global settings

**CRITICAL:** Use absolute path, NOT `~` (Python doesn't expand tilde)

Get your home path:
```bash
echo $HOME
```

Edit `~/.claude/settings.json`:
```json
{
  "statusLine": {
    "type": "command",
    "command": "python C:/Users/YOUR_USERNAME/.claude/scripts/context-monitor.py"
  }
}
```

**Replace `YOUR_USERNAME` with actual username from $HOME output.**

### Step 4: Verify

Restart Claude Code. You should see the statusline at the bottom.

---

## Troubleshooting

### Statusline not showing

1. Check script exists: `ls ~/.claude/scripts/context-monitor.py`
2. Check settings.json has statusLine configured
3. Verify path is ABSOLUTE (not using `~`)

### Error in statusline

- JSON parse error: Normal when running script manually (needs Claude Code input)
- Python not found: Ensure Python is in PATH

### Wrong context percentage

The script estimates based on 200k context window. Adjust in script if using different model.

---

## Script Location

After installation:
- Script: `~/.claude/scripts/context-monitor.py`
- Config: `~/.claude/settings.json`

---

*Part of fleet-dev plugin - Development Operations toolkit*
