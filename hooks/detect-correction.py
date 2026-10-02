#!/usr/bin/env python3
"""mentis: a correction from the person is noticed and turned into a lesson (UserPromptSubmit). OPT-IN:
needs MENTIS_CORRECTION_DETECTOR=1 in the session environment.

When the prompt opens with, or contains, a phrase that corrects the previous answer ("no, that is wrong",
"you forgot", "I told you", "non, c'est faux", "pas ça"), it appends one line to MENTIS_CORRECTIONS_LOG
(default ~/.mentis-corrections.jsonl, text truncated to 300 characters) and returns a short reminder as
additional context: state what rule or assumption was wrong, fix the work, and propose the rule that would
have prevented it (a guardrail line in a block) instead of only apologising.

Never blocks. Fails open on any error. A heuristic on wording: it misses corrections phrased in no way
it knows, and it can fire on a prompt that quotes such a phrase.
"""
import json
import os
import re
import sys
import time

PATTERNS = [
    r"^\s*(no|nope|non|nein)\s*[,.!:]",
    r"\b(that'?s|this is|it'?s|c'?est|ce n'?est pas|ce n'est) +(wrong|incorrect|not (right|what)|faux|incorrect|pas (ça|ce que))",
    r"\b(you|tu|vous) +(forgot|missed|ignored|broke|didn'?t|did not|as oublié|avez oublié|n'as pas|n'avez pas)\b",
    r"\bi (already )?(told|said|asked)\b",
    r"\b(je t'ai|je vous ai) +(déjà )?(dit|demandé)\b",
    r"\b(stop|arrête|arrêtez)\b[ ,]+(doing|de |d')",
    r"\bnot what i (asked|wanted|meant)\b",
    r"\bpas (ça|ce que j'ai demandé)\b",
]
COMPILED = [re.compile(p, re.I) for p in PATTERNS]
REMINDER = ('The person is correcting you. Before answering: name in one line the assumption or rule that was '
            'wrong, fix the work, and propose the one-line guardrail that would have prevented it (in the '
            'relevant block, or the project memory if it is specific to this project). Do not only apologise.')


def main():
    if os.environ.get('MENTIS_CORRECTION_DETECTOR') != '1':
        return
    try:
        data = json.loads(sys.stdin.read())
        prompt = data.get('prompt') or ''
        if not isinstance(prompt, str):
            return
        head = prompt[:600]
        if not any(p.search(head) for p in COMPILED):
            return
        log = os.environ.get('MENTIS_CORRECTIONS_LOG') or os.path.join(os.path.expanduser('~'), '.mentis-corrections.jsonl')
        try:
            with open(log, 'a', encoding='utf-8') as handle:
                handle.write(json.dumps({'at': int(time.time()), 'session': data.get('session_id') or '',
                                         'text': prompt[:300]}, ensure_ascii=False) + '\n')
        except OSError:
            pass
        sys.stdout.write(json.dumps({'hookSpecificOutput': {'hookEventName': 'UserPromptSubmit',
                                                            'additionalContext': REMINDER}}))
    except Exception:
        return


if __name__ == '__main__':
    main()
