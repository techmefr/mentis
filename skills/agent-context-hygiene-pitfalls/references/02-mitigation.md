# agent-context-hygiene-pitfalls §2 — Mitigation

## 2.1 Four moves
1. **Write.** Save material outside the context window in scratch files or external storage and read it back
   through a tool call when needed. The skill points to this when the window is filling up.
2. **Select.** Pull in only what is relevant, by retrieval, filtering and prioritising. The skill points to this
   when distraction or confusion shows up, and says to leave out what scores as irrelevant instead of including
   everything available.
3. **Compress.** Reduce tokens while keeping the information: summarise, abstract repeated patterns into one
   reference, replace verbose tool output with a compact structured summary. The skill points to this when the
   context is growing but all of it is relevant.
4. **Isolate.** Split work across sub-agents or sessions so no single context grows past the point where it
   degrades. The skill points to this for confusion and clash, or when tasks are independent, and calls it the most
   aggressive and often the most effective move. Designing the split is in `multi-agent-design-pitfalls`.
5. **Match the move to the pattern.** Truncation or restart for poisoning, precedence rules for clash, segmentation
   for confusion, curation for distraction, placement for lost in the middle (§1 here).

## 2.2 Habits that keep a context small
1. **Load just in time.** Retrieve information when the current reasoning step needs it, not in advance. Material
   that might be needed behind a tool call costs nothing until it is.
2. **Mask old observations.** After a verbose tool result has been used, replace it with a compact reference to it.
3. **Give each agent only its task's context.** A specialist that holds only what its task needs has less to be
   distracted by.
4. **Put the compaction trigger before the onset,** not after the symptoms. The skill says to compact before the
   context passes the model-specific point where degradation starts, and not to wait for the first bad output.
5. **Keep bulky raw output inspectable without keeping it in the prompt.** The skill relates this to offloading
   logs and outputs to files, so that a poisoned or oversized result can be examined later without staying
   in the context.

## 2.3 Compaction is itself a source of error
1. **A model-written summary is one of the skill's three entry points for poisoning** (§1 here). Whatever the
   summary says becomes input to every later step.
2. **Keep the provenance of a claim through compaction** (own guidance): which source, which turn. The recovery
   sequence in §1 here needs to find the turn where a claim entered, which a summary that merged turns can no
   longer show.
3. **Do not compress a section you already suspect is poisoned** (own guidance). Truncate it or re-derive it from
   verified sources, then compress what remains.
4. **Check a summary against its source before it replaces the source** (own guidance), particularly for names,
   numbers and decisions, since those are what later steps act on.

## 2.4 Finding the onset on your workload
1. **Test the same task at growing context sizes.** The skill's guidelines say to monitor how length and
   performance correlate during development and to test with progressively larger contexts to locate the point
   where results change.
2. **Repeat each size several times,** because a single run cannot separate degradation from ordinary variance
   (§1 here); the baseline and assertion practice is in `llm-eval-regression-pitfalls` §1.
3. **Run the same prompt at a small context as the control.** If the control fails, the problem is not size.
4. **Record the model and version with the result** and re-measure after a model update, since the onset moves
   (§1 here).
5. **Set the trigger well below the measured onset** and record the margin you chose and why (own guidance).
6. **Design for degraded behaviour as well as for the threshold** (the skill's own guideline): decide what the
   agent should do when the context is already past it. Own examples: compaction, a restart from a saved
   file, or a handoff to a fresh session (see `handoff`).
