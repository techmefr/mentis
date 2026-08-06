#!/usr/bin/env bash
# mentis: companion to verify-gate.sh (step 7 of WORKFLOW.md)
#
# Appends every evidence file actually read to a read log, so the gate hook can tell
# "evidence exists" apart from "evidence was looked at".
#
# Wiring: see hooks/README.md.
#
# This half always exits 0: it observes, it never blocks. If it fails to record a read, the
# consequence lands in verify-gate.sh, which will refuse the claim. That's the safe
# direction: a missing record means "not proven", never "proven".

set -uo pipefail

EVIDENCE_DIR="${MENTIS_EVIDENCE_DIR:-.claude/evidence}"
READ_LOG="${MENTIS_READ_LOG:-.claude/evidence/.read-log}"

payload=$(cat)

# Parser-free pre-filter: nothing to do unless an evidence path is involved at all.
printf '%s' "$payload" | grep -qF "$EVIDENCE_DIR" || exit 0

file_path=$(printf '%s' "$payload" | python3 -c "
import json,sys
try:
    d = json.load(sys.stdin)
    sys.stdout.write(d.get('tool_input',{}).get('file_path','') or '')
except Exception:
    pass
" 2>/dev/null)

[ -z "$file_path" ] && exit 0

case "$file_path" in
  *"$EVIDENCE_DIR"*) ;;
  *) exit 0 ;;
esac

mkdir -p "$(dirname "$READ_LOG")" 2>/dev/null
printf '%s\n' "$file_path" >> "$READ_LOG" 2>/dev/null

exit 0
