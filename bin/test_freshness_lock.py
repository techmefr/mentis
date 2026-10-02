#!/usr/bin/env python3
"""Checks for bin/check_freshness_lock.py. No network:

    python3 bin/test_freshness_lock.py
"""
import datetime
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("lock", os.path.join(HERE, "check_freshness_lock.py"))
lock = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lock)

ok = fail = 0


def check(label, got, want):
    global ok, fail
    if got == want:
        ok += 1
        print(f"PASS  {label}")
    else:
        fail += 1
        print(f"FAIL  {label}: got {got!r}, wanted {want!r}")


skills = os.path.join(lock.REPO, "skills")
today = datetime.date(2026, 10, 2)
good_t = {"vite": {"blocks": ["vite-bundler-conventions"]}}
good_l = {"vite": {"version": "8.3.2", "generatedAt": "2026-10-02"}}

check("the committed files are consistent", lock.validate(lock.load(lock.TRACKED), lock.load(lock.LOCK), skills, today), [])
check("a consistent pair has no problem", lock.validate(good_t, good_l, skills, today), [])
check("a tracked package missing from the lock", len(lock.validate(good_t, {}, skills, today)), 1)
check("a locked package that is not tracked", len(lock.validate({}, good_l, skills, today)), 1)
check("a block that does not exist", len(lock.validate({"vite": {"blocks": ["nope"]}}, good_l, skills, today)), 1)
check("a range instead of a version", len(lock.validate(good_t, {"vite": {"version": "^8", "generatedAt": "2026-10-02"}}, skills, today)), 1)
check("a malformed date", len(lock.validate(good_t, {"vite": {"version": "8.3.2", "generatedAt": "10/02"}}, skills, today)), 1)
check("an impossible date", len(lock.validate(good_t, {"vite": {"version": "8.3.2", "generatedAt": "2026-13-45"}}, skills, today)), 1)
check("a date in the future", len(lock.validate(good_t, good_l, skills, datetime.date(2026, 9, 1))), 1)
check("a verification past the window",
      len(lock.validate(good_t, {"vite": {"version": "8.3.2", "generatedAt": "2026-01-01"}}, skills, today)), 1)
check("a tracked entry without blocks", len(lock.validate({"vite": {}}, good_l, skills, today)), 1)

check("a patch bump is not a move", lock.moved(good_l, lambda p: "8.3.9"), [])
check("a minor bump is a move", lock.moved(good_l, lambda p: "8.4.0"), [("vite", "8.3.2", "8.4.0")])
check("a major bump is a move", lock.moved(good_l, lambda p: "9.0.0"), [("vite", "8.3.2", "9.0.0")])


def boom(pkg):
    raise RuntimeError("offline")


check("an unreadable registry is reported, not hidden", lock.moved(good_l, boom)[0][2], "unreadable: offline")

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
