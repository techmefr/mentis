# gate §10 — Excuses and red flags

> Section 10 of `skills/gate`. Read it when you notice yourself explaining why a check can be skipped, or when
> the evaluator's verdict feels like a formality. **These excuses are predicted, not recorded**: they are what a
> verifying agent under pressure is likely to say, written before a run exists. When `skills/testing-blocks` §1
> yields the sentences a run without this block really produced, replace them here, verbatim, and drop this notice.

1. **How to use the table.** Find the thought. If it matches, do what the right column says before the next
   action. The thoughts are the symptom; the check they excuse is the cure.

   | The thought | What is actually true |
   |---|---|
   | "It should work now" | Should is the word for not having run it. Run it. |
   | "I am confident" | Confidence is a feeling about the code; the gate wants the output. |
   | "The linter passed" | A linter does not compile and does not run tests. |
   | "It is only a small change" | The gate is about the claim, not the size. Small changes break builds too. |
   | "The worker said it passed" | A report is a claim. Check the diff and run it yourself. |
   | "Just this once" | There is no once. The next once is the one that ships a broken build. |
   | "A partial run is enough" | A partial run proves the part it ran. |
   | "I am tired, it is probably fine" | Tired is when the broken thing gets through. Run the command. |
   | "Different wording, so the rule does not apply" | The rule is about the claim, whatever the words. |
   | "The test passes, so the requirement is met" | The test checks what was written into it. Check the criterion. |
   | "The earlier run was green" | Earlier than your last edit it proves the old code. |

2. **Red flags that mean stop and return to step 1 of the block:**
   - a hedge word in a status sentence (should, probably, seems, I think it works);
   - satisfaction expressed before a command ran ("done", "perfect", "all set");
   - about to commit, push or open a request without having run the proof for what the message claims;
   - forwarding a worker's report instead of checking its diff;
   - relying on a partial check as if it were the full one;
   - a verdict written before the evidence file was opened;
   - a failing check being described as flaky, unrelated or pre-existing without having shown that it also fails
     on the base;
   - the phrase "just this once".
3. **A failure you explain away without evidence is a failure you have accepted.** If a red result is truly
   unrelated, show it: run the same check on the base and report both results. "Pre-existing" with no run behind
   it is the most common way a regression is waved through.
4. **Violating the letter is violating the spirit.** Finding a phrasing the rule does not literally mention is
   still the rule applying. If the sentence implies the work is good, the evidence has to exist.
