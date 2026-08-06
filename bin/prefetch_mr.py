#!/usr/bin/env python3
"""Dump everything a review needs about one merge request, in parallel, with no clone.

    python3 bin/prefetch_mr.py <namespace/repo> <mr-iid> [gitlab-host]

Writes into $MR_SCRATCH/mr<iid>/ (default ~/mr-review-scratch/mr<iid>/):
    mr.json           the MR itself, including diff_refs and the source branch
    diffs.json        every diff entry, all pages
    discussions.json  existing discussions, so a review replies instead of duplicating
    files/            each touched file on the head side, path flattened with __

The host resolves in this order: the third argument, then $GITLAB_HOST, then glab's own
default. On a self-hosted instance glab silently falls back to gitlab.com when the host is
implicit, and the resulting 404 reads like a permissions problem, so pass it explicitly.
"""
import json
import os
import subprocess
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

HOST = os.environ.get("GITLAB_HOST")
SCRATCH = os.environ.get("MR_SCRATCH", "~/mr-review-scratch")


def glab(path, raw=False):
    cmd = ["glab", "api"]
    if HOST:
        cmd += ["--hostname", HOST]
    cmd.append(path)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{path}: {r.stderr[:300]}")
    return r.stdout if raw else json.loads(r.stdout)


def main():
    if len(sys.argv) < 3:
        sys.exit("usage: prefetch_mr.py <namespace/repo> <mr-iid> [gitlab-host]")
    project, iid = sys.argv[1], sys.argv[2]
    global HOST
    if len(sys.argv) > 3:
        HOST = sys.argv[3]
    enc = urllib.parse.quote(project, safe="")
    out = os.path.expanduser(f"{SCRATCH}/mr{iid}")
    os.makedirs(f"{out}/files", exist_ok=True)

    with ThreadPoolExecutor(max_workers=3) as ex:
        f_mr = ex.submit(glab, f"projects/{enc}/merge_requests/{iid}")
        f_disc = ex.submit(
            glab, f"projects/{enc}/merge_requests/{iid}/discussions?per_page=100"
        )
        mr = f_mr.result()
        disc = f_disc.result()

    diffs = []
    page = 1
    while True:
        batch = glab(
            f"projects/{enc}/merge_requests/{iid}/diffs?per_page=100&page={page}"
        )
        diffs += batch
        if len(batch) < 100:
            break
        page += 1

    json.dump(mr, open(f"{out}/mr.json", "w"))
    json.dump(diffs, open(f"{out}/diffs.json", "w"))
    json.dump(disc, open(f"{out}/discussions.json", "w"))

    head = mr["diff_refs"]["head_sha"]

    def fetch(d):
        if d.get("deleted_file"):
            return None
        p = d["new_path"]
        try:
            content = glab(
                f"projects/{enc}/repository/files/{urllib.parse.quote(p, safe='')}/raw?ref={head}",
                raw=True,
            )
        except RuntimeError as e:
            return f"FAIL  {p} ({e})"
        with open(f"{out}/files/{p.replace('/', '__')}", "w") as fh:
            fh.write(content)
        return f"OK    {p}"

    with ThreadPoolExecutor(max_workers=8) as ex:
        for res in ex.map(fetch, diffs):
            if res:
                print(res)

    open_disc = [
        d for d in disc if any(not n.get("system") for n in d.get("notes", []))
    ]
    print(f"\ndump: {out}")
    print(f"title: {mr['title']}")
    print(f"source branch: {mr['source_branch']}  head: {head[:12]}")
    print(f"{len(diffs)} diff entries, {len(open_disc)} non-system discussions")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        sys.exit(f"error: {e}")
    except FileNotFoundError:
        sys.exit("error: glab not found on PATH")
