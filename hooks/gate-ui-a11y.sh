#!/usr/bin/env bash
if ! command -v python3 >/dev/null 2>&1; then
  [ "${MENTIS_A11Y_GATE:-}" = "1" ] || exit 0
  echo "BLOCKED by mentis gate-ui-a11y: python3 not available, cannot check this edit. Unset MENTIS_A11Y_GATE to remove the gate deliberately." >&2
  exit 2
fi
exec python3 "$(dirname "$0")/gate-ui-a11y.py"
