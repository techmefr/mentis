#!/usr/bin/env python3
"""mentis: shared command-boundary reader for the opt-in command hooks.

Not a hook by itself. block-no-verify, guard-commit-message and guard-destructive import it so
that the three agree on what "a command" is. Copy it next to them.

A word counts as a command only where a command starts: the start of the text, or after an unquoted
newline, ; & | ( ) or a backtick, once leading wrappers (sudo, env, VAR=value, time, xargs) are
peeled off. Quoted text is one argument and never a command, so `grep "rm -rf" notes` and
`git commit -m "fix: no --no-verify"` carry the words as data. The command inside `ssh host "..."`,
`sh -c "..."`, `bash -lc '...'`, `eval ...` and `find -exec ...` is unwrapped and judged the same way.

Limits, stated because a reader trusts a guard as far as it is honest: a command substitution
inside double quotes is data here, an alias or a script assembled at run time is not seen, and a
quoting error makes the broken segment be read with a plain whitespace split instead of failing.
"""
import json
import os
import re
import shlex
import sys

LEADERS = {'{', 'then', 'do', 'else', 'elif', 'if', 'while', 'until', '!'}
WRAPPERS = {'sudo', 'doas', 'env', 'nohup', 'time', 'command', 'exec', 'nice', 'stdbuf', 'xargs', 'timeout'}
SHELLS = {'sh', 'bash', 'zsh', 'dash', 'ksh'}
SSH_ARG_FLAGS = {'-p', '-i', '-l', '-o', '-F', '-J', '-L', '-R', '-D', '-b', '-c', '-e', '-E', '-I',
                 '-m', '-O', '-Q', '-S', '-w', '-W'}
MAX_DEPTH = 5

HEREDOC = re.compile(r"<<(-?)\s*(['\"]?)([A-Za-z_][A-Za-z0-9_-]*)\2")
REDIRECT = re.compile(r'^\d*(>>?|<)(&?\d+|&-)?$|^&>>?$')
GLUED_REDIRECT = re.compile(r'^\d*(>>?|<)(?!<)\S+$|^\d*>&\d+$')


class View:
    def __init__(self, tokens, env, privileged, heredocs, depth):
        self.tokens = tokens
        self.env = env
        self.privileged = privileged
        self.heredocs = heredocs
        self.depth = depth

    @property
    def name(self):
        return os.path.basename(self.tokens[0]) if self.tokens else ''


