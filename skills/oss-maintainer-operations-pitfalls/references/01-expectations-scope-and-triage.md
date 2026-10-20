# oss-maintainer-operations-pitfalls §1 — Expectations, scope and triage

> Part 1 of `skills/oss-maintainer-operations-pitfalls`. Read it when the queue grows or a contribution does not
> fit. Source, read 2026-10-20: Open Source Guides, "Best Practices for Maintainers" (CC BY 4.0). Sentences marked
> "own guidance" are ours and rest on no source read.

1. **Write the rules down, even as bullets.** The guide's first advice is documentation: it clarifies the
   maintainer's own thinking, tells people what is expected before they ask, makes a refusal easier and a helping
   hand easier to offer. Rough bullets beat nothing. Symptom: the same question answered in ten threads. Fix: put
   the answer in a file and link it.
2. **Write the vision and the scope.** Put the project's goals in the README or a separate vision file, and
   publish any roadmap. The scope is what lets a maintainer decline something without it being personal.
3. **State what the process is.** The guide lists what to spell out: how a contribution is reviewed and accepted
   (tests required, an issue template), which kinds of contribution are welcome, when it is fair to follow up,
   and how much time the maintainers really have. Own guidance: a stated reply window is a promise, so set one
   you can keep; a window missed three times teaches people to stop waiting.
4. **Keep the conversation in public.** The guide says to move private requests into the open and to keep your
   own discussions public too. Reason: a decision made in a private message has to be made again for the next
   person, and a public thread is documentation. Where a thing must stay private (a security report, a conduct
   complaint), say so and use the channel written for it (`skills/security-advisory-comms-pitfalls` §1).
5. **Decline in four moves.** Thank them for the contribution; explain why it does not fit the project and, if
   possible, what would; link the relevant documentation; close the request. The guide asks for kind but firm.
   Symptom: a thread that argues for weeks. Fix: one reply with all four moves, then close.
6. **Turn repeated refusals into documentation.** When the same unwanted request keeps arriving, add it to the
   documented non-goals so the next refusal is a link. Own guidance: list each non-goal with a one-line reason.
7. **Ask for the shape of the request up front.** The guide suggests an issue or pull request template with a
   checklist, and asking contributors to open an issue before a large pull request. Own guidance: a template
   that asks for the version, the steps and the expected result cuts the "please add more detail" round trip;
   the issue-first rule for large changes spares both sides a rejected week of work.
8. **Triage on a cadence, with one owner at a time.** Own guidance: a queue read "when someone has time" is read
   by nobody. Fix: a fixed slot, one named person per slot, and four outcomes for every new item: reproduce or
   ask for the missing detail, label, route to a person or a milestone, or close with a reason. Leave no item
   with no outcome.
9. **Close the stale ones by rule, kindly.** Own guidance: an item waiting for the reporter's answer gets one
   reminder and a written deadline, then is closed with a sentence saying how to reopen it. The guide mentions
   a bot that closes issues whose author never answered a request for information; a visible written rule is
   the condition (`skills/oss-maintainer-operations-pitfalls` §3).
10. **Mentor the first contribution.** The guide recommends treating a newcomer's change as a chance to teach:
    point to the right documents, label starter tasks, and review for the person as well as the patch. Own
    guidance: a "good first task" label is worth keeping only while at least one such task is really open.

## Checks (own guidance)
1. A stranger finds the scope, the contribution steps and the reply window without opening a thread.
2. Every closed item shows a reason and a way back.
3. The oldest open item without an outcome is younger than one triage cycle.
