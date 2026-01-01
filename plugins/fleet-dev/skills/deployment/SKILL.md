---
name: deployment
description: Deployment strategies, folder structures, and workflows for creating production-ready releases. Applies to WordPress plugins, Python packages, Node applications, and other software projects. Use when user says "deploy", "release", or needs to package a project for distribution.
---

# Deployment Skill - Best Practices & Workflow

Version: 1.01
Timestamp: 2025-10-03 11:45 CET
<!-- ⚠️ ON EDIT: date "+%H:%M" → update timestamp, +0.01 minor | +0.10 significant | +1.00 major -->

## Overview

This skill defines deployment strategies, folder structures, and workflows for creating production-ready releases. Applies to WordPress plugins, Python packages, Node applications, and other software projects.

## Philosophy

**Dual-Format Approach:**
- **Loose Files:** Current version in deployment/{project-name}/ for quick SSH/manual deployment
- **ZIP Archives:** Versioned {project-name}-v{version}.zip for clean installations and backup history

**Benefits:**
- Fast iteration: Copy loose files directly to server via SSH
- Clean installs: Use ZIP for first-time installation
- Version history: All previous releases archived as ZIPs
- Rollback capability: Previous versions always available

## Deployment Structure

### Universal Pattern

```
project-root/
├── deployment/
│   ├── {project-name}/           # Loose files, current version
│   │   ├── index.php             # Main entry point
│   │   ├── README.md
│   │   ├── LICENSE
│   │   └── ...                   # Production files only
│   ├── {project-name}-v1.0.0.zip
│   ├── {project-name}-v1.1.0.zip
│   └── {project-name}-v1.2.0.zip  # Latest ZIP
```

### Git Integration

**Add to .gitignore:**
```gitignore
# Deployment builds (optional - decide per project)
deployment/
```

**Consideration:** Some projects commit deployment/ for distribution, others exclude it and build on release. Choose based on:
- ✅ Commit: Small projects, simple releases, demo/distribution focus
- ❌ Exclude: Large projects, complex builds, CI/CD pipeline

## Best Practices

### What Belongs in Deployment

**✅ Include:**
- Production code (PHP, Python, JavaScript, etc.)
- Compiled assets (minified CSS/JS, compiled SCSS/TypeScript)
- README, LICENSE, CHANGELOG
- Language files (translations)
- Essential vendor dependencies (if needed at runtime)
- Database migration scripts (if applicable)

**❌ Exclude (via .distignore or similar):**
- Version control (.git/, .github/, .gitignore)
- Development dependencies (node_modules/dev, composer require-dev)
- Source files (SCSS, TypeScript, uncompiled assets)
- Tests and test data (/tests/, /test/, pytest/, phpunit.xml)
- CI/CD configuration (.travis.yml, .gitlab-ci.yml, github workflows)
- Editor configs (.vscode/, .idea/, .editorconfig)
- Linting configs (.eslintrc, .prettierrc, .phpcs.xml)
- Build tools (webpack.config.js, gulpfile.js, package.json for build-only projects)
- Documentation source (if compiled to different format)
- Development databases, logs, caches

**Common deployment violations:**
- ❌ Customer domain in demo URLs or examples
- ❌ Real email addresses in code comments
- ❌ Server paths with customer names (`/home/customer/`)
- ❌ Database connection strings with real credentials
- ❌ API keys or tokens in config examples
- ❌ Customer-specific configuration files

**For private/internal deployments:**
- Still check for credentials and API keys
- Verify .env files excluded
- Consider if deployment contains customer data

## Build Deployment

**Documentation** (IN THIS ORDER - IMMEDIATELY after implementation):
   - Update Memory Bank (activeContext.md with session results)
   - Update project docs (README.md version + features, CHANGELOG.md detailed entry)
   - Update architecture/design docs if applicable
**Version Bump**: Update version in main file (plugin header, package.json, setup.py, etc.)
**Deployment Prep**:
   - Clear deployment folder: `rm -rf deployment/{project-name}/*`
   - Copy production files: `cp -r {files} deployment/{project-name}/`
   - Create ZIP (CRITICAL - cd into deployment/ first!): `cd deployment && "/c/Program Files/7-Zip/7z.exe" a -tzip {project-name}-vX.X.X.zip {project-name}/`
   - **NEVER use PowerShell's `Compress-Archive`** - creates Windows path separators (backslashes) which Linux interprets as filename characters
   - **NOTE:** Simple `7z` command doesn't work in Git Bash - use full path `/c/Program Files/7-Zip/7z.exe` (quoted because of spaces)
**Commit**: ONLY after all above steps complete
**Request Testing**: Ask user to test the changes
