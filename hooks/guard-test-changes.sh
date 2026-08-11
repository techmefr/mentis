#!/usr/bin/env bash
# mentis: no-test-tampering hook (skills/debug §3.4, skills/code, skills/tdd)
#
# Refuses an Edit/Write on a test file that makes a pre-existing assertion line disappear
# (deleted, commented out, or its expected value changed) unless MENTIS_ALLOW_TEST_CHANGES
# is set. Extending a test file with a new case is unaffected: this only fires when a line
# that matched an assertion pattern BEFORE the edit is no longer present, verbatim, AFTER it.
#
# Wiring: see hooks/README.md.
#
# Contract: reads the tool call as JSON on stdin. Exit 0 allows, exit 2 blocks and returns
# stderr to the model.
#
# Fail-closed, but only on the guarded path: if the file being touched doesn't look like a
# test file, we exit 0 without needing any JSON parser. If it does look like a test file and
# we cannot parse the payload, we BLOCK — same reasoning as verify-gate.sh: a guard that
# fails open on the path it exists to guard reports a safety that isn't there.

set -uo pipefail

ALLOW="${MENTIS_ALLOW_TEST_CHANGES:-}"

payload=$(cat)

# --- Fast path, parser-free -------------------------------------------------------------
# Deliberately crude: does the raw payload even mention something that looks like a test
# file? If not, this hook has no business here. A real dependency-graph check isn't worth
# it for a filter this cheap to run on every Edit/Write.
if ! printf '%s' "$payload" | grep -qE '\.(test|spec)\.|_test\.|test_[A-Za-z0-9_]*\.py|Test\.(php|java)'; then
  exit 0
fi

if [ -n "$ALLOW" ]; then
  exit 0
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "BLOCKED by mentis guard-test-changes: python3 not available, cannot check this edit." >&2
  echo "Install python3, or remove this hook deliberately. It will not fail open." >&2
  exit 2
fi

printf '%s' "$payload" | python3 "$(dirname "$0")/guard-test-changes.py"
