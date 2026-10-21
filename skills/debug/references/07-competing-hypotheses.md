# debug §7 — Competing hypotheses and the evidence protocol

> Section 7 of `skills/debug`. Read it when the cause is unclear after the loop of §5 exists and the single
> hypothesis of `SKILL.md` §1 has not converged, when two people or agents investigate the same failure, or when a
> report of a root cause has to be judged. Source, read 2026-10-20: the parallel-debugging skill and the
> team-debugger agent of wshobson/agents (MIT, root licence). Sentences marked "own guidance" are ours. 🟡: never
> run on a real bug.

**How this fits the single-hypothesis rule.** `SKILL.md` §1 says one hypothesis per fix attempt, and §5 keeps it.
This section does not allow several at once in one investigator. It sets up the case where there are several
investigators, or where one investigator must choose which hypothesis to test next: each hypothesis is tested
separately, with its own criteria, and the fix is attempted only for the one that survives.

1. **Use it when the cause is genuinely open.** The source's cases: several plausible causes, early attempts have
   not found it, the failure spans modules, and you want to avoid settling on the first story that fits. Own
   guidance: if one cause is obvious and cheap to check, check it; this is for the second round, not the first.
2. **Generate hypotheses across kinds, not variations of one.** The source groups causes into logic, data, state,
   integration, resource and environment. Own guidance: write one hypothesis from at least three of the kinds
   before ranking, or the list is three versions of the first idea.
3. **A hypothesis is a falsifiable sentence about the cause.** "Something is wrong with the cache" is not one;
   "a stale cache entry is returned after the update, so the second read shows the old value" is. Check: you can
   say what you would see if it were false.
4. **Write the confirming and the falsifying evidence before looking.** For each hypothesis, list what you would
   observe if it were true and what you would observe if it were false, then go and look. The source's task
   template has both lists; writing them first is what stops a search from finding what it expected.
5. **Give each hypothesis its own investigation,** with its own scope: files to read, tests to run, the history
   range to inspect. Own guidance: two investigators who share one scope will converge on one story; two who
   share one working tree will also edit the same files (`skills/dispatch-parallel` §2).
6. **Classify the evidence by strength.** Direct (the code or a result shows it), correlational (it started after a
   change), testimonial ("it works for me"), and absence (nothing found). The source treats the last as variable.
   Rule: a cause needs direct evidence; correlation chooses where to look next, and testimony chooses nothing.
7. **Cite every piece of evidence by location.** File and line, a command and its output, a log line with its
   time. Own guidance: "I saw that" without a location is testimony.
8. **Report contradicting evidence as well.** The investigator's report lists what points against its own
   hypothesis. The source's report template has a section for it. Symptom of omitting it: the arbiter sees only
   confirmations from each side.
9. **State a confidence level and what it rests on.** The source uses three bands (high, medium, low) tied to the
   amount of direct evidence, whether the causal chain is complete and whether anything contradicts. The
   percentages it attaches are conventions, not measurements; use the bands and the three questions, not the
   numbers.
10. **Arbitrate with four outcomes.** Confirmed, plausible, falsified, inconclusive. Rank confirmed ones by
    confidence, amount of direct evidence, completeness of the causal chain and absence of contradiction. One
    clear winner is the root cause; several equally supported may be a compound cause; none confirmed means
    generate new hypotheses from what the investigations found.
11. **Write the causal chain from cause to symptom.** Each step is a thing that happened and a place where it can
    be seen. Own guidance: a chain with a step you cannot point at is a hypothesis still.
12. **Validate the fix against the chain, not only the symptom.** The source's list: the fix addresses the
    identified cause, introduces nothing new, the original reproduction no longer fails, and nearby edge cases are
    covered. This is `SKILL.md` §3 and §5 again; the new part is that the fix is tied to the chosen cause.
13. **Do not average the investigators.** Own guidance: three reports saying "probably" are not evidence for any
    of them. A confirmed hypothesis is one whose evidence you checked yourself, in the loop of §5.
14. **Anchor hypotheses on the symptom.** Own guidance: the source's starter lists by error kind (a server error, an
    intermittent failure, works locally but not in production, a regression after a release) are prompts for the
    kinds in point 2, not a diagnosis; re-derive them from your own repro.
