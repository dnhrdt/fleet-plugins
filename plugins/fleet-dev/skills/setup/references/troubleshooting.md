# Setup Troubleshooting

Solutions for common setup issues.

---

## Memory Bank Creation Fails

**Problem**: Cannot create memory-bank/ directory

**Solution**:
- Check write permissions
- Verify current working directory
- Try manual creation: `mkdir memory-bank`

---

## Tool Setup Fails

**Problem**: Obsidian/Linting/DSGVO setup fails

**Solution**:
- Load the respective skill
- Follow troubleshooting section in that skill
- Verify prerequisites met

---

## Git Not Initialized

**Problem**: Not a git repository

**Solution**:
```bash
git init
git branch -M main
# Then continue with Phase 6
```

---

## Hook Installation Fails

**Problem**: Cannot install git hooks

**Solution**:
- Verify `.git/` directory exists (Phase 5 must complete first)
- Check permissions on `.git/hooks/`
- Run `git init` if needed

---

## User Unsure About Questions

**Problem**: User doesn't know answers in Phase 1

**Solution**:
- Use sensible defaults
- Can update Memory Bank later
- Project type: Default to "Internal tool"
- Stack: Scan project files to detect

---

## Tools Directory Missing

**Problem**: `tools/` directory doesn't exist or is empty

**Solution**:
```bash
# Copy from fleet-dev plugin via GitHub
git clone --depth 1 https://github.com/dnhrdt/fleet-plugins.git /tmp/fleet-plugins
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/obsidian-sync tools/
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/linting-system tools/
cp -r /tmp/fleet-plugins/plugins/fleet-dev/tools/dsgvo-check tools/
rm -rf /tmp/fleet-plugins
```

---

## Timestamp Hook Not Working

**Problem**: No timestamp appears when editing Memory Bank files

**Solution**:
1. Check if hook is installed: `grep -q "memory-bank" ~/.claude/settings.local.json`
2. If not installed, run: `bash tools/timestamp-hook/install-timestamp-hook.sh`
3. Restart Claude Code session
4. Try editing a Memory Bank file again
