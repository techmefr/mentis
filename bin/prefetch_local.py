#!/usr/bin/env python3
"""Dump a local git diff in the exact shape the review readers already know.

    python3 bin/prefetch_local.py                    # working tree vs the merge base with the default branch
    python3 bin/prefetch_local.py origin/main        # everything on this branch since origin/main
    python3 bin/prefetch_local.py main..feature/x    # an explicit range
    python3 bin/prefetch_local.py --staged           # what is about to be committed

No forge, no account, no network: this is the transport that works everywhere, and it is the
default one. The readers do not care where the dump came from — same files, same keys — so a
review runs identically on a local branch, in CI, or against a merge request.

Writes into $MR_SCRATCH/local-<slug>/ (default ~/mr-review-scratch/local-<slug>/):
    mr.json           range, branch, head, base — the metadata a reader reads
    diffs.json        one entry per file: new_path, old_path, diff, new_file, deleted_file
    discussions.json  always [] — nothing to reply to outside a forge
    files/            each touched file at head, path flattened with __

Findings come back as a report you fix yourself. Nothing is ever posted from here.
"""
import json
import os
import subprocess
import sys

SCRATCH = os.environ.get("MR_SCRATCH", "~/mr-review-scratch")


def git(*args, check=True):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[:300]}")
    return r.stdout


def default_base():
    """The branch this work forked from, best effort, without asking the network."""
    for ref in ("origin/HEAD", "origin/main", "origin/master", "main", "master"):
        if subprocess.run(["git", "rev-parse", "--verify", "--quiet", ref],
                          capture_output=True).returncode == 0:
            return git("rev-parse", "--abbrev-ref", ref).strip() if ref == "origin/HEAD" else ref
    return "HEAD~1"


def split_files(raw_diff):
    """Cut a multi-file `git diff` into one entry per file, keeping the hunks intact."""
    out, cur = [], None
    for line in raw_diff.splitlines(keepends=True):
        if line.startswith("diff --git "):
            if cur:
                out.append(cur)
            parts = line.split(" b/")
            old = parts[0].replace("diff --git a/", "").strip()
            new = parts[1].strip() if len(parts) > 1 else old
            cur = {"old_path": old, "new_path": new, "diff": "",
                   "new_file": False, "deleted_file": False, "renamed_file": old != new}
        elif cur is None:
            continue
        elif line.startswith("new file mode"):
            cur["new_file"] = True
        elif line.startswith("deleted file mode"):
            cur["deleted_file"] = True
        elif line.startswith(("@@", "+", "-", " ", "\\")) and not line.startswith(("+++", "---")):
            cur["diff"] += line
    if cur:
        out.append(cur)
    return [f for f in out if f["diff"]]


def main():
    args = [a for a in sys.argv[1:] if a != "--staged"]
    staged = "--staged" in sys.argv[1:]

    git("rev-parse", "--is-inside-work-tree")  # fails clearly outside a repo
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    head = git("rev-parse", "HEAD").strip()

    if staged:
        rng, diff_args, slug = "staged", ["diff", "--cached"], "staged"
    elif args and ".." in args[0]:
        rng = args[0]
        diff_args = ["diff", rng]
        slug = rng.replace("/", "-").replace("..", "-to-")
    else:
        base = args[0] if args else default_base()
        merge_base = git("merge-base", base, "HEAD").strip()
        rng = f"{base}...HEAD"
        diff_args = ["diff", merge_base, "HEAD"]
        slug = branch.replace("/", "-")

    raw = git(*diff_args, "--no-color", "--no-ext-diff", "-M")
    diffs = split_files(raw)

    out = os.path.expanduser(f"{SCRATCH}/local-{slug}")
    os.makedirs(f"{out}/files", exist_ok=True)
    json.dump({"range": rng, "source_branch": branch, "head_sha": head,
               "title": f"local diff on {branch}", "transport": "local"},
              open(f"{out}/mr.json", "w"))
    json.dump(diffs, open(f"{out}/diffs.json", "w"))
    json.dump([], open(f"{out}/discussions.json", "w"))

    for d in diffs:
        if d["deleted_file"]:
            continue
        p = d["new_path"]
        try:
            content = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        with open(f"{out}/files/{p.replace('/', '__')}", "w") as fh:
            fh.write(content)
        print(f"OK    {p}")

    print(f"\ndump: {out}")
    print(f"range: {rng}  branch: {branch}  head: {head[:12]}")
    print(f"{len(diffs)} files in the diff, 0 discussions (local transport)")
    if not diffs:
        print("nothing to review: the range is empty")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        sys.exit(f"error: {e}")
    except FileNotFoundError:
        sys.exit("error: git not found on PATH")
