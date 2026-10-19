#!/usr/bin/env bash
command -v python3 >/dev/null 2>&1 || exit 0
py="$(dirname "$0")/session-start-using-mentis.py"
[ -f "$py" ] || exit 0
exec python3 "$py"
