#!/usr/bin/env bash
# mentis: fact-forcing gate before the first edit of a file (PreToolUse on Edit/Write/MultiEdit)
#
# OPT-IN. Does nothing unless MENTIS_GATEGUARD=1 is set in the environment of the session.
#
# The first Edit or Write on a file is refused with a request for facts that only an investigation can
# supply: who imports this file (a Grep, not a recollection), which public API the change touches, the
# shape of any data it reads or writes, and the user's instruction quoted verbatim. The retry on the same
# file is allowed. Asking "are you sure?" gets "yes" every time; asking for the importers makes the agent
# go and look, and the looking is the point.
#
# State is per session, in MENTIS_GATEGUARD_DIR (default ~/.mentis-gateguard), expires after 30 minutes
# of inactivity and holds at most 500 files. Paths matching MENTIS_GATEGUARD_EXEMPT (comma-separated
# globs, matched against the path and its basename) are never gated.
#
# Contract: tool call as JSON on stdin; exit 0 allows, exit 2 blocks and returns stderr to the model.
# Fails OPEN on any error: this is a prompt for diligence, not a security boundary.

set -uo pipefail

[ "${MENTIS_GATEGUARD:-0}" = "1" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

payload=$(cat)

verdict=$(MENTIS_PAYLOAD="$payload" python3 - 2>/dev/null <<'PY'
import fnmatch, json, os, sys, time

TIMEOUT = 30 * 60
MAX_ENTRIES = 500

try:
    d = json.loads(os.environ.get('MENTIS_PAYLOAD', ''))
    tool = d.get('tool_name', '')
    if tool not in ('Edit', 'Write', 'MultiEdit'):
        sys.exit(0)
    path = (d.get('tool_input') or {}).get('file_path') or ''
    if not path:
        sys.exit(0)

    exempt = [g.strip() for g in os.environ.get('MENTIS_GATEGUARD_EXEMPT', '').split(',') if g.strip()]
    base = os.path.basename(path)
    if any(fnmatch.fnmatch(path, g) or fnmatch.fnmatch(base, g) for g in exempt):
        sys.exit(0)

    state_dir = os.path.expanduser(os.environ.get('MENTIS_GATEGUARD_DIR', '~/.mentis-gateguard'))
    os.makedirs(state_dir, exist_ok=True)
    session = ''.join(c for c in str(d.get('session_id') or 'default') if c.isalnum() or c in '-_')[:64] or 'default'
    state_file = os.path.join(state_dir, session + '.json')

    now = time.time()
    state = {'last': now, 'files': {}}
    try:
        with open(state_file, encoding='utf-8') as fh:
            loaded = json.load(fh)
        if isinstance(loaded, dict) and now - float(loaded.get('last', 0)) <= TIMEOUT:
            state = loaded
    except Exception:
        pass

    files = state.get('files') or {}
    state['last'] = now
    entry = files.get(path)

    if entry == 'asked':
        files[path] = 'allowed'
        verdict = ''
    elif entry == 'allowed':
        verdict = ''
    else:
        files[path] = 'asked'
        verdict = path

    if len(files) > MAX_ENTRIES:
        for k in list(files)[:len(files) - MAX_ENTRIES]:
            files.pop(k, None)
    state['files'] = files
    with open(state_file, 'w', encoding='utf-8') as fh:
        json.dump(state, fh)
    print(verdict)
except SystemExit:
    raise
except Exception:
    sys.exit(0)
PY
)

[ -z "$verdict" ] && exit 0

{
  echo "BLOCKED (gateguard): first edit of $verdict in this session."
  echo ""
  echo "Before editing it, state these facts, each from something you just looked at:"
  echo "  1. Every file that imports or references it (run a Grep, list the paths)."
  echo "  2. The public functions, classes or routes this change touches or could break."
  echo "  3. The shape of any data it reads or writes (fields, types, who produces them)."
  echo "  4. The user's instruction for this change, quoted verbatim."
  echo ""
  echo "Then repeat the same edit; it will go through."
} >&2
exit 2
