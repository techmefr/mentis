"""mentis: no-test-tampering hook, python half. See guard-test-changes.sh for the wiring
and the fast path. This is only ever invoked once the shell wrapper already decided the
payload is worth a real look.

Exit 0: allow. Exit 2: block, with the reason on stderr.
"""
import json
import os
import re
import sys
from collections import Counter

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


SKIP_RE = re.compile(
    r"(?:\.|->)(?:skip|todo)\s*\("
    r"|\b(?:xit|xtest|xdescribe)\s*\("
    r"|\bmarkTest(?:Skipped|Incomplete)\s*\("
    r"|@pytest\.mark\.(?:skip|skipif|xfail)"
    r"|\bpytest\.(?:skip|xfail)\s*\("
    r"|@unittest\.skip"
    r"|\bt\.Skip(?:Now|f)?\s*\("
    r"|@(?:Disabled|Ignore)\b"
    r"|@group\s+skip"
)

TRIVIAL_RES = [
    re.compile(r"\bassertTrue\s*\(\s*true\s*\)", re.I),
    re.compile(r"\bassertFalse\s*\(\s*false\s*\)", re.I),
    re.compile(r"\bassertNull\s*\(\s*null\s*\)", re.I),
    re.compile(r"\bassert(?:Same|Equals|EqualsCanonicalizing|Identical)\s*\(\s*([^,()]+?)\s*,\s*\1\s*\)"),
    re.compile(r"\bexpect\s*\(\s*true\s*\)\s*(?:->|\.)(?:toBeTrue|toBeTruthy)\s*\("),
    re.compile(r"\bexpect\s*\(\s*false\s*\)\s*(?:->|\.)(?:toBeFalse|toBeFalsy)\s*\("),
    re.compile(r"\bexpect\s*\(\s*([^()]+?)\s*\)\s*(?:->|\.)(?:toBe|toEqual|toBeSame)\s*\(\s*\1\s*\)"),
    re.compile(r"\bassert\s+True\s*$", re.M),
    re.compile(r"\bassert\s+(\S+)\s*==\s*\1\s*$", re.M),
]

TEST_DECL_RE = re.compile(
    r"\b(?:it|test)\s*\(\s*(['\"`])(.+?)\1"
    r"|\bfunction\s+(test\w+)\s*\("
    r"|\bdef\s+(test_\w+)"
    r"|\bfunc\s+(Test\w+)\s*\("
    r"|#\[Test\]\s*(?:#\[[^\]]*\]\s*)*(?:public\s+)?function\s+(\w+)"
    r"|@test\s*\*/\s*(?:public\s+)?function\s+(\w+)"
)

MUTATOR_RE = re.compile(
    r"(?:^|\s)(?:rm|mv|truncate|tee|shred)\s"
    r"|(?:^|\s)sed\s+(?:-\S*\s+)*-\S*i"
    r"|(?:^|\s)perl\s+(?:-\S*\s+)*-\S*i"
    r"|(?:^|\s)git\s+(?:rm|checkout|restore|stash|reset|clean)\b"
)

OPENERS, CLOSERS = "([{", ")]}"


def _unbalanced(text):
    return sum(text.count(c) for c in OPENERS) - sum(text.count(c) for c in CLOSERS)


def _normalise(text):
    """What makes two spellings of one assertion compare equal.

    All whitespace out, and a comma before a closing bracket out with it: a formatter that
    inlines a multi-line call drops the trailing comma, and blocking on that alone would
    refuse a reformat that weakened nothing.
    """
    return re.sub(r",(?=[)\]}])", "", "".join(text.split())).rstrip(";")


def assertion_statements(text, span=40):
    """Every assertion in the text: {compared form -> the form worth showing a reader}.

    A statement rather than a line, because a formatter puts the expected value on its own
    line: comparing lines let `retentionDays: 30` become `60` without touching any line that
    matches an assertion pattern, which is exactly the edit this hook exists to refuse.
    """
    lines = text.splitlines()
    found, index = {}, 0
    while index < len(lines):
        if not ASSERTION_RE.search(lines[index]):
            index += 1
            continue
        chunk, last = lines[index], index
        while _unbalanced(chunk) > 0 and last + 1 < len(lines) and last - index < span:
            last += 1
            chunk += " " + lines[last]
        found[_normalise(chunk)] = " ".join(chunk.split())
        index = last + 1
    return found


