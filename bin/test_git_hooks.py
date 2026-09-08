#!/usr/bin/env python3
"""Checks that this repo's test gate is actually wired to pushes:

    python3 bin/test_git_hooks.py

Why this suite exists. `bin/pre-push` is the gate; `.git/hooks/pre-push` is what git runs.
Until 2026-09-08 the installer put the gate in place with `cp`, so the hook was a **fork**
of the file, frozen at install time. Two suites added afterwards — `test_frontmatter.py`
(2026-09-07) and `test_rule_c.py` (2026-09-07) — therefore never gated a push in this
clone: the hook installed on 2026-08-11 kept announcing and running four suites, and it
said "all suites green" while doing so, which is the worst shape a stale guard can take.
It was only caught because a push was rejected for an unrelated reason and the hook's
output was read.

So what is checked here is not the gate's content — the other suites do that — but the
wiring: that the installer delegates instead of copying, that the shim it writes really
reaches `bin/pre-push`, that this clone's installed hook has not drifted, and that the
suite list inside `bin/pre-push` is declared once and announced honestly.

No network, nothing to install: a throwaway `git init` in a temp directory is the fixture.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

BIN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BIN)
INSTALLER = f"{BIN}/install-git-hooks.sh"
GATE = f"{BIN}/pre-push"
ok = fail = 0


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"PASS  {label}")
    else:
        fail += 1
        print(f"FAIL  {label} {detail}")


installer_src = io.open(INSTALLER, encoding="utf-8").read()
gate_src = io.open(GATE, encoding="utf-8").read()

# ---- 1. the installer delegates, it does not copy the gate
check("the installer does not cp bin/pre-push into the hook",
      not re.search(r"^\s*cp\s+.*\$src", installer_src, re.M),
      "a copied hook is a fork frozen at install time")
check("the installer writes a shim that execs bin/pre-push",
      "exec " in installer_src and "bin/pre-push" in installer_src)
check("the shim resolves the repo root at run time, not at install time",
      "git rev-parse --show-toplevel" in installer_src.split("SHIM")[1]
      if "SHIM" in installer_src else False)

# ---- 2. functional: install into a throwaway repo and run the hook
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["git", "init", "-q", tmp], check=True)
    os.makedirs(f"{tmp}/bin")
    shutil.copy2(GATE, f"{tmp}/bin/pre-push")
    shutil.copy2(INSTALLER, f"{tmp}/bin/install-git-hooks.sh")

    r = subprocess.run(["bash", f"{tmp}/bin/install-git-hooks.sh"],
                       cwd=tmp, capture_output=True, text=True)
    hook = f"{tmp}/.git/hooks/pre-push"
    check("the installer exits 0 and reports where it installed",
          r.returncode == 0 and "installed:" in r.stdout, r.stderr[:120])
    check("it produced an executable .git/hooks/pre-push",
          os.path.isfile(hook) and os.access(hook, os.X_OK))

    hook_src = io.open(hook, encoding="utf-8").read() if os.path.isfile(hook) else ""
    check("the installed hook is a shim, not a copy of the gate",
          len(hook_src) < len(gate_src) and "test_scripts.py" not in hook_src,
          f"{len(hook_src)} bytes vs gate {len(gate_src)}")

    # replace the gate with a marker so we can prove the shim reaches it
    with io.open(f"{tmp}/bin/pre-push", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("#!/usr/bin/env bash\necho REACHED-THE-GATE\n")
    os.chmod(f"{tmp}/bin/pre-push", 0o755)
    r = subprocess.run(["bash", hook], cwd=tmp, capture_output=True, text=True)
    check("running the hook reaches bin/pre-push",
          "REACHED-THE-GATE" in r.stdout, (r.stdout + r.stderr)[:120])

    # and a red gate must refuse the push
    with io.open(f"{tmp}/bin/pre-push", "w", encoding="utf-8", newline="\n") as fh:
        fh.write("#!/usr/bin/env bash\nexit 1\n")
    os.chmod(f"{tmp}/bin/pre-push", 0o755)
    r = subprocess.run(["bash", hook], cwd=tmp, capture_output=True, text=True)
    check("a failing gate makes the hook exit non-zero",
          r.returncode != 0, f"returncode {r.returncode}")

# ---- 3. this clone's own hook has not drifted
installed = os.path.join(
    subprocess.run(["git", "rev-parse", "--git-path", "hooks"], cwd=ROOT,
                   capture_output=True, text=True).stdout.strip(), "pre-push")
if not os.path.isabs(installed):
    installed = os.path.join(ROOT, installed)
if os.path.isfile(installed):
    live = io.open(installed, encoding="utf-8").read()
    check("this clone's installed hook delegates rather than duplicating the gate",
          "test_scripts.py" not in live,
          "it inlines the suite list, so it is a stale fork — run bin/install-git-hooks.sh")
else:
    check("this clone's installed hook delegates rather than duplicating the gate",
          True, "(no hook installed in this clone, nothing to drift)")

# ---- 4. the suite list is declared once and announced honestly
declared = re.search(r"suites=\(\s*(.*?)\s*\)", gate_src, re.S)
names = declared.group(1).split() if declared else []
check("bin/pre-push declares its suites in one list",
      bool(names), "no suites=( ... ) array found")
check("the announcement is derived from that list, not retyped",
      "${suites[*]}" in gate_src,
      "an echo with the names spelled out is a second place to forget one")
check("every suite it names exists in bin/",
      all(os.path.isfile(os.path.join(ROOT, n)) for n in names),
      str([n for n in names if not os.path.isfile(os.path.join(ROOT, n))]))
check("this suite is itself in the list",
      "bin/test_git_hooks.py" in names,
      "a gate check that the gate does not run is decoration")

# ---- 5. both files stay Linux-runnable
for path in (GATE, INSTALLER):
    rel = os.path.relpath(path, ROOT)
    first = io.open(path, encoding="utf-8").readline().strip()
    check(f"{rel} has a shebang and is executable",
          first == "#!/usr/bin/env bash" and os.access(path, os.X_OK), first)
    check(f"{rel} has LF endings only",
          b"\r\n" not in io.open(path, "rb").read())

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
