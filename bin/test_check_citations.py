#!/usr/bin/env python3
"""Checks bin/check_citations.py, and that this repo's own citations all resolve:

    python3 bin/test_check_citations.py

What it actually proves, since a wrong citation is invisible in review: that every `§N.M` in
the repo points at a section that exists and at a point inside it, and that the checker still
catches the four ways a citation goes wrong — a missing section, a point past the end of a
section, a name that is not a block, and a number attributed to the wrong block because the
prose named someone else first. The attribution rules are checked against fixtures rather
than against the repo, so tightening one of them cannot quietly stop finding anything.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

BIN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BIN)
SCRIPT = f"{BIN}/check_citations.py"
ok = fail = 0


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"PASS  {label}")
    else:
        fail += 1
        print(f"FAIL  {label} {detail}")


def run(*args, cwd=ROOT):
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True,
                          cwd=cwd)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def fixture(prose, *, sections=("# § 1 — One\n\n1. first\n2. second\n",), extra=None):
    """a two-block repo: skills/target with sections, skills/citer holding the prose."""
    root = tempfile.mkdtemp(prefix="citations-")
    write(f"{root}/skills/target/SKILL.md", "# target\n\nRouter.\n")
    for number, body in enumerate(sections, start=1):
        write(f"{root}/skills/target/references/{number:02d}-section.md", body)
    write(f"{root}/skills/citer/SKILL.md", f"# citer\n\n{prose}\n")
    write(f"{root}/skills/citer/references/01-only.md", "# § 1 — Only\n\n1. first\n")
    for name, body in (extra or {}).items():
        write(f"{root}/{name}", body)
    return root


def unresolved(prose, **kwargs):
    root = fixture(prose, **kwargs)
    try:
        result = run("--json", "--root", root)
        return json.loads(result.stdout)["unresolved"]
    finally:
        shutil.rmtree(root, ignore_errors=True)


live = run()
check("the script runs and exits 0", live.returncode == 0, live.stderr.strip()[:200])
check("every citation in this repo resolves", "0 unresolved" in live.stdout,
      live.stdout.strip().split("\n")[-1])

as_json = run("--json")
payload = json.loads(as_json.stdout) if as_json.stdout.strip().startswith("{") else {}
check("--json emits the same verdict", payload.get("unresolved") == [], as_json.stdout[:200])
check("--json counts every block", payload.get("blocks", 0) >= 80, payload.get("blocks"))
check("--json counts more than a thousand citations", payload.get("citations", 0) > 1000,
      payload.get("citations"))

bad = run("--nope")
check("an unknown flag is refused rather than ignored", bad.returncode == 2, bad.returncode)

misses = unresolved("The rule is `target` §4.")
check("a citation of a section that does not exist is caught",
      len(misses) == 1 and "no section 4" in misses[0]["reason"], misses)

misses = unresolved("The rule is `target` §1.9.")
check("a point past the end of a section is caught",
      len(misses) == 1 and "stops at point 2" in misses[0]["reason"], misses)

misses = unresolved("The rule is `skills/gone` §1.")
check("a name that is not a block is caught",
      len(misses) == 1 and "no block called" in misses[0]["reason"], misses)

misses = unresolved("`target` also says it, and §1.1 here covers the rest.")
check("a `here` marker keeps the citation local", misses == [], misses)

misses = unresolved("`target` §1.1 is the one, and §1.7 is ours.")
check("a citation after a named block belongs to that block, points included",
      len(misses) == 1 and "target" in misses[0]["reason"], misses)

misses = unresolved("§1 kept its number (`target` cites it) and §1.1 stayed put.")
check("a name inside a closed parenthetical stops claiming the next citation", misses == [],
      misses)

misses = unresolved("As `target` says. §9 is a different thing.")
check("a sentence break gives the citation back to the citing block",
      len(misses) == 1 and "skills/citer" in misses[0]["reason"], misses)

misses = unresolved("Stamped in `references/notes.md` §4 rather than here.")
check("a document name takes the citation out of scope", misses == [], misses)

misses = unresolved("The rule is target §1.9.")
check("a block named without backticks claims the citation too",
      len(misses) == 1 and "stops at point" in misses[0]["reason"], misses)

misses = unresolved(
    "See `target` §2.3.",
    sections=("# § 1 — One\n\n1. first\n",
              "# target §2 — Two\n\n1. first\n2. second\n3. third\n"),
)
check("both section-heading shapes are read", misses == [], misses)

root = fixture("See `inline` §2.2.", extra={
    "skills/inline/SKILL.md": "# inline\n\n### 1. First\n\n1. one\n\n### 2. Second\n\n"
                              "1. one\n2. two\n",
})
try:
    result = json.loads(run("--json", "--root", root).stdout)
    check("an inline-sectioned single-file block declares its sections",
          result["unresolved"] == [], result["unresolved"])
finally:
    shutil.rmtree(root, ignore_errors=True)

with open(SCRIPT, "rb") as fh:
    raw = fh.read()
check("check_citations.py has a shebang", raw.startswith(b"#!/usr/bin/env python3"))
check("check_citations.py has LF endings only", b"\r\n" not in raw)
check("check_citations.py is executable", os.access(SCRIPT, os.X_OK))

with open(f"{ROOT}/bin/pre-push", encoding="utf-8") as fh:
    check("the gate runs this suite", "bin/test_check_citations.py" in fh.read())

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
