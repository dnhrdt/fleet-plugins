# fleet-core

Core utilities for all Fleet instances.

**Version:** 1.0.0

## Skills

| Skill | Description |
|-------|-------------|
| `housekeeping` | Memory Bank cleanup and optimization |
| `debugging` | Systematic debugging methodology (STOP protocol) |
| `feedback` | Create structured feedback issues on GitHub |

## Installation

```bash
claude plugin install fleet-core
```

## Usage

```bash
# Memory Bank cleanup
/fleet-core:housekeeping

# Start debugging session
/fleet-core:debugging

# Submit project feedback
/fleet-core:feedback
```

## When to Use

- **housekeeping**: At end of major project phases, when Memory Bank grows too large
- **debugging**: When encountering bugs, before making code changes
- **feedback**: At project milestones, after rule violations, when patterns discovered

## Notes

- Housekeeping only on explicit request (never automatic)
- Feedback creates GitHub Issues in fleet-plugins repo
- All skills follow Fleet development standards
