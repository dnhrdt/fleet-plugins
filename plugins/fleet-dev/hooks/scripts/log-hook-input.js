#!/usr/bin/env node
/**
 * log-hook-input.js
 * Logs all PreToolUse hook inputs for debugging
 * Runs parallel to other hooks, always allows
 */

const fs = require('fs');
const path = require('path');

const LOG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.claude', 'logs');
const getLogFile = () => {
  const date = new Date().toISOString().split('T')[0];
  return path.join(LOG_DIR, `hook-debug-${date}.log`);
};

const log = (data) => {
  try {
    if (!fs.existsSync(LOG_DIR)) {
      fs.mkdirSync(LOG_DIR, { recursive: true });
    }
    const timestamp = new Date().toISOString();
    const entry = JSON.stringify({ timestamp, ...data }) + '\n';
    fs.appendFileSync(getLogFile(), entry);
  } catch (e) {
    // Silent fail
  }
};

let inputData = '';

process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
  try {
    const input = JSON.parse(inputData);

    log({
      event: 'PreToolUse',
      tool_name: input.tool_name,
      command: input.tool_input?.command?.substring(0, 500),
      session_id: input.session_id,
      hook: 'log-hook-input'
    });

    // Always allow - this is just for logging
    console.log(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "allow"
      }
    }));
    process.exit(0);
  } catch (err) {
    log({ event: 'error', error: err.message, raw: inputData.substring(0, 200) });
    console.log(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "allow"
      }
    }));
    process.exit(0);
  }
});
