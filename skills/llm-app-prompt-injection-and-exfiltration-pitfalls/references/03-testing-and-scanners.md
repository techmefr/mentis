# llm-app-prompt-injection-and-exfiltration-pitfalls §3 — Testing and scanners

## 3.1 Attack sets as regression cases
1. **A probe set is a list of cases you can rerun.** garak groups probes by family: latent injection in
   documents, markdown and script exfiltration, system prompt extraction, encoding tricks, and a multi-turn
   probe that studies the tools of an agent and tries to misuse them. Pick the families that match your
   paths from §1 and §2, not all of them.
2. **Keep the set versioned next to the app,** run on every change to prompts, model, retrieval or tools, and
   compare with the last run as in `llm-eval-regression-pitfalls`. Attack payloads are data; do not copy
   them into docs or tickets.
3. **Test the application, not the bare model.** The exposure is in your rendering, retrieval and tools; a
   probe pointed at the model API alone misses all of it. Where the tool allows, point it at the app's own
   endpoint (re-read the tool's documentation for target options before relying on this).
4. **Run against staging with fake data** and a marker host you control, never against production or real
   customers' data.

## 3.2 Success criteria
1. **Define success as an observed effect at the outbound path:** a request to the marker host, a tool
   invocation, a record changed, a rendered image with a foreign host. The PyRIT scoring pages describe
   true/false scorers for exactly this kind of success question, next to graded scorers for severity.
2. **A model refusal is not a pass** (own guidance). A refusal in the text with the tool call still issued is
   a failure; a long compliant-looking answer with no outbound effect is a pass for exfiltration though it
   may fail another test.
3. **Detector coverage is part of the result.** The garak markdown detectors are pattern checks on the output;
   an exfiltration shape they do not list scores clean. Read what the detector looks for before trusting a
   zero.
4. **Scorers are measured too.** PyRIT has a page on measuring the performance of scorer configurations (details not read); do the equivalent
   for any model-based scorer you use as the pass criterion (`llm-eval-regression-pitfalls` §2).
5. **Report counts, not only a rate:** attempts, repeats, errors and skipped cases (`llm-eval-regression-pitfalls`
   §3).

## 3.3 Scanners in the request path
1. **Input scanners** in llm-guard include a classifier for injection, a check for invisible characters, a
   secrets check and an anonymiser, among others; output scanners include sensitive-data detection, URL checks,
   refusal detection, relevance and factual-consistency checks.
2. **Use each for what its page says.** The injection classifier page says it is meant for user input and is
   not recommended for system prompts, and that its match mode can change accuracy on long inputs. The
   relevance scanner compares embeddings of prompt and answer, which catches an off-topic answer and not
   an on-topic one with a hidden link.
3. **URL checks do two different things:** one scores whether a link looks malicious, the other only checks that
   it answers. Neither tells you whether the host is yours; the allowlist of §2.1 does.
4. **Each scanner adds latency and a false-positive rate.** Measure both on your own traffic before putting
   it on the path (re-measure; the documentation's own benchmark figures are for its test machine and
   are not reproduced here).

## 3.4 What a filter does not do
1. **A classifier answers "does this look like an attack I have seen",** not "is this input safe". Rephrasing,
   another language, splitting across turns or documents, and encodings can pass it.
2. **Matching phrases is a test generator, not a defence** (§1.2.3).
3. **A scanner that fails open hides outages.** If the scanner times out, decide in writing whether the request
   is refused or allowed, and alert on it (own guidance).
4. **A clean scan does not license a risky capability.** The capability decisions of §2.4 stand regardless.
5. **List, per scanner, what it does not catch,** next to the control that does (the checkpoint of this block).
