#!/usr/bin/env python3
"""
Session Inspector - Analyze Claude Code sessions for hook/permission debugging.

Designed as backend for Fleet Plugin skill. Provides:
- Permission request analysis (approve/reject/DCG block)
- Tool call overview (frequency, duration)
- Chronological event timeline (filterable)
- Error/rejection extraction

Usage:
    python session_inspector.py permissions [--current] [--session UUID] [--project NAME]
    python session_inspector.py tools [--current] [--last N]
    python session_inspector.py timeline [--current] [--filter TYPE] [--last N]
    python session_inspector.py errors [--current] [--last N]
    python session_inspector.py summary [--current]
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict, Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path


# === Configuration ===

DEFAULT_CLAUDE_PATH = Path(os.path.expanduser('~')) / '.claude' / 'projects'

# Result classification patterns
USER_REJECTION_PATTERNS = [
    'User rejected tool use',
    "The user doesn't want to proceed",
]

DCG_BLOCK_PATTERN = 'BLOCKED by dcg'

TOOL_ERROR_PREFIXES = [
    'Error: Exit code',
    'Error: File does not exist',
    'Error: File has not been read',
    'Error: String to replace not found',
    'Error: Request failed',
    'Error: File content',
    'Sibling tool call errored',
]


# === Session Finding ===

def find_sessions(base_path: Path, session_id: str = None, project: str = None,
                  current: bool = False, recent: int = None) -> list:
    """Find session file(s) matching criteria."""
    candidates = []

    for proj_dir in base_path.iterdir():
        if not proj_dir.is_dir():
            continue
        if project and project.lower() not in proj_dir.name.lower():
            continue

        for f in proj_dir.glob('*.jsonl'):
            if 'subagent' in f.name:
                continue
            if session_id and not f.stem.startswith(session_id):
                continue
            candidates.append((f.stat().st_mtime, f, proj_dir.name))

    candidates.sort(reverse=True)

    if current:
        return candidates[:1]
    if recent:
        return candidates[:recent]
    if session_id:
        return candidates  # filtered above
    return candidates


def decode_project_name(encoded: str) -> str:
    """Convert encoded path back to readable project name."""
    # d--dev-Projects-fleet-plugins -> fleet-plugins
    parts = encoded.split('-')
    # Find last meaningful segment
    if 'Projects' in parts:
        idx = parts.index('Projects')
        return '-'.join(parts[idx + 1:])
    return encoded


# === JSONL Parsing ===

def parse_session(session_file: Path) -> dict:
    """Parse session JSONL into structured data."""
    entries = []
    lines = []

    try:
        with open(session_file, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {session_file}: {e}", file=sys.stderr)
        return {'entries': [], 'lines': [], 'file': session_file}

    for line in lines:
        try:
            entry = json.loads(line)
            entries.append(entry)
        except json.JSONDecodeError:
            continue

    return {'entries': entries, 'lines': lines, 'file': session_file}


def extract_tool_calls(entries: list) -> list:
    """Extract all tool calls with their results."""
    # Build UUID -> entry index for fast lookup
    uuid_map = {}
    for i, entry in enumerate(entries):
        uid = entry.get('uuid')
        if uid:
            uuid_map[uid] = i

    tool_calls = []

    for entry in entries:
        if entry.get('type') != 'assistant':
            continue

        msg = entry.get('message', {})
        content = msg.get('content', [])
        if not isinstance(content, list):
            continue

        timestamp = entry.get('timestamp', '')

        for block in content:
            if not isinstance(block, dict) or block.get('type') != 'tool_use':
                continue

            tool_name = block.get('name', 'unknown')
            tool_id = block.get('id', '')
            tool_input = block.get('input', {})

            # Extract command for Bash
            command = None
            if tool_name == 'Bash':
                command = tool_input.get('command', '')

            tool_call = {
                'tool': tool_name,
                'command': command,
                'input': tool_input,
                'tool_id': tool_id,
                'timestamp': timestamp,
                'assistant_uuid': entry.get('uuid', ''),
                'result': None,
                'result_class': 'pending',
                'duration_ms': None,
            }

            tool_calls.append(tool_call)

    # Match results to tool calls
    for entry in entries:
        if entry.get('type') != 'user':
            continue
        source_uuid = entry.get('sourceToolAssistantUUID', '')
        result = entry.get('toolUseResult')
        if not source_uuid or result is None:
            continue

        # Find matching tool call(s) by assistant UUID
        for tc in tool_calls:
            if tc['assistant_uuid'] == source_uuid and tc['result'] is None:
                tc['result'] = result
                tc['result_class'] = classify_result(result)
                break

    # Extract turn durations from system entries
    for entry in entries:
        if entry.get('type') == 'system' and entry.get('subtype') == 'turn_duration':
            duration = entry.get('durationMs')
            if duration:
                # Attach to most recent tool calls (approximate)
                pass  # Duration is per-turn, not per-tool

    # Extract hook info from system entries
    hook_events = []
    for entry in entries:
        if entry.get('type') == 'system':
            subtype = entry.get('subtype', '')
            if subtype == 'stop_hook_summary':
                hook_events.append({
                    'subtype': subtype,
                    'hookCount': entry.get('hookCount', 0),
                    'hookErrors': entry.get('hookErrors', []),
                    'hookInfos': entry.get('hookInfos', []),
                    'preventedContinuation': entry.get('preventedContinuation', False),
                    'timestamp': entry.get('timestamp', ''),
                })

    return tool_calls


def classify_result(result) -> str:
    """Classify a toolUseResult: success / user_rejected / dcg_blocked / error.

    IMPORTANT: Only string results indicate errors/rejections.
    Dict results contain tool output (file content, command output) and are always success.
    Searching dict content would cause false positives (e.g. file containing 'BLOCKED by dcg').
    """
    if result is None:
        return 'pending'

    # Dict results = tool output = success
    if isinstance(result, dict):
        return 'success'

    # String results indicate errors/rejections
    if not isinstance(result, str):
        return 'success'

    # DCG block
    if DCG_BLOCK_PATTERN in result:
        return 'dcg_blocked'

    # User rejection
    for pattern in USER_REJECTION_PATTERNS:
        if pattern in result:
            return 'user_rejected'

    # Tool error (not permission-related)
    for prefix in TOOL_ERROR_PREFIXES:
        if result.startswith(prefix):
            return 'error'
    # Any other string starting with Error:
    if result.startswith('Error:'):
        return 'error'

    return 'success'


def get_bash_cmd_name(command: str) -> str:
    """Extract the command name from a bash command string."""
    if not command:
        return ''
    parts = re.split(r'\s*[&|;]\s*', command)
    if parts:
        first = parts[0].strip()
        if first:
            cmd = first.split()[0]
            return os.path.basename(cmd)
    return ''


# === Subcommands ===

def cmd_permissions(sessions: list, args):
    """Analyze permission requests (approve/reject/block)."""
    aggregated = defaultdict(lambda: {
        'total': 0, 'success': 0, 'user_rejected': 0,
        'dcg_blocked': 0, 'error': 0, 'examples': []
    })

    total_calls = 0

    for _, session_file, proj_name in sessions:
        data = parse_session(session_file)
        tool_calls = extract_tool_calls(data['entries'])

        for tc in tool_calls:
            if tc['result'] is None:
                continue  # No result recorded

            tool = tc['tool']
            if tool == 'Bash' and tc['command']:
                key = f"Bash:{get_bash_cmd_name(tc['command'])}"
            else:
                key = tool

            agg = aggregated[key]
            agg['total'] += 1
            total_calls += 1

            rc = tc['result_class']
            if rc in agg:
                agg[rc] += 1

            # Keep rejection examples
            if rc in ('user_rejected', 'dcg_blocked') and len(agg['examples']) < 3:
                example = tc['command'][:80] if tc['command'] else str(tc['input'])[:80]
                agg['examples'].append({'class': rc, 'detail': example})

    items = sorted(aggregated.items(), key=lambda x: x[1]['total'], reverse=True)

    if args.json:
        output = {k: {kk: vv for kk, vv in v.items() if kk != 'examples'}
                  for k, v in items}
        print(json.dumps(output, indent=2))
        return

    # Report
    total_rejected = sum(d['user_rejected'] for _, d in items)
    total_blocked = sum(d['dcg_blocked'] for _, d in items)
    total_errors = sum(d['error'] for _, d in items)
    total_success = sum(d['success'] for _, d in items)

    print(f"Sessions analyzed: {len(sessions)}")
    print(f"Total tool calls:  {total_calls}")
    print(f"  Success:         {total_success}")
    print(f"  User rejected:   {total_rejected}")
    print(f"  DCG blocked:     {total_blocked}")
    print(f"  Tool errors:     {total_errors}")
    print()

    # DCG blocked commands
    dcg_items = [(k, d) for k, d in items if d['dcg_blocked'] > 0]
    if dcg_items:
        print("--- DCG BLOCKED ---")
        print(f"{'Tool/Command':<40} {'Blocked':>8} {'Total':>8}")
        print("-" * 58)
        for key, data in dcg_items:
            print(f"{key:<40} {data['dcg_blocked']:>8} {data['total']:>8}")
            for ex in data['examples']:
                if ex['class'] == 'dcg_blocked':
                    print(f"  -> {ex['detail']}")
        print()

    # User rejected commands
    rejected_items = [(k, d) for k, d in items if d['user_rejected'] > 0]
    if rejected_items:
        print("--- USER REJECTED ---")
        print(f"{'Tool/Command':<40} {'Rejected':>8} {'Total':>8} {'Rate':>8}")
        print("-" * 66)
        for key, data in rejected_items:
            rate = 100 * data['success'] / data['total'] if data['total'] > 0 else 0
            print(f"{key:<40} {data['user_rejected']:>8} {data['total']:>8} {rate:>7.0f}%")
        print()

    # Auto-approve candidates (100% success, no rejections/blocks)
    candidates = [(k, d) for k, d in items
                  if d['user_rejected'] == 0 and d['dcg_blocked'] == 0 and d['total'] >= 3]
    if candidates:
        print("--- AUTO-APPROVE CANDIDATES (100% success, 3+ calls) ---")
        print(f"{'Tool/Command':<40} {'Count':>8}")
        print("-" * 50)
        for key, data in candidates:
            print(f"{key:<40} {data['total']:>8}")
        print()

    # Full table
    if not args.brief:
        print("--- ALL TOOL CALLS ---")
        print(f"{'Tool/Command':<35} {'Total':>6} {'OK':>6} {'Reject':>7} {'DCG':>5} {'Error':>6}")
        print("-" * 67)
        for key, data in items:
            print(f"{key:<35} {data['total']:>6} {data['success']:>6} "
                  f"{data['user_rejected']:>7} {data['dcg_blocked']:>5} {data['error']:>6}")


def cmd_tools(sessions: list, args):
    """Tool call frequency overview."""
    tool_counts = Counter()
    tool_first = {}
    tool_last = {}

    for _, session_file, proj_name in sessions:
        data = parse_session(session_file)
        tool_calls = extract_tool_calls(data['entries'])

        for tc in tool_calls:
            tool = tc['tool']
            tool_counts[tool] += 1
            ts = tc.get('timestamp', '')
            if ts:
                if tool not in tool_first or ts < tool_first[tool]:
                    tool_first[tool] = ts
                if tool not in tool_last or ts > tool_last[tool]:
                    tool_last[tool] = ts

    if args.json:
        print(json.dumps(dict(tool_counts.most_common()), indent=2))
        return

    print(f"Sessions analyzed: {len(sessions)}")
    print()
    print(f"{'Tool':<40} {'Count':>8} {'%':>7}")
    print("-" * 57)
    total = sum(tool_counts.values())
    for tool, count in tool_counts.most_common():
        pct = 100 * count / total if total else 0
        print(f"{tool:<40} {count:>8} {pct:>6.1f}%")
    print("-" * 57)
    print(f"{'TOTAL':<40} {total:>8}")


def cmd_timeline(sessions: list, args):
    """Chronological event timeline."""
    events = []

    for _, session_file, proj_name in sessions:
        data = parse_session(session_file)
        project = decode_project_name(proj_name)

        for entry in data['entries']:
            ts = entry.get('timestamp', '')
            etype = entry.get('type', '')

            if etype == 'assistant':
                msg = entry.get('message', {})
                content = msg.get('content', [])
                if isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get('type') == 'tool_use':
                            events.append({
                                'timestamp': ts,
                                'event': 'tool_call',
                                'tool': block.get('name', ''),
                                'detail': _tool_detail(block),
                                'project': project,
                            })
                        elif isinstance(block, dict) and block.get('type') == 'text':
                            text = block.get('text', '')
                            if text.strip():
                                events.append({
                                    'timestamp': ts,
                                    'event': 'assistant_text',
                                    'tool': '',
                                    'detail': text[:100].replace('\n', ' '),
                                    'project': project,
                                })

            elif etype == 'user':
                result = entry.get('toolUseResult')
                source = entry.get('sourceToolAssistantUUID')
                msg = entry.get('message', {})

                if source and result is not None:
                    rc = classify_result(result)
                    events.append({
                        'timestamp': ts,
                        'event': f'tool_result:{rc}',
                        'tool': '',
                        'detail': _result_preview(result),
                        'project': project,
                    })
                elif msg:
                    # User message
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        text = ' '.join(b.get('text', '') for b in content
                                       if isinstance(b, dict) and b.get('type') == 'text')
                    elif isinstance(content, str):
                        text = content
                    else:
                        text = str(content)
                    if text.strip():
                        events.append({
                            'timestamp': ts,
                            'event': 'user_message',
                            'tool': '',
                            'detail': text[:100].replace('\n', ' '),
                            'project': project,
                        })

            elif etype == 'system':
                subtype = entry.get('subtype', '')
                if subtype == 'stop_hook_summary':
                    errors = entry.get('hookErrors', [])
                    infos = entry.get('hookInfos', [])
                    prevented = entry.get('preventedContinuation', False)
                    detail_parts = []
                    if errors:
                        detail_parts.append(f"errors={len(errors)}")
                    if infos:
                        cmds = [i.get('command', '')[:40] for i in infos]
                        detail_parts.append(f"hooks=[{', '.join(cmds)}]")
                    if prevented:
                        detail_parts.append("PREVENTED")
                    events.append({
                        'timestamp': ts,
                        'event': f'hook:{subtype}',
                        'tool': '',
                        'detail': ' '.join(detail_parts),
                        'project': project,
                    })
                elif subtype == 'turn_duration':
                    duration = entry.get('durationMs')
                    if duration:
                        events.append({
                            'timestamp': ts,
                            'event': 'turn_duration',
                            'tool': '',
                            'detail': f"{duration / 1000:.1f}s",
                            'project': project,
                        })
                elif subtype == 'api_error':
                    events.append({
                        'timestamp': ts,
                        'event': 'api_error',
                        'tool': '',
                        'detail': str(entry.get('message', ''))[:100],
                        'project': project,
                    })

    # Sort by timestamp
    events.sort(key=lambda e: e.get('timestamp', ''))

    # Apply filter
    if args.filter:
        filter_lower = args.filter.lower()
        events = [e for e in events if filter_lower in e['event'].lower()
                  or filter_lower in e.get('tool', '').lower()
                  or filter_lower in e.get('detail', '').lower()]

    # Apply --last
    if args.last:
        events = events[-args.last:]

    if args.json:
        print(json.dumps(events, indent=2, ensure_ascii=False))
        return

    print(f"Events: {len(events)}")
    print()
    print(f"{'Time':<12} {'Event':<25} {'Tool':<15} {'Detail'}")
    print("-" * 90)
    for e in events:
        ts = _format_time(e['timestamp'])
        event_display = e['event']
        # Color-code via markers
        if 'rejected' in event_display or 'blocked' in event_display:
            event_display = f"[!] {event_display}"
        elif 'error' in event_display:
            event_display = f"[E] {event_display}"
        print(f"{ts:<12} {event_display:<25} {e.get('tool', ''):<15} {e.get('detail', '')[:50]}")


def cmd_errors(sessions: list, args):
    """Extract only errors, rejections, and failures."""
    errors = []

    for _, session_file, proj_name in sessions:
        data = parse_session(session_file)
        tool_calls = extract_tool_calls(data['entries'])
        project = decode_project_name(proj_name)

        for tc in tool_calls:
            if tc['result_class'] in ('user_rejected', 'dcg_blocked', 'error'):
                tool = tc['tool']
                if tool == 'Bash' and tc['command']:
                    tool = f"Bash:{get_bash_cmd_name(tc['command'])}"

                detail = ''
                if tc['result_class'] == 'dcg_blocked':
                    result_str = tc['result'] if isinstance(tc['result'], str) else ''
                    detail = result_str[:120]
                elif tc['result_class'] == 'user_rejected':
                    detail = tc['command'][:80] if tc['command'] else str(tc['input'])[:80]
                elif tc['result_class'] == 'error':
                    result_str = tc['result'] if isinstance(tc['result'], str) else ''
                    detail = result_str[:120]

                errors.append({
                    'timestamp': tc['timestamp'],
                    'tool': tool,
                    'class': tc['result_class'],
                    'command': tc['command'][:80] if tc['command'] else '',
                    'detail': detail,
                    'project': project,
                    'session': session_file.stem[:20],
                })

    errors.sort(key=lambda e: e.get('timestamp', ''))

    if args.last:
        errors = errors[-args.last:]

    if args.json:
        print(json.dumps(errors, indent=2, ensure_ascii=False))
        return

    print(f"Errors/Rejections: {len(errors)}")
    print()

    # Group by class
    by_class = defaultdict(list)
    for e in errors:
        by_class[e['class']].append(e)

    for cls in ['dcg_blocked', 'user_rejected', 'error']:
        items = by_class.get(cls, [])
        if not items:
            continue
        label = {'dcg_blocked': 'DCG BLOCKED', 'user_rejected': 'USER REJECTED',
                 'error': 'TOOL ERRORS'}[cls]
        print(f"--- {label} ({len(items)}) ---")
        print(f"{'Time':<12} {'Tool':<30} {'Detail'}")
        print("-" * 80)
        for e in items:
            ts = _format_time(e['timestamp'])
            detail = e['command'] if e['command'] else e['detail']
            print(f"{ts:<12} {e['tool']:<30} {detail[:50]}")
        print()


def cmd_summary(sessions: list, args):
    """Quick session summary."""
    for _, session_file, proj_name in sessions:
        data = parse_session(session_file)
        entries = data['entries']
        project = decode_project_name(proj_name)

        # Basic stats
        user_msgs = [e for e in entries if e.get('type') == 'user'
                     and not e.get('sourceToolAssistantUUID')]
        assistant_msgs = [e for e in entries if e.get('type') == 'assistant']
        tool_calls = extract_tool_calls(entries)

        # Time range
        timestamps = [e.get('timestamp', '') for e in entries if e.get('timestamp')]
        timestamps = [t for t in timestamps if t]
        first_ts = min(timestamps) if timestamps else ''
        last_ts = max(timestamps) if timestamps else ''

        # Classify results
        result_counts = Counter(tc['result_class'] for tc in tool_calls)

        # Turn durations
        turn_durations = []
        for e in entries:
            if e.get('type') == 'system' and e.get('subtype') == 'turn_duration':
                d = e.get('durationMs')
                if d:
                    turn_durations.append(d)

        # Hook summary
        hook_entries = [e for e in entries if e.get('type') == 'system'
                       and e.get('subtype') == 'stop_hook_summary']
        hook_errors_total = sum(len(e.get('hookErrors', [])) for e in hook_entries)

        if args.json:
            print(json.dumps({
                'session': session_file.stem,
                'project': project,
                'start': first_ts,
                'end': last_ts,
                'user_messages': len(user_msgs),
                'assistant_turns': len(assistant_msgs),
                'tool_calls': len(tool_calls),
                'results': dict(result_counts),
                'turn_durations': turn_durations,
                'hook_events': len(hook_entries),
                'hook_errors': hook_errors_total,
            }, indent=2))
            continue

        print(f"Session:  {session_file.stem}")
        print(f"Project:  {project}")
        print(f"Start:    {_format_datetime(first_ts)}")
        print(f"End:      {_format_datetime(last_ts)}")
        print(f"Duration: {_format_duration(first_ts, last_ts)}")
        print()
        print(f"User messages:    {len(user_msgs)}")
        print(f"Assistant turns:  {len(assistant_msgs)}")
        print(f"Tool calls:       {len(tool_calls)}")
        print(f"  Success:        {result_counts.get('success', 0)}")
        print(f"  User rejected:  {result_counts.get('user_rejected', 0)}")
        print(f"  DCG blocked:    {result_counts.get('dcg_blocked', 0)}")
        print(f"  Errors:         {result_counts.get('error', 0)}")
        print(f"  Pending:        {result_counts.get('pending', 0)}")
        print()
        if turn_durations:
            avg = sum(turn_durations) / len(turn_durations)
            print(f"Turn durations:   {len(turn_durations)} turns, avg {avg/1000:.1f}s")
        print(f"Hook events:      {len(hook_entries)}")
        if hook_errors_total:
            print(f"Hook errors:      {hook_errors_total}")

        # Top tools
        tool_counter = Counter(tc['tool'] for tc in tool_calls)
        print()
        print("Top tools:")
        for tool, count in tool_counter.most_common(10):
            print(f"  {tool:<30} {count:>5}")
        print()


# === Helpers ===

def _tool_detail(block: dict) -> str:
    """Short description of a tool call."""
    name = block.get('name', '')
    inp = block.get('input', {})
    if name == 'Bash':
        cmd = inp.get('command', '')
        return cmd[:60].replace('\n', ' ')
    elif name in ('Read', 'Write', 'Edit'):
        path = inp.get('file_path', '')
        return os.path.basename(path) if path else ''
    elif name == 'Glob':
        return inp.get('pattern', '')
    elif name == 'Grep':
        return inp.get('pattern', '')[:40]
    elif name == 'Task':
        return inp.get('description', '')[:40]
    elif name == 'Skill':
        return inp.get('skill', '')
    else:
        return str(inp)[:40]


def _result_preview(result) -> str:
    """Short preview of a tool result."""
    if isinstance(result, str):
        return result[:60].replace('\n', ' ')
    elif isinstance(result, dict):
        if 'stdout' in result:
            return result['stdout'][:60].replace('\n', ' ')
        elif 'file' in result:
            fp = result['file']
            if isinstance(fp, dict):
                return f"file: {os.path.basename(fp.get('filePath', ''))}"
        elif 'filePath' in result:
            return f"edited: {os.path.basename(result['filePath'])}"
        return str(result)[:60]
    return str(result)[:60]


def _format_time(ts: str) -> str:
    """Format ISO timestamp to HH:MM:SS."""
    if not ts:
        return ''
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        # Convert to local time
        local = dt.astimezone()
        return local.strftime('%H:%M:%S')
    except (ValueError, TypeError):
        return ts[:8]


def _format_datetime(ts: str) -> str:
    """Format ISO timestamp to readable datetime."""
    if not ts:
        return 'N/A'
    try:
        dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
        local = dt.astimezone()
        return local.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return ts


def _format_duration(start: str, end: str) -> str:
    """Format duration between two ISO timestamps."""
    if not start or not end:
        return 'N/A'
    try:
        dt_start = datetime.fromisoformat(start.replace('Z', '+00:00'))
        dt_end = datetime.fromisoformat(end.replace('Z', '+00:00'))
        delta = dt_end - dt_start
        hours = int(delta.total_seconds() // 3600)
        minutes = int((delta.total_seconds() % 3600) // 60)
        return f"{hours}h {minutes}min"
    except (ValueError, TypeError):
        return 'N/A'


# === Main ===

def main():
    parser = argparse.ArgumentParser(
        description='Session Inspector - Analyze Claude Code sessions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s summary -c
  %(prog)s permissions -c
  %(prog)s permissions -p fleet-plugins -r 5
  %(prog)s errors -c -n 20
  %(prog)s timeline -c -f dcg
  %(prog)s timeline -c -f rejected -n 10
  %(prog)s tools -c
        """
    )

    # Common args (shared by all subcommands via parents)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument('--path', type=Path, default=DEFAULT_CLAUDE_PATH,
                        help='Path to Claude projects directory')
    common.add_argument('--session', '-s', help='Session UUID (or prefix)')
    common.add_argument('--project', '-p', help='Filter by project name')
    common.add_argument('--current', '-c', action='store_true',
                        help='Use most recent session')
    common.add_argument('--recent', '-r', type=int,
                        help='Analyze N most recent sessions')
    common.add_argument('--last', '-n', type=int,
                        help='Show only last N entries')
    common.add_argument('--json', action='store_true',
                        help='Output as JSON')
    common.add_argument('--brief', '-b', action='store_true',
                        help='Brief output (skip full tables)')

    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    subparsers.add_parser('summary', parents=[common], help='Quick session summary')
    subparsers.add_parser('permissions', parents=[common], help='Permission request analysis')
    subparsers.add_parser('tools', parents=[common], help='Tool call frequency overview')

    timeline_parser = subparsers.add_parser('timeline', parents=[common],
                                            help='Chronological event timeline')
    timeline_parser.add_argument('--filter', '-f', help='Filter events (text match)')

    subparsers.add_parser('errors', parents=[common], help='Errors, rejections, and failures')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if not args.path.exists():
        print(f"Error: Path not found: {args.path}", file=sys.stderr)
        sys.exit(1)

    # Find sessions
    sessions = find_sessions(args.path, args.session, args.project,
                             args.current, args.recent)

    if not sessions:
        print("No sessions found matching criteria.", file=sys.stderr)
        sys.exit(1)

    print(f"[{len(sessions)} session(s) | "
          f"{decode_project_name(sessions[0][2]) if sessions else '?'}]",
          file=sys.stderr)

    # Dispatch
    commands = {
        'summary': cmd_summary,
        'permissions': cmd_permissions,
        'tools': cmd_tools,
        'timeline': cmd_timeline,
        'errors': cmd_errors,
    }
    commands[args.command](sessions, args)


if __name__ == '__main__':
    main()
