# DSGVO Customer Data Check - Integration Guide

Version: 1.5.0

---

## Purpose

Automatic detection of customer data in Git commits to prevent DSGVO violations and accidental data leaks in public repositories.

## What It Checks

The DSGVO check scans staged files for:

1. **Customer domains** (configurable)
2. **Customer names** (configurable)
3. **Real email addresses** (excludes example.com, test.com, etc.)
4. **Specific user paths** (excludes /home/username/)
5. **Memory Bank files** (should be .gitignored)

## Installation

### Option 1: As Pre-Commit Hook (Recommended for Public Repos)

```bash
# From project root
bash tools/dsgvo-check/install-pre-commit-hook.sh
```

**When to use:**
- Projects that will be published publicly
- Projects with risk of customer data exposure
- Team projects where multiple people commit

**Effect:**
- Runs automatically before EVERY commit
- Blocks commit if customer data detected
- Can be bypassed with `git commit --no-verify` (not recommended)

### Option 2: Manual Check Before Push

```bash
# Stage your changes
git add .

# Run check manually
bash tools/dsgvo-check/check-customer-data.sh

# If clean, commit
git commit -m "Your message"
```

**When to use:**
- Private repos where you want occasional checks
- Before pushing to GitHub/GitLab
- One-time check before making repo public

## Configuration (Optional)

### Custom Customer Patterns

1. **Copy example config:**
   ```bash
   cp tools/dsgvo-check/.dsgvo-check.conf.example .dsgvo-check.conf
   ```

2. **Edit `.dsgvo-check.conf`:**
   ```bash
   # Add your customer domains (pipe-separated regex)
   CUSTOMER_DOMAINS="customerdomain\.com|clientsite\.de|acmecorp\.net"

   # Add customer names
   CUSTOMER_NAMES="ACME Corp|Customer Inc|ClientName GmbH"
   ```

3. **Add to .gitignore:**
   ```gitignore
   # Keep customer list private
   .dsgvo-check.conf
   ```

### Built-in Checks (No Configuration Needed)

Even without configuration, the script checks for:
- Real email addresses (non-example domains)
- Specific user paths (like `/home/john/`)
- Memory Bank files

## What Gets Flagged

### ❌ BLOCKED Examples

```bash
# Customer domains
example@customerdomain.com
https://acmecorp.net/api

# Real email addresses
john.doe@gmail.com
support@realclient.com

# Specific paths
/home/michael/projects/
/home/projectx/var/mail/

# Memory Bank
memory-bank/activeContext.md
```

### ✅ ALLOWED Examples

```bash
# Generic examples
example@example.com
user@test.com
admin@domain.com

# Generic paths
/home/username/projects/
~/projects/
/var/www/html/

# Generic names
account1, account2, account3
username, user, admin
```

## Integration with Setup Module

The setup module (`.claude/modules/setup.md`) automatically:

1. **Phase 2:** Asks if repo is public/private
2. **Phase 4:** Creates .gitignore with memory-bank/ excluded
3. **Phase 3:** Offers to install DSGVO check for public repos

**Manual integration:**
```bash
# During project setup
Will this repository be public or private? [public/private]: public

# Setup will offer:
Install DSGVO pre-commit hook? [Y/n]: Y
```

## Workflow Integration

### Before Making Repo Public

```bash
# 1. Run full check on entire repo
git add .
bash tools/dsgvo-check/check-customer-data.sh

# 2. If violations found, anonymize data
# Replace with example.com, username, etc.

# 3. Re-run check
git add .
bash tools/dsgvo-check/check-customer-data.sh

# 4. When clean, commit and push
git commit -m "Prepare for public release"
git push
```

### Daily Development (Hook Installed)

```bash
# Normal workflow - hook runs automatically
git add .
git commit -m "Add feature"

# If hook blocks commit:
# 1. Review flagged content
# 2. Replace customer data
# 3. git add again
# 4. git commit again
```

## Uninstalling

### Remove Pre-Commit Hook

```bash
# Simple removal
rm .git/hooks/pre-commit

# Restore backup if exists
mv .git/hooks/pre-commit.backup .git/hooks/pre-commit
```

### Remove Tool Completely

```bash
rm -rf tools/dsgvo-check/
```

## Troubleshooting

### Hook Not Running

**Problem:** Commits succeed without check running

**Solution:**
```bash
# Verify hook exists and is executable
ls -la .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Test hook manually
bash .git/hooks/pre-commit
```

### False Positives

**Problem:** Generic examples flagged as violations

**Solution:**
- Ensure using standard generic domains (example.com, test.com, domain.com)
- Check .dsgvo-check.conf for overly broad patterns
- Use `--no-verify` ONLY if absolutely certain content is safe

### Hook Blocks Valid Commit

**Problem:** Need to commit despite warnings (rare)

**Solution:**
```bash
# ONLY if you're certain content is safe
git commit --no-verify -m "Your message"

# Better: Fix the flagged content instead
```

## Best Practices

### 1. Install Early

Install DSGVO check BEFORE first commit to public repo, not after.

### 2. Configure for Your Clients

Add all customer domains to `.dsgvo-check.conf` for comprehensive protection.

### 3. Team Awareness

Ensure all team members understand:
- Why hook exists
- What gets blocked
- How to fix violations

### 4. Memory Bank Always Private

NEVER disable Memory Bank protection. It's .gitignored for a reason.

### 5. Review Before Public

Before `git push` to public repo:
```bash
# Manual final check
bash tools/dsgvo-check/check-customer-data.sh
```

## Incident Recovery

If customer data was already committed and pushed:

### Private Repo → Public Repo

**DO NOT just make repo public!**

1. Run DSGVO check on all files
2. Anonymize ALL violations
3. Create new clean commit
4. Only then make public

### Already Public (Emergency)

See `DSGVO-INCIDENT-REPORT.md` for recovery procedure:

1. Force-push clean history (Git history rewrite)
2. Notify affected customers (if required by DSGVO)
3. Document incident
4. Install DSGVO check to prevent recurrence

## Reference

**Related Files:**
- Main guidelines: `CLAUDE.md` (DSGVO & Data Privacy section)
- Setup workflow: `.claude/modules/setup.md` (Phase 2: DSGVO Configuration)
- Incident report: `DSGVO-INCIDENT-REPORT.md` (Lessons learned)

**Scripts:**
- `tools/dsgvo-check/check-customer-data.sh` - Main check script
- `tools/dsgvo-check/install-pre-commit-hook.sh` - Hook installer
- `tools/dsgvo-check/.dsgvo-check.conf.example` - Config template

---

**Created:** 2025-10-03
**Last Updated:** 2025-10-03
**Status:** Production Ready
