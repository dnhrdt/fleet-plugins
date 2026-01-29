#!/usr/bin/env node
/**
 * block-npm-npx.js
 * Blocks direct npm/npx calls in Git Bash on Windows
 * These commands produce no stdout in Git Bash - must use cmd //c wrapper
 *
 * Cross-platform: Works on Windows and Linux
 */

let inputData = '';

process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => inputData += chunk);
process.stdin.on('end', () => {
  try {
    const input = JSON.parse(inputData);
    const command = input.tool_input?.command || '';

    // Check if command starts with npm or npx (but not cmd)
    if (/^(npm|npx)\s/.test(command)) {
      // Block with helpful message
      const response = {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny"
        },
        systemMessage: `BLOCKED: npm/npx has no stdout in Git Bash on Windows. Use: cmd //c "${command}"`
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
