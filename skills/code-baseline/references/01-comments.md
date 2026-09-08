# code-baseline §1 — Comments

> Section 1 of `skills/code-baseline`. Read it when a comment is about to be written. The other sections and the guardrails stay in `SKILL.md`.

1. **No comments.** The one exception is a documentation block attached to a declaration — a function,
   method, class or module. Nothing else: no inline comment in a body, no comment above a statement, no
   end-of-line note, no commented-out code, no "why" comment.
2. The reason isn't aesthetic. **Nothing verifies a comment**: the compiler and the tests verify the code, so
   every comment is a future lie waiting for the next refactor. And a comment explaining code is a
   confession that the code is unreadable — the fix is the code.
3. **The lie is worse than the absence.** Code with no explanation makes a reader work; code with a stale
   explanation makes a reader wrong, and confidently — they act on the sentence rather than reading the
   twelve lines under it. That is the same asymmetry §8 is built on: a declaration consumes the attention
   that would otherwise have found the truth.
4. **The three replacements, in order**: *rename* (a `// days until expiry` note next to `$d` disappears when
   the variable becomes `$daysUntilExpiry`); *extract a well-named function* (two statements wanting a
   `// validate then charge` note become `validateThenCharge()`); *restructure* until the shape carries the
   intent — early returns instead of a `// happy path` marker, a named constant instead of a `// 30 days`
   note.
5. **A comment in a diff is a missing rename or a missing extraction**, and that is how to read one at
   review time. The useful question is never "is this comment accurate" but "what did the author fail to be
   able to say in the code" — which usually answers itself in one line of the surrounding function.
6. **The docblock carries the contract, not the signature.** What the types already state does not need
   restating: a block that lists each parameter's type and nothing else is pure duplication, so it carries
   the same staleness risk with none of the value. What belongs there is what a caller cannot see — which
   failures it raises (§3), what it returns at the edges, whether it is safe to call twice, what it costs.
7. **Commented-out code is deleted.** Version control already holds it, and the commented block is worse
   than an absence because nobody can tell whether it is a rollback plan, a half-finished idea or something
   that was disabled during an incident and forgotten. It also silently escapes every tool: it is not
   compiled, not tested, not linted, and not found when its function is renamed.
8. **A `TODO` is a decision left to nobody.** In the code it is invisible to whoever plans the work and
   permanent to whoever reads the file, and its most common effect is to make an unfinished guarantee look
   handled (§8.3). Do it, or record it where work is actually tracked — the same reasoning as point 10.
9. **A section-divider comment is a file asking to be split.** `// ---- helpers ----` marks a seam that the
   author has already found; §2.4 is the response to it. The same applies to a comment introducing "the
   validation part" of a long function.
10. **No ticket, story or issue identifier anywhere in the code** — not in a docblock, not in a variable,
    method or test name, not as "the story" or "user story 4.2". A tracker key describes *when* the code was
    written, not what it does, and it dies with the tracker. It belongs in the commit message, the MR
    title/description, and therefore in `git blame` — which is where anyone tracing a line will actually look.
11. **The "why" that genuinely matters belongs where it is durable.** A rationale written in the code decays
    with the code and is invisible to anyone reading a diff; the same paragraph in the commit message and
    the MR description is reachable from every line it touched, for ever, through blame. The subset of "why"
    that must live in the code is not prose: it is a named constant, a named function, or a test that fails
    if the constraint is ever violated — three things that cannot go stale silently.
12. **A workaround for someone else's bug is the strongest case, and it still resolves the same way.** It is
    isolated behind a wrapper (§7.4), the reason goes in that wrapper's docblock — where point 6 already
    allows it — and a test asserts the behaviour so that the day upstream fixes it, something goes red
    instead of the workaround living for ever unnoticed.
13. **Comment-shaped things that are not comments.** An annotation or directive the tooling reads (a type
    hint, a suppression the linter acts on, a framework attribute), a shebang, and a licence header where
    licensing requires one are all code as far as this rule is concerned: something consumes them, so
    something breaks when they are wrong. A comment nothing consumes is the thing under discussion.
14. **No AI attribution**: no co-author trailer naming an assistant, no "generated with" footer in a commit or
    MR body, no `@author`/`// AI-assisted` note in the code. Authorship records the **accountable human** —
    the engineer who reviewed it and will be asked about it. It also keeps `git blame` and contributor stats
    readable. Two carve-outs: a **real human** pair genuinely gets a co-author trailer, and existing commits
    that already carry an AI trailer are **never** rewritten (rewriting published history to strip a line is
    worse than the line).
15. **It binds this diff.** Comments found in code you are not otherwise touching stay: stripping them is an
    unrelated change that makes the diff unreviewable, and the rule exists to stop comments being written,
    not to license a sweep (§8.6). Removing one you are already editing around is fine.
