#!/usr/bin/env python3
"""Checks that every block's frontmatter is machine-readable. No network, no fixtures:

    python3 bin/test_frontmatter.py

Why this suite exists: on 2026-09-07, 63 of the 109 blocks in this repo had frontmatter that a
real YAML parser refuses, because a `description` containing `: ` was left unquoted. Claude Code's
own reader is lenient and every block loaded fine, so nothing surfaced it — and `bin/install_agents.py`
plus `skills/distributing-blocks` mean a consumer parses these files with whatever they have. A
block nobody can parse is a block nobody can install.

What it proves: the frontmatter delimiters are where they should be, the block parses as a mapping,
`name` and `description` are present and are strings, and no value carries the specific shape that
broke here. `pyyaml` is used when it is importable and the parser-free checks still run without it —
this repo installs nothing to test itself.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_-]*:")
ok = fail = 0

try:
    import yaml
except ImportError:
    yaml = None


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"PASS  {label}")
    else:
        fail += 1
        print(f"FAIL  {label} {detail}")


def blocks():
    """Every file in this repo that carries a frontmatter contract."""
    found = []
    agents = os.path.join(REPO, "agents")
    if os.path.isdir(agents):
        for name in sorted(os.listdir(agents)):
            if name.endswith(".md"):
                found.append(os.path.join(agents, name))
    for layer in ("skills", "business"):
        root = os.path.join(REPO, layer)
        if not os.path.isdir(root):
            continue
        for name in sorted(os.listdir(root)):
            path = os.path.join(root, name, "SKILL.md")
            if os.path.isfile(path):
                found.append(path)
    return found


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 3)
    return None if end == -1 else text[4:end + 1]


def unquoted_colon(fm):
    """The exact defect: a plain scalar whose value contains `: `, which YAML reads as a mapping."""
    offenders = []
    for line in fm.split("\n"):
        if not KEY.match(line):
            continue
        value = line.split(":", 1)[1].strip()
        if not value or value.startswith(("\"", "'", "|", ">", "#", "[", "{")):
            continue
        if ": " in value or value.endswith(":"):
            offenders.append(line.split(":", 1)[0])
    return offenders


paths = blocks()
check("the repo has blocks to check", len(paths) > 0, f"found {len(paths)}")

no_fm, not_mapping, bad_yaml, colon, missing_key, wrong_type = [], [], [], [], [], []

for path in paths:
    rel = os.path.relpath(path, REPO)
    with open(path, encoding="utf-8") as handle:
        text = handle.read()

    fm = frontmatter(text)
    if fm is None:
        no_fm.append(rel)
        continue

    offenders = unquoted_colon(fm)
    if offenders:
        colon.append(f"{rel} ({', '.join(offenders)})")

    if yaml is None:
        data = None
    else:
        try:
            data = yaml.safe_load(fm)
        except Exception as exc:
            bad_yaml.append(f"{rel}: {str(exc).splitlines()[0]}")
            continue
        if not isinstance(data, dict):
            not_mapping.append(rel)
            continue

    if data is None:
        continue
    for key in ("name", "description"):
        if key not in data:
            missing_key.append(f"{rel} ({key})")
        elif not isinstance(data[key], str) or not data[key].strip():
            wrong_type.append(f"{rel} ({key})")

check("every block opens and closes its frontmatter", not no_fm, str(no_fm[:5]))
check("no value carries an unquoted `: ` (the 2026-09-07 defect)", not colon, str(colon[:5]))
check("every frontmatter parses as YAML", not bad_yaml, str(bad_yaml[:5]))
check("every frontmatter parses as a mapping", not not_mapping, str(not_mapping[:5]))
check("every block declares name and description", not missing_key, str(missing_key[:5]))
check("name and description are non-empty strings", not wrong_type, str(wrong_type[:5]))

if yaml is None:
    print("NOTE  pyyaml not importable: the parser-based checks were skipped, "
          "the parser-free ones ran. Nothing was installed to get around it.")

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
