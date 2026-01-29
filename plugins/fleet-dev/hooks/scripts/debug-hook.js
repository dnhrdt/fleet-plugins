#!/usr/bin/env node
// Debug script - outputs immediately without reading stdin
console.log(JSON.stringify({
  hookSpecificOutput: { permissionDecision: "allow" },
  systemMessage: "DEBUG: Hook script executed successfully"
}));
process.exit(0);
