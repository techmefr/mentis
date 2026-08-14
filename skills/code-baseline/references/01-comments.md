# code-baseline §1 — Comments

> Section 1 of `skills/code-baseline`. Read it when a comment is about to be written. The other sections and the guardrails stay in `SKILL.md`.

1. **No comments.** The one exception is a documentation block attached to a declaration — a function,
   method, class or module. Nothing else: no inline comment in a body, no comment above a statement, no
   end-of-line note, no commented-out code, no "why" comment.
2. The reason isn't aesthetic. **Nothing verifies a comment**: the compiler and the tests verify the code, so
   every comment is a future lie waiting for the next refactor. And a comment explaining code is a
   confession that the code is unreadable — the fix is the code.
3. **The three replacements, in order**: *rename* (a `// days until expiry` note next to `$d` disappears when
   the variable becomes `$daysUntilExpiry`); *extract a well-named function* (two statements wanting a
   `// validate then charge` note become `validateThenCharge()`); *restructure* until the shape carries the
   intent — early returns instead of a `// happy path` marker, a named constant instead of a `// 30 days`
   note.
4. **No ticket, story or issue identifier anywhere in the code** — not in a docblock, not in a variable,
   method or test name, not as "the story" or "user story 4.2". A tracker key describes *when* the code was
   written, not what it does, and it dies with the tracker. It belongs in the commit message, the MR
   title/description, and therefore in `git blame` — which is where anyone tracing a line will actually look.
5. **No AI attribution**: no co-author trailer naming an assistant, no "generated with" footer in a commit or
   MR body, no `@author`/`// AI-assisted` note in the code. Authorship records the **accountable human** —
   the engineer who reviewed it and will be asked about it. It also keeps `git blame` and contributor stats
   readable. Two carve-outs: a **real human** pair genuinely gets a co-author trailer, and existing commits
   that already carry an AI trailer are **never** rewritten (rewriting published history to strip a line is
   worse than the line).
