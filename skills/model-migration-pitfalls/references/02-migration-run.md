# model-migration-pitfalls §2 — The migration run

## 2.1 Own cases, not public benchmarks
1. **Generic benchmarks are for generic use.** promptfoo's model comparison guides make the same point and
   show the shape of the answer: your prompts, your cases, both models side by side, with quality, cost and
   latency in one table.
2. **Build the set from production traffic classes:** typical requests, the long tail, known failures, attack
   cases and refusal cases. A set of easy cases shows no difference and proves nothing.
3. **Keep the set separate from what the prompt was tuned on,** or the current model wins by familiarity
   (own guidance).

## 2.2 Side-by-side run
1. **Same cases, same prompt bundle, only the model differs,** each in a clean context, with repeats for sampled
   outputs (`llm-eval-regression-pitfalls` §1.2). Changing the prompt in the same run hides the cause.
2. **Read the diff by case.** List cases where the candidate wins, loses and ties; read the losses in full. An
   equal average can hide a new failure class that matters more than the gains.
3. **Include cost and latency per case** (`llm-cost-latency-control-pitfalls`): a better model that is slower on
   the long tail may break a timeout.
4. **Report errors, retries and skipped cases beside the pass counts** (`llm-eval-regression-pitfalls` §3). A new
   model that refuses more or times out more reads as a quality drop in a naive score.
5. **Re-run the attack and safety cases** (`llm-app-prompt-injection-and-exfiltration-pitfalls` §3). Resistance
   is not transferred between models. promptfoo's drift guidance proposes a fixed adversarial set run repeatedly
   and compared over time, with a consistent target label for tracking.
6. **Check any model judge against humans again** if the judge was the old or the new model
   (`llm-eval-regression-pitfalls` §2): a model tends to favour its own style.

## 2.3 What does not transfer
1. **Prompts tuned to a model's quirks:** emphasis, formatting tricks and example styles that the old model
   needed can cause over-literal or verbose output on the new one; Anthropic's prompting guide says that on newer models
   emphatic wording written to prevent under-triggering of tools can now cause over-triggering and should be dialled back. Symptom: output length or tone shifts across
   the board. Fix: retune after the first diff, as a separate gated change
   (`prompt-versioning-and-change-gating-pitfalls` §2).
2. **Sampling and limit parameters:** temperature, maximum output, stop sequences, tool-call options and
   reasoning or effort settings may mean different things or be unsupported. Re-read the new model's
   documentation and test each. Concrete case in one provider's docs: on its newer models a non-default temperature,
   top-p or top-k returns a 400 error, and its deprecation page says most SDKs keep the field so code still
   type-checks, with one language's SDK removing it; the recommendation is to omit them. Some models also reject turning thinking off. The provider's models
   endpoint reports maximum input tokens, maximum output tokens and capabilities per model (including whether thinking
   can be turned off), so read them in code instead of assuming (Anthropic deprecations and
   models overview pages).
3. **Output format and parsing:** whitespace, wrapper text, field order and escape habits shift. Validate with the
   real parser, not by eye.
4. **Tool use:** a new model can call tools more or less eagerly or with different argument shapes; rerun the
   tool-choice cases (`agent-run-limits-and-guardrail-pitfalls` for the caps that must still hold).
5. **Context window and tokenisation:** the same text costs a different number of tokens (the Anthropic overview says the tokenizer introduced with one generation fits fewer words
   into the same token count than the earlier ones); budgets in §1.3 of
   `llm-cost-latency-control-pitfalls` need re-measuring.
6. **Refusals and safety behaviour** differ; the user-visible tone may too. Review a sample of both.

## 2.4 The fallback model
1. **A fallback is a model migration waiting to happen.** Run the same cases on it, record its gap from the
   primary, and decide in writing which features degrade or stop when it takes over.
2. **Cap its spend** (`llm-cost-latency-control-pitfalls` §1.4.4) and alert when it serves traffic.
3. **Exercise it on a schedule** so it does not rot between outages.

## 2.5 Cutover and rollback
1. **Shadow first where traffic and privacy allow:** send a copy of real requests to the candidate, store its
   answers unseen by users, and compare. Mind data handling for the copy (own guidance).
2. **Then a small share of live traffic,** with the same metrics as the case set, and a result stated in advance
   that turns it back (no figure suggested here).
3. **Keep the old path deployable** until the observation window ends, and make the switch a configuration change,
   not a deploy (`prompt-versioning-and-change-gating-pitfalls` §1.3).
4. **Keep the case set and its results** as the baseline for the next migration, and add each production incident
   from the new model to the set.
5. **After the cutover, update the inventory and the calendar** of §1, and remove the old identifier from every
   configuration found in §1.1.
