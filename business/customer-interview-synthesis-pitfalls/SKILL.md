---
name: customer-interview-synthesis-pitfalls
description: "Use when customer interviews are planned, run or turned into findings: a question that leads the answer, an interview of whoever replied first, a polite compliment or a future promise read as demand, a quote that is really the interviewer's inference, a theme claimed from one voice, a persona or roadmap line built on a handful of calls, a write-up that cannot be traced back to who said what. Question design, recruiting, separating quote from inference, coding observations, counting distinct people, confidence labels, claims the sample cannot carry."
---

# customer-interview-synthesis-pitfalls

Business layer (`business/README.md`), research. Interviews fail in three places: the question that suggests its
own answer, the step where a quote becomes an interpretation without anyone noticing, and the claim that outruns the
number of people behind it. This block is the check for each. Testing an assumption with a stated success
criterion is `skills/assumption-validation-pitfalls`; scoring a running app against contrasting personae is
`skills/persona-ux-audit`; judging someone else's study is `business/evidence-appraisal`; turning a stakeholder
request into a story is `business/product-ownership`; measuring behaviour with a controlled test is
`skills/experiment-design-pitfalls`; handling the personal data in recordings and notes is `business/data-protection`.

It states method only. It carries no sample size, no incentive amount, no survey benchmark and no
"enough interviews" figure: the sources gave such numbers from named studies or from experience without a
derivation, and a count depends on the question, the segment and the risk of being wrong.

## When
- A round of interviews or a discovery call series is being planned.
- A guide of questions is written or reviewed.
- Notes, transcripts or recordings are turned into themes, personas, quotes or roadmap input.
- A finding from interviews is about to be quoted as "customers say".

## Steps

**Read only the section the task meets.** §1 before fielding; §2 while coding notes; §3 before any claim leaves
the team.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Questions and recruiting: past behaviour over opinion, leading and hypothetical questions, compliments and promises, who is in the room | a guide is written or a participant list is built | [`01-questions-and-recruiting.md`](./references/01-questions-and-recruiting.md) |
| 2 | Observations versus inferences: verbatim quote, context, who said it, one fact per line, coding that can be redone | notes are taken or coded | [`02-quote-versus-inference.md`](./references/02-quote-versus-inference.md) |
| 3 | From themes to claims: distinct people not mentions, confidence label, contradictions, what a small sample can and cannot say | a theme, persona or recommendation is written | [`03-themes-and-claims.md`](./references/03-themes-and-claims.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the guide with the decision it feeds, a participant table
(segment, how found, why included), a coded observation sheet (who, verbatim, context, tag), and a findings list
where each line shows how many distinct people stand behind it and a confidence label. The research owner or
product owner decides what to build; a finding is input to that decision, never the decision.

## Guardrails
- Ask about what the person did, last time, and what happened. Never ask whether they would use, buy or like a
  thing, or put the answer in the question (§1).
- Say who was interviewed, how they were found and who is missing. Never present a handful of friendly
  volunteers as "customers" (§1).
- Keep the person's words, the context and your reading on separate lines. Never write an inference inside quotation
  marks (§2).
- Count distinct people behind a theme, not mentions. Never promote one loud voice or one long session into a
  pattern (§3).
- Label each finding with a confidence and name what would change it. Never write a persona, a market size or a
  priority from a few calls as if it were measured (§3).
- Record contradictions between what people said and did. Never drop the quote that breaks the story (§3).
- Keep notes traceable to a participant code and handle recordings as personal data. Never circulate a
  transcript with names to people who do not need it (§2).
- This block is a method written from two young public repositories and general research craft, never run by us on
  a real interview round. Source status and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the customer-research notes of an MIT marketing skills repository and the research
method notes of an MIT research-operations skill, read 2026-10-20, plus general interviewing craft. 🟡: never run
by us. Details in [`references/origin.md`](./references/origin.md).
