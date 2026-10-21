#!/usr/bin/env python3
"""Render selected blocks into the rule formats other coding agents read.

Rule D of the sourcing programme says block substance is harness-neutral and the harness-specific
parts stay at the edges. This script is that edge for two targets, and it is a pilot: two blocks
(`export/manifest.json`), two targets, golden files, a `--check` that pre-push can run.

Targets:
- `agents-md`: one `AGENTS.md`, a section per block.
- `cursor`: one `.cursor/rules/<name>.mdc` per block (a block with inlined references becomes one rule
  for `SKILL.md` plus one per reference, since Cursor recommends rules under 500 lines), with `description` and `globs` taken from the
  manifest. The `globs` spelling (a comma-separated string) is our reading of the format and has
  not been run against the tool: 🟡.

What it does to a block: drops the frontmatter, keeps `description` as the "when" line, drops the
`# title` line (the section heading replaces it) and demotes the remaining headings by one level.
A manifest entry with `"references": "inline"` also appends the block's `references/NN-*.md` files
(never `origin.md`) as sub-sections, because for those blocks the rules live there. Links that would
dangle outside this repo (other blocks, `WORKFLOW.md`, references that were not inlined) are listed on
stderr so the gap is visible instead of silent.

No dependency (this repo installs nothing to test itself), and the output is deterministic, so a
byte comparison against `export/golden/` is a valid check.

Usage:
    python3 bin/export_rules.py --target agents-md --out ./some-project
    python3 bin/export_rules.py --target cursor --out ./some-project
    python3 bin/export_rules.py --check              # compare both targets with export/golden/
    python3 bin/export_rules.py --write-golden       # refresh export/golden/ after a deliberate change
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "export" / "manifest.json"
GOLDEN = REPO / "export" / "golden"
TARGETS = ("agents-md", "cursor")
LARGE_OUTPUT = 20000
LINK = re.compile(r"\]\((\.{0,2}/?[^)\s#]+\.md)(?:#[^)]*)?\)")
BARE_REPO_DOC = re.compile(r"`((?:WORKFLOW|CONVENTIONS|CATALOG)\.md)`")


class ExportError(Exception):
    pass


def split_frontmatter(text: str, label: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ExportError(f"{label}: no frontmatter")
    end = text.find("\n---\n", 3)
    if end == -1:
        raise ExportError(f"{label}: frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in text[4:end].split("\n"):
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key.strip()] = value
    body = text[end + 5:]
    for key in ("name", "description"):
        if not fields.get(key):
            raise ExportError(f"{label}: frontmatter has no {key}")
    return fields, body


def demote_headings(body: str) -> str:
    out = []
    in_fence = False
    for line in body.split("\n"):
        if line.startswith("```"):
            in_fence = not in_fence
        if not in_fence and re.match(r"^#{1,5} ", line):
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def drop_title(body: str) -> str:
    lines = body.lstrip("\n").split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip("\n")


def load_manifest() -> list[dict]:
    try:
        data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ExportError(f"missing {MANIFEST.relative_to(REPO)}")
    blocks = data.get("blocks")
    if not isinstance(blocks, list) or not blocks:
        raise ExportError("manifest has no blocks")
    for entry in blocks:
        if not entry.get("name"):
            raise ExportError("manifest entry without a name")
        if not isinstance(entry.get("globs", []), list):
            raise ExportError(f"{entry['name']}: globs must be a list")
    return blocks


def read_block(entry: dict) -> tuple[str, str, str, list[str], list[tuple[str, str, str]]]:
    name = entry["name"]
    path = REPO / "skills" / name / "SKILL.md"
    if not path.is_file():
        raise ExportError(f"{name}: skills/{name}/SKILL.md does not exist")
    fields, body = split_frontmatter(path.read_text(encoding="utf-8"), name)
    if fields["name"] != name:
        raise ExportError(f"{name}: frontmatter name is {fields['name']!r}")
    body = drop_title(body)
    inlined: dict[str, str] = {}
    parts: list[tuple[str, str, str]] = []
    if entry.get("references") == "inline":
        extra = []
        for ref in sorted((REPO / "skills" / name / "references").glob("[0-9][0-9]-*.md")):
            ref_lines = ref.read_text(encoding="utf-8").strip("\n").split("\n")
            match = re.match(r"^# (?:.*? )?\u00a7 ?(\d+) \u2014 (.*)$", ref_lines[0])
            if not match:
                raise ExportError(f"{name}: {ref.name} first line is not a reference title")
            title = f"Part {match.group(1)}: {match.group(2)}"
            rest = "\n".join(ref_lines[1:]).strip("\n")
            extra.append(f"## {title}\n\n{rest}")
            parts.append((ref.stem, title, rest))
            inlined[f"./references/{ref.name}"] = f"Part {match.group(1)}"
        body = body + "\n\n" + "\n\n".join(extra)
        for target, label in inlined.items():
            body = re.sub(r"\[([^\]]*)\]\(" + re.escape(target) + r"\)", lambda m, l=label: f"{m.group(1)} ({l}, below)", body)
    dangling = sorted((set(LINK.findall(body)) | set(BARE_REPO_DOC.findall(body))) - set(inlined))
    return name, fields["description"], body, dangling, parts


def render_agents_md(blocks: list[tuple[str, str, str, list[str]]]) -> str:
    parts = [
        "# Rules exported from mentis",
        "",
        "Generated by `bin/export_rules.py`; edit the block in `skills/`, not this file.",
        "Each section is one block. Files under `references/` are not inlined.",
        "",
    ]
    for name, description, body, _, _ in blocks:
        parts += [f"## {name}", "", f"When: {description}", "", demote_headings(body), ""]
    return "\n".join(parts).rstrip("\n") + "\n"


def render_cursor(name: str, description: str, body: str, globs: list[str]) -> str:
    head = ["---", f"description: {json.dumps(description, ensure_ascii=False)}"]
    if globs:
        head.append("globs: " + ", ".join(globs))
    head += ["alwaysApply: false", "---", ""]
    return "\n".join(head) + body.strip("\n") + "\n"


def render_all() -> tuple[dict[str, dict[str, str]], dict[str, list[str]]]:
    entries = load_manifest()
    blocks = [read_block(e) for e in entries]
    files: dict[str, dict[str, str]] = {
        "agents-md": {"AGENTS.md": render_agents_md(blocks)},
        "cursor": {},
    }
    for entry, (name, description, body, _, parts) in zip(entries, blocks):
        globs = entry.get("globs", [])
        if parts:
            main = body[: body.index(f"\n\n## {parts[0][1]}")]
            files["cursor"][f".cursor/rules/{name}.mdc"] = render_cursor(name, description, main, globs)
            for stem, title, rest in parts:
                files["cursor"][f".cursor/rules/{name}-{stem}.mdc"] = render_cursor(
                    name, f"{description} ({title})", f"# {title}\n\n{rest}", globs
                )
        else:
            files["cursor"][f".cursor/rules/{name}.mdc"] = render_cursor(name, description, body, globs)
    warnings = {name: dangling for name, _, _, dangling, _ in blocks if dangling}
    return files, warnings


def write_tree(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def check() -> int:
    files, _ = render_all()
    bad = 0
    for target in TARGETS:
        for rel, text in files[target].items():
            golden = GOLDEN / target / rel
            if not golden.is_file():
                print(f"MISSING golden: {golden.relative_to(REPO)}")
                bad += 1
            elif golden.read_text(encoding="utf-8") != text:
                print(f"DIFF golden: {golden.relative_to(REPO)}")
                bad += 1
    expected = {target: set(files[target]) for target in TARGETS}
    for target in TARGETS:
        base = GOLDEN / target
        if base.is_dir():
            for path in base.rglob("*"):
                if path.is_file() and path.relative_to(base).as_posix() not in expected[target]:
                    print(f"STALE golden: {path.relative_to(REPO)}")
                    bad += 1
    print("export check: " + ("ok" if not bad else f"{bad} problem(s); run --write-golden if deliberate"))
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--target", choices=TARGETS)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write-golden", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.check:
            return check()
        files, warnings = render_all()
        for target_name, rendered in files.items():
            for rel, text in rendered.items():
                if len(text) > LARGE_OUTPUT:
                    print(f"warning: {rel} is {len(text)} characters; an agent reads it in full each session, "
                          f"so keep the blocks short or drop \"references\": \"inline\"", file=sys.stderr)
        for name, dangling in warnings.items():
            print(f"warning: {name} links outside the export: {', '.join(dangling)}", file=sys.stderr)
        if args.write_golden:
            for target in TARGETS:
                base = GOLDEN / target
                if base.is_dir():
                    for path in sorted(base.rglob("*"), reverse=True):
                        path.unlink() if path.is_file() else path.rmdir()
                write_tree(base, files[target])
            print(f"wrote {GOLDEN.relative_to(REPO)}")
            return 0
        if not args.target or not args.out:
            parser.error("--target and --out are required (or use --check / --write-golden)")
        write_tree(args.out, files[args.target])
        for rel in files[args.target]:
            print(f"wrote {args.out / rel}")
        return 0
    except ExportError as exc:
        print(f"export: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
