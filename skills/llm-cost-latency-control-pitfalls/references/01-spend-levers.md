# llm-cost-latency-control-pitfalls §1 — Spend levers

## 1.1 Measure before pulling a lever
1. **Attribute every call to a request class:** feature, prompt version (`prompt-versioning-and-change-gating-pitfalls`
   §1), model, and whether it was a retry. Symptom of skipping this: the team argues about "the model" while one
   background job causes most of the tokens.
2. **Record input tokens, output tokens and the cached share separately.** Output tokens are usually priced
   differently from input tokens and are the slower part of a response (own guidance; re-read the provider's
   price page, no price is stated here).
3. **Find the cost per successful outcome,** not per call. A cheap call that fails and is retried or
   escalated can cost more than one good call. Count retries and fallbacks in the numerator.
4. **Look for the loops first:** an agent that rereads its whole history each turn, a retry storm, a scheduled job
   that reprocesses unchanged input. These beat any per-call tuning.

## 1.2 Caching repeated prefixes
1. **Provider-side prompt caching reuses an identical beginning of the prompt** (own guidance; the exact
   minimum size, lifetime, price and opt-in rules are provider-specific, re-read them). The consequence for layout
   holds everywhere: long stable text first (instructions, tool definitions, reference material), variable text
   last.
2. **Symptom: the cache never hits.** Typical causes: a timestamp, request identifier or user name near the top;
   tool definitions listed in a different order each call; a template that renders whitespace differently;
   a prompt edited mid-day. Check: log the cached share per call; a share near zero on a prompt you believe is
   stable is the bug.
3. **A cache hit share is a metric with an alert,** not a one-time check. Prompt edits, a model change or a
   changed tool list silently remove it (`prompt-versioning-and-change-gating-pitfalls` §2).
4. **Application-side response caching is a different thing:** it returns a stored answer for a repeated
   request. promptfoo's evaluation cache keys on the provider, the request content and the configuration, does
   not store errors, and keeps separate entries per repeat index so repeated runs stay distinct. Borrow the
   rules: key on everything that shapes the answer, never cache a failure, expire entries, and give the test
   suite a way to bypass the cache.
5. **Never cache across users when the answer depends on user data** (own guidance). The key must include the
   tenant and the permissions that shaped retrieval, or one user's answer is served to another.
6. **A cached answer is stale on a model or prompt change.** Include the prompt bundle hash in the key.

## 1.3 Token budgets
1. **Cap output explicitly** per request class with the provider's maximum-output setting, and design the
   caller to cope with a cut answer. Symptom of a missing cap: one runaway generation costs more than a day of
   normal traffic.
2. **Budget the input too:** instructions, examples, retrieved passages and history each get a share. A prompt
   that grows by appending is a cost incident on a timer. In retrieval apps, trimming the number of passages is
   a quality decision first (`rag-retrieval-quality-pitfalls` §2).
3. **Summarise or drop history on a rule,** not when the window overflows; see `agent-context-hygiene-pitfalls`.
4. **Ask for the short form when the caller needs it,** and measure that the shorter answers still pass the
   quality cases; length instructions interact with the model's behaviour.
5. **Hard limits are enforced outside the model:** a per-user or per-key cap that refuses by default is
   `spend-guard-fail-closed`, not a prompt line.

## 1.4 Routing work to a cheaper model
1. **Route by task, with the rule written down:** extraction, classification and formatting versus open-ended
   reasoning, as in `choose-model`. A router without a stated rule is a coin flip.
2. **Evaluate the router and the small model together.** Run the case set through the routed path and the
   always-large path, and compare pass counts per class (`llm-eval-regression-pitfalls` §1). Symptom of skipping
   it: costs fall, complaints rise two weeks later.
3. **A model that decides the route is itself a call** with cost, latency and error rate. Count them. A
   rule-based or keyword route is often enough and has no failure mode of its own (own guidance).
4. **Fallback to a pricier model on failure needs a cap,** or an outage doubles the bill; the cap is a gate in
   the sense of `spend-guard-fail-closed`.
5. **Log the routed share and the escalation share.** A drift in either is a signal that traffic or the small
   model changed.
6. **Do not assume a routing gateway's savings.** Any claim of percentage saved comes from measured traffic of
   your own, not from a product page.

## 1.5 Batching and offline work
1. **Work nobody waits for can use a batch interface** where the provider offers one, usually at lower cost and
   longer, looser delivery times (own guidance; re-read the terms). Evaluation runs, backfills and nightly
   enrichment are the typical candidates.
2. **Design the job to be resumable and idempotent:** a batch can partly fail, expire or return out of order.
   Match results to requests by an identifier, never by position.
3. **Dedupe before sending:** identical inputs in one batch should be one call.
4. **Use the cache for evaluation reruns:** rerunning an unchanged case set against an unchanged bundle should
   cost nothing (§1.2.4), and a rerun after a change should cost exactly the cases that changed.
