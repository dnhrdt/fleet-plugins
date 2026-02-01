#!/usr/bin/env node
/**
 * research-skill-reminder.js
 * Reminds to use Fleet skills instead of direct gh issue commands
 *
 * - gh issue ... claude-research → Use /fleet-dev:research
 * - gh issue create (any repo) → Use /fleet-core:feedback
 */

let inputData = '';

process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
  try {
    const input = JSON.parse(inputData);
    const command = input.tool_input?.command || '';

    // Check if command contains gh and issue
    const isGhIssue = /\bgh\b.*\bissue\b/i.test(command);

    if (isGhIssue) {
      // Check if it's specifically for claude-research
      const isClaudeResearch = /claude-research/i.test(command);

      let message;
      if (isClaudeResearch) {
        message = "STOP: Use /fleet-dev:research skill for research requests to claude-research. " +
                  "The skill ensures proper formatting and Source-Repo tracking.";
      } else {
        message = "STOP: Consider using /fleet-core:feedback skill for structured issue creation. " +
                  "Direct gh commands bypass the templated workflow.";
      }

      // Ask user instead of blocking outright
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
