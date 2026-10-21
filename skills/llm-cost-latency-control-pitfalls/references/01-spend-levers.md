# llm-cost-latency-control-pitfalls §1 — Spend levers

## 1.1 Measure before pulling a lever
1. **Attribute every call to a request class:** feature, prompt version (`prompt-versioning-and-change-gating-pitfalls`
   §1), model, and whether it was a retry. Symptom of skipping this: the team argues about "the model" while one
   background job causes most of the tokens.
2. **Record input tokens, output tokens and the cached share separately.** Providers price output tokens
   separately from input tokens (Anthropic models overview; no price is stated here, re-read the price page) and
   output is the slower part of a response (own guidance). Cached reads and writes show up in their own usage fields
   (Anthropic and OpenAI caching docs), so log them rather than the total only.
3. **Find the cost per successful outcome,** not per call. A cheap call that fails and is retried or
   escalated can cost more than one good call. Count retries and fallbacks in the numerator.
4. **Look for the loops first:** an agent that rereads its whole history each turn, a retry storm, a scheduled job
   that reprocesses unchanged input. These beat any per-call tuning.

## 1.2 Caching repeated prefixes
1. **Provider-side prompt caching reuses an identical beginning of the prompt.** Anthropic documents the order as
   tool definitions, then system, then messages, with a hit requiring an exact match up to the marked block;
   OpenAI documents the same exact-prefix rule. The two differ on opt-in: one provider requires marking, the other
   caches automatically on supported models. Both have a minimum cacheable length, lifetime and price that are
   provider-specific; re-read them (caching docs of both). The consequence for layout
   holds everywhere: long stable text first (instructions, tool definitions, reference material), variable text
   last.
2. **Symptom: the cache never hits.** Typical causes: a timestamp, request identifier or user name near the top;
   tool definitions listed in a different order each call; a template that renders whitespace differently;
   a prompt edited mid-day; a prompt shorter than the model's minimum, which one provider processes uncached with no
   error; a change to tool definitions, which on that provider invalidates everything after it, or to tool choice,
   thinking or effort settings, which invalidate later parts; parallel requests sent before the first response has
   begun, since an entry only becomes available then. Check: log the cached share per call; a share near zero on a prompt you believe is
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
7. **A cache hit is not guaranteed even when the prefix is identical.** One provider says its prefix lifetime is short
   by default, refreshed on each use, and counted from the start of the request that wrote or read it, so a long
   generation eats into it; another says its routing key helps but does not guarantee a hit. Treat hit share as
   measured, never assumed (caching docs of both).

8. **Bulky tool results make the history the cost.** An agent that receives a screenshot or a large document on
   almost every turn re-sends all of them on every call; a long run's history can dwarf the instructions.
   Source, read 2026-10-20: the macOS computer-use reference of anthropics/claude-quickstarts (MIT). Check: log the
   input tokens per turn against the turn number; a line that climbs steadily is this.
9. **"Keep the last N and replace older ones with a placeholder" defeats the cache.** Once there are more than N,
   every new turn changes which old item is replaced, so the start of the request differs on each call and the
   exact-prefix match of point 1 fails every time. Symptom: bounded history, and a cached share near zero.
10. **Make the pruning step, not slide.** Let the number kept grow from a minimum up to a ceiling, then drop back
    to the minimum. Between drops the same old items map to the same placeholders, the prefix is identical and the
    cache keeps hitting; you pay one re-write per cycle instead of one per turn. The minimum has to be high enough
    that the model still has what it needs to see after a drop (own guidance: test the task across a drop).
11. **Do not prune a run that never gets long.** Reading an already-cached item costs little, while dropping it
    forces everything after it to be re-written, so the saving pays back only if the item would have been read
    many more times. The repository's own figure is "about ten" and comes from its README; re-read before relying
    on it. Rule: on short tasks, prune nothing.
12. **Pruning and summarising bound context at different prices.** A summary is an extra model call over the whole
    history and the next turn starts with a cold cache, but it keeps a text account of what happened; pruning
    removes only the bulky items, is cheap and fast, and leaves the text turns to accumulate. Choose pruning for
    long, image-heavy runs that would otherwise hit the summary trigger, summarising as the rare safety net, and
    neither for short runs.
13. **Providers cap the request body.** A hosted platform may reject a request whose serialised size exceeds a
    limit even when the token count is fine. Own guidance: check the serialised size before sending and force a
    prune when it is near the cap, then restart the step cycle of point 10. The limits are the platforms'; re-read.
14. **Show the cached share in the run's own log line,** per turn (point 3 above), so a pruning change that breaks
    the prefix shows up in the next run, not on the invoice.

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
1. **Work nobody waits for can use a batch interface** where the provider offers one, at lower cost and with a
   delivery window instead of an immediate answer: the Anthropic batch page says most batches finish quickly, that a
   batch expires if not finished within its window, and that results stay downloadable only for a limited time
   (re-read the figures, none is stated here). Evaluation runs, backfills and nightly
   enrichment are the typical candidates.
2. **Design the job to be resumable and idempotent:** a batch can partly fail, expire or return out of order.
   Match results to requests by an identifier, never by position (the Anthropic page states results may come back in
   any order and gives each request its own identifier). A result can be succeeded, errored, canceled or expired,
   and the last two are not billed on that provider; collect and resubmit them, and download results before they
   age out. Batches have their own queue and rate limits, and caching inside a batch is best effort.
3. **Dedupe before sending:** identical inputs in one batch should be one call.
4. **Use the cache for evaluation reruns:** rerunning an unchanged case set against an unchanged bundle should
   cost nothing (§1.2.4), and a rerun after a change should cost exactly the cases that changed.
