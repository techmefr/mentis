#!/usr/bin/env python3
"""Checks for the three review scripts. No network, no GitLab, no fixtures to install:

    python3 bin/test_scripts.py

What it actually proves, because these are the parts that fail silently rather than loudly:
resolving a new-side line number to a position (added line, context line, out-of-hunk, bad
hunk header), the shape of the POST/DELETE calls that the four inline-posting traps are
about, the two environment variables and their defaults, the usage guards, a clean error
instead of a traceback on a missing or malformed payload file, and that the files stay
Linux-runnable (shebang, exec bit, LF endings).
"""
import importlib.util, io, json, os, subprocess, sys, tempfile

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


def run(args, env=None, stdin=""):
    e = dict(os.environ)
    e.pop("GITLAB_HOST", None)
    e.pop("MR_SCRATCH", None)
    if env:
        e.update(env)
    return subprocess.run([sys.executable] + args, capture_output=True, text=True,
                          input=stdin, env=e)


# ---- 1. position resolution against a synthetic diff (the part that breaks silently)
post = load("post_mr_comments")
DIFF = [{
    "new_path": "src/thing.ts",
    "diff": "@@ -10,6 +10,7 @@\n context a\n context b\n-removed line\n+added line\n+added two\n context c\n",
}]
# hunk starts at old 10 / new 10:
#   " context a"   -> old 10, new 10
#   " context b"   -> old 11, new 11
#   "-removed"     -> old 12
#   "+added line"  -> new 12
#   "+added two"   -> new 13
#   " context c"   -> old 13, new 14
check("added line resolves to new_line only",
      post.find_position(DIFF, "src/thing.ts", 12) == {"new_line": 12},
      post.find_position(DIFF, "src/thing.ts", 12))
check("context line resolves to old_line + new_line",
      post.find_position(DIFF, "src/thing.ts", 11) == {"old_line": 11, "new_line": 11},
      post.find_position(DIFF, "src/thing.ts", 11))
check("context line after the hunk keeps both",
      post.find_position(DIFF, "src/thing.ts", 14) == {"old_line": 13, "new_line": 14},
      post.find_position(DIFF, "src/thing.ts", 14))
check("line outside the hunks returns None",
      post.find_position(DIFF, "src/thing.ts", 999) is None)
check("unknown path returns None",
      post.find_position(DIFF, "src/other.ts", 12) is None)
check("a malformed hunk header does not crash",
      post.find_position([{"new_path": "a", "diff": "@@ garbage @@\n+x\n"}], "a", 1) is None)

# ---- 2. the POST/DELETE command shape carries the traps' fixes
import unittest.mock as mock
with mock.patch("subprocess.run") as r:
    r.return_value = mock.Mock(returncode=0, stdout="{}", stderr="")
    post.api("projects/1/x", method="DELETE", host="h.example")
    cmd = r.call_args[0][0]
    sent = r.call_args[1].get("input")
check("DELETE sends a body (an empty one hangs glab)", sent == "{}", sent)
check("json content-type header present",
      "Content-Type: application/json" in cmd, cmd)
check("body goes through --input, not -f position[...]",
      "--input" in cmd and not any("position[" in c for c in cmd), cmd)
check("host passed as --hostname", "--hostname" in cmd and "h.example" in cmd, cmd)

# ---- 3. env vars and defaults
pre = load("prefetch_mr")
check("MR_SCRATCH default is the documented one",
      pre.SCRATCH == "~/mr-review-scratch", pre.SCRATCH)
os.environ["MR_SCRATCH"] = "/tmp/mentis-test-scratch"
os.environ["GITLAB_HOST"] = "h.example"
pre2 = load("prefetch_mr")
check("MR_SCRATCH read from the environment",
      pre2.SCRATCH == "/tmp/mentis-test-scratch", pre2.SCRATCH)
check("GITLAB_HOST read from the environment", pre2.HOST == "h.example", pre2.HOST)
del os.environ["MR_SCRATCH"], os.environ["GITLAB_HOST"]

# ---- 4. usage guards and clean errors, as real subprocesses
for name, args, expect in [
    ("prefetch_mr", [], "usage:"),
    ("search_blobs", ["repo"], "usage:"),
    ("post_mr_comments", ["--file"], "usage:"),
]:
    r = run([f"{BIN}/{name}.py"] + args)
    check(f"{name} usage guard exits non-zero with a usage line",
          r.returncode != 0 and expect in (r.stderr + r.stdout), (r.returncode, r.stderr[:60]))

r = run([f"{BIN}/post_mr_comments.py", "--file", "/tmp/mentis-does-not-exist.json"])
check("missing payload file gives a clean error, no traceback",
      r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:80])

with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
    fh.write("{not json")
    bad = fh.name
r = run([f"{BIN}/post_mr_comments.py", "--file", bad])
check("malformed payload gives a clean error, no traceback",
      r.returncode != 0 and "Traceback" not in r.stderr, r.stderr[:80])
os.unlink(bad)

# ---- 5. shebang + exec bit: runnable directly on Linux
for name in ("prefetch_mr", "search_blobs", "post_mr_comments"):
    p = f"{BIN}/{name}.py"
    first = io.open(p, encoding="utf-8").readline().strip()
    check(f"{name} has a shebang and is executable",
          first == "#!/usr/bin/env python3" and os.access(p, os.X_OK), first)
r = subprocess.run([f"{BIN}/prefetch_mr.py"], capture_output=True, text=True)
check("runs as ./prefetch_mr.py (shebang honoured)",
      "usage:" in (r.stderr + r.stdout), r.stderr[:60])

# ---- 6. no CRLF: these run on Linux
for name in ("prefetch_mr", "search_blobs", "post_mr_comments"):
    check(f"{name} has LF endings only",
          b"\r\n" not in io.open(f"{BIN}/{name}.py", "rb").read())

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
