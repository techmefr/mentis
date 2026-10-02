#!/usr/bin/env python3
"""mentis: the entry-point habit survives a cleared or compacted context (SessionStart). OPT-IN.

After a clear or a compaction the model keeps none of the discipline it was following, and
`skills/using-mentis` is exactly the habit that goes first: name the block before acting. This hook prints
a condensed copy of it to standard output, which the harness adds to the new context.

The condensed text is derived from skills/using-mentis/SKILL.md at the moment it runs, never kept as a
second copy: the frontmatter, `When`, `Output / checkpoint` and `Origin` are dropped and the rest is
printed as written, so editing the block edits what is re-injected. The file is looked for, in order,
at MENTIS_USING_MENTIS, next to this script (../skills/using-mentis), in the project's .claude/skills
and in the user's ~/.claude/skills. Not found, or any error: prints nothing and allows the session.

Which session starts trigger it: MENTIS_SESSION_START_SOURCES, default `clear,compact`. The payload's
`source` field names the start (startup, resume, clear, compact); matching it in the harness
configuration as well as here is harmless.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import command_views as cv

DROPPED = {'when', 'output / checkpoint', 'origin'}


def candidates():
    explicit = os.environ.get('MENTIS_USING_MENTIS')
    if explicit:
        yield explicit
    here = os.path.dirname(os.path.abspath(__file__))
    yield os.path.join(here, '..', 'skills', 'using-mentis', 'SKILL.md')
    for root in (os.environ.get('CLAUDE_PROJECT_DIR'), os.getcwd()):
        if root:
            yield os.path.join(root, '.claude', 'skills', 'using-mentis', 'SKILL.md')
    yield os.path.join(os.path.expanduser('~'), '.claude', 'skills', 'using-mentis', 'SKILL.md')


def condense(text):
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            text = text[end + 4:]
    out = []
    keep = True
    for line in text.splitlines():
        m = re.match(r'^##\s+(.*?)\s*$', line)
        if m:
            keep = m.group(1).strip().lower() not in DROPPED
        if keep:
            out.append(line)
    return '\n'.join(out).strip()


def main():
    payload = cv.load_payload() or {}
    wanted = {s.strip() for s in (os.environ.get('MENTIS_SESSION_START_SOURCES') or 'clear,compact').split(',') if s.strip()}
    if payload.get('source') not in wanted:
        return
    for path in candidates():
        if os.path.isfile(path):
            with open(path, encoding='utf-8', errors='replace') as fh:
                body = condense(fh.read())
            if body:
                print('mentis reminder after a ' + str(payload.get('source')) + ': the entry-point habit, read from '
                      'skills/using-mentis. Follow it for the rest of this task.\n')
                print(body)
            return


if __name__ == '__main__':
    cv.guarded(main)
