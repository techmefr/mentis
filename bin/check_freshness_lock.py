#!/usr/bin/env python3
"""Machine-readable freshness lock for the packages a block pins a fact to (skills/source-freshness step 5).

    python3 bin/check_freshness_lock.py                 offline: both files are well-formed and agree
    python3 bin/check_freshness_lock.py --sync-check    also asks the registry (read only) which packages moved
    python3 bin/check_freshness_lock.py --stamp PKG VER write the version a human just re-verified, dated today

Two files in skills/source-freshness/references/:
  tracked.json         {"<package>": {"blocks": ["<block>", ...], "note": "..."}}
  freshness.lock.json  {"<package>": {"version": "x.y.z", "generatedAt": "YYYY-MM-DD"}}

The lock records the version a block's facts were last verified against, and the day. It is not a
dependency of any block and is never read when a block runs; `--sync-check` is run by a person, at
authoring time, and only reads (`npm view <package> version`). A package that moved is a block to
re-read with skills/source-freshness step 3, not a block to edit by script.

Exit 1 when the offline check fails, or when --sync-check finds a package whose latest major or minor
differs from the locked one.
"""
import datetime
import json
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(REPO, "skills", "source-freshness", "references")
TRACKED = os.path.join(DIR, "tracked.json")
LOCK = os.path.join(DIR, "freshness.lock.json")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
DAY = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STALE_DAYS = 120


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def validate(tracked, lock, skills_dir, today):
    problems = []
    for pkg, entry in tracked.items():
        blocks = entry.get("blocks") if isinstance(entry, dict) else None
        if not blocks or not isinstance(blocks, list):
            problems.append(f"{pkg}: tracked without a list of blocks")
            continue
        for block in blocks:
            if not os.path.isfile(os.path.join(skills_dir, block, "SKILL.md")):
                problems.append(f"{pkg}: block {block} does not exist")
        stamp = lock.get(pkg)
        if not isinstance(stamp, dict):
            problems.append(f"{pkg}: tracked but not in the lock")
            continue
        if not SEMVER.match(str(stamp.get("version", ""))):
            problems.append(f"{pkg}: version {stamp.get('version')!r} is not a full semantic version")
        day = str(stamp.get("generatedAt", ""))
        if not DAY.match(day):
            problems.append(f"{pkg}: generatedAt {day!r} is not YYYY-MM-DD")
        else:
            try:
                age = (today - datetime.date.fromisoformat(day)).days
            except ValueError:
                problems.append(f"{pkg}: generatedAt {day!r} is not a date")
                continue
            if age < 0:
                problems.append(f"{pkg}: generatedAt {day} is in the future")
            elif age > STALE_DAYS:
                problems.append(f"{pkg}: verified {age} days ago, past the {STALE_DAYS}-day window")
    for pkg in lock:
        if pkg not in tracked:
            problems.append(f"{pkg}: in the lock but not tracked")
    return problems


def registry_latest(pkg):
    result = subprocess.run(["npm", "view", pkg, "version"], capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "npm view failed")
    return result.stdout.strip()


def moved(lock, latest_of):
    out = []
    for pkg, stamp in sorted(lock.items()):
        try:
            latest = latest_of(pkg)
        except Exception as error:
            out.append((pkg, stamp["version"], f"unreadable: {error}"))
            continue
        old = stamp["version"].split("-")[0].split(".")
        new = latest.split("-")[0].split(".")
        if old[:2] != new[:2]:
            out.append((pkg, stamp["version"], latest))
    return out


def main(argv, today=None):
    today = today or datetime.date.today()
    if argv[:1] == ["--stamp"]:
        if len(argv) != 3 or not SEMVER.match(argv[2]):
            print("usage: --stamp PACKAGE x.y.z")
            return 2
        tracked, lock = load(TRACKED), load(LOCK)
        if argv[1] not in tracked:
            print(f"{argv[1]} is not in tracked.json; add it there first")
            return 2
        lock[argv[1]] = {"version": argv[2], "generatedAt": today.isoformat()}
        with open(LOCK, "w", encoding="utf-8") as handle:
            json.dump(dict(sorted(lock.items())), handle, indent=2)
            handle.write("\n")
        print(f"stamped {argv[1]} {argv[2]} {today.isoformat()}")
        return 0
    tracked, lock = load(TRACKED), load(LOCK)
    problems = validate(tracked, lock, os.path.join(REPO, "skills"), today)
    for problem in problems:
        print("FAIL ", problem)
    code = 1 if problems else 0
    if not problems:
        print(f"OK    {len(tracked)} tracked packages, lock consistent")
    if "--sync-check" in argv:
        for pkg, old, new in moved(lock, registry_latest):
            print(f"MOVED {pkg}: locked {old}, registry {new}")
            code = 1
        if code == 0:
            print("OK    no tracked package moved")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
