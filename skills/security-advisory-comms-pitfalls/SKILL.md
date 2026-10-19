---
name: security-advisory-comms-pitfalls
description: "Use when a vulnerability report from outside the team has to be answered and announced: acknowledging the report, assessing it into working as intended, bug, feature request or vulnerability and saying why, agreeing an embargo with the reporter, crediting them, writing the embargoed notice and the public advisory with affected and fixed versions, choosing the release day, handling a partial fix, a fix that is impossible, a report that went public without you, and a reporter who stops answering."
---

# security-advisory-comms-pitfalls

The premise: **the people who report a vulnerability have done you a favour, and most of what goes wrong is
communication, not code: a silent first week, a vague deadline, an advisory without version ranges, a leak from
a list that grew too large.** This block covers the words and the sequence. For a customer-wide incident
notice, read `incident-comms-pitfalls`; for the written review afterwards, `blameless-incident-review-pitfalls`;
for hardening the code itself, `security-hardening`; for turning an advisory into release text,
`release-notes-writing-pitfalls`.

The source is a guide for open-source maintainers. A company that ships a product has contracts and customers
who expect a named contact; the sequence below still applies, but who agrees the dates and who signs the
advisory is your own governance.

## When
- A report claiming a vulnerability has just arrived, from a customer, a researcher or a colleague.
- A fix is nearly ready and someone has to decide who is told, when, and with what.
- A deadline set by a reporter is about to pass without a complete fix.
- A vulnerability turned up in public before you knew about it.

## Steps

**Read only the section the task meets.**

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Acknowledging, assessing, telling the reporter why, the embargo conversation, credit | a report has just arrived | [`01-intake-and-embargo.md`](./references/01-intake-and-embargo.md) |
| 2 | The patch, the release day, the embargoed notice, the public advisory and what it must contain | a fix exists or is close | [`02-notices-and-disclosure.md`](./references/02-notices-and-disclosure.md) |
| 3 | Partial fix, impossible fix, public disclosure without you, silent reporter, exploitation in the wild | the plan is not going smoothly | [`03-when-it-goes-wrong.md`](./references/03-when-it-goes-wrong.md) |

## Output / checkpoint
The acknowledgement sent, with its date; the assessment and the reason given to the reporter; the agreed
embargo end and who agreed it; the credit wording the reporter chose; the affected and fixed versions; the
embargoed notice if one is used, with its recipients; the public advisory with its timeline; what is still
open. Anything not checked (for example a regulatory reporting duty) is listed as not checked.

## Guardrails
- Never leave a report unacknowledged while you assess it (§1.1).
- Never close a non-vulnerability report without saying why (§1.2).
- Never set an embargo alone, or leave one open-ended (§1.3).
- Never omit a reporter's credit unless they asked for that (§1.4).
- Never cut the release before the embargoed notice has gone out (§2.2).
- Never publish an advisory without the affected and fixed versions (§2.5).
- Never hold exploit details back for more than a few days (§2.5).
- Never claim a partial fix is complete (§3.1).
- This block states no regulatory reporting duty and no embargo length as a rule; the published figures differ
  and none was re-checked at its source (see [`references/origin.md`](./references/origin.md)).

## Origin
Rewritten from the OpenSSF vulnerability disclosure guide for maintainers (CC-BY-4.0, attribution in the
origin file), read 2026-10-16. The guide's step numbering is garbled in places and is not mirrored. 🟡: never
used by us on a real report; details in [`references/origin.md`](./references/origin.md).
