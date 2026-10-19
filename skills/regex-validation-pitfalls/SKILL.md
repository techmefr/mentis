---
name: regex-validation-pitfalls
description: "Use when a regular expression decides whether untrusted input is acceptable (validating an identifier, a path, a hostname, a redirect target, a header or a form field, or a pattern inside an allow-list, a route or a sanitiser config): matching the whole input, the anchors that differ between languages, a trailing newline slipping past the end anchor, alternation precedence and patterns that backtrack catastrophically."
---

# regex-validation-pitfalls

A defensive block for one narrow job: using a regular expression as a gate. Regexes are good at it, and they
fail in two quiet ways: the pattern accepts more than the author meant, because `$` does not mean the same
thing in every language, and the pattern can be made to run for minutes on a short hostile string. Neither shows
up in a test with only valid and clearly invalid inputs. The rules are the OpenSSF Best Practices Working
Group's guide to correct regex use for input validation, restated and credited in `references/origin.md`.
`skills/security-hardening` §1 owns the wider rule about validating at the boundary against an explicit shape;
this block owns the regex part of it.

## When
- A diff adds or changes a regex that accepts or rejects input: a username, a slug, a file name, a URL path, a
  host, an email-like value, a version string, a header value.
- A regex is copied from another language, a forum answer or a library into code in a different language.
- A framework validator takes a pattern and the pattern lives in configuration.
- A pattern matches user-controlled text and the service is shared.

## Steps

**Read the section for the failure you are worried about.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Matching the whole input: fullmatch, anchors per platform, the permissive `$`, alternation, tests | the pattern is a yes-or-no gate | [`01-whole-input.md`](./references/01-whole-input.md) |
| 2 | ReDoS: non-backtracking engines, pattern shape, bounds, timeouts | the pattern runs on text an outsider chooses | [`02-redos.md`](./references/02-redos.md) |

## Output / checkpoint
For each regex used as a gate: the language and engine, whether it uses a full-match call or explicit anchors
and which, how alternations are grouped, whether the engine can backtrack and what bounds the input length. The
evidence is two replays in a local environment: the valid value with a newline appended is rejected, and a
long near-miss string finishes in a time you wrote down.

## Guardrails
- Never accept a partial match for validation; anchor the pattern or call the full-match form (§1.1, §1.2).
- Never use `$` as "end of input" until the platform's behaviour is confirmed; prefer the explicit end anchor
  (§1.4).
- Never put alternatives in a pattern ungrouped (§1.5).
- Never port a regex between languages without translating its anchors and flags (§1.6).
- Never run a regex built from, or applied without a length bound to, untrusted input on a backtracking engine
  (§2.2, §2.4).
- Do not paste a real user's input or a production path into a prompt or a fixture; use made-up values.

## Origin
Rewritten from the OpenSSF Best Practices Working Group guide "Correctly Using Regular Expressions for Secure
Input Validation" and its rationale (CC-BY-4.0), read 2026-10-16. The attribution required by that licence, the
full provenance, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
