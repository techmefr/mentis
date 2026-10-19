# session-retro §2 — Classify and place

> Section 2 of `skills/session-retro`. §1 produces the candidates, this section decides where each fix goes.

## 2.1 The classification comes first
1. **Classify the violation before choosing a fix.** Mechanical: a fixed syntactic pattern, a banned call, an
   import shape, a file-location rule. Judgement: consistency across files, "matches the surrounding style",
   anything no tool could substitute for.
2. **A mechanical violation gets a deterministic check, and the default is to build the check rather than write
   the rule.** The cheapest of: a custom rule in the repository's own linter, a pre-commit hook, a CI job.
3. **Only a judgement call becomes prose**, in the file the reviewer reads.
4. **Worked case (ours).** A session left a database call inside a loop and the reviewer let it through. The
   pattern is mechanical (a query function called within an iteration body), so the candidate is a lint rule in the
   project's linter, not a line "never query in a loop" in a steering file. A session in which the agent chose a
   clumsy but valid abstraction is a judgement call: it goes to the standards the reviewer applies.

## 2.2 Where a fix lands
| Category | Destination |
|---|---|
| Navigation | a pointer from a file the agent already reads |
| Automated checks, mechanical standards | the check itself, or wiring the one that exists |
| Judgement standards | the standards file the reviewer reads, not the file loaded into every session |
| Steering-file size | move the content out to standards or to a check |
| Tool economy | streamline or replace the tool |
| No-ops | delete the line |
| Information access | widen access (tee a log to a file, a read-only view of a service) |

1. **Standards are imposed at review, not at implementation.** The implementing agent carries the most context
   pressure (exploring, writing, debugging); the reviewer receives a diff and has room to apply a rule. A new
   standard goes where there is room.
2. **Steering files carry pointers and little else.** They load into every session whether relevant or not, so a
   line added there dilutes every other line and goes stale as the code changes.
3. **Use a document for reference, pointed to by others; look for an existing one before writing a new one.**

## 2.3 What the report must carry
1. **Per candidate**: the moment (cited), the category, the mechanical-or-judgement call, the proposed fix and
   where it lands.
2. **An existing but unwired check is reported as that.**
3. **Nothing is applied.** The operator picks a candidate; a proposed check is code like any other and is tried
   against the repository before it is allowed to block a merge.
4. **State the blind spot.** This looks at one session. It cannot tell that a rule proposed earlier now fires too
   often or that the bug behind it is gone; pruning checks is a separate act, and a rule that keeps firing on good
   code is the sign to remove it (`skills/maintaining-blocks` §4).
