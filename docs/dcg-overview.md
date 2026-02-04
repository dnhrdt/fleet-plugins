# DCG (Destructive Command Guard) - Overview

Version: 1.00
Timestamp: 2026-02-01 21:00 CET

## What is DCG?

High-performance Rust hook for Claude Code that blocks dangerous Bash commands before execution.
- SIMD-accelerated, sub-millisecond latency
- 49+ security packs (git, rm, databases, K8s, AWS, Docker...)
- Custom YAML packs for organization-specific policies
- Fail-open philosophy (errors → allow, never block workflow)

**Source:** https://github.com/Dicklesworthstone/destructive_command_guard
**Version:** v0.2.15 (2026-01-20)

---

## Quick Reference

### Installation (Windows)

```powershell
# Download from GitHub Releases
gh release download v0.2.15 --repo Dicklesworthstone/destructive_command_guard --pattern "dcg-x86_64-pc-windows-msvc.zip"
```

### Claude Code Hook Configuration

`~/.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "dcg"
      }]
    }]
  }
}
```

### Essential CLI Commands

| Command | Purpose |
|---------|---------|
| `dcg test "command"` | Test if command would be blocked |
| `dcg explain "command"` | Detailed trace of why blocked/allowed |
| `dcg allow-once <code>` | Temporary 24h exception |
| `dcg allowlist add <rule> --project` | Permanent allowlist entry |
| `dcg packs` | List enabled packs |
| `dcg packs --verbose` | All packs with pattern counts |
| `dcg pack validate file.yaml` | Validate custom pack |
| `dcg scan --staged` | Scan staged files for destructive patterns |
| `dcg --version` | Version and build info |

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `DCG_PACKS="pack1,pack2"` | Enable packs |
| `DCG_DISABLE="pack"` | Disable packs |
| `DCG_BYPASS=1` | Emergency bypass (use sparingly!) |
| `DCG_VERBOSE=1` | Verbose output |
| `DCG_ROBOT=1` | Machine-friendly JSON output |

---

## Custom Packs (YAML)

Location: `~/.config/dcg/packs/*.yaml`

```yaml
schema_version: 1
id: fleet.github              # namespace.name format
name: Fleet GitHub Policies
version: 1.0.0
description: |
  Block direct gh issue commands - use Fleet skills instead.

keywords:                     # Performance gating - only check if keyword present
  - gh

destructive_patterns:
  - name: gh-issue-direct
    pattern: \bgh\s+issue\b   # fancy-regex syntax
    severity: high            # critical/high/medium/low
    description: "Use Fleet skills instead"
    explanation: |
      Use /fleet-core:review-issues or /fleet-dev:research

safe_patterns:
  - name: gh-issue-view
    pattern: \bgh\s+issue\s+view\b
    description: "Viewing is allowed"
```

---

## Architecture

### Hook Protocol (PreToolUse)

**Input (stdin):**
```json
{"tool_name":"Bash","tool_input":{"command":"git reset --hard"}}
```

**Output - DENY (stdout):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "...",
    "ruleId": "core.git:reset-hard",
    "packId": "core.git"
  }
}
```

**Output - ALLOW:** Empty (no output)

### 3-Tier Heredoc Detection

```
Command → Tier 0: Quick Reject (<10μs)
        → Tier 1: Trigger Detection (<100μs)
        → Tier 2: Content Extraction (<1ms)
        → Tier 3: AST Pattern Match (<5ms)
```

### Agent Detection

DCG detects Claude Code via `CLAUDE_CODE=1` or `CLAUDE_SESSION_ID` env vars.
Trust levels: high/medium/low (configurable per agent).

---

## What DCG Does NOT Support

- Other tools (Edit, Read, Write, Glob, Grep) - only Bash
- PostToolUse hooks
- Prompt-based hooks

For these, use custom Claude Code hooks.

---

## Documentation Index

Full documentation: `docs/dicklesworthstone-destructive_command_guard.txt` (531KB)

### Core Documents

| Document | Location | Content |
|----------|----------|---------|
| README | `research/destructive_command_guard/README.md` | Main docs, installation, usage |
| AGENTS.md | `research/destructive_command_guard/AGENTS.md` | AI agent guidelines, hook protocol |
| SKILL.md | `research/destructive_command_guard/SKILL.md` | Claude Code skill format |

### Configuration & Security

| Document | Location | Content |
|----------|----------|---------|
| configuration.md | `research/.../docs/configuration.md` | Config hierarchy, packs, allowlists |
| security.md | `research/.../docs/security.md` | Heredoc threat model |
| security-model.md | `research/.../docs/security-model.md` | Interactive mode, verification codes |
| agents.md | `research/.../docs/agents.md` | Agent profiles, trust levels, robot mode |

### Pattern Development

| Document | Location | Content |
|----------|----------|---------|
| custom-packs.md | `research/.../docs/custom-packs.md` | YAML pack authoring guide |
| pack.schema.yaml | `research/.../docs/pack.schema.yaml` | JSON Schema for packs |
| patterns.md | `research/.../docs/patterns.md` | Heredoc pattern inventory |
| adr-001-heredoc-scanning.md | `research/.../docs/adr-001-heredoc-scanning.md` | 3-tier architecture |

### Operations

| Document | Location | Content |
|----------|----------|---------|
| allow-once-usage.md | `research/.../docs/allow-once-usage.md` | Temporary exceptions |
| troubleshooting.md | `research/.../docs/troubleshooting.md` | Debug guide |
| scan-precommit-guide.md | `research/.../docs/scan-precommit-guide.md` | CI/pre-commit integration |

### Pack Reference

| Document | Location | Content |
|----------|----------|---------|
| packs/README.md | `research/.../docs/packs/README.md` | Pack index (49+ packs) |
| packs/core.md | `research/.../docs/packs/core.md` | core.git + core.filesystem |

---

## Fleet Use Cases

| Use Case | Solution |
|----------|----------|
| npm/npx block (Git Bash issue) | Custom pack or allowlist for `cmd //c` |
| gh issue block | Custom pack `fleet.github` |
| Memory Bank edit reminder | Keep own PostToolUse hook (DCG doesn't support) |

---

## Next Steps

1. Install DCG on Windows
2. Create `fleet.yaml` custom pack
3. Test with our use cases
4. Document integration in systemPatterns.md
