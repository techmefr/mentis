# agent-context-hygiene-pitfalls §1 — Patterns and diagnosis

Everything here is the context-degradation skill's own account. Its supporting research was not read, and its
figures are not carried over.

## 1.1 The five patterns
1. **Degradation is a continuum with five named patterns:** important text lost in the middle, poisoning,
   distraction, confusion and clash. Each has its own signal and its own remedy, so name the pattern before
   choosing one.
2. **Lost in the middle.** The skill says attention is reliable at the start and end of a long context and weaker
   in the middle, and attributes this to attention mechanics. Symptoms: the right information is in the
   context and the model ignores it, answers contradict the provided data, or it forgets an instruction
   given early in a long prompt.
3. **Placement is the remedy.** Put what matters at the beginning and the end, add section headers and
   structural markers as anchors, and when a document must be included whole, put a summary of its key points
   before it and the critical conclusions after it.
4. **Poisoning.** A wrong claim, a tool error or an incorrect retrieved fact enters the context and is then
   treated as ground truth and repeated. The skill names three entry points: tool outputs, retrieved documents
   and model-generated summaries.
5. **Signals of poisoning:** quality drops on tasks that used to work, tools are called with the wrong
   parameters or the wrong tool, and a hallucination persists after it has been corrected. When these appear
   together, suspect poisoning before suspecting the model.
6. **Recover by removing, not by correcting on top.** Truncate to before the point where the bad content entered,
   restart with only verified material, or mark the poisoned section and ask for a fresh evaluation. The skill
   says layered corrections rarely work because the original error keeps its weight in attention.
7. **The skill's circuit-breaker sequence:** find the first turn where the bad claim entered; truncate or restart
   from before it; reload only verified sources; record the rejected claim and where it came from.
8. **Distraction.** Irrelevant material in the context degrades results even when it is only a little, and the
   model cannot skip it. Filter before loading and prefer access through a retrieval step to pre-loading
   reference material.
9. **Confusion.** The model applies the constraints or tools of another task to the current one, answers a different
   aspect of the question or blends requirements from several sources. Segment tasks into separate contexts;
   when one session must switch tasks, use explicit reset markers that say which constraints now apply, and keep
   objectives, constraints and tool definitions per task.
10. **Clash.** Sources that are each correct contradict each other, such as two versions of the same
    documentation. Settle the precedence before the conflict arises, filter out outdated versions before they
    enter, and when a contradiction must stay, annotate it: what conflicts, which source says what, which wins and
    why. Without a rule the model resolves it unpredictably.
11. **A conflict annotation can be as plain as this:**

    ```yaml
    conflict:
      topic: export endpoint name
      source_a: reference for the previous release names it as /exports
      source_b: reference for the current release names it as /downloads
      precedence: source_b
      reason: the current release is what is deployed
    ```

## 1.2 Rule out the cheap explanations first
1. **Ordinary variance looks like degradation.** Output quality fluctuates between runs. Establish a baseline over
   several runs and look for a sustained decline that follows context growth; a single bad run is not evidence.
   Measuring across runs is in `llm-eval-regression-pitfalls` §1.
2. **A poor prompt produces the same symptoms.** Ambiguous instructions, missing constraints or an unclear task give
   inconsistent output and wrong tool use. Run the same prompt at a small context first; if it fails there, the
   prompt is the problem and not the context.
3. **Contradicting retrieved documents poison silently.** When retrieval returns two sources that disagree, the
   model may pick one without saying so, and the answer looks right. Detect contradictions in the retrieval layer,
   before the documents enter the context.
4. **A needle-in-a-haystack score says little about a real workload.** The skill warns that a high score on
   that single-fact retrieval test does not predict multi-fact reasoning, instruction following and synthesis
   across the whole window. Test with tasks shaped like the real ones.
5. **A large window delays degradation; it does not remove it.** A model's advertised context length is not a
   promise that tasks perform well at that length.

## 1.3 Why a published threshold does not transfer
1. **Onset varies by model, by task and by version.** The skill's tables are for specific model versions and the
   skill says they go stale after updates. Re-measure after a model change.
2. **Degradation tends to hold steady and then drop,** the skill says, so monitoring that expects a gentle slope
   misses it. Set the compaction trigger well before the onset you measured, not at it.
3. **Over-organising can backfire.** The skill reports studies in which a shuffled context sometimes beat a
   coherent one for retrieval, because coherence can create false associations. Test whether heavy structure
   helps for your task instead of assuming it does.
4. **Dissimilar content degrades faster.** Tasks that need inference across material unlike the question
   degrade sooner than tasks with high surface similarity, per the skill; design retrieval for overlap between
   the question and what is retrieved.
5. **The skill's own figures are left out here on purpose,** because a number from another model's study is the
   least portable part of it. Measure the onset on your workload (see §2 here).