def skip_markers(text):
    return Counter(" ".join(m.group(0).split()) for m in SKIP_RE.finditer(text))


def trivial_assertions(text):
    found = Counter()
    for rx in TRIVIAL_RES:
        for m in rx.finditer(text):
            found[" ".join(m.group(0).split())] += 1
    return found


def declared_tests(text):
    names = set()
    for m in TEST_DECL_RE.finditer(text):
        if m.group(1):
            names.add(m.group(2))
        else:
            names.add(next(g for g in m.groups()[2:] if g))
    return names


def block(headline, lines, hint):
    print(f"BLOCKED by mentis guard-test-changes: {headline}", file=sys.stderr)
    print("", file=sys.stderr)
    for line in lines:
        print(f"  - {line}", file=sys.stderr)
    print("", file=sys.stderr)
    print(hint, file=sys.stderr)
    sys.exit(2)


def check_bash(command):
    for segment in re.split(r"&&|\|\||[;|\n]", command):
        targets = [t.strip("\"'") for t in re.findall(r">>?\s*(\S+)", segment)]
        touches_test = any(TEST_FILE_RE.search(t) for t in targets)
        if MUTATOR_RE.search(" " + segment) and TEST_FILE_RE.search(segment):
            touches_test = True
        if touches_test:
            block(
                "a shell command rewrites, moves or reverts a test file.",
                [" ".join(segment.split())],
                "Editing or deleting a test through the shell skips the assertion check the "
                "edit tools get. Fix the implementation instead; if the test is truly wrong, "
                "that is a human or tdd/dozer decision. To allow it deliberately, set "
                "MENTIS_ALLOW_TEST_CHANGES=1 for this task (skills/debug 3.4).",
            )


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

    command = tool_input.get("command")
    if isinstance(command, str) and not file_path:
        check_bash(command)
        sys.exit(0)

    if not TEST_FILE_RE.search(file_path):
        sys.exit(0)

    old_string = tool_input.get("old_string")
    new_string = tool_input.get("new_string")
    content = tool_input.get("content")

    if old_string is not None and new_string is not None:
        # The hunk on its own is not enough: an edit that changes only the expected value
        # carries no assertion line at all, so comparing the two strings sees nothing. Apply
        # the replacement to the file as it stands and compare the whole thing.
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
            count = -1 if tool_input.get("replace_all") else 1
            after = before.replace(old_string, new_string, count)
        else:
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

    gone_tests = sorted(declared_tests(before) - declared_tests(after))
    if gone_tests:
        block(
            "a test that existed before this edit is gone.",
            gone_tests,
            "A deleted or renamed test is coverage that vanished. Keep it, or hand the "
            "removal to a human. To allow it deliberately, set MENTIS_ALLOW_TEST_CHANGES=1 "
            "for this task (skills/debug 3.4).",
        )

    new_skips = skip_markers(after) - skip_markers(before)
    if new_skips:
        block(
            "this edit turns a test off (skip, todo, incomplete or expected-failure).",
            sorted(new_skips),
            "A skipped test cannot fail, which is the same as deleting it with a trace left "
            "behind. Fix the implementation. To allow it deliberately, set "
            "MENTIS_ALLOW_TEST_CHANGES=1 for this task (skills/debug 3.4).",
        )

    new_trivial = trivial_assertions(after) - trivial_assertions(before)
    if new_trivial:
        block(
            "this edit adds an assertion that cannot fail.",
            sorted(new_trivial),
            "Asserting a literal against itself passes whatever the code does. Assert the "
            "behaviour under test, or drop the test. To allow it deliberately, set "
            "MENTIS_ALLOW_TEST_CHANGES=1 for this task (skills/debug 3.4).",
        )

    was, now = assertion_statements(before), assertion_statements(after)
    removed = [was[key] for key in sorted(set(was) - set(now))]
    if not removed:
        sys.exit(0)

    print(
        "BLOCKED by mentis guard-test-changes: a pre-existing assertion is gone from this edit.",
        file=sys.stderr,
    )
    print("", file=sys.stderr)
    print(
        "These assertions existed before the edit and no longer appear after it — deleted, "
        "commented out, or their expected value changed:",
        file=sys.stderr,
    )
    for line in removed:
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
