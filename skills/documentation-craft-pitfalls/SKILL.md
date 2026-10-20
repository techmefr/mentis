---
name: documentation-craft-pitfalls
description: "Use when a page of documentation is warranted and has to be written, restructured or reviewed (a README, a how-to, a reference page, a runbook): decide what the reader came to do, keep one purpose per page, write headings and steps people can scan and follow, and keep it true after the code moves."
---

# documentation-craft-pitfalls

A method for documentation that is read once under pressure and then trusted. The usual failures: a page that
tries to teach, instruct and specify at once and does none of them, steps that skip the one thing the reader
had to know, examples that no longer run, and a page nobody owns that keeps describing last year's system. The
block owns no docs tool, site generator or style linter. It sits beside `skills/documentation-adr` (a decision
record, a different document) and `skills/prose-lint-gate-pitfalls` (mechanical prose checks), and it does not
decide whether a document gets written: in a project repo that is the owner's call, and a page nobody asked for
is a cost, not a gift.

## When
- A document is requested or approved and the structure is still open.
- An existing README, guide or runbook is reviewed because people keep asking the question it should answer.
- Generated reference text (from comments or schemas) is about to be published.
- A page is found out of date and the question is how to keep the next one true.

**Skip when** there is no page to write or review, or the repository is a personal or one-maintainer project and the check needs a team: the owner is then the maintainer, and a step that does not fit is reported as "not applicable: reason", never as an invented finding. Reading existing pages for review is always in scope; only adding a file needs the owner's request.

## Steps

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Who reads it, what they came to do, one purpose per page, picking the page type | a page is planned or a page does two jobs | [`01-reader-and-page-type.md`](./references/01-reader-and-page-type.md) |
| 2 | Headings, lists, procedures and code examples that can be scanned and followed | a page is written or edited | [`02-writing-for-scanning-and-following.md`](./references/02-writing-for-scanning-and-following.md) |
| 3 | Keeping it true: ownership, tested examples, runbooks, the final review | a page is reviewed, or will outlive its author | [`03-keeping-it-true.md`](./references/03-keeping-it-true.md) |

## Output / checkpoint
No pipeline checkpoint. A short brief before writing (reader, the task they arrive with, the page type, what is
out of scope, who owns the page) and, after, the page plus the list of statements in it that a code change
could make false, each with the check that would notice.

## Guardrails
- Ask whether a page is warranted before drafting it. Never add a documentation file unprompted; explain in the
  conversation, the commit message or the review instead, unless the owner asked for the page or the repository
  already has one for this subject. Reviewing, correcting or reading existing pages needs no such permission.
- Check what a page says about privacy, security, tracking, versions and commands against the shipped code and
  the other pages of the same repository. Never leave two pages that contradict each other (§3.15, §3.16).
- Give each page one purpose and link to the others. Never merge a tutorial, a procedure and a specification
  because they share a subject.
- Run every command and example in the page before it ships. Never publish a snippet that was only read.
- Name an owner and a trigger for the next check. Never leave a runbook that nobody has executed since it was
  written.
- Mark what you did not verify in the page itself. Never present a guess about system behaviour as a fact.

## Origin
Microsoft Writing Style Guide (CC BY 4.0, read 2026-10-20) for content planning, headings, lists, procedures,
code examples, reference pages and the final review, rewritten, plus own guidance flagged in the references.
Provenance, what was removed and not verified: [`references/origin.md`](./references/origin.md). 🟡: never
dogfooded.
