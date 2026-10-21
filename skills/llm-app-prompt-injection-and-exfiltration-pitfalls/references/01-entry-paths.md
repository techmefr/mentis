# llm-app-prompt-injection-and-exfiltration-pitfalls §1 — Entry paths

## 1.1 Direct and indirect
1. **Direct injection comes from the user of your app;** indirect comes from content the app fetches for them.
   The llm-guard documentation draws the same line: direct overwrites the system instructions, indirect alters
   input from an external source. Symptom of forgetting the second: the app is hardened against its own users
   and obeys a web page.
2. **Anything an outsider can write to is an input:** a retrieval corpus fed by shared drives or tickets, a
   web page the assistant browses, an inbox it summarises, an uploaded file, a product review, a calendar
   invite. llm-guard names three exposed shapes: retrieval over a document store, a browsing chatbot, and an
   automated mailbox assistant. The browsing case is worst because the page can change after review.
3. **A poisoned document works later.** For retrieval, the attack lies dormant in the index and fires when a
   question retrieves it. Review who can add to the corpus the way you review who can deploy
   (`rag-retrieval-quality-pitfalls` §1.2).

## 1.2 Latent injection
1. **The instruction is hidden inside an ordinary task document.** The garak probe set for this buries
   instructions in a résumé, a report, a translation task, a whois record and a factual snippet, with the
   injected text placed as a normal-looking part of the document. Symptom: the app is asked to translate or
   summarise, and does something else.
2. **The unit under test is the task, not the model.** Test every product task that takes outside text
   (summarise, translate, extract, classify, reply) with a document that carries planted instructions; each
   is its own path.
3. **Delimiters and "ignore the above" are the common shapes** (the garak probes use end-of-input markers and
   override phrasing); do not match on those phrases to defend (§3.4), use them to build test cases.

## 1.3 Hidden characters
1. **Text a human cannot see can still reach the model.** The garak documentation describes encoding text as
   invisible Unicode tag characters appended to an emoji, and as variation selectors that need no emoji, which
   many tokenisers pass on and a reviewer's screen does not show. The llm-guard scanner for invisible text
   targets private-use, format, control and unassigned characters.
2. **A human-in-the-loop check fails if the human sees something else than the model.** Symptom: a reviewer
   approves a prompt or document that looks harmless. Fix: normalise or strip these categories before the
   text is shown to anyone and before it is sent to the model, and log that it happened.
3. **Stripping has a cost** (own guidance): legitimate scripts use some format characters. Strip with a rule
   for the scripts your users write, and test on real samples.
4. **Check whether the code does it at all** (own guidance). Grep the path from the input to the prompt for any
   removal of tag characters, variation selectors, zero-width and other format characters. A Unicode
   normalisation form (used for comparing strings) is not that removal. Report "no stripping before the prompt" as
   a finding with its impact (section 2.0), not a silent pass.

## 1.4 Tool results are inputs
1. **Whatever a tool returns is outside text,** whether it came from a search, a database field a customer
   typed, a file read or an API of a third party. Treat the result as data in the prompt, and keep the
   authority to act with the application, not with the text.
2. **The same rule holds model-to-model.** A summary written by a model that read untrusted text carries the
   taint onward (own guidance); do not let a second model treat it as trusted instruction.
3. **Server and tool descriptions are the MCP side of the same problem** and are covered in
   `agent-mcp-trust-pitfalls` §1 and §3.

## 1.5 The planted-content test
1. **Plant, then watch the outbound path.** The PyRIT cross-domain workflow models this: the attacker never
   talks to the application; they put instructions in a page, file or message, and a normal user action
   (asking the app to read it) triggers the model. Its worked example uploads a page to storage, has a
   summariser fetch it, and scores the answer.
2. **Run the test on a copy of the pipeline with a harmless marker action,** and stage the data (own guidance).
   Never plant instructions that act on production data or reach real third parties.
3. **Score the effect, not the wording** (§3.2): did a request go to the marker host, did a tool run, did a
   record change.
4. **Repeat each case several times;** outputs vary and one clean run proves little (own guidance).
5. **If the repository has only a fake, canned or stub provider, the behavioural test cannot run there.** Such a provider returns fixed output and shows nothing about what a model does with planted text. Say "not run: no real provider in this environment" and test the code paths that do not depend on the model (escaping, stripping, schema checks, the render policy) instead.

## 1.6 Delimiters around outside text (points 1 to 5 own guidance, points 6 and 7 sourced)
1. **A prompt that says "everything inside these tags is untrusted data" is only as strong as the tag.** Symptom: outside text placed inside the tags contains the closing tag, the wrapper ends early and what follows is read as the application's own instruction. The same holds for fences, quotes and "end of input" markers.
2. **Check every place outside text is interpolated into a prompt.** List each template that builds a prompt, and for each find whether the text is inserted raw, or only partly cleaned (for example only line breaks replaced). Each raw insertion inside a wrapper is a finding.
3. **Fix in layers.** Remove or escape the closing delimiter (and the opening one) inside the text before insertion; prefer a delimiter the text cannot contain, such as one random per request; keep the instruction about untrusted text outside the wrapper, once, before it.
4. **State the impact, not only the shape.** With no tools, a schema-checked output and nothing rendered, a breakout changes what the model says and is low impact; with tools or rendering it opens §2. Say which.
5. **Treat the wrapper as lowering the odds.** The control remains what the output can reach (§2).
6. **The conversation format has its own delimiters, and outside text can carry them.** A red-team plugin documentation lists tokens that close a user turn and open a fake system or assistant turn (the chat-markup tags of several model families, instruction brackets, and plain role labels) and tests them by asking for a harmless marker string in the answer. Symptom: text that contains such tokens changes the role the model believes it is hearing. Check: put each family's tokens into every outside-text field, with a marker request, and see whether the marker appears. Fix: strip or neutralise those tokens in outside text before assembly, and let the provider's message roles, not text, carry the structure. Source: the promptfoo red-team special-token-injection page (MIT, commit 5f1904c), read 2026-10-20.
7. **Official-looking markup raises compliance.** The same project documents a strategy that wraps a request in structured, authoritative-looking formatting because models tend to trust such content more. Consequence: outside text formatted like the application's own instructions (headers, tags, "policy" blocks) is a stronger attack than plain prose, so test with formatted payloads and do not rely on the model telling them apart. Source: the authoritative markup injection page, same commit, read 2026-10-20.
