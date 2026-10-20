---
name: lifecycle-email-program-design-pitfalls
description: "Use when someone designs, audits or launches an automated email flow (welcome, onboarding, nurture, re-engagement, win-back, abandoned cart, a recurring digest) and the copy or the calendar is about to be written before the program is defined: no trigger or audience filter, no goal, no list of who must never get it, no exit condition, one mega-flow, several flows mailing the same person, suppression set per flow, a preference page standing in for the unsubscribe path, a sequence never read as the recipient will read it. A flow is a trigger, an audience, a suppression rule and an exit condition."
---

# lifecycle-email-program-design-pitfalls

Business layer (`business/README.md`), marketing. The repeated failure in automated email is a sequence written
as a pile of messages: the copy is polished, nobody wrote down what puts a person in, what keeps a person out,
or what takes them out, so the flow keeps mailing people who already did the thing, who now belong to another
flow, or who asked to stop. This block is the protocol for defining and reading a lifecycle program before any
copy exists. What a message needs to reach the inbox is `business/email-deliverability-and-sender-requirements-pitfalls`;
what a campaign metric can and cannot say, and how to test one, is `business/email-campaign-measurement-and-testing-pitfalls`;
a single outgoing one-to-one draft is `skills/customer-email-review-pitfalls`; one release announcement is
`business/release-communication`.

It states method only. It carries no sequence length, no day offset, no send hour, no frequency figure and no
benchmark, because the sources disagreed with each other on them and they are taste or folklore for one
audience. It is not legal advice: whether a message needs consent, what evidence of consent to keep, how long a
suppression record may live and what applies to business mail are questions for the person who owns data
protection, routed through `business/data-protection` (its email paragraph names them). Platform requirements it
mentions are marked `re-read before relying`.

## When
- A welcome, onboarding, nurture, re-engagement, win-back or abandoned-cart flow is being designed or audited.
- Someone asks "what emails should we send" and a calendar of subjects is about to be drafted.
- A second program is about to be added to a list that already receives one.
- A preference page, a pause option or a "manage emails" screen is being built or reviewed.
- A flow is about to go live, or has just gone live.

## Steps

**Read only the section the task meets.** §1 for any new or audited flow; §2 when a second program touches the
same people or a flow is growing; §3 for suppression, unsubscribe and preference pages; §4 before launch and
after it.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | The program definition: trigger, audience filter, goal, success metric, who must never get it, exit condition | a flow is being designed, audited or extended | [`01-define-the-program.md`](./references/01-define-the-program.md) |
| 2 | One purpose per flow, each message standing alone, and collisions between programs: an inventory of everything that can mail a person and one frequency rule across all of it | a flow is long, a second program joins the same audience, or someone asks "how often" | [`02-one-purpose-and-collisions.md`](./references/02-one-purpose-and-collisions.md) |
| 3 | Suppression and unsubscribe at account level, the classification of a message by what it is for, the preference page as a non-substitute for one-click unsubscribe | a bounce, complaint or unsubscribe rule is being set, or a preference page is proposed | [`03-suppression-and-preference-centre.md`](./references/03-suppression-and-preference-centre.md) |
| 4 | The pre-launch read as the recipient, and the first checks after launch: audience before copy | a flow is about to be activated or its first results are being read | [`04-pre-launch-read-and-first-checks.md`](./references/04-pre-launch-read-and-first-checks.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes, for each program: a one-page definition (trigger,
audience filter, goal, success metric with its system of record, never-send list, exit conditions, the other
programs that can reach the same people and the frequency rule that governs them); for an audit, each finding
as pass, fail or unknown; for a launch, the result of the pre-launch read per message. The owner of the program
reads it and decides; the block never activates a flow.

## Guardrails
- Define the program before writing any message: trigger, audience filter, goal, success metric, never-send
  list, exit conditions. Never start from the copy or from a calendar of subjects (§1).
- Give every flow an exit, and list who must never receive it. Never leave a flow that keeps mailing people who
  already reached its goal, became customers, replied or left (§1.3, §1.4).
- Keep one purpose per flow and make each message stand alone. Split a mega-flow into flows wired together.
  Never fold welcome, education and the first sales push into one sequence (§2.1, §2.2).
- Keep an inventory of every program that can mail a person and one frequency rule over all of them. Never add
  a program to an audience without asking what else that audience receives (§2.3).
- Apply suppression and unsubscribe to the whole account, and classify each message by what it is for. Never
  scope an unsubscribe to the flow that carried it, or sell mail as transactional because it was triggered
  (§3.1, §3.2).
- Offer a preference page as an addition, with the one-click path beside it. Never make a preference page the
  only way out (§3.3).
- Read the whole sequence as the recipient over the real timing, with the unsubscribe path visible, before
  activating it. Never launch a flow that has only been seen in the editor (§4.1).
- Judge a first result by the audience before the copy, and on a conversion, not on opens. Never tune the
  wording of a flow whose audience filter is unverified (§4.2).
- Treat consent, suppression retention and business-to-business questions as questions for data protection,
  not as defaults of this block (`business/data-protection`).
- This block is a method written from two young public repositories and never run on a real program by us.
  Source status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the program-definition, suppression and quality-check notes of an MIT marketing
skills repository and an MIT email-lifecycle skill, with a list-management reference from an MIT email-vendor
skills repository, read 2026-10-20. 🟡: never run by us, written without email-marketing expertise. Details in
[`references/origin.md`](./references/origin.md).