def load_payload():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def split_segments(text):
    """Split on unquoted command boundaries. Returns [(segment_text, [heredoc_body, ...])]."""
    text = text.replace('\\\n', ' ')
    segments = []
    buf = []
    heredocs = []
    pending = []
    quote = None
    i = 0
    n = len(text)

    def flush():
        nonlocal buf, heredocs
        seg = ''.join(buf).strip()
        if seg:
            segments.append((seg, heredocs))
        buf = []
        heredocs = []

    while i < n:
        ch = text[i]
        if quote:
            buf.append(ch)
            if ch == '\\' and quote == '"' and i + 1 < n:
                buf.append(text[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            i += 1
            continue
        if ch == '\\' and i + 1 < n:
            buf.append(ch)
            buf.append(text[i + 1])
            i += 2
            continue
        if ch in ('"', "'"):
            quote = ch
            buf.append(ch)
            i += 1
            continue
        if ch == '#' and (not buf or buf[-1] in ' \t'):
            while i < n and text[i] != '\n':
                i += 1
            continue
        if text.startswith('<<', i) and not text.startswith('<<<', i):
            m = HEREDOC.match(text, i)
            if m:
                pending.append((m.group(3), m.group(1) == '-'))
                buf.append(m.group(0))
                i = m.end()
                continue
        if ch == '\n':
            flush()
            i += 1
            while pending:
                delim, strip = pending.pop(0)
                body = []
                while i < n:
                    j = text.find('\n', i)
                    line = text[i:] if j == -1 else text[i:j]
                    i = n if j == -1 else j + 1
                    if (line.strip('\t') if strip else line).rstrip() == delim:
                        break
                    body.append(line)
                if segments:
                    segments[-1][1].append('\n'.join(body))
            continue
        if text.startswith('$(', i):
            flush()
            i += 2
            continue
        if ch == '&' and buf and buf[-1] in '<>':
            buf.append(ch)
            i += 1
            continue
        if ch in ';&|()`':
            flush()
            i += 1
            continue
        buf.append(ch)
        i += 1
    flush()
    return segments


def is_env_assignment(tok):
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*=', tok) is not None


def strip_leaders(toks):
    privileged = False
    env = []
    i = 0
    while i < len(toks):
        tok = toks[i]
        base = os.path.basename(tok)
        if is_env_assignment(tok):
            env.append(tok)
            i += 1
        elif tok in LEADERS:
            i += 1
        elif base in WRAPPERS:
            if base in ('sudo', 'doas'):
                privileged = True
            i += 1
            while i < len(toks) and (toks[i].startswith('-') or is_env_assignment(toks[i])
                                     or (base == 'timeout' and re.match(r'^\d', toks[i]))):
                if is_env_assignment(toks[i]):
                    env.append(toks[i])
                i += 1
        else:
            break
    return toks[i:], privileged, env


def drop_redirects(toks):
    out = []
    skip = False
    for tok in toks:
        if skip:
            skip = False
            continue
        if REDIRECT.match(tok):
            skip = not re.search(r'&', tok)
            continue
        if GLUED_REDIRECT.match(tok):
            continue
        out.append(tok)
    return out


def tokenize(seg):
    try:
        return shlex.split(seg)
    except ValueError:
        return seg.split()


def inner_commands(toks):
    out = []
    for k, tok in enumerate(toks):
        if os.path.basename(tok) in SHELLS:
            for j in range(k + 1, len(toks) - 1):
                if re.match(r'^-[A-Za-z]*c[A-Za-z]*$', toks[j]):
                    out.append(toks[j + 1])
                    break
                if not toks[j].startswith('-'):
                    break
            break
    if toks and os.path.basename(toks[0]) == 'ssh':
        j = 1
        while j < len(toks) and toks[j].startswith('-'):
            j += 2 if toks[j] in SSH_ARG_FLAGS else 1
        if j + 1 < len(toks):
            out.append(' '.join(toks[j + 1:]))
    if toks and toks[0] == 'eval' and len(toks) > 1:
        out.append(' '.join(toks[1:]))
    if toks and os.path.basename(toks[0]) == 'find':
        for k, tok in enumerate(toks):
            if tok in ('-exec', '-execdir', '-ok', '-okdir'):
                body = []
                for t in toks[k + 1:]:
                    if t in (';', '+'):
                        break
                    body.append(t)
                if body:
                    out.append(' '.join(shlex.quote(t) for t in body))
    return out


def views(text, depth=0):
    """Yield one View per command found in the text, including unwrapped inner commands."""
    for seg, heredocs in split_segments(text):
        toks = drop_redirects(tokenize(seg))
        rest, privileged, env = strip_leaders(toks)
        if not rest:
            if env:
                yield View([], env, privileged, heredocs, depth)
            continue
        yield View(rest, env, privileged, heredocs, depth)
        if depth < MAX_DEPTH:
            for inner in inner_commands(rest):
                yield from views(inner, depth + 1)


GIT_OPTS_WITH_VALUE = {'-C', '-c', '--git-dir', '--work-tree', '--namespace', '--exec-path',
                       '--super-prefix', '--config-env', '--attr-source'}


def git_parts(view):
    """For a View whose command is git: (global option pairs, subcommand, args)."""
    toks = view.tokens
    opts = []
    i = 1
    while i < len(toks) and toks[i].startswith('-'):
        tok = toks[i]
        if tok in GIT_OPTS_WITH_VALUE:
            opts.append((tok, toks[i + 1] if i + 1 < len(toks) else ''))
            i += 2
        else:
            opts.append((tok.split('=', 1)[0], tok.split('=', 1)[1] if '=' in tok else ''))
            i += 1
    sub = toks[i] if i < len(toks) else ''
    return opts, sub, toks[i + 1:]


def block(tool, why, lines):
    print('BLOCKED by mentis ' + tool + ': ' + why + '.', file=sys.stderr)
    for line in lines:
        print(line, file=sys.stderr)
    sys.exit(2)


def guarded(main):
    """Run a hook. Any failure of the hook itself allows the call: a tripwire that breaks the session gets removed."""
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)
    sys.exit(0)
