# prompt-versioning-and-change-gating-pitfalls §2 — Change gating

## 2.1 Things that must change together
1. **Prompt and output schema.** Symptom: parse errors begin the day a field is renamed in the instruction but not
   in the parser, or the reverse. Fix: one change, one review, one gate run, covering text, schema and parser.
2. **Prompt and few-shot examples.** Examples teach format and tone more strongly than the sentences around them.
   Symptom: output copies an example's length, order or wording. Check: remove or reorder an example and see
   whether the output follows. Fix: vary the examples, and review them as part of the prompt (own guidance).
3. **Prompt and model.** A prompt tuned for one model is not neutral on another; changing the model is a prompt
   change for gating purposes (`model-migration-pitfalls`).
4. **Prompt and tools.** Adding or renaming a tool changes what the model decides to call. Rerun the cases that
   exercise tool choice.

## 2.2 Placement
1. **Standing rules go in the system part, per-request data in the user part** (own guidance), and the two are
   not mixed. Symptom of mixing: an instruction that a pasted document seems to override.
2. **Wrap untrusted text in a clearly delimited region and say what it is,** but do not count the delimiter as a
   security control; see `llm-app-prompt-injection-and-exfiltration-pitfalls` §1 for what delimiters do not stop.
3. **Never assemble the instruction part by concatenating user text.** Fill variables only in the data part; if
   user text must influence the instruction, let it choose from a fixed set of options (own guidance).
4. **Keep long stable text before variable text** where the provider reuses an identical prefix; the reason and
   the rules are in `llm-cost-latency-control-pitfalls` §1.

## 2.3 Few-shot and structured output
1. **Drift in examples is silent.** An example added to fix one case changes the average case. Symptom: the
   fixed case passes, an unrelated one regresses a week later. Fix: the gate of §2.4 includes cases far from the
   motivating one.
2. **Prefer the provider's structured-output or tool-schema mechanism over asking for JSON in prose,** where it
   exists, and still validate the result in code; a schema-conforming answer can be semantically wrong
   (own guidance).
3. **Define what a failed parse does** before it happens: retry once with the error message, then a typed
   failure the caller handles, never a silent default (`failure-classification-before-retry`).

## 2.4 The rerun gate
1. **Run the same cases against the previous and the new bundle,** in clean contexts, as in
   `llm-eval-regression-pitfalls` §1. The promptfoo model is exactly this: prompts and providers on one side, test
   cases with assertions on the other, results side by side.
2. **Include cost and latency as assertions** next to quality. promptfoo has assertion types for both; a prompt
   that wins on quality and doubles the bill is a trade, not a win.
3. **Keep the motivating case.** Each production complaint that causes an edit becomes a permanent case with its
   expected behaviour. Symptom of skipping it: the same complaint returns after the next edit.
4. **Gate on the set, not on the first case.** Passing and failing counts, errors and retries are reported as in
   `llm-eval-regression-pitfalls` §3.
5. **Repeat when the output is sampled.** One run per case hides variance; compare pass counts over several runs
   before calling a small difference real.

## 2.5 Editing by symptom
1. **Stacking "never do X" lines is the usual end state.** Symptom: a prompt that grows with every incident, with
   contradictions between old and new rules. Fix: after each edit, read the whole prompt, remove what the new
   rule makes redundant, and rerun the gate on the shorter version too.
2. **State the reason beside an instruction** instead of capitalising it; a reason generalises, a shout does not
   (own guidance, in line with the Agent Skills guide cited in `llm-eval-regression-pitfalls`).
3. **Delete before adding.** If a rerun shows the shorter prompt holds, ship the shorter one.
