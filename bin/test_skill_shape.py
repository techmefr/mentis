#!/usr/bin/env python3
"""Checks the shape rules of `skills/writing-skills` points 39 and 12 of the vendor guide. No network:

    python3 bin/test_skill_shape.py

A `SKILL.md` body stays under 500 lines, and a reference file past 100 lines opens with a contents list
(provenance files, `origin.md`, are exempt: they are read to trace a source, never to apply a rule).
The rule functions are exercised on synthetic good and bad text first, so a loosened rule fails here.
"""
import glob
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BODY_MAX = 500
REFERENCE_TOC_FROM = 100
ok = fail = 0


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
    else:
        fail += 1
        print(f"FAIL  {label} {detail}")


def lines_of(text):
    return text.count("\n") + 1


def has_contents(text):
    return re.search(r"(?im)^#{1,3}\s*(contents|table of contents|sommaire)\s*$", text[:4000]) is not None


def reference_problem(name, text):
    if name == "origin.md" or lines_of(text) <= REFERENCE_TOC_FROM:
        return None
    return None if has_contents(text) else "no contents list"


check("synthetic: 501-line body is refused", lines_of("x\n" * 500) > BODY_MAX)
check("synthetic: long reference without contents is refused", reference_problem("a.md", "x\n" * 150) is not None)
check("synthetic: long reference with contents passes", reference_problem("a.md", "# T\n\n## Contents\n\n- a\n" + "x\n" * 150) is None)
check("synthetic: origin file is exempt", reference_problem("origin.md", "x\n" * 150) is None)
check("synthetic: short reference passes", reference_problem("a.md", "x\n" * 50) is None)

for path in sorted(glob.glob(os.path.join(REPO, "skills", "*", "SKILL.md")) + glob.glob(os.path.join(REPO, "business", "*", "SKILL.md"))):
    text = open(path, encoding="utf-8").read()
    rel = os.path.relpath(path, REPO)
    check(f"{rel} body within {BODY_MAX} lines", lines_of(text) <= BODY_MAX, f"({lines_of(text)} lines)")

for path in sorted(glob.glob(os.path.join(REPO, "skills", "*", "references", "*.md")) + glob.glob(os.path.join(REPO, "business", "*", "references", "*.md"))):
    text = open(path, encoding="utf-8").read()
    rel = os.path.relpath(path, REPO)
    problem = reference_problem(os.path.basename(path), text)
    check(f"{rel} contents list", problem is None, f"({problem})")

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
