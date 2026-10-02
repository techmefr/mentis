#!/usr/bin/env python3
"""mentis: a check is not made to pass by loosening it (PreToolUse on Edit/Write/MultiEdit). OPT-IN.

When code fails a linter, a formatter, a type checker or a static analyser, the easy way out is to edit
the tool's configuration until the failure is gone. This hook refuses that edit and sends the work back
to the code. Two tiers, because the files are not alike:

  strict   linter, formatter and hook-manager configuration, and their ignore lists. Any edit to an
           existing file is refused.
  loosen   type-checker, analyser and test-runner configuration, which also holds legitimate settings
           (paths, targets). An edit is refused only when it loosens: a strictness flag turned off, an
           ignore or baseline entry added, a level lowered, a "warnings are errors" switch removed.

Creating the file passes. MENTIS_ALLOW_CONFIG_CHANGES=1 in the human's own environment lifts it for a
task (the spec changed on purpose). Heuristics, not parsing: the loosen tier counts tokens before and
after, so a rewrite that moves a flag around can still read as neutral. Only Edit/Write/MultiEdit are
seen; the same change through a shell command is not. Fails open on any error.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import command_views as cv

STRICT_NAME = [re.compile(p, re.I) for p in (
    r'^(\.eslintrc|eslint\.config|\.prettierrc|prettier\.config|\.stylelintrc|stylelint\.config|'
    r'\.oxlintrc|oxlint\.config|commitlint\.config|\.commitlintrc|\.lintstagedrc|lint-staged\.config|'
    r'\.markdownlint|\.markdownlint-cli2|\.huskyrc|lefthook|\.lefthook)(\.[\w-]+)*$',
    r'^\.?(biome)(\.[\w-]+)*\.jsonc?$',
    r'^\.(eslint|prettier|stylelint|markdownlint)ignore$',
    r'^(\.?ruff\.toml|\.flake8|\.?pylintrc|\.pycodestyle|\.isort\.cfg|\.editorconfig|\.shellcheckrc|'
    r'\.sqlfluff|\.hadolint\.ya?ml|\.yamllint(\.ya?ml)?|\.pre-commit-config\.ya?ml|\.dprint\.jsonc?)$',
    r'^(\.php-cs-fixer(\.dist)?\.php|pint\.json|phpcs\.xml(\.dist)?|\.phpcs\.xml(\.dist)?|phpmd\.xml)$',
    r'^(\.rubocop\.ya?ml|\.golangci\.(ya?ml|toml|json)|\.?rustfmt\.toml|\.?clippy\.toml|\.swiftlint\.ya?ml)$',
)]
STRICT_PATH = re.compile(r'(^|/)\.husky/')
LOOSEN_NAME = [re.compile(p, re.I) for p in (
    r'^(tsconfig|jsconfig)(\.[\w-]+)*\.json$',
    r'^(phpstan|psalm)(\.[\w-]+)*\.(neon|xml|dist)$|^phpstan\.neon\.dist$|^psalm\.xml\.dist$',
    r'^(\.?mypy\.ini|pyrightconfig\.json|phpunit\.xml(\.dist)?|analysis_options\.yaml|Directory\.Build\.props|\.globalconfig)$',
    r'\.csproj$',
)]

KEYS = (r'strict|noImplicitAny|strictNullChecks|strictFunctionTypes|strictBindCallApply|strictPropertyInitialization|'
        r'noImplicitThis|useUnknownInCatchVariables|alwaysStrict|noImplicitReturns|noFallthroughCasesInSwitch|'
        r'noUnusedLocals|noUnusedParameters|noUncheckedIndexedAccess|exactOptionalPropertyTypes|noImplicitOverride|'
        r'noPropertyAccessFromIndexSignature|checkJs')
PHPUNIT_KEYS = (r'failOnWarning|failOnRisky|failOnDeprecation|failOnNotice|failOnEmptyTestSuite|'
                r'beStrictAboutTestsThatDoNotTestAnything|beStrictAboutOutputDuringTests|beStrictAboutChangesToGlobalState|'
                r'convertWarningsToExceptions|convertNoticesToExceptions|convertDeprecationsToExceptions|convertErrorsToExceptions')

LOOSEN = [re.compile(p, re.I | re.M) for p in (
    r'"(' + KEYS + r')"\s*:\s*false',
    r'"skip(Default)?LibCheck"\s*:\s*true',
    r'^\s*ignoreErrors\s*:',
    r'^\s*-\s*[\'"]?#.*#',
    r'^\s*(check\w+|report\w+|treatPhpDocTypesAsCertain)\s*:\s*false',
    r'^\s*excludePaths\s*:',
    r'<ignoreFiles|<issueHandlers|errorLevel="[4-8]"',
    r'\bignore_errors\s*=\s*true|\bignore_missing_imports\s*=\s*true',
    r'\b(disallow_\w+|warn_\w+|check_untyped_defs|strict\w*)\s*=\s*false',
    r'"typeCheckingMode"\s*:\s*"(off|basic)"|"report\w+"\s*:\s*("none"|false)',
    r'(' + PHPUNIT_KEYS + r')\s*=\s*"(false|0)"',
    r'<exclude\b',
    r'^\s*[\w-]+\s*:\s*ignore\s*$',
    r'^\s*strict-[\w-]+\s*:\s*false',
    r'^\s*[a-z_]+\s*:\s*false\s*$',
    r'<TreatWarningsAsErrors>\s*false|<Nullable>\s*disable|<NoWarn>|<WarningLevel>\s*[0-3]\b',
)]
TIGHTEN = [re.compile(p, re.I | re.M) for p in (
    r'"(' + KEYS + r')"\s*:\s*true',
    r'\bstrict\w*\s*=\s*true|\bdisallow_\w+\s*=\s*true|\bwarn_\w+\s*=\s*true',
    r'(' + PHPUNIT_KEYS + r')\s*=\s*"(true|1)"',
    r'<TreatWarningsAsErrors>\s*true|<Nullable>\s*enable',
    r'"typeCheckingMode"\s*:\s*"strict"',
)]
LEVEL = re.compile(r'^\s*level\s*:\s*(\d+|max)\b', re.M)


def level_of(text):
    m = LEVEL.search(text)
    if not m:
        return None
    return 99 if m.group(1) == 'max' else int(m.group(1))


def score(text):
    return sum(len(p.findall(text)) for p in LOOSEN) - sum(len(p.findall(text)) for p in TIGHTEN)


def loosens(before, after):
    lb, la = level_of(before), level_of(after)
    if lb is not None and la is not None and la < lb:
        return True
    return score(after) > score(before)


def tier(path):
    base = os.path.basename(path)
    if STRICT_PATH.search(path.replace('\\', '/')) or any(p.search(base) for p in STRICT_NAME):
        return 'strict'
    if any(p.search(base) for p in LOOSEN_NAME):
        return 'loosen'
    return None


def after_edit(before, tool_input):
    if 'content' in tool_input and tool_input.get('content') is not None:
        return tool_input['content']
    edits = tool_input.get('edits')
    pairs = []
    if isinstance(edits, list):
        pairs = [(e.get('old_string'), e.get('new_string'), e.get('replace_all')) for e in edits if isinstance(e, dict)]
    elif tool_input.get('old_string') is not None and tool_input.get('new_string') is not None:
        pairs = [(tool_input['old_string'], tool_input['new_string'], tool_input.get('replace_all'))]
    text = before
    for old, new, every in pairs:
        if old is None or new is None:
            continue
        text = text.replace(old, new, -1 if every else 1)
    return text


def main():
    if os.environ.get('MENTIS_ALLOW_CONFIG_CHANGES'):
        return
    payload = cv.load_payload()
    if not payload:
        return
    tool_input = payload.get('tool_input') or {}
    if not isinstance(tool_input, dict):
        return
    path = tool_input.get('file_path') or ''
    if not path or payload.get('tool_name') not in ('Edit', 'Write', 'MultiEdit'):
        return
    kind = tier(path)
    if not kind:
        return
    full = path if os.path.isabs(path) else os.path.join(payload.get('cwd') or os.getcwd(), path)
    if not os.path.isfile(full):
        return
    with open(full, encoding='utf-8', errors='replace') as fh:
        before = fh.read()
    after = after_edit(before, tool_input)
    if after == before:
        return
    if kind == 'loosen' and not loosens(before, after):
        return
    what = ('a lint, format or hook configuration file' if kind == 'strict'
            else 'a type-check, analysis or test configuration that this edit loosens')
    cv.block('config-protection', os.path.basename(path) + ' is ' + what, [
        '',
        'Do not change the checker to make the code pass it: fix the code the check complains about.',
        'A rule that is genuinely wrong for this project is a decision for the user, not for the agent that',
        'is currently failing it: state which rule, why it is wrong, and what you would change, then wait.',
        'Creating the file for the first time is allowed; so is a change the user makes or asks for explicitly',
        '(they can lift this guard for a task with MENTIS_ALLOW_CONFIG_CHANGES=1 in their own environment).',
    ])


if __name__ == '__main__':
    cv.guarded(main)
