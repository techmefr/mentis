#!/usr/bin/env python3
"""Checks bin/measure_depth.py and, more importantly, that CATALOG.md's depth table still
matches what it computes:

    python3 bin/test_measure_depth.py

What it actually proves, because these are the parts that fail silently rather than loudly:
that every block a row names exists (a rename would otherwise drop a block from a total and
the total would still look plausible), that no block is counted in two rows, that the count
excludes the frontmatter and `origin.md` the way the convention says, that the arithmetic in
the table is the arithmetic the script does, and that the table in CATALOG.md is the script's
output rather than a figure somebody typed. That last one is the whole point: the table
drifted twice by being written from memory.
"""
import importlib.util
import json
import os
import subprocess
import sys

BIN = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BIN)
SAMPLE = "skills/code-baseline"
ok = fail = 0


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"PASS  {label}")
    else:
        fail += 1
        print(f"FAIL  {label} {detail}")


def words(path):
    with open(path, encoding="utf-8") as fh:
        return len(fh.read().split())


def run(*args):
    return subprocess.run([sys.executable, f"{BIN}/measure_depth.py", *args],
                          capture_output=True, text=True, cwd=ROOT)


spec = importlib.util.spec_from_file_location("measure_depth", f"{BIN}/measure_depth.py")
md = importlib.util.module_from_spec(spec)
spec.loader.exec_module(md)

rows = md.measure()
with open(f"{ROOT}/CATALOG.md", encoding="utf-8") as fh:
    catalog = fh.read()

check("every row names at least one block", all(r["blocks"] for r in rows))

missing = [b for r in rows for b in r["blocks"]
           if not os.path.isfile(os.path.join(ROOT, b, "SKILL.md"))]
check("every block a row names exists", not missing, missing)

seen, dupes = {}, []
for r in rows:
    for b in r["blocks"]:
        if b in seen:
            dupes.append(f"{b} in {seen[b]} and {r['stack']}")
        seen[b] = r["stack"]
check("no block is counted in two rows", not dupes, dupes)

check("deficit is ours minus theirs",
      all(r["deficit"] == r["our_words"] - r["their_words"] for r in rows))
check("our_words is the sum of the per-block figures",
      all(r["our_words"] == sum(r["per_block"].values()) for r in rows))
try:
    md.block_words("skills/there-is-no-such-block")
    refused = False
except SystemExit:
    refused = True
check("a missing block is refused rather than counted as zero", refused)

# --- the counting convention, checked against an independently computed figure ---
skill = f"{ROOT}/{SAMPLE}/SKILL.md"
refs = f"{ROOT}/{SAMPLE}/references"
with open(skill, encoding="utf-8") as fh:
    text = fh.read()
end = text.find("\n---\n", 3)
router = len(text[end + 5:].split())
names = sorted(n for n in os.listdir(refs) if n.endswith(".md"))
sections = sum(words(f"{refs}/{n}") for n in names if n != "origin.md")
origin = words(f"{refs}/origin.md")
measured = md.block_words(SAMPLE)

check("the sample block has a frontmatter block to skip", end != -1)
check("the sample block has a non-empty origin.md to exclude", origin > 100)
check("the count is the router body plus the sections", measured == router + sections)
check("origin.md is genuinely left out", measured != router + sections + origin)
check("the frontmatter is genuinely left out", measured != len(text.split()) + sections)

# --- the table in CATALOG.md is this script's output, not a typed figure ---
printed = run()
check("the script runs and exits 0", printed.returncode == 0, printed.stderr[-300:])
table_lines = [l for l in printed.stdout.splitlines()
               if l.startswith("| ") and " / " in l and "their skills" not in l]
check("the script prints one row per declared stack", len(table_lines) == len(rows),
      f"{len(table_lines)} lines for {len(rows)} rows")
absent = [l for l in table_lines if l not in catalog]
check("every table row in CATALOG.md matches the measured figures", not absent, absent[:2])

comp_lines = [l for l in printed.stdout.splitlines()
              if l and not l.startswith("|") and ": " in l]
check("the script prints one composition line per stack", len(comp_lines) == len(rows),
      f"{len(comp_lines)} lines")
comp_absent = [l for l in comp_lines if l not in catalog]
check("every row's composition is recorded in CATALOG.md", not comp_absent, comp_absent[:2])

as_json = run("--json")
check("--json exits 0 and emits valid JSON",
      as_json.returncode == 0 and isinstance(json.loads(as_json.stdout or "0"), list))
check("an unknown flag is refused rather than ignored", run("--nope").returncode != 0)

with open(f"{BIN}/measure_depth.py", "rb") as fh:
    raw = fh.read()
check("measure_depth.py has a shebang", raw.startswith(b"#!/usr/bin/env python3"))
check("measure_depth.py has LF endings only", b"\r\n" not in raw)
check("measure_depth.py is executable", os.access(f"{BIN}/measure_depth.py", os.X_OK))

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
