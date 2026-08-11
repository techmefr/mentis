#!/usr/bin/env python3
"""Checks for hooks/guard-test-changes.sh (+ its .py half). No network, nothing installed:

    python3 bin/test_guard_test_changes.py

Two things are being proven: a pre-existing assertion that disappears from a test file —
deleted, commented out, or retargeted to a different expected value — is refused, while
extending a test file with a new case, or touching a non-test file, goes through untouched.
skills/debug §3.4 names the failure mode this exists to make mechanical: a build agent
editing a failing test's expectation instead of the implementation.
"""
import json
import os
import subprocess
import sys
import tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hooks", "guard-test-changes.sh")
ok = fail = 0


def run(payload, allow=None):
    env = dict(os.environ)
    env.pop("MENTIS_ALLOW_TEST_CHANGES", None)
    if allow is not None:
        env["MENTIS_ALLOW_TEST_CHANGES"] = allow
    r = subprocess.run(["bash", HOOK], input=payload, capture_output=True, text=True, env=env)
    return r.returncode, r.stderr


def check(desc, expect, payload, allow=None):
    global ok, fail
    code, err = run(payload, allow=allow)
    if code == expect:
        ok += 1
        print(f"PASS  {desc}")
    else:
        fail += 1
        print(f"FAIL  {desc} (expected exit {expect}, got {code}): {err[:200]}")


def edit(file_path, old_string, new_string):
    return json.dumps({"tool_input": {"file_path": file_path, "old_string": old_string, "new_string": new_string}})


def write(file_path, content):
    return json.dumps({"tool_input": {"file_path": file_path, "content": content}})


check("non-test file is untouched by the guard", 0, edit("src/foo.ts", "a", "b"))

check(
    "adding a new case while keeping the old assertion",
    0,
    edit("src/foo.test.ts", "expect(x).toBe(1)", "expect(x).toBe(1)\nexpect(y).toBe(2)"),
)

check(
    "retargeting an existing assertion's expected value",
    2,
    edit("src/foo.test.ts", "expect(x).toBe(1)", "expect(x).toBe(2)"),
)

check(
    "deleting an existing assertion outright",
    2,
    edit("src/foo.test.ts", "setup()\nexpect(x).toBe(1)", "setup()"),
)

check(
    "commenting out an existing assertion",
    2,
    edit("src/foo.test.ts", "expect(x).toBe(1)", "// expect(x).toBe(1)"),
)

check(
    "MENTIS_ALLOW_TEST_CHANGES lets a retargeting edit through deliberately",
    0,
    edit("src/foo.test.ts", "expect(x).toBe(1)", "expect(x).toBe(2)"),
    allow="1",
)

check(
    "unparseable payload on a test-shaped filename fails closed",
    2,
    "not json but mentions foo.test.ts",
)

check(
    "a brand-new test file (nothing on disk yet) is unaffected",
    0,
    write(f"src/does-not-exist-{os.getpid()}.test.ts", "expect(1).toBe(1)"),
)

check(
    "PHPUnit-style assertion retargeted",
    2,
    edit("tests/FooTest.php", "$this->assertEquals(1, $x);", "$this->assertEquals(2, $x);"),
)

check(
    "pytest-style bare assert retargeted",
    2,
    edit("tests/test_foo.py", "assert result == 1", "assert result == 2"),
)

with tempfile.NamedTemporaryFile(suffix=".test.ts", delete=False) as f:
    f.write(b"expect(x).toBe(1)\n")
    real_test_file = f.name
try:
    check(
        "Write overwriting an existing test file drops an assertion",
        2,
        write(real_test_file, "expect(y).toBe(2)\n"),
    )
    check(
        "Write overwriting an existing test file keeps + extends",
        0,
        write(real_test_file, "expect(x).toBe(1)\nexpect(y).toBe(2)\n"),
    )
finally:
    os.unlink(real_test_file)

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
