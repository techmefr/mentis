# skill-trigger-eval-pitfalls §2 — Description optimisation

## 2.1 Writing principles
1. **Frame it as an instruction to the agent.** The guide prefers "use this skill when" to "this skill does",
   because the agent is deciding whether to act.
2. **Describe the user's intent, not the skill's mechanics.** The agent matches against what the user asked for.
3. **Err on the side of listing contexts,** including those where the user does not name the domain, for
   example a request for a chart from a data file that never says "CSV".
4. **Keep it to a few sentences or a short paragraph.** It has to cover the scope and not bloat the context of
   an agent that carries many skills.
5. **Say both what the skill does and when to use it.** The specification asks for both and for specific
   keywords that help an agent identify relevant tasks; its poor example is a three-word statement that only
   names a file type.

## 2.2 The character limit and keyword stuffing
1. **The portable specification limits `description` to 1 to 1024 characters** and the field must not be empty.
   The independent validator enforces the same limit and counts Unicode code points, not bytes, so a
   description in a multi-byte script is not rejected well below the limit.
2. **Re-check the limit after every iteration.** The guide warns that descriptions tend to grow during
   optimisation.
3. **A client may apply a different limit** (own guidance). A figure for a specific client's listing was not
   found in any file read for this block and is not stated. Staying under the portable limit keeps the
   description valid everywhere; check the client's own documentation before relying on anything longer.
4. **The validator warns about keyword stuffing in two shapes:** many quoted phrases with little prose around
   them, and a single sentence that is a long run of very short comma-separated segments. A prose sentence
   followed by a short list of trigger phrases is accepted. The counts that trigger the warning are heuristics
   in its code and are not carried over here.
5. **Keywords are not the defect; a list that does not say what the skill does or when to use it is.** The
   specification itself asks for specific keywords.
6. **Stuffing buys train-set hits at the price of near-miss false triggers** (own guidance). A list of phrases
   that matches every query that mentions the vocabulary is the description's equivalent of an assertion that
   passes in every arm.
7. **A validator checks the shape, not the behaviour.** Passing its checks says nothing about whether an agent
   loads the skill; only the runs in §1 here do.

## 2.3 Train and validation split
1. **Optimising against all queries overfits.** The description comes to work for those phrasings and fails on
   new ones.
2. **Split the set, roughly 60 percent train and 40 percent validation.** Train queries identify failures and
   guide changes; validation queries are set aside and only check whether the changes generalise.
3. **Keep a proportional mix in both sets.** Shuffle randomly and do not put all the positives in one set.
4. **Keep the split fixed across iterations** so the iterations are comparable.
5. **Run the script on each set separately,** for example from two query files.

## 2.4 The loop
1. **Evaluate the current description on both sets.** Train results guide the change; validation results say
   whether it generalises.
2. **Identify failures in the train set only:** positives that did not trigger and negatives that did. The guide
   says this holds whether you revise by hand or prompt a model: keep validation results out of the process.
3. **Revise toward the general case.** Failing positives suggest the scope is too narrow (broaden it or add
   context about when the skill helps). False-triggering negatives suggest it is too broad (say what the skill
   does not do and where the boundary with adjacent capabilities lies).
4. **Do not add keywords taken from failed queries.** That is overfitting. Find the category the failures
   represent and address that.
5. **If several iterations stall, change the structure,** a different framing or sentence shape, rather than
   adding another increment.
6. **Repeat until the train set passes or the improvement stops,** which the guide says is usually within about
   five iterations. If nothing improves, suspect the queries (too easy, too hard or mislabelled) before the
   description.
7. **Select the iteration by its validation pass rate,** the fraction of validation queries that passed. The
   best description may be an earlier one, because later ones can overfit the train set.
8. **The guide mentions an automated version of this loop** in Anthropic's skill-creator skill: it splits the set,
   measures trigger rates in parallel, proposes revisions with a model and writes a live report. It was not
   read here.

## 2.5 Applying the result
1. **Update the `description` field** and confirm it is under the limit in §2.2 here.
2. **Try a few prompts by hand** as a quick sanity check.
3. **For a rigorous check, write 5 to 10 fresh queries** with both kinds, never used in the optimisation, and
   run them through the same eval. They are the only honest test of generalisation.
4. **Re-run the set when the surroundings change** (own guidance): a new neighbour skill with overlapping
   vocabulary, or a different model or client version, can change the rates without any edit to the description.
5. **Output quality is checked separately.** A description that triggers reliably still has to be measured
   against a baseline; see `llm-eval-regression-pitfalls` §1.
