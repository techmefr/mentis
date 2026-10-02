#!/usr/bin/env python3
"""mentis: a commit message is checked before the commit exists (PreToolUse on Bash). OPT-IN.

Reads the message of a `git commit` (-m, --message, -F, a heredoc) and refuses it when:
  - the subject is not a conventional commit (`type(scope)!: description`);
  - the description does not start lowercase (a leading acronym is fine);
  - any line attributes the change to a tool (a co-author trailer or a "generated with" line naming an
    AI assistant). The commit is the developer's: they reviewed it and answer for it.

A commit with no message on the command line (editor, --amend with no -m, -C, --no-edit) is not judged:
the text is not visible here. Merge, revert, fixup, squash and amend subjects git writes itself pass.
MENTIS_COMMIT_TYPES (comma-separated) replaces the default type list. Fails open on any error.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import command_views as cv

DEFAULT_TYPES = 'feat,fix,docs,style,refactor,perf,test,build,ci,chore,revert'
TOOL_NAMES = (r'claude|anthropic|copilot|chatgpt|openai|gpt-?\d|codex|gemini|cursor|aider|windsurf|'
              r'tabnine|codeium|llm')
TOOLS = r'\b(' + TOOL_NAMES + r')\b'
PROSE_TOOLS = r'\b(' + TOOL_NAMES + r'|ai|artificial intelligence)\b'
TRAILER = re.compile(r'^\s*(co-authored-by|signed-off-by|assisted-by|generated-by|created-by|authored-by|'
                     r'made-with|written-by|reviewed-by)\s*:.*' + TOOLS, re.I)
PROSE = re.compile(r'\b(generated|written|authored|created|assisted|made|produced|drafted)\s+(with|by|using)\b'
                   r'.*' + PROSE_TOOLS, re.I)
ROBOT = re.compile('\U0001F916')
GIT_WRITTEN = re.compile(r'^(Merge |Revert "|fixup! |squash! |amend! )')
HEREDOC_VALUE = re.compile(r"^\$\(\s*cat\s*<<-?\s*['\"]?(\w+)['\"]?\n(.*?)\n[ \t]*\1[ \t\n]*\)$", re.S)
VALUE_SHORT = set('mFCctu')


def message_parts(args, heredocs, cwd):
    parts = []
    undetermined = False
    i = 0

    def take(value):
        nonlocal undetermined
        m = HEREDOC_VALUE.match(value)
        if m:
            parts.append(m.group(2))
        elif '$(' in value or '`' in value:
            undetermined = True
        else:
            parts.append(value)

    def read_file(path):
        nonlocal undetermined
        if path == '-':
            if heredocs:
                parts.append(heredocs[0])
            else:
                undetermined = True
            return
        full = path if os.path.isabs(path) else os.path.join(cwd or os.getcwd(), path)
        try:
            with open(full, encoding='utf-8', errors='replace') as fh:
                parts.append(fh.read())
        except OSError:
            undetermined = True

    while i < len(args):
        arg = args[i]
        if arg == '--':
            break
        if arg in ('-m', '--message') and i + 1 < len(args):
            take(args[i + 1])
            i += 2
            continue
        if arg.startswith('--message='):
            take(arg.split('=', 1)[1])
        elif arg in ('-F', '--file') and i + 1 < len(args):
            read_file(args[i + 1])
            i += 2
            continue
        elif arg.startswith('--file='):
            read_file(arg.split('=', 1)[1])
        elif re.match(r'^-[A-Za-z]', arg):
            for pos, ch in enumerate(arg[1:], start=1):
                if ch in VALUE_SHORT:
                    glued = arg[pos + 1:]
                    if ch == 'm':
                        if glued:
                            take(glued)
                        elif i + 1 < len(args):
                            take(args[i + 1])
                            i += 1
                    elif ch == 'F':
                        if glued:
                            read_file(glued)
                        elif i + 1 < len(args):
                            read_file(args[i + 1])
                            i += 1
                    elif not glued:
                        i += 1
                    break
        elif arg in ('--author', '--date', '--cleanup', '--template', '--trailer', '-C', '-c',
                     '--reuse-message', '--reedit-message', '--fixup', '--squash'):
            i += 1
        i += 1
    return parts, undetermined


def judge(message, types):
    lines = message.splitlines()
    subject = next((ln for ln in lines if ln.strip()), '')
    problems = []
    for ln in lines:
        if TRAILER.search(ln) or PROSE.search(ln) or ROBOT.search(ln):
            problems.append('attribution to a tool: ' + ln.strip()[:100])
    if subject and not GIT_WRITTEN.match(subject):
        m = re.match(r'^(' + '|'.join(re.escape(t) for t in types) + r')(\([^()\s]+\))?!?: (\S.*)$', subject)
        if not m:
            problems.append('the subject is not "type(scope): description" with a type from: ' + ', '.join(types)
                            + ' -> ' + subject[:100])
        else:
            first_word = m.group(3).split()[0]
            if m.group(3)[0].isupper() and not (len(first_word) > 1 and first_word.isupper()):
                problems.append('the description starts with a capital letter -> ' + subject[:100])
    return problems


def main():
    payload = cv.load_payload()
    if not payload:
        return
    tool_input = payload.get('tool_input') or {}
    command = tool_input.get('command', '') if isinstance(tool_input, dict) else ''
    if not isinstance(command, str) or 'commit' not in command:
        return
    types = [t.strip() for t in (os.environ.get('MENTIS_COMMIT_TYPES') or DEFAULT_TYPES).split(',') if t.strip()]
    for view in cv.views(command):
        if view.name != 'git':
            continue
        _opts, sub, args = cv.git_parts(view)
        if sub != 'commit':
            continue
        parts, undetermined = message_parts(args, view.heredocs, payload.get('cwd', ''))
        if not parts:
            continue
        message = '\n\n'.join(parts)
        problems = judge(message, types)
        if problems:
            cv.block('guard-commit-message', 'this commit message breaks the house format', [''] + ['  - ' + p for p in problems] + [
                '',
                'Format: type(scope)!: description, in lowercase, one subject line, then an optional body.',
                'No line may credit a tool for the change: no co-author trailer or "generated with" footer naming',
                'an assistant. The author of a commit is the developer who reviewed it and answers for it.',
                'Rewrite the message and commit again.',
            ])


if __name__ == '__main__':
    cv.guarded(main)
