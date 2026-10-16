---
name: deprecation-notice-pitfalls
description: "Use when an API, a version or a feature is being deprecated or sunset and the notice has to reach the people who must act: recording the deprecation in the API specification, obtaining consent to a sunset date instead of assuming it, monitoring who still calls it, the Deprecation and Sunset response headers and their limits, a human-readable warning header, reaching the developer rather than the account contact, and the per-release removed-APIs page with replacements and changed defaults."
---

# deprecation-notice-pitfalls

The premise: **a deprecation notice is part of the interface, not a blog post, and shutting a feature down is a
breaking change until every client has agreed a date.** Most failures are communication failures: the notice
went to the wrong person, a header was taken for consent, or a changed default was not mentioned. This block is
about the notice. The mechanics of migrating callers and keeping old and new side by side are in
`deprecation-migration`; the design of the interface in `api-design`; the changelog or announcement text in
`release-notes-writing-pitfalls`; a breaking change in one framework in `laravel-api-breaking-changes`.

## When
- An endpoint, a field, a version or a whole feature is about to be marked deprecated or given a sunset date.
- You are about to rely on a response header or an email to tell callers.
- A release removes an interface and the "removed" page is being written.
- You consume someone else's API and want to be told in time.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Specification first, consent, the minimum time, monitoring usage, the two headers and their limits | you are the producer planning a deprecation | [`01-producer-rules.md`](./references/01-producer-rules.md) |
| 2 | Warning a human, reaching the right reader, the removed-APIs page, what clients must do | you write the notice text or consume an API | [`02-notice-and-clients.md`](./references/02-notice-and-clients.md) |

## Output / checkpoint
The deprecated element marked in the specification with its replacement, migration steps and, if planned, a
sunset date; the consent record per client (or the decision that none is needed and why); the usage monitor
and who reads it; the headers sent and on which responses; the human-readable warning and its trigger; the
removed-APIs entry with replacement, versions, stored data and behaviour changes. What could not be checked is
listed.

## Guardrails
- Never treat a header or an email as consent to a sunset (§1.2, §1.5).
- Never shut a feature down while anyone still uses it without an agreed date (§1.2).
- Never put the notice only in a changelog line, and never leave out changed defaults (§2.3).
- Never mention a warning header to scare callers whose call will keep working (§2.1).
- Never write a fixed minimum window as a rule; the sources disagree and the choice is yours (§1.3).
- The standards behind the headers were not read; the sources cite them and the numbers are theirs. Check
  before citing (see [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten from Zalando's REST API guidelines on deprecation, Microsoft's API guidelines for Graph and Azure
deprecation, and the Kubernetes deprecated-API migration guide (all CC-BY-4.0, attribution in the origin file),
read 2026-10-16. 🟡: never used by us in a real deprecation; details in
[`references/origin.md`](./references/origin.md).
