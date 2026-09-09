#!/usr/bin/env python3
"""Resolves every `§N` and `§N.M` citation in the repo against the block it points at.

    python3 bin/check_citations.py          # one line per unresolved citation
    python3 bin/check_citations.py --json   # machine-readable
    python3 bin/check_citations.py --list   # every citation and where it resolved

Why this exists: the repo cross-references itself by number, in prose, across 84 blocks —
and a number is the one kind of reference nothing checks. A section renumbered, a block
re-sectioned, a point removed, and the citation still reads perfectly while pointing at
nothing. `skills/maintaining-blocks` §1.3 has asked for exactly this check since it was
written; until now it had to be done by hand, which meant it was never done. Ten citations
were wrong the first time it ran.

A citation is a number, and the block it belongs to is not written down, so it has to be
attributed the way a reader attributes it. In order: `here` just after the number makes it
local; otherwise the nearest backquoted block name earlier on the line (or at the end of the
line above, since the prose wraps at about 105 characters) claims it, up to 90 characters
away; a sentence or clause break between that name and the number — or a closing parenthesis,
since a name inside a parenthetical stops claiming anything once it is closed — gives it back
to the citing block; and a backquoted name that is a document rather than a block, anything
ending in `.md` and the `agents/` files, takes the number out of scope, because those are that
document's own sections. A block name written without backticks immediately before the number
claims it too, which is how the source tables are written.

Exit code 0 when every citation resolves, 1 when at least one does not.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUPS = ("skills", "business")

CITATION = re.compile(r"§\s*(\d+)(?:\.(\d+))?")
FILE_SECTION = re.compile(r"^#\s+(?:[A-Za-z0-9._-]+\s+)?§\s*(\d+)\s*(?:[—–-]|$)")
INLINE_SECTION = re.compile(r"^#{2,4}\s+(?:§\s*)?(\d+)[.\s]")
POINT = re.compile(r"^(\d+)\. ")
QUOTED = re.compile(r"`([^`]+)`")
BARE_NAME = re.compile(r"([a-z][a-z0-9-]*(?:/[a-z][a-z0-9-]*)?)\s+$")
LOCAL_MARKER = re.compile(r"^\W{0,4}here\b", re.IGNORECASE)

NAME_REACH = 90
LOCAL_REACH = 12


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def block_dirs():
    for group in GROUPS:
        base = os.path.join(ROOT, group)
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if os.path.isfile(os.path.join(base, name, "SKILL.md")):
                yield "%s/%s" % (group, name)


def sections_of(block):
    """section number -> highest point number declared in it."""
    sections = {}
    refs = os.path.join(ROOT, block, "references")
    if os.path.isdir(refs):
        for name in sorted(os.listdir(refs)):
            if not name.endswith(".md") or name == "origin.md":
                continue
            lines = read(os.path.join(refs, name)).split("\n")
            heading = next((FILE_SECTION.match(ln) for ln in lines if ln.startswith("# ")), None)
            if not heading:
                continue
            points = [int(m.group(1)) for m in (POINT.match(ln) for ln in lines) if m]
            sections[int(heading.group(1))] = max(points) if points else 0
    lines = read(os.path.join(ROOT, block, "SKILL.md")).split("\n")
    current, points = None, []
    for line in lines:
        heading = INLINE_SECTION.match(line)
        if heading or line.startswith("#"):
            if current is not None and current not in sections:
                sections[current] = max(points) if points else 0
            current, points = (int(heading.group(1)) if heading else None), []
            continue
        point = POINT.match(line)
        if point and current is not None:
            points.append(int(point.group(1)))
    if current is not None and current not in sections:
        sections[current] = max(points) if points else 0
    return sections


def documents():
    """every markdown file in the repo, as paths relative to the root."""
    found = []
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in sorted(dirs) if not d.startswith(".") and d != "__pycache__"]
        for name in sorted(names):
            if name.endswith(".md"):
                found.append(os.path.relpath(os.path.join(base, name), ROOT))
    return found


def owning_block(path, blocks):
    parts = path.replace("\\", "/").split("/")
    if len(parts) >= 2 and "/".join(parts[:2]) in blocks:
        return "/".join(parts[:2])
    return None


def looks_like_a_document(name):
    return name.endswith(".md") or name.startswith("agents/") or name.startswith("bin/")


def resolve_name(name, blocks):
    if name in blocks:
        return name
    for block in blocks:
        if block.split("/")[-1] == name:
            return block
    return None


def attribute(before, citing, blocks):
    """(target block, unknown name) — either resolves to a block, or names what it could not.

    The backtick pairing is computed over the whole prefix rather than over the reach window:
    a window that starts inside a code span pairs its closing backtick with the next opening
    one and reads the prose between them as the name.
    """
    bare = BARE_NAME.search(before)
    if bare:
        named = resolve_name(bare.group(1), blocks)
        if named:
            return named, None
    names = [m for m in QUOTED.finditer(before) if len(before) - m.end() <= NAME_REACH]
    if not names:
        return citing, None
    last = names[-1]
    between = before[last.end():]
    if ". " in between or "; " in between or between.strip().endswith("."):
        return citing, None
    closing, opening = between.find(")"), between.find("(")
    if closing != -1 and (opening == -1 or closing < opening):
        return citing, None
    name = last.group(1).strip()
    if looks_like_a_document(name):
        return None, None
    resolved = resolve_name(name, blocks)
    if resolved:
        return resolved, None
    if name.split("/")[0] in GROUPS:
        return None, name
    return None, None


def check(root=ROOT):
    global ROOT
    ROOT = root
    blocks = {block: sections_of(block) for block in block_dirs()}
    citations, unresolved = 0, []
    for path in documents():
        citing = owning_block(path, blocks)
        lines = read(os.path.join(ROOT, path)).split("\n")
        for number, line in enumerate(lines, start=1):
            carried = lines[number - 2] if number >= 2 else ""
            for hit in CITATION.finditer(line):
                citations += 1
                section = int(hit.group(1))
                point = int(hit.group(2)) if hit.group(2) else None
                after = line[hit.end():]
                if LOCAL_MARKER.match(after[:LOCAL_REACH]):
                    target, unknown = citing, None
                else:
                    target, unknown = attribute(carried + " " + line[: hit.start()],
                                                citing, blocks)
                if unknown is not None:
                    unresolved.append({"file": path, "line": number, "citation": hit.group(0),
                                       "reason": "no block called %s" % unknown})
                    continue
                if target is None:
                    continue
                sections = blocks[target]
                if section not in sections:
                    unresolved.append({"file": path, "line": number, "citation": hit.group(0),
                                       "reason": "%s has no section %d" % (target, section)})
                elif point is not None and point > sections[section]:
                    unresolved.append({
                        "file": path, "line": number, "citation": hit.group(0),
                        "reason": "%s §%d stops at point %d" % (target, section,
                                                                sections[section])})
    return {"blocks": len(blocks), "files": len(documents()), "citations": citations,
            "unresolved": unresolved}


def main(argv=None):
    parser = argparse.ArgumentParser(description="resolve every §N.M citation in the repo")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--root", default=ROOT, help="repository root to check")
    args = parser.parse_args(argv)

    result = check(os.path.abspath(args.root))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for miss in result["unresolved"]:
            print("%s:%d  %s  %s" % (miss["file"], miss["line"], miss["citation"],
                                     miss["reason"]))
        print("%d blocks, %d files, %d citations, %d unresolved"
              % (result["blocks"], result["files"], result["citations"],
                 len(result["unresolved"])))
    return 1 if result["unresolved"] else 0


if __name__ == "__main__":
    sys.exit(main())
