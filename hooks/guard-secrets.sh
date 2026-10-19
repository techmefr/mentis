#!/usr/bin/env bash
# mentis: no obvious secret enters the tree (PreToolUse on Write/Edit/MultiEdit/Bash)
#
# OPT-IN: active only where it is wired (hooks/README.md). Small on purpose: it refuses the evident cases,
# a private key block, a token with a well-known prefix, a populated .env file, a git add of a .env file.
# It is a tripwire, not a scanner; a secret scanner in CI is still the real control.
#
# Contract: tool call as JSON on stdin; exit 0 allows, exit 2 blocks and returns stderr to the model.
# Fails OPEN on any error (no python3, unreadable payload): a tripwire that breaks the session gets removed.

set -uo pipefail

command -v python3 >/dev/null 2>&1 || exit 0

payload=$(cat)

verdict=$(MENTIS_PAYLOAD="$payload" python3 - 2>/dev/null <<'PY'
import json, os, re, sys

try:
    d = json.loads(os.environ.get('MENTIS_PAYLOAD', ''))
    tool = d.get('tool_name', '')
    ti = d.get('tool_input') or {}
    if tool == 'Bash':
        texts = [ti.get('command', '')]
        path = ''
    elif tool in ('Write', 'Edit', 'MultiEdit'):
        path = ti.get('file_path', '') or ''
        texts = [ti.get('content', ''), ti.get('new_string', '')]
        texts += [e.get('new_string', '') for e in (ti.get('edits') or []) if isinstance(e, dict)]
    else:
        sys.exit(0)

    body = '\n'.join(t for t in texts if isinstance(t, str))

    PATTERNS = [
        (r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY(?: BLOCK)?-----', 'a private key block'),
        (r'\bAKIA[0-9A-Z]{16}\b', 'an AWS access key id'),
        (r'\bgh[pousr]_[A-Za-z0-9]{36,}\b', 'a GitHub token'),
        (r'\bgithub_pat_[A-Za-z0-9_]{40,}\b', 'a GitHub fine-grained token'),
        (r'\bglpat-[A-Za-z0-9_-]{20,}\b', 'a GitLab token'),
        (r'\bxox[baprs]-[A-Za-z0-9-]{10,}\b', 'a Slack token'),
        (r'\bsk_live_[0-9A-Za-z]{24,}\b', 'a live Stripe key'),
        (r'\bsk-ant-[A-Za-z0-9_-]{20,}\b', 'an Anthropic API key'),
        (r'\bAIza[0-9A-Za-z_-]{35}\b', 'a Google API key'),
        (r'\bnpm_[A-Za-z0-9]{36}\b', 'an npm token'),
    ]
    for pat, why in PATTERNS:
        if re.search(pat, body):
            print(why)
            sys.exit(0)

    base = os.path.basename(path)
    is_env = re.match(r'^\.env(\..+)?$', base) and not re.search(r'\.(example|sample|template|dist)$', base)
    if is_env:
        for line in body.splitlines():
            m = re.match(r'^\s*(?:export\s+)?[A-Z][A-Z0-9_]*(?:KEY|SECRET|TOKEN|PASSWORD|PASSWD|CREDENTIAL)[A-Z0-9_]*\s*=\s*(\S+)', line)
            if m and m.group(1).strip('"\'') not in ('', 'changeme', 'your-key-here'):
                print('a populated secret variable in ' + base)
                sys.exit(0)

    if tool == 'Bash':
        for seg in re.split(r'[;&|\n]', body):
            if re.search(r'\bgit\s+add\b', seg) and re.search(r'(?:^|[\s/])\.env(?:\.[A-Za-z0-9_-]+)?(?=\s|$)', seg) \
                    and not re.search(r'\.env\.(?:example|sample|template|dist)(?=\s|$)', seg):
                print('staging a .env file')
                sys.exit(0)
    print('')
except SystemExit:
    raise
except Exception:
    sys.exit(0)
PY
)

[ -z "$verdict" ] && exit 0

{
  echo "BLOCKED (guard-secrets): this would introduce $verdict."
  echo ""
  echo "Keep secrets out of the tree: read them from the environment or a secret store, commit a"
  echo ".env.example with empty values, and add the real .env file to .gitignore."
  echo "If this is a deliberate fixture, build the value at runtime in the test instead of writing it out."
} >&2
exit 2
