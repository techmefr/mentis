#!/usr/bin/env python3
"""Checks the rule exporter. No network, no dependency:

    python3 bin/test_export_rules.py

What it proves: the committed golden files match what the exporter renders today (the same call
`pre-push` relies on), rendering is deterministic, the frontmatter is gone from the output, the
title line is replaced by the section heading, headings are demoted, the Cursor files carry the
manifest globs, and bad input fails loudly instead of producing a partial export.
"""
import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("export_rules", REPO / "bin" / "export_rules.py")
export_rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export_rules)

ok = fail = 0


def check(label, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"PASS  {label}")
    else:
        fail += 1
        print(f"FAIL  {label} {detail}")


files, warnings = export_rules.render_all()
again, _ = export_rules.render_all()
check("rendering is deterministic", files == again)

agents = files["agents-md"]["AGENTS.md"]
check("AGENTS.md has one section per manifest block",
      "## laravel-no-observers" in agents and "## accessibility" in agents)
check("AGENTS.md carries no frontmatter delimiter line", "\n---\nname:" not in agents)
check("AGENTS.md keeps the 'when' line", "When: Use when a model needs to react" in agents)
check("source title line is replaced by the section heading", "\n# laravel-no-observers" not in agents)
check("body headings are demoted one level", "\n### " in agents and "\n## When" not in agents)

mdc = files["cursor"][".cursor/rules/laravel-no-observers.mdc"]
check("cursor file opens with frontmatter", mdc.startswith("---\ndescription: \""))
check("cursor file carries the manifest globs", "\nglobs: app/**/*.php\n" in mdc)
check("cursor file is never always-on", "\nalwaysApply: false\n" in mdc)
check("cursor file has one block per manifest entry", len(files["cursor"]) == 2)

rc = subprocess.run([sys.executable, str(REPO / "bin" / "export_rules.py"), "--check"],
                    capture_output=True, text=True).returncode
check("golden files match the exporter (--check)", rc == 0)

with tempfile.TemporaryDirectory() as tmp:
    rc = subprocess.run([sys.executable, str(REPO / "bin" / "export_rules.py"),
                         "--target", "cursor", "--out", tmp], capture_output=True, text=True).returncode
    written = sorted(p.name for p in Path(tmp).rglob("*.mdc"))
    check("--target cursor --out writes the files", rc == 0 and len(written) == 2, written)

fm, body = export_rules.split_frontmatter('---\nname: x\ndescription: "Use when: a"\n---\n# x\nbody\n', "x")
check("quoted description with a colon parses", fm["description"] == "Use when: a")
for label, text in (("no frontmatter", "# x\n"), ("unclosed", "---\nname: x\n"),
                    ("no description", "---\nname: x\n---\nbody\n")):
    try:
        export_rules.split_frontmatter(text, "x")
        check(f"{label} is refused", False)
    except export_rules.ExportError:
        check(f"{label} is refused", True)

check("headings inside code fences are not demoted",
      export_rules.demote_headings("```\n## keep\n```\n## move") == "```\n## keep\n```\n### move")

saved = export_rules.MANIFEST
try:
    with tempfile.TemporaryDirectory() as tmp:
        bad = Path(tmp) / "m.json"
        bad.write_text('{"blocks": [{"name": "does-not-exist"}]}', encoding="utf-8")
        export_rules.MANIFEST = bad
        try:
            export_rules.render_all()
            check("unknown block fails the export", False)
        except export_rules.ExportError:
            check("unknown block fails the export", True)
finally:
    export_rules.MANIFEST = saved

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
