#!/usr/bin/env python3
"""Post a batch of inline review comments on a merge request, from a payload file.

    python3 bin/post_mr_comments.py --file <payloads.json> [--dry-run]

The payload file, which a reader agent writes in REPORT mode:

    {
      "project": "namespace/repo",
      "iid": 42,
      "host": "gitlab.example.com",        // optional, else $GITLAB_HOST, else glab's default
      "comments": [
        {"path": "src/thing.ts", "line": 87, "body": "..."}
      ]
    }

`line` is the line as it appears on the **new** side of the diff. The script resolves the
line code itself: for an added line `new_line` alone is enough, for an unmodified context
line GitLab needs **both** `old_line` and `new_line` or it answers 400 `line_code can't be
blank`, so the hunk is walked to recover the matching old line.

Three traps this handles, all of which cost a real review:
  * the `Content-Type: application/json` header is mandatory, without it the API answers 415;
  * `glab -f position[...]` flags go out flat, GitLab **silently ignores them**, and the
    comment lands as a general note with no error at all — hence a full JSON body on stdin;
  * a response whose `notes[0].position` is null means exactly that silent fallback, so it
    is deleted again rather than left as a stray general note (the DELETE carries `{}` as a
    body: an empty body makes glab wait on stdin forever).

`--dry-run` resolves every position and prints what would be posted, without writing
anything to the MR. Worth one run whenever the payload file was generated earlier: a stale
file posts duplicates, and its line numbers are not necessarily the current diff's.
"""
import json
import os
import re
import subprocess
import sys

HOST = os.environ.get("GITLAB_HOST")


def api(path, method="GET", data=None, host=None):
    cmd = ["glab", "api"]
    if host:
        cmd += ["--hostname", host]
    cmd.append(path)
    if method != "GET":
        cmd += [
            "--method", method,
            "-H", "Content-Type: application/json",
            "--input", "-",
        ]
        data = data if data is not None else "{}"
    r = subprocess.run(cmd, capture_output=True, text=True, input=data)
    if r.returncode != 0:
        raise RuntimeError(f"{path}: {r.stderr[:800]}")
    return json.loads(r.stdout) if r.stdout.strip() else {}


def find_position(diffs, path, target_new):
    """Walk the hunks to turn a new-side line number into a usable position."""
    for f in diffs:
        if f["new_path"] != path:
            continue
        old = new = None
        for line in f["diff"].splitlines():
            if line.startswith("@@"):
                m = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
                if not m:
                    continue
                old, new = int(m.group(1)), int(m.group(2))
                continue
            if old is None:
                continue
            if line.startswith("+"):
                if new == target_new:
                    return {"new_line": target_new}
                new += 1
            elif line.startswith("-"):
                old += 1
            elif line.startswith(" ") or line == "":
                if new == target_new:
                    return {"old_line": old, "new_line": target_new}
                old += 1
                new += 1
    return None


def post_all(project, iid, comments, host=None, dry_run=False):
    enc = project.replace("/", "%2F")
    mr = api(f"projects/{enc}/merge_requests/{iid}", host=host)
    refs = mr["diff_refs"]
    diffs = api(f"projects/{enc}/merge_requests/{iid}/diffs?per_page=100", host=host)
    results = []
    for c in comments:
        pos = find_position(diffs, c["path"], c["line"])
        if pos is None:
            results.append(f"SKIP {c['path']}:{c['line']} — line outside the diff hunks")
            continue
        if dry_run:
            kind = "added line" if "old_line" not in pos else "context line"
            results.append(
                f"DRY  {c['path']}:{c['line']} — {kind}, {len(c['body'])} chars"
            )
            continue
        payload = {
            "body": c["body"],
            "position": {
                "base_sha": refs["base_sha"],
                "start_sha": refs["start_sha"],
                "head_sha": refs["head_sha"],
                "position_type": "text",
                "new_path": c["path"],
                "old_path": c["path"],
                **pos,
            },
        }
        try:
            resp = api(
                f"projects/{enc}/merge_requests/{iid}/discussions",
                method="POST",
                data=json.dumps(payload),
                host=host,
            )
        except RuntimeError as e:
            results.append(f"FAIL {c['path']}:{c['line']} — {e}")
            continue
        note = (resp.get("notes") or [{}])[0]
        if note.get("position"):
            results.append(f"OK   {c['path']}:{c['line']} — note {note['id']}, inline")
        else:
            nid = note.get("id")
            api(
                f"projects/{enc}/merge_requests/{iid}/notes/{nid}",
                method="DELETE",
                host=host,
            )
            results.append(
                f"FAIL {c['path']}:{c['line']} — went out as a general note, deleted again "
                f"(note {nid})"
            )
    return results


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    if len(args) != 2 or args[0] != "--file":
        sys.exit("usage: post_mr_comments.py --file <payloads.json> [--dry-run]")
    spec = json.load(open(os.path.expanduser(args[1])))
    out = post_all(
        spec["project"],
        spec["iid"],
        spec["comments"],
        host=spec.get("host", HOST),
        dry_run=dry_run,
    )
    print("\n".join(out))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        sys.exit(f"error: {e}")
    except FileNotFoundError as e:
        sys.exit(f"error: {e}")
    except (KeyError, json.JSONDecodeError) as e:
        sys.exit(f"error: malformed payload file ({e})")
