#!/usr/bin/env python3
"""Checks for the local transport. Builds a throwaway git repo, no network:

    python3 bin/test_local.py

The property that matters is the last one: the position resolver written for the forge
transport must work unchanged on a diff produced locally. If that breaks, the two transports
have silently drifted apart and every reader is affected.
"""
import importlib.util, json, os, shutil, subprocess, sys, tempfile

BIN = os.path.dirname(os.path.abspath(__file__))
ok = fail = 0


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"PASS  {label}")
    else:
        fail += 1
        print(f"FAIL  {label} {detail}")


def load(name):
    spec = importlib.util.spec_from_file_location(name, f"{BIN}/{name}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def git(cwd, *args):
    return subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True)


repo = tempfile.mkdtemp(prefix="mentis-local-")
scratch = tempfile.mkdtemp(prefix="mentis-scratch-")
try:
    git(repo, "init", "-q", "-b", "main", ".")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "t")
    open(f"{repo}/a.txt", "w").write("line1\nline2\nline3\n")
    open(f"{repo}/gone.txt", "w").write("bye\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "init")
    git(repo, "checkout", "-qb", "feat")
    open(f"{repo}/a.txt", "w").write("line1\nCHANGED\nline3\nadded\n")
    open(f"{repo}/b.txt", "w").write("new file\n")
    os.unlink(f"{repo}/gone.txt")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "work")

    env = dict(os.environ, MR_SCRATCH=scratch)
    r = subprocess.run([sys.executable, f"{BIN}/prefetch_local.py", "main"],
                       cwd=repo, capture_output=True, text=True, env=env)
    check("prefetch_local exits 0 on a real range", r.returncode == 0, r.stderr[:120])

    out = f"{scratch}/local-feat"
    check("dump directory named after the branch", os.path.isdir(out), out)
    for f in ("mr.json", "diffs.json", "discussions.json"):
        check(f"{f} written (same shape as the forge transport)", os.path.exists(f"{out}/{f}"))

    diffs = json.load(open(f"{out}/diffs.json"))
    paths = {d["new_path"] for d in diffs}
    check("modified file in the diff", "a.txt" in paths, paths)
    check("added file in the diff", "b.txt" in paths, paths)
    check("added file flagged new_file", any(d["new_file"] for d in diffs if d["new_path"] == "b.txt"))
    check("deleted file flagged deleted_file",
          any(d["deleted_file"] for d in diffs if d["old_path"] == "gone.txt"),
          [(d["old_path"], d["deleted_file"]) for d in diffs])

    meta = json.load(open(f"{out}/mr.json"))
    check("metadata carries branch, head and transport",
          meta["source_branch"] == "feat" and len(meta["head_sha"]) == 40
          and meta["transport"] == "local", meta)
    check("no discussions on a local diff", json.load(open(f"{out}/discussions.json")) == [])
    check("head-side file content dumped",
          "CHANGED" in open(f"{out}/files/a.txt").read())
    check("deleted file not dumped", not os.path.exists(f"{out}/files/gone.txt"))

    # the property the design rests on
    post = load("post_mr_comments")
    check("forge position resolver works on a local diff: changed line",
          post.find_position(diffs, "a.txt", 2) == {"new_line": 2},
          post.find_position(diffs, "a.txt", 2))
    check("forge position resolver works on a local diff: context line",
          post.find_position(diffs, "a.txt", 1) == {"old_line": 1, "new_line": 1},
          post.find_position(diffs, "a.txt", 1))

    r = subprocess.run([sys.executable, f"{BIN}/prefetch_local.py", "--staged"],
                       cwd=repo, capture_output=True, text=True, env=env)
    check("--staged mode runs with nothing staged", r.returncode == 0, r.stderr[:120])
    check("empty range says so, rather than pretending to review",
          "nothing to review" in r.stdout, r.stdout[-120:])

    r = subprocess.run([sys.executable, f"{BIN}/prefetch_local.py"],
                       cwd=tempfile.gettempdir(), capture_output=True, text=True, env=env)
    check("outside a git repo: clean error, no traceback",
          r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:120])
finally:
    shutil.rmtree(repo, ignore_errors=True)
    shutil.rmtree(scratch, ignore_errors=True)

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
