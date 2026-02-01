#!/usr/bin/env node
/**
 * research-skill-reminder.js
 * Reminds to use Fleet skills instead of direct gh issue commands
 *
 * Skill Mapping:
 * - gh issue list/view → /fleet-core:review-issues
 * - gh issue create (claude-research) → /fleet-dev:research
 * - gh issue create (other) → /fleet-core:feedback
 */

const fs = require('fs');
const path = require('path');

// Logging setup - rotating daily logs
const LOG_DIR = path.join(process.env.USERPROFILE || process.env.HOME, '.claude', 'logs');
const getLogFile = () => {
  const date = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
  return path.join(LOG_DIR, `hook-research-${date}.log`);
};

const log = (level, message, data = {}) => {
  try {
    if (!fs.existsSync(LOG_DIR)) {
      fs.mkdirSync(LOG_DIR, { recursive: true });
    }
    const timestamp = new Date().toISOString();
    const entry = JSON.stringify({ timestamp, level, message, ...data }) + '\n';
    fs.appendFileSync(getLogFile(), entry);
  } catch (e) {
    // Logging should never break the hook
  }
};

let inputData = '';

process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
  try {
    const input = JSON.parse(inputData);
    const command = input.tool_input?.command || '';

    log('debug', 'Hook triggered', { command: command.substring(0, 200) });

    // Check if command contains gh and issue
    const isGhIssue = /\bgh\b.*\bissue\b/i.test(command);

    if (isGhIssue) {
      const isClaudeResearch = /claude-research/i.test(command);
      const isListOrView = /\bissue\s+(list|view)\b/i.test(command);
      const isCreate = /\bissue\s+create\b/i.test(command);

      let skill, message;

      if (isListOrView) {
        skill = '/fleet-core:review-issues';
        message = `STOP: Use ${skill} skill for reviewing issues. Direct gh commands bypass the structured workflow.`;
      } else if (isCreate && isClaudeResearch) {
        skill = '/fleet-dev:research';
        message = `STOP: Use ${skill} skill for research requests to claude-research. The skill ensures proper formatting and Source-Repo tracking.`;
      } else if (isCreate) {
        skill = '/fleet-core:feedback';
        message = `STOP: Use ${skill} skill for structured issue creation. Direct gh commands bypass the templated workflow.`;
      } else {
        skill = '/fleet-core:review-issues';
        message = `STOP: Consider using Fleet skills for GitHub issues. ${skill} for reviewing, /fleet-core:feedback for creating.`;
      }

      log('info', 'gh issue detected', { command: command.substring(0, 100), skill, decision: 'ask' });

      const response = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "ask"
        },
        systemMessage: message
      };
      console.log(JSON.stringify(response));
      process.exit(0);
    } else {
      // Allow all other commands
      log('debug', 'Command allowed', { command: command.substring(0, 50) });

      const response = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "allow"
        }
      };
      console.log(JSON.stringify(response));
      process.exit(0);
    }
  } catch (err) {
    log('error', 'Hook error', { error: err.message, input: inputData.substring(0, 200) });

    // On parse error, allow (fail open)
    console.log(JSON.stringify({
      hookSpecificOutput: {
        hookEventName: "PreToolUse",
        permissionDecision: "allow"
      }
    }));
    process.exit(0);
  }
});
