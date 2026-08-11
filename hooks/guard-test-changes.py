"""mentis: no-test-tampering hook, python half. See guard-test-changes.sh for the wiring
and the fast path. This is only ever invoked once the shell wrapper already decided the
payload is worth a real look.

Exit 0: allow. Exit 2: block, with the reason on stderr.
"""
import json
import os
import re
import sys

TEST_FILE_RE = re.compile(r"\.(test|spec)\.|_test\.|test_[A-Za-z0-9_]*\.py|Test\.(php|java)")

ASSERTION_RE = re.compile(
    r"\bexpect\s*\("
    r"|\bassert[A-Za-z_]*\s*\("
    r"|\bthis->assert[A-Za-z]*\("
    r"|\bself\.assert[A-Za-z]*\("
    r"|\bassert\s+\S"
    r"|Assert::[A-Za-z]+\("
    r"|Assert\.[A-Za-z]+\("
    r"|\.(toBe|toEqual|toHaveBeenCalled\w*|toThrow|toMatch|toContain"
    r"|toBeTruthy|toBeFalsy|toBeNull|toHaveLength)\("
    r"|\bt\.(Error|Fatal|Errorf|Fatalf)\("
    r"|\brequire\.[A-Za-z]+\("
)


def assertion_lines(text):
    return {line.strip() for line in text.splitlines() if ASSERTION_RE.search(line)}


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        print(
            "BLOCKED by mentis guard-test-changes: could not parse the tool call payload.",
            file=sys.stderr,
        )
        print(
            "Refusing to allow an unverifiable edit to what looks like a test file.",
            file=sys.stderr,
        )
        sys.exit(2)

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "") or ""

    if not TEST_FILE_RE.search(file_path):
        sys.exit(0)

    old_string = tool_input.get("old_string")
    new_string = tool_input.get("new_string")
    content = tool_input.get("content")

    if old_string is not None and new_string is not None:
        before, after = old_string, new_string
    elif content is not None:
        if os.path.isfile(file_path):
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    before = f.read()
            except Exception:
                print(
                    "BLOCKED by mentis guard-test-changes: could not read the existing "
                    "file to compare.",
                    file=sys.stderr,
                )
                sys.exit(2)
        else:
            sys.exit(0)  # brand-new file, nothing to tamper with
        after = content
    else:
        sys.exit(0)  # a shape this hook wasn't written for; don't block on it

    removed = assertion_lines(before) - assertion_lines(after)
    if not removed:
        sys.exit(0)

    print(
        "BLOCKED by mentis guard-test-changes: a pre-existing assertion is gone from this edit.",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print(
        "These lines matched an assertion pattern before the edit and no longer appear, "
        "verbatim, after it:",
        file=sys.stderr,
    )
    for line in sorted(removed):
        print(f"  - {line}", file=sys.stderr)
    print("", file=sys.stderr)
    print("If this bug is real, fix the implementation and leave the assertion as it is.", file=sys.stderr)
    print(
        "If the test itself is genuinely wrong (the spec changed), that edit belongs to a "
        "human or an explicit tdd/dozer pass, not to a build agent working around a red "
        "result. To let it through deliberately, set MENTIS_ALLOW_TEST_CHANGES=1 for this "
        "task (skills/debug §3.4).",
        file=sys.stderr,
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
