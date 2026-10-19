#!/usr/bin/env python3
"""Install this repo's agents into a Claude Code agents directory, localised.

`skills/distributing-blocks` forbids a silent auto-update: an install that rewrites someone's agents
without them reading it is exactly what rule B forbids others from doing to us. So this script is a
**pull**, run deliberately, and it reports every file it would touch before touching anything —
`--dry-run` is the default, `--apply` is the explicit opt-in.

Two things it never does:

- **It never touches a file the repo does not own.** Agents that exist only in the target directory
  (locally-calibrated ones, kept out of the repo under rule C) are listed and left alone.
- **It never overwrites without a backup.** `--apply` copies the current target into
  `<target>/.backup-<stamp>/` first, so the previous version stays readable.

The repo is de-identified (rule C): it says "the operator", `<scratch>`, "an org skill catalogue".
A local install usually wants the real names back. That mapping is **not in this repo** — it names
real people, hosts and paths. Pass it with `--localise <file.json>`, a flat `{"from": "to"}` object,
and keep that file outside the repo.

Usage:
    python3 bin/install_agents.py --target ~/.claude/agents
    python3 bin/install_agents.py --target ~/.claude/agents --localise ~/.claude/mentis-local.json
    python3 bin/install_agents.py --target ~/.claude/agents --localise ~/... --apply
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO_AGENTS = Path(__file__).resolve().parent.parent / "agents"


def localise(text: str, mapping: dict[str, str]) -> str:
    # longest key first, so "the operator's" is replaced before "the operator"
    for src in sorted(mapping, key=len, reverse=True):
        text = text.replace(src, mapping[src])
    return text


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", required=True, type=Path, help="the agents directory to install into")
    ap.add_argument("--localise", type=Path, help='JSON file of {"from": "to"} substitutions, kept outside this repo')
    ap.add_argument("--apply", action="store_true", help="actually write; without it, nothing is touched")
    ap.add_argument("--stamp", default="backup", help="suffix for the backup directory under the target")
    args = ap.parse_args()

    target: Path = args.target.expanduser()
    if not target.is_dir():
        print(f"target is not a directory: {target}", file=sys.stderr)
        return 2

    mapping: dict[str, str] = {}
    if args.localise:
        mapping = json.loads(args.localise.expanduser().read_text(encoding="utf-8"))
        if not isinstance(mapping, dict) or not all(isinstance(v, str) for v in mapping.values()):
            print("--localise must be a flat object of string to string", file=sys.stderr)
            return 2

    repo_files = {p.name: p for p in sorted(REPO_AGENTS.glob("*.md"))}
    target_files = {p.name for p in target.glob("*.md")}

    new, changed, identical = [], [], []
    for name, src in repo_files.items():
        text = localise(src.read_text(encoding="utf-8"), mapping)
        dst = target / name
        if not dst.exists():
            new.append((name, text))
        elif dst.read_text(encoding="utf-8") != text:
            changed.append((name, text))
        else:
            identical.append(name)

    local_only = sorted(target_files - set(repo_files))

    print(f"target      : {target}")
    print(f"substitutions: {len(mapping)}")
    print(f"new         : {len(new)}  {[n for n, _ in new]}")
    print(f"updated     : {len(changed)}  {[n for n, _ in changed]}")
    print(f"unchanged   : {len(identical)}")
    print(f"left alone  : {len(local_only)}  {local_only}")

    if mapping:
        # a source contained in its own replacement ("references/" → "~/mentis/references/")
        # survives by design and is not a miss
        leftover = sorted({
            s for s, r in mapping.items()
            if s not in r and any(s in t for _, t in new + changed)
        })
        if leftover:
            print(f"\nWARNING, substitution source still present after mapping: {leftover}")

    if not args.apply:
        print("\ndry run, nothing written. re-run with --apply once the list above reads right.")
        return 0

    if changed:
        backup = target / f".{args.stamp}"
        backup.mkdir(exist_ok=True)
        for name, _ in changed:
            shutil.copy2(target / name, backup / name)
        print(f"\nbacked up {len(changed)} files into {backup}")

    for name, text in new + changed:
        (target / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(new) + len(changed)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
