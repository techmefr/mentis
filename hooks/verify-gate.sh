#!/usr/bin/env bash
# mentis: default-FAIL gate hook (step 7 of WORKFLOW.md)
#
# Refuses any edit that flips a test-results.json line to "passes": true unless the
# matching evidence file exists AND has been read in this session.
#
# Wiring: see hooks/README.md.
#
# Contract: reads the tool call as JSON on stdin. Exit 0 allows, exit 2 blocks and returns
# stderr to the model.
#
# Fail-closed, but only on the guarded path: if the target file isn't the contract file we
# exit 0 without needing any JSON parser, so a repo with no parser installed still works
# normally. If the target IS the contract file and we cannot parse it, we BLOCK. A guard
# that fails open is worse than no guard: it reports a safety that isn't there.

set -uo pipefail

EVIDENCE_DIR="${MENTIS_EVIDENCE_DIR:-.claude/evidence}"
READ_LOG="${MENTIS_READ_LOG:-.claude/evidence/.read-log}"
CONTRACT_NAME="${MENTIS_CONTRACT_NAME:-test-results.json}"

payload=$(cat)

# --- Fast path, parser-free -------------------------------------------------------------
# If the contract file isn't mentioned anywhere in this tool call, this hook has no
# business here. Deliberately crude: it only decides whether to look closer.
if ! printf '%s' "$payload" | grep -qF "$CONTRACT_NAME"; then
  exit 0
fi

# --- From here on we need a real JSON parser ------------------------------------------
parse() { # $1 = python expression over `d`
  printf '%s' "$payload" | python3 -c "
import json,sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(3)
try:
    sys.stdout.write($1 or '')
except Exception:
    sys.exit(3)
" 2>/dev/null
}

if ! command -v python3 >/dev/null 2>&1; then
  echo "BLOCKED by mentis verify-gate: python3 not available, cannot verify the gate contract." >&2
  echo "Install python3, or remove this hook deliberately. It will not fail open." >&2
  exit 2
fi

file_path=$(parse "d.get('tool_input',{}).get('file_path','')")
if [ $? -eq 3 ]; then
  echo "BLOCKED by mentis verify-gate: could not parse the tool call payload." >&2
  echo "Refusing to allow an unverifiable edit to $CONTRACT_NAME." >&2
  exit 2
fi

# The contract name appeared in the payload, but not as the file being written: allow.
case "$file_path" in
  *"$CONTRACT_NAME") ;;
  *) exit 0 ;;
esac

# Which criteria does this edit declare as passing? Handles both the whole-file write
# (`content`) and the targeted edit (`new_string`), and both the nested and flat shapes.
claimed=$(parse "'\n'.join(sorted(__import__('re').findall(
    r'\"([A-Za-z0-9_.:\\-]+)\"\s*:\s*\{[^{}]*?\"passes\"\s*:\s*true',
    (d.get('tool_input',{}).get('content') or '') + '\n' +
    (d.get('tool_input',{}).get('new_string') or ''))))")
if [ $? -eq 3 ]; then
  echo "BLOCKED by mentis verify-gate: could not read the claimed criteria from the edit." >&2
  exit 2
fi

# Nothing declared passing: nothing to prove.
[ -z "$claimed" ] && exit 0

missing_evidence=()
unread_evidence=()

while IFS= read -r criterion; do
  [ -z "$criterion" ] && continue

  # Evidence for a criterion is any file under EVIDENCE_DIR whose name contains its id.
  found=$(find "$EVIDENCE_DIR" -type f -name "*${criterion}*" 2>/dev/null | head -n 1)

  if [ -z "$found" ]; then
    missing_evidence+=("$criterion")
    continue
  fi

  # Produced is not enough: it has to have been read. record-read.sh appends to the read
  # log on every Read of an evidence file; no entry means nobody looked at it.
  if ! grep -qF "$found" "$READ_LOG" 2>/dev/null; then
    unread_evidence+=("$criterion -> $found")
  fi
done <<< "$claimed"

if [ ${#missing_evidence[@]} -eq 0 ] && [ ${#unread_evidence[@]} -eq 0 ]; then
  exit 0
fi

{
  echo "BLOCKED by mentis verify-gate: default = failure (WORKFLOW.md section 3)."
  echo
  if [ ${#missing_evidence[@]} -gt 0 ]; then
    echo "No evidence found under ${EVIDENCE_DIR} for:"
    for c in "${missing_evidence[@]}"; do echo "  - $c"; done
    echo
    echo "Produce it first: test output, a screenshot, or a log, named so the filename"
    echo "contains the criterion id."
  fi
  if [ ${#unread_evidence[@]} -gt 0 ]; then
    echo "Evidence exists but was never read in this session:"
    for c in "${unread_evidence[@]}"; do echo "  - $c"; done
    echo
    echo "Read it before declaring the criterion passing. Producing evidence and not looking"
    echo "at it is how a green run hides a real failure."
  fi
} >&2

exit 2
