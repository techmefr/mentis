#!/usr/bin/env bash
# Wires bin/pre-push as this clone's pre-push git hook.
#
# It installs a shim that delegates, never a copy. A copy is a fork: it is frozen at the
# moment it was installed, so every suite added to bin/pre-push afterwards silently stops
# gating pushes in that clone. That is not hypothetical — it is what happened here between
# 2026-08-11 and 2026-09-08, and it meant the rule-C and frontmatter suites were not
# actually guarding anything.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
src="$repo_root/bin/pre-push"
hooks_dir="$(git rev-parse --git-path hooks)"
dst="$hooks_dir/pre-push"

if [ ! -f "$src" ]; then
  echo "install-git-hooks: $src not found" >&2
  exit 1
fi

mkdir -p "$hooks_dir"

cat > "$dst" <<'SHIM'
#!/usr/bin/env bash
# Installed by bin/install-git-hooks.sh. Delegates on purpose: the suite list lives in
# bin/pre-push, which is versioned. Do not inline it here — a copy goes stale in silence.
set -euo pipefail
exec "$(git rev-parse --show-toplevel)/bin/pre-push" "$@"
SHIM

chmod +x "$dst"
echo "installed: $dst (delegates to bin/pre-push)"
