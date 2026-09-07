#!/usr/bin/env python3
"""Checks that no internal fact reached the publishable tree. No network, no fixtures:

    python3 bin/test_rule_c.py

Why this suite exists: on 2026-09-07 a scan of the 200 tracked files found 38 occurrences of
internal content already committed — an internal documentation host cited three times as a source,
the org's private skill marketplace and the slugs of individual skills inside it named about ten
times, two real repository names, and one real ticket key. Rule C had been written from the first
commit and held everywhere it was thought about; it failed in `origin.md` provenance stamps and in
`CATALOG.md` source columns, which is exactly where an author is being scrupulous about *where a
fact came from* and forgets that the citation itself is the fact.

Prose cannot enforce that, and `code-baseline` section 8 says so: prefer the mechanism the runtime
holds over the sentence someone has to remember. So this is the mechanism.

What it proves: no tracked file carries an internal host, an org-private marketplace path, a real
project or repository name, a tracker key, a credential-bearing URL or a private IP. The carve-out
is explicit and narrow — a first-party package the company publishes openly may be named, because
rule C's generic-citation default is about internal facts, not about a tool anyone outside can
already read. A carve-out entry is a package *name*, never a host: rule C lists hosts as infra.
"""
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ok = fail = 0

# The narrow carve-out: openly published first-party packages, by name, no host.
ALLOWED = (
    "xefi/laravel-osdd",
    "github.com/xefi/laravel-osdd",
)

FORBIDDEN = [
    ("an internal documentation host",
     r"doc\.stacktim\.[a-z]+|\bdoc\.[a-z0-9-]+\.(?:internal|local|lan)\b"),
    ("an org-private skill marketplace or one of its skill paths",
     r"xefi-claude-skills|(?:bi|global|xefi|laravel|nuxt|react|python|csharp|flutter|design"
     r"|design-patterns|project-management)/skills/[a-z0-9-]+"),
    ("a real project or repository name",
     r"\bskera(?:-[a-z-]+)?\b|\bnexeren\b|\bstacktim\b|\bpilota\b|\bgalaxity\b"),
    ("an internal host or subdomain",
     r"\b[a-z0-9-]+\.(?:xefi|skera|stacktim)\.[a-z]{2,}\b|gitlab\.(?:xefi|skera)\.[a-z]{2,}"),
    ("an internal database or server hostname",
     r"\bXFISRV[A-Z0-9]*\b|\bINFOCENTRE\b|\bDAILYBIZ\b"),
    ("a tracker key", r"\b(?:SKR|STK|KS|GCI|CRM)-\d{2,}\b"),
    ("a credential embedded in a URL", r"https?://[^/\s]+:[^/@\s]+@"),
    ("what looks like an access token",
     r"\bgh[pousr]_[A-Za-z0-9]{16,}\b|\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    ("a private IP address",
     r"\b(?:10|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b"),
]

SELF = os.path.join("bin", "test_rule_c.py")


def tracked():
    out = subprocess.run(["git", "-C", REPO, "ls-files"], capture_output=True, text=True)
    return [p for p in out.stdout.split("\n") if p.strip()]


def check(label, got, want):
    global ok, fail
    if got == want:
        ok += 1
        print("PASS  " + label)
    else:
        fail += 1
        print("FAIL  %s\n        expected %r, got %r" % (label, want, got))


files = tracked()
check("the repo has tracked files to scan", len(files) > 50, True)

# This suite must not flag its own patterns, so it excludes itself by path and says so.
scanned = [p for p in files if p != SELF]
check("this suite excludes itself from the scan", SELF not in scanned, True)

allowed_rx = re.compile("|".join(re.escape(a) for a in ALLOWED))

for label, pattern in FORBIDDEN:
    rx = re.compile(pattern)
    hits = []
    for rel in scanned:
        path = os.path.join(REPO, rel)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError:
            continue
        # Blank the carve-out before matching, so an allowed package name cannot mask a real hit
        # elsewhere on the same line and cannot itself be reported.
        text = allowed_rx.sub(" ", text)
        for m in rx.finditer(text):
            line = text[:m.start()].count("\n") + 1
            hits.append("%s:%d (%s)" % (rel, line, m.group(0)[:60]))
    if hits:
        print("        " + "\n        ".join(hits[:12]))
        if len(hits) > 12:
            print("        ... and %d more" % (len(hits) - 12))
    check("no tracked file carries %s" % label, len(hits), 0)

# The carve-out is a name, never a host: a *.xefi.com style reference is infra, not a package.
check("the carve-out list contains no host",
      all(not re.search(r"\b[a-z0-9-]+\.[a-z]+\.[a-z]{2,}\b", a.replace("github.com/", ""))
          for a in ALLOWED), True)

print("\n%d passed, %d failed" % (ok, fail))
sys.exit(1 if fail else 0)
