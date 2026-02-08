#!/usr/bin/env node
/**
 * Fleet Deck Status Hook for fleet-dev plugin (v6)
 * Updates .fleet-deck-status.json in the project directory
 *
 * Usage: node fleet-deck-status.js [EventName]
 * Events: UserPromptSubmit, PostToolUse, Stop, Notification, PermissionRequest, SessionEnd
 *
 * CHANGELOG:
 * v6 (2026-02-08): PostToolUse only changes status if blocked → running (permission granted)
 *                   Fixes 7-8 sec latency (stdin blocking) and missing red for PermissionRequest
 * v5 (2026-02-05): Added event logging
 * v4 (2026-02-05): DESTROY STDIN immediately to fix Windows blocking
 * v3 (2026-02-05): No stdin at all - still blocked (Windows bug)
 * v2 (2026-02-05): Sync stdin read - blocked on Windows (fs.readSync hangs 7-8 sec)
 * v1 (2026-02-04): Async stdin listeners - blocked Claude input
 *
 * CRITICAL FIX (v4+): stdin must be destroyed IMMEDIATELY.
 * On Windows, fs.readSync(0,...) on stdin hangs for 7-8 seconds even with
 * "non-blocking" patterns. This blocks the entire hook and delays status updates.
 * Trade-off: We lose hookData fields (tool_name, session_id, etc.) but gain
 * reliable instant status updates. Project dir comes from CLAUDE_PROJECT_DIR env.
 */

// IMMEDIATELY destroy stdin to release the handle - BEFORE anything else
process.stdin.destroy();

const fs = require('fs');
const path = require('path');

// Get event from command line arg
const event = process.argv[2] || 'unknown';

// Get project directory from env (Claude Code sets this)
const projectDir = process.env.CLAUDE_PROJECT_DIR || process.cwd();
const statusFile = path.join(projectDir, '.fleet-deck-status.json');

// Determine instance name
const instanceName = getInstanceName(projectDir);

// Read existing status or create new
let status = readExistingStatus(statusFile);
const previousStatus = status.status || 'none';

// Update based on event
switch (event) {
  case 'SessionStart':
  case 'UserPromptSubmit':
    // UserPromptSubmit: User sent a prompt → session is active
    // NOTE: SessionStart is BROKEN on Windows (Issue #9542) - use UserPromptSubmit instead
    status.status = 'running';
    status.needs_attention = false;
    status.attention_reason = null;
    status.last_activity = new Date().toISOString();
    // Initialize if new session
    if (!status.instance) status.instance = instanceName;
    if (!status.project) status.project = projectDir;
    if (status.context_percent === undefined) status.context_percent = 0;
    break;

  case 'SessionEnd':
    status.status = 'stopped';
    status.last_activity = new Date().toISOString();
    status.needs_attention = false;
    break;

  case 'PostToolUse':
    // Only change status if currently blocked (= permission was just granted)
    // This avoids thousands of unnecessary status writes per session
    // (PostToolUse fires 3x more than UserPromptSubmit - ~43/session avg)
    if (previousStatus === 'blocked') {
      status.status = 'running';
      status.needs_attention = false;
      status.error = null;
    }
    // Always update activity timestamp
    status.last_activity = new Date().toISOString();
    break;

  case 'Notification':
  case 'PermissionRequest':
    // URGENT: Claude is blocked, needs permission/input to continue
    status.status = 'blocked';
    status.needs_attention = true;
    status.attention_reason = 'Permission or input required';
    status.last_activity = new Date().toISOString();
    break;

  case 'Stop':
    status.status = 'waiting';
    status.needs_attention = true;
    status.attention_reason = 'Task completed or waiting';
    status.last_activity = new Date().toISOString();
    break;

  default:
    status.last_activity = new Date().toISOString();
}

// Ensure instance name is set
status.instance = status.instance || instanceName;
status.project = status.project || projectDir;

// Write status file
try {
  fs.writeFileSync(statusFile, JSON.stringify(status, null, 2));
} catch (err) {
  // Silent fail
}

// Output empty JSON (hook success) and exit immediately
console.log('{}');

// === Helper Functions ===

function getInstanceName(projectDir) {
  const configFile = path.join(projectDir, '.fleet-deck.json');
  if (fs.existsSync(configFile)) {
    try {
      const config = JSON.parse(fs.readFileSync(configFile, 'utf8'));
      if (config.instance) return config.instance;
    } catch (e) {
      // Fall through
    }
  }
  return path.basename(projectDir);
}

function readExistingStatus(statusFile) {
  if (fs.existsSync(statusFile)) {
    try {
      return JSON.parse(fs.readFileSync(statusFile, 'utf8'));
    } catch (e) {
      // Corrupt file
    }
  }
  return {};
}
