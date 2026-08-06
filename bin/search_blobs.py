#!/usr/bin/env python3
"""Run several repository searches in parallel, in one call.

    python3 bin/search_blobs.py <namespace/repo> <ref> term1 term2 term3 ...

One tool call instead of one per term: accumulate the terms a review needs (other callers,
an interface definition, a config key) and fire once. The host comes from $GITLAB_HOST, or
glab's default when unset.

The GitLab blob search is basic — tokenised, no regex — so a conclusion like "no caller
left" must rest on results you actually read. When the output looks incomplete or
ambiguous, fall back to a clone rather than asserting.
"""
import json
import os
import subprocess
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

HOST = os.environ.get("GITLAB_HOST")
PER_PAGE = 50


def search(enc, ref, term):
    q = urllib.parse.quote(term, safe="")
    cmd = ["glab", "api"]
    if HOST:
        cmd += ["--hostname", HOST]
    cmd.append(
        f"projects/{enc}/search?scope=blobs&search={q}"
        f"&ref={urllib.parse.quote(ref, safe='')}&per_page={PER_PAGE}"
    )
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return term, None, r.stderr[:200]
    return term, json.loads(r.stdout), None


def main():
    if len(sys.argv) < 4:
        sys.exit("usage: search_blobs.py <namespace/repo> <ref> term1 [term2 ...]")
    project, ref = sys.argv[1], sys.argv[2]
    terms = sys.argv[3:]
    enc = urllib.parse.quote(project, safe="")
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(lambda t: search(enc, ref, t), terms))
    for term, hits, err in results:
        print(f"=== {term} ===")
        if err:
            print(f"ERROR {err}")
            continue
        if not hits:
            print("(no result)")
            continue
        for h in hits:
            print(f"{h['path']}:{h.get('startline', '?')}")
            for line in h.get("data", "").splitlines()[:4]:
                print(f"    {line}")
        print(
            f"({len(hits)} results"
            f"{f', truncated at {PER_PAGE}' if len(hits) == PER_PAGE else ''})"
        )


if __name__ == "__main__":
    main()
