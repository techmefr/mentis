#!/usr/bin/env bash
exec_py="$(dirname "$0")/guard-commit-message.py"
command -v python3 >/dev/null 2>&1 || exit 0
[ -f "$exec_py" ] || exit 0
exec python3 "$exec_py"
