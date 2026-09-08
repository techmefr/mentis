#!/usr/bin/env python3
"""Recomputes CATALOG.md's depth table from the repo, instead of from memory.

    python3 bin/measure_depth.py            # print the table rows
    python3 bin/measure_depth.py --json     # machine-readable

Why this exists: the table used to be produced by hand, so two of its rows drifted into
figures nobody could reproduce (the `global` row, and a `python` row whose second block was
never identified). The composition below is the part that was missing — each row now names
the blocks it aggregates, so a row can be re-measured rather than remembered.

A block's size is its **rules**: the router body of `SKILL.md` (frontmatter excluded) plus
every file under `references/` except `origin.md`. `origin.md` is provenance — where a rule
came from, what was re-checked, what a pass changed — and the catalogue being compared
against has no equivalent of it, so counting ours measured our own bookkeeping.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# stack -> (their skills, their words, [our blocks], note)
ROWS = [
    ("laravel", 65, 79825,
     ["skills/laravel-conventions", "skills/php-patterns", "skills/inertia-conventions"],
     "the stack this repo ships on"),
    ("csharp", 37, 56718, ["skills/dotnet-conventions"],
     "worst ratio, stack nobody here writes"),
    ("python", 20, 22097,
     ["skills/python-conventions", "skills/data-pipeline-conventions"], ""),
    ("flutter", 40, 20772, ["skills/flutter-conventions"], ""),
    ("nuxt", 21, 19869, ["skills/vue-nuxt-vuetify-conventions"], ""),
    ("global", 18, 20280,
     ["skills/code-baseline", "skills/security-hardening", "skills/api-design",
      "skills/documentation-adr", "skills/observability-instrumentation"],
     "composition declared 2026-09-08, not inherited"),
    ("project-management", 10, 14536,
     ["business/product-ownership", "skills/spec"], ""),
    ("design-patterns", 7, 12179, ["skills/design-patterns"], ""),
    ("react", 36, 9302, ["skills/react-nextjs-conventions"], ""),
    ("bi, design, xefi", 16, 17306,
     ["business/data-analytics", "business/interface-design", "business/ux-writing",
      "skills/accessibility"],
     "internal landscape, rule C keeps it out"),
]


def block_words(rel):
    """Rules words of one block: the router body plus references/, minus origin.md."""
    path = os.path.join(ROOT, rel)
    skill = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill):
        raise SystemExit(f"no SKILL.md at {rel}")
    with open(skill, encoding="utf-8") as fh:
        text = fh.read()
    end = text.find("\n---\n", 3)
    total = len((text[end + 5:] if end != -1 else text).split())
    refs = os.path.join(path, "references")
    if os.path.isdir(refs):
        for name in sorted(os.listdir(refs)):
            if name.endswith(".md") and name != "origin.md":
                with open(os.path.join(refs, name), encoding="utf-8") as fh:
                    total += len(fh.read().split())
    return total


def measure():
    out = []
    for stack, their_skills, their_words, blocks, note in ROWS:
        per = {b: block_words(b) for b in blocks}
        ours = sum(per.values())
        out.append({
            "stack": stack, "their_skills": their_skills, "their_words": their_words,
            "blocks": blocks, "per_block": per, "our_words": ours,
            "deficit": ours - their_words,
            "ratio": round(their_words / ours, 2) if ours else None,
            "note": note,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    rows = measure()
    if args.json:
        json.dump(rows, sys.stdout, indent=2)
        print()
        return
    print("| stack | their skills / words | our blocks / words | deficit | ratio |")
    print("|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: r["deficit"]):
        sign = "+" if r["deficit"] > 0 else "−"
        print(f"| {r['stack']} | {r['their_skills']} / {r['their_words']:,} | "
              f"{len(r['blocks'])} / {r['our_words']:,} | {sign}{abs(r['deficit']):,} | "
              f"x{r['ratio']} |")
    print()
    for r in rows:
        parts = ", ".join(f"{b.split('/')[-1]} {n:,}" for b, n in r["per_block"].items())
        print(f"{r['stack']}: {parts}")


if __name__ == "__main__":
    main()
