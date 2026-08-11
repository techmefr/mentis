#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
src="$repo_root/bin/pre-push"
dst="$repo_root/.git/hooks/pre-push"

if [ ! -f "$src" ]; then
  echo "install-git-hooks: $src not found" >&2
  exit 1
fi

cp "$src" "$dst"
chmod +x "$dst"
echo "installed: $dst"
