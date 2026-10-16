# support-queue-design-pitfalls §3 — Handling and closing

The failure this section prevents is silent closes, stale bots closing confirmed bugs, and a greeting
bot followed by weeks of nothing.

## 3.1 One order for every item
1. **Run the same questions in the same order and stop at the first that resolves the item**: is it a
   duplicate, is it already answered or shipped, is it actionable as written, is it in scope, and only then
   classify and assign.
2. **The order is queue removed per minute**: a duplicate or an already-shipped item closes with a search, the
   scope decision costs the most thought. Re-rank if your queue is mostly one kind.
3. **Actionable as written**: ask for exactly one missing element and set the waiting-on-reporter state.
4. **"Accepted" without an owner is an honest state; "accepted" implying someone is working on it is not.**
   An honest "real, unstaffed, no date" ages better than silence or an optimistic estimate.
5. **Time-box the pass.** Most items resolve fast; batch the rest for a decision.

## 3.2 Closing and staleness
1. **Auto-close only items waiting on a reporter who stopped replying.** Never one waiting on you: a confirmed
   bug closed by a bot tells the reporter their evidence was worthless.
2. **Restrict the sweep to that one state, exempt confirmed, accepted, blocked and security states, warn
   first, and run the first sweep as a dry run** so you know the blast radius before it fires.
3. **Every close carries a reason and how to reopen.** Never close silently.
4. **Anchor each clock to a named waiting party**, not to the item in the abstract.
5. **Mass-closing an old backlog is legitimate once**, as the opening move of a new policy announced the same
   day as the new intake. A maintainer account the source quotes found it works once and the backlog returned.

## 3.3 What to automate
1. **Automate classification and routing, deterministically**: the area from changed paths, the type from the
   form, the owning team as reviewer, the staleness clock.
2. **Keep a human as final decision-maker** on accept, reject or close. Treat any model as a suggestion layer.
3. **Never automate the first human reply.** Reporters discount it, response metrics exclude it by
   definition, and a greeting followed by silence makes the wait feel worse.
4. **Disclose agent-written comments in the comment itself.**
5. **Automate who is on duty, not what to decide**: sync the owner field to whoever is on the rota.

## 3.4 Reply craft
1. **Thank, decide, close, in two sentences.** First-time reporters get the patient version, regulars the
   terse one, deliberately.
2. **A "needs information" reply names the one thing missing and what is already established**, so a resumed
   thread does not re-ask settled questions. "Please provide more information" fails.
3. **An out-of-scope reply cites a recorded decision**, gives one sentence of reasoning and leaves a door open
   for a different framing.
4. **Keep one rejection file per rejected concept, not per ticket**, holding the decision, the reasoning and
   the earlier requests. When the request returns under a new name, link the file. The reasoning then survives
   its author.
5. **Hostile or abusive behaviour is not a triage decision**; hand it to the conduct process.

## 3.5 Metrics
1. **Four monthly numbers**: time to first human response, untriaged share, queue age, created versus closed.
2. **Exclude bots and self-replies from first response**, or the greeting hides the delay you are measuring.
3. **Do not track total open count as health, or closed-per-week as productivity**; the second rewards
   closing hard items without deciding them.
4. **Pair every count with a human-driven signal**, such as how many people could cover triage if one left.
5. **Adjust the target or the intake, never the definition of a response.**
