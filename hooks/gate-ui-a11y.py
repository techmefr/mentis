#!/usr/bin/env python3
"""mentis: a user-interface file is not edited before the accessibility review is done (PreToolUse on
Edit/Write/MultiEdit). OPT-IN: needs MENTIS_A11Y_GATE=1 in the session environment.

The review (skills/accessibility) ends by creating a marker file for the session; until it exists,
an edit to a UI file (.vue .svelte .tsx .jsx .html .astro, not a test or a story) is refused with the
command that creates it. The marker lives in MENTIS_A11Y_DIR (default ~/.mentis-a11y), one file per
session id, expiring after MENTIS_A11Y_TTL_HOURS (default 12).

Fail-closed for this gate only: when the target is a UI file and the payload cannot be understood, the
edit is refused. Anything that is not a UI file never reaches the parser's failure path.
"""
import json
import os
import re
import sys
import time

UI = re.compile(r'\.(vue|svelte|tsx|jsx|html|astro)$', re.I)
EXEMPT = re.compile(r'(\.(test|spec|stories|story)\.|(^|/)(__tests__|__mocks__|node_modules|dist|build)/)', re.I)
RAW_UI = re.compile(r'\.(vue|svelte|tsx|jsx|html|astro)\b', re.I)


def block(message):
    sys.stderr.write('BLOCKED by mentis gate-ui-a11y: ' + message + '\n')
    sys.exit(2)


def marker_dir():
    return os.environ.get('MENTIS_A11Y_DIR') or os.path.join(os.path.expanduser('~'), '.mentis-a11y')


def safe_name(value):
    return re.sub(r'[^A-Za-z0-9_.-]', '_', value or 'default')[:120] or 'default'


def main():
    if os.environ.get('MENTIS_A11Y_GATE') != '1':
        return
    raw = sys.stdin.read()
    if not RAW_UI.search(raw):
        return
    try:
        data = json.loads(raw)
        tool_input = data.get('tool_input') or {}
        path = tool_input.get('file_path') or tool_input.get('path') or ''
        session = data.get('session_id') or ''
        if not isinstance(path, str) or not isinstance(session, str):
            raise ValueError('shape')
    except Exception:
        block('the payload could not be parsed and may touch a UI file; this gate does not fail open. '
              'Unset MENTIS_A11Y_GATE to remove it deliberately.')
    path = path.replace('\\', '/')
    if not UI.search(path) or EXEMPT.search(path):
        return
    directory = marker_dir()
    marker = os.path.join(directory, safe_name(session))
    ttl = float(os.environ.get('MENTIS_A11Y_TTL_HOURS') or 12) * 3600
    try:
        fresh = time.time() - os.path.getmtime(marker) < ttl
    except OSError:
        fresh = False
    if fresh:
        return
    block('the accessibility review (skills/accessibility) is not done for this session, so ' + path +
          ' stays untouched. Run the review, then record it with: mkdir -p "' + directory + '" && touch "' +
          marker + '" and retry the edit.')


if __name__ == '__main__':
    main()
