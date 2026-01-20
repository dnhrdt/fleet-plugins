# Fork/Clone and Existing Project Workflows

Instructions for setting up projects that aren't completely new.

---

## Fork/Clone Project Workflow

**When user indicates fork/clone:**

### 1. Clone First

```bash
git clone <repository-url>
cd <project-name>
```

### 2. Analyze Existing Setup

- Check for existing linting configs (.eslintrc, pyproject.toml, etc.)
- Check for existing CI/CD (.github/workflows/)
- Check for existing documentation

### 3. Extend, Don't Replace

- If linting exists → Only offer improvements
- If CI exists → Integrate with existing
- Add Memory Bank alongside existing docs

### 4. Continue with Phase 4+

- .gitignore: MERGE with existing (don't overwrite)
- Git: Already initialized (skip Phase 5)
- Tools: Only add what's missing

---

## Existing Project Integration

If integrating setup into existing project:

### Modified Workflow

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

## Best Practices for Integration

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

## Merging .gitignore

When project already has .gitignore:

```bash
# Check existing content
cat .gitignore

# Add Memory Bank exclusion if missing
if ! grep -q "memory-bank" .gitignore; then
    echo "" >> .gitignore
    echo "# DSGVO: Internal documentation" >> .gitignore
    echo "memory-bank/" >> .gitignore
fi
```

**Never overwrite** existing .gitignore entries - only add what's missing.
