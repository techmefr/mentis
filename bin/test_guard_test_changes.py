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

# The formatted shape, found by wiring this hook into a real repo on 2026-09-09: prettier
# puts the expected value on its own line, so the value can change without any line that
# matches an assertion pattern changing with it. Comparing lines allowed exactly the edit
# this guard exists to refuse, and the hunk alone does not even carry the assertion.
FORMATTED = """describe('resolvePruneRule', () => {
  it("resolves the project's configured default retention", () => {
    expect(resolvePruneRule('BlogPost')).toEqual({
      retentionDays: 30,
      lock: false,
    });
  });
});
"""

with tempfile.NamedTemporaryFile(suffix=".spec.ts", delete=False) as f:
    f.write(FORMATTED.encode())
    formatted_file = f.name
try:
    check(
        "an expected value on its own line under a multi-line assertion",
        2,
        edit(formatted_file, "retentionDays: 30,", "retentionDays: 60,"),
    )
    check(
        "the same value change written as a hunk carrying no assertion at all",
        2,
        edit(formatted_file, "      retentionDays: 30,\n      lock: false,",
             "      retentionDays: 60,\n      lock: false,"),
    )
    check(
        "inlining a multi-line assertion weakens nothing and is allowed",
        0,
        write(formatted_file, FORMATTED.replace(
            """    expect(resolvePruneRule('BlogPost')).toEqual({
      retentionDays: 30,
      lock: false,
    });""",
            "    expect(resolvePruneRule('BlogPost')).toEqual({ retentionDays: 30, lock: false });",
        )),
    )
    check(
        "re-indenting an assertion is allowed",
        0,
        edit(formatted_file, "    expect(resolvePruneRule('BlogPost')).toEqual({",
             "      expect(resolvePruneRule('BlogPost')).toEqual({"),
    )
    check(
        "renaming the symbol under test blocks, deliberately",
        2,
        write(formatted_file, FORMATTED.replace("resolvePruneRule", "resolveRetentionRule")),
    )
    check(
        "a replace_all edit is applied everywhere before comparing",
        2,
        json.dumps({"tool_input": {"file_path": formatted_file, "old_string": "30",
                                   "new_string": "60", "replace_all": True}}),
    )
finally:
    os.unlink(formatted_file)

check("markTestSkipped added to an existing test", 2,
      edit("tests/Feature/FooTest.php", "it('works', function () {", "it('works', function () {\n    $this->markTestSkipped('later');"))
check("Pest ->todo() chained onto a test", 2,
      edit("tests/Feature/FooTest.php", "it('works', fn () => expect(1)->toBe(2));", "it('works', fn () => expect(1)->toBe(2))->todo();"))
check("jest it.skip introduced", 2, edit("src/foo.test.ts", "it('a', () => {", "it.skip('a', () => {"))
check("pytest skip marker added", 2, edit("tests/test_foo.py", "def test_a():", "@pytest.mark.skip\ndef test_a():"))
check("go t.Skip added", 2, edit("pkg/foo_test.go", "func TestA(t *testing.T) {", "func TestA(t *testing.T) {\n\tt.Skip()"))
check("assertTrue(true) added", 2,
      edit("tests/FooTest.php", "$this->assertSame(1, $x);", "$this->assertSame(1, $x);\n$this->assertTrue(true);"))
check("expect(true)->toBeTrue() added", 2,
      edit("tests/Feature/FooTest.php", "});", "    expect(true)->toBeTrue();\n});"))
check("pytest assert True added", 2, edit("tests/test_foo.py", "def test_a():\n    pass", "def test_a():\n    assert True"))
check("self-comparing assertSame added", 2,
      edit("tests/FooTest.php", "$this->assertSame(1, $x);", "$this->assertSame(1, $x);\n$this->assertSame($y, $y);"))
check("a meaningful new assertion is allowed", 0,
      edit("tests/FooTest.php", "$this->assertSame(1, $x);", "$this->assertSame(1, $x);\n$this->assertSame(3, $y);"))
check("a skip marker already present and left alone is allowed", 0,
      edit("tests/test_foo.py", "x = 1\n@pytest.mark.skip\ndef test_a(): pass", "x = 2\n@pytest.mark.skip\ndef test_a(): pass"))

PHP_BODY = ("<?php\nclass FooTest {\n    public function test_a() { $this->assertSame(1, 1 + 0); }\n"
            "    public function test_b() { $this->assertSame(2, 1 + 1); }\n}\n")
with tempfile.NamedTemporaryFile(suffix="Test.php", delete=False) as f:
    f.write(PHP_BODY.encode())
    php_file = f.name
try:
    check("removing a test method is refused", 2,
          write(php_file, PHP_BODY.replace("    public function test_b() { $this->assertSame(2, 1 + 1); }\n", "")))
    check("emptying a test file is refused", 2, write(php_file, ""))
    check("adding a test method is allowed", 0,
          write(php_file, PHP_BODY[:-2] + "    public function test_c() { $this->assertSame(3, 2 + 1); }\n}\n"))
finally:
    os.unlink(php_file)


def bash(command):
    return json.dumps({"tool_input": {"command": command}})


check("sed -i on a test file is refused", 2, bash("sed -i 's/1/2/' tests/FooTest.php"))
check("rm of a test file is refused", 2, bash("rm tests/Feature/FooTest.php"))
check("git checkout of a test file is refused", 2, bash("git checkout HEAD -- tests/FooTest.php"))
check("redirect into a test file is refused", 2, bash("echo '' > tests/FooTest.php"))
check("running a test file is allowed", 0, bash("vendor/bin/phpunit tests/FooTest.php"))
check("rm of a build directory next to a test run is allowed", 0, bash("rm -rf build && vendor/bin/phpunit tests/FooTest.php"))
check("shell edit allowed under the explicit override", 0, bash("rm tests/FooTest.php"), allow="1")

print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
