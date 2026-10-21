# llm-cost-latency-control-pitfalls §2 — Latency and load

## 2.1 Where the time goes
1. **Split the time into stages:** your own preprocessing and retrieval, the wait for the first token, the
   generation of the rest, and your postprocessing. Symptom of one number only: effort spent shaving the model
   call while retrieval or a downstream step takes longer.
2. **First token and total time are different budgets.** A chat feels fast if text starts quickly; a
   background step cares only about the total. Measure both, per request class, as percentiles, not averages.
3. **Output length drives total time** (OpenAI's latency guide: shorter outputs cut latency roughly in proportion;
   Anthropic's: fewer tokens to generate means a faster response), so a token cap (`llm-cost-latency-control-pitfalls` §1.3) is
   also a latency control.
4. **Put cost and latency in the case set.** promptfoo offers cost and latency assertions beside quality ones;
   use the equivalent so a prompt change that doubles time fails the gate (`prompt-versioning-and-change-gating-pitfalls`
   §2.4).

## 2.2 Streaming
1. **Stream when a person is reading.** The user sees progress sooner even though the total time is unchanged;
   both vendors' latency guides present streaming as a perceived-latency measure.
2. **Streaming moves the failure point.** An error can arrive after text was shown: Anthropic's errors page says
   an error can occur after the API already returned a 200, with its own error event in the stream (an
   overloaded error is the example), outside the usual status-code handling. Define what the interface does
   with a half answer: mark it, offer retry, never present it as complete.
3. **Validate before acting.** A streamed structured answer is not valid until it ends; do not trigger tools or
   writes on a partial parse. Anthropic's streaming page says tool input arrives as partial JSON strings, to be
   accumulated and parsed once the content block stops.
4. **Proxies and platforms may buffer** streamed bodies and defeat the point; test the real path, not only the
   local one.
5. **Output filters need the whole text** or a rolling window; decide which and say so (see
   `llm-app-prompt-injection-and-exfiltration-pitfalls` §3.3 on the latency a scanner adds).

## 2.3 Timeouts, retries, concurrency
1. **Set a deadline per user request** and derive per-call timeouts from it. Symptom of timeouts set one by one:
   a request that waits several times the page's patience because each layer waited its own full time.
2. **Retry only what is retryable and only with a budget** (`failure-classification-before-retry`). A rate-limit
   or overload response is retryable after the delay the provider states; a malformed request is not. A 429 is not
   always a rate limit: one provider answers a reached monthly spend cap with the same status and error type but no
   retry-after header, and retries, including the SDK's automatic ones, fail until access resumes; read the error
   details field to tell the two apart (Anthropic rate-limits page).
3. **Multiply the layers.** Official SDKs retry on their own (Anthropic's twice by default with backoff, honouring
   the retry-after header; OpenAI's for eligible 429 and 503 responses, with version-dependent handling of long
   delays), so your own loop on top multiplies. promptfoo documents two retry layers (a scheduler and an HTTP layer) that share one
   retry setting; stacked clients and gateways in your own stack can do the same. Three layers with three tries
   each is nine calls per failure. Write the product down and keep one layer responsible.
4. **Honour the provider's wait signals.** OpenAI's rate-limit guide treats the retry-after value as a minimum
   wait plus a small random delay, falls back to exponential backoff with jitter when it is absent, and says to
   limit both attempts and total retry time. promptfoo reads the retry-after header and the remaining-quota
   headers of several providers and lowers concurrency when limits bite. Do the same: back off with jitter, not
   in lockstep, and never retry instantly in a loop.
5. **Prefer adaptive concurrency to a fixed guess.** promptfoo's scheduler halves concurrency on a limit hit and
   grows it slowly after sustained success (the idea, not its numbers). Under a provider slowdown a fixed high
   concurrency becomes a queue of timeouts.
6. **Isolate by credential and by class.** A batch job and an interactive endpoint sharing one key and one pool
   let the batch starve the interactive path; separate limits per class (own guidance).
7. **Put a circuit breaker in front of a failing provider** so you fail fast or fall back, instead of piling up
   waiting requests; the fallback has its own cost cap (§1.4.4). The Azure Architecture Center pattern describes
   closed, open and half-open states, notes that retry logic should stop when the breaker says the fault is not
   transient, warns against one breaker over independent upstreams, and says a long timeout can still tie up
   threads before the breaker reacts.
8. **Rate limits are per key and per token or request,** and the two can bind at different times. Track both. The
   Anthropic page measures requests, input tokens and output tokens per minute separately, enforces them as a token
   bucket that refills continuously, can trip on a sharp ramp-up even under the nominal limit (ramp gradually), and
   for most models does not count cached reads toward the input limit, so caching also raises throughput. Output
   limits count tokens actually produced, so a high max-tokens setting does not itself consume them. Rate-limit
   response headers report the remaining quota; read them instead of guessing. OpenAI's guide likewise has a
   429 for a request rate that rose too quickly, with the advice to reduce the rate and raise it gradually.

## 2.4 Checks
1. **Load test the model path with the provider slowed or failing,** not only healthy, and watch queue length,
   retries per request and cost per minute.
2. **Alert on cost per minute and retries per request,** not only on errors; a retry storm shows up there first.
3. **Check the fail mode of every limit:** when the counter is missing, does the request go through or stop
   (`spend-guard-fail-closed`)?
