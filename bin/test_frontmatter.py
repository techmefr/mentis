#!/usr/bin/env python3
"""Checks that every block's frontmatter is machine-readable. No network, no fixtures:

    python3 bin/test_frontmatter.py

Why this suite exists: on 2026-09-07, 63 of the 109 blocks in this repo had frontmatter that a
real YAML parser refuses, because a `description` containing `: ` was left unquoted. Claude Code's
own reader is lenient and every block loaded fine, so nothing surfaced it — and `bin/install_agents.py`
plus `skills/distributing-blocks` mean a consumer parses these files with whatever they have. A
block nobody can parse is a block nobody can install.

Since 2026-10-19 it also enforces the constraints the open Agent Skills specification states for
`name`, `description`, `compatibility`, `metadata` and `allowed-tools` (rewritten here, no dependency on
the specification's reference validator), because they held only by habit across the blocks. The rule
functions are exercised on synthetic good and bad values first, so a loosened rule fails this suite.

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


NAME_MAX = 64
DESCRIPTION_MAX = 1024
COMPATIBILITY_MAX = 500


def name_problems(name, directory=None):
    """The spec's `name` rules; `directory` is the parent directory name, None for a file that is no skill."""
    found = []
    if not isinstance(name, str) or not name:
        return ["name is empty or not a string"]
    if len(name) > NAME_MAX:
        found.append(f"longer than {NAME_MAX} characters")
    if any(not (c == "-" or (c.isalnum() and c.lower() == c)) for c in name):
        found.append("characters other than lowercase letters, digits and hyphens")
    if name.startswith("-") or name.endswith("-"):
        found.append("starts or ends with a hyphen")
    if "--" in name:
        found.append("consecutive hyphens")
    if directory is not None and name != directory:
        found.append(f"does not match its directory `{directory}`")
    return found


def description_problems(description):
    if not isinstance(description, str) or not description.strip():
        return ["description is empty or not a string"]
    if len(description) > DESCRIPTION_MAX:
        return [f"longer than {DESCRIPTION_MAX} characters ({len(description)})"]
    return []


def compatibility_problems(value):
    if not isinstance(value, str) or not value.strip():
        return ["compatibility is empty or not a string"]
    if len(value) > COMPATIBILITY_MAX:
        return [f"longer than {COMPATIBILITY_MAX} characters ({len(value)})"]
    return []


def metadata_problems(value):
    if not isinstance(value, dict):
        return ["metadata is not a mapping"]
    if any(not isinstance(k, str) or not isinstance(v, str) for k, v in value.items()):
        return ["metadata keys and values must all be strings"]
    return []


def allowed_tools_problems(value):
    if not isinstance(value, str):
        return ["allowed-tools must be a space-separated string, not a list or mapping"]
    if not value.strip():
        return ["allowed-tools is empty"]
    return []


def self_test():
    cases = [
        ("a plain name passes", not name_problems("pdf-processing", "pdf-processing")),
        ("digits pass", not name_problems("s3-backup2", "s3-backup2")),
        ("64 characters pass", not name_problems("a" * 64, "a" * 64)),
        ("65 characters fail", bool(name_problems("a" * 65, "a" * 65))),
        ("uppercase fails", bool(name_problems("PDF-Processing", "PDF-Processing"))),
        ("underscore fails", bool(name_problems("pdf_processing", "pdf_processing"))),
        ("space fails", bool(name_problems("pdf processing", "pdf processing"))),
        ("leading hyphen fails", bool(name_problems("-pdf", "-pdf"))),
        ("trailing hyphen fails", bool(name_problems("pdf-", "pdf-"))),
        ("consecutive hyphens fail", bool(name_problems("pdf--processing", "pdf--processing"))),
        ("a directory mismatch fails", bool(name_problems("pdf-processing", "pdf"))),
        ("no directory means no match rule", not name_problems("code-reviewer", None)),
        ("an empty name fails", bool(name_problems("", "x"))),
        ("a non-string name fails", bool(name_problems(12, "12"))),
        ("a description passes", not description_problems("Use when handling PDFs.")),
        ("1024 characters pass", not description_problems("x" * 1024)),
        ("1025 characters fail", bool(description_problems("x" * 1025))),
        ("a blank description fails", bool(description_problems("   "))),
        ("a non-string description fails", bool(description_problems(["a"]))),
        ("500 compatibility characters pass", not compatibility_problems("x" * 500)),
        ("501 compatibility characters fail", bool(compatibility_problems("x" * 501))),
        ("an empty compatibility fails", bool(compatibility_problems(""))),
        ("string metadata passes", not metadata_problems({"author": "a", "version": "1.0"})),
        ("a non-string metadata value fails", bool(metadata_problems({"version": 1.0}))),
        ("a list as metadata fails", bool(metadata_problems(["a"]))),
        ("space-separated allowed-tools passes", not allowed_tools_problems("Bash(git:*) Read")),
        ("a list as allowed-tools fails", bool(allowed_tools_problems(["Bash", "Read"]))),
        ("an empty allowed-tools fails", bool(allowed_tools_problems("  "))),
    ]
    for label, cond in cases:
        check(f"rule self-test: {label}", cond)


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


self_test()

paths = blocks()
check("the repo has blocks to check", len(paths) > 0, f"found {len(paths)}")

no_fm, not_mapping, bad_yaml, colon, missing_key, wrong_type = [], [], [], [], [], []
bad_name, bad_description, bad_optional = [], [], []

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

    directory = os.path.basename(os.path.dirname(path)) if os.path.basename(path) == "SKILL.md" else None
    if "name" in data:
        bad_name.extend(f"{rel}: {p}" for p in name_problems(data["name"], directory))
    if "description" in data:
        bad_description.extend(f"{rel}: {p}" for p in description_problems(data["description"]))
    for key, rule in (("compatibility", compatibility_problems), ("metadata", metadata_problems),
                      ("allowed-tools", allowed_tools_problems)):
        if key in data:
            bad_optional.extend(f"{rel} ({key}): {p}" for p in rule(data[key]))

check("every block opens and closes its frontmatter", not no_fm, str(no_fm[:5]))
check("no value carries an unquoted `: ` (the 2026-09-07 defect)", not colon, str(colon[:5]))
check("every frontmatter parses as YAML", not bad_yaml, str(bad_yaml[:5]))
check("every frontmatter parses as a mapping", not not_mapping, str(not_mapping[:5]))
check("every block declares name and description", not missing_key, str(missing_key[:5]))
check("name and description are non-empty strings", not wrong_type, str(wrong_type[:5]))

check("every name follows the spec: length, charset, hyphens, equals its directory", not bad_name, str(bad_name[:5]))
check("every description is non-empty and within 1024 characters", not bad_description, str(bad_description[:5]))
check("compatibility, metadata and allowed-tools, where declared, follow the spec", not bad_optional, str(bad_optional[:5]))

if yaml is None:
    print("NOTE  pyyaml not importable: the parser-based checks were skipped, "
          "the parser-free ones ran. Nothing was installed to get around it.")

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
