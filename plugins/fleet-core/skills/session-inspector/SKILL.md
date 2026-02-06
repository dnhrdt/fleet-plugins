---
name: session-inspector
description: >-
  This skill should be used when the user says "check sessions", "search sessions",
  "we had this before", "session analysis", "permission issues", "what happened last session",
  "DCG blocks", "auto-approve candidates", or when debugging permission/hook problems.
  Analyzes Claude Code session JSONL files for tool usage, permissions, errors, and DCG decisions.
triggers:
  - user mentions past sessions or "we had this before"
  - debugging permission requests or DCG blocks
  - looking for auto-approve candidates
  - reviewing what happened in a session
  - user says "session inspector" or "inspect session"
---

# Session Inspector

Analyze Claude Code sessions for hook development, permission debugging, and DCG tuning.

## Tool Location

```
${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py
```

Requires: Python 3.10+, no external dependencies.

## Commands

### Quick Overview

```bash
# Current session summary
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" summary -c

# Last session in specific project
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" summary -p fleet-plugins -c
```

### Permission Analysis

Find DCG blocks, user rejections, and auto-approve candidates.

```bash
# Current session
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" permissions -c

# Across last 10 sessions (all projects)
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" permissions -r 10

# Specific project, brief output
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" permissions -p fleet-plugins -r 5 -b
```

Output sections: DCG BLOCKED, USER REJECTED, AUTO-APPROVE CANDIDATES, ALL TOOL CALLS.

### Error Investigation

Only errors, rejections, and DCG blocks.

```bash
# Current session errors
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" errors -c

# Last 20 errors across project
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" errors -p fleet-plugins -r 10 -n 20
```

### Timeline

Chronological event stream with filtering.

```bash
# Full timeline
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" timeline -c

# Filter for DCG events
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" timeline -c -f dcg

# Filter for specific tool
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" timeline -c -f Bash

# Last 10 events only
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" timeline -c -n 10
```

### Tool Usage Stats

```bash
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" tools -c
```

## Common Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--current` | `-c` | Most recent session |
| `--recent N` | `-r N` | Analyze N most recent sessions |
| `--project NAME` | `-p NAME` | Filter by project name (substring) |
| `--session UUID` | `-s UUID` | Specific session (prefix match) |
| `--last N` | `-n N` | Limit output entries |
| `--json` | | JSON output for programmatic use |
| `--brief` | `-b` | Highlights only |

## Typical Workflows

### "We had this problem before"

Search recent sessions across projects for similar errors:

```bash
# Check errors across last 20 sessions
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" errors -r 20

# Check specific project
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" errors -p maison -r 10
```

### "Why is DCG blocking this?"

```bash
# See DCG blocks in current session
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" errors -c

# Timeline filtered for DCG
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" timeline -c -f dcg
```

### "Which tools can we auto-approve?"

```bash
# Permission analysis across many sessions
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" permissions -r 20
```

Look for AUTO-APPROVE CANDIDATES section: 100% success rate, 3+ calls.

### "What happened in the last session?"

```bash
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" summary -c
python "${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py" timeline -c -n 20
```

## Result Classification

Tool results are classified into 4 categories:

| Class | Indicator |
|-------|-----------|
| `success` | Dict result (file content, command output) |
| `dcg_blocked` | String: `"Error: BLOCKED by dcg..."` |
| `user_rejected` | String: `"User rejected tool use"` |
| `error` | String: `"Error: Exit code N..."`, file not found, etc. |

Only string-type results indicate errors. Dict results are always success.

## Windows Note

Run via `cmd //c` if Python is not in Git Bash PATH:

```bash
cmd //c "python \"${CLAUDE_PLUGIN_ROOT}/tools/session-inspector/session_inspector.py\" summary -c"
```
