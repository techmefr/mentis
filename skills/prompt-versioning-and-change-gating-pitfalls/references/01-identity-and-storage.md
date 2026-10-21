# prompt-versioning-and-change-gating-pitfalls §1 — Identity and storage

## 1.1 One source of truth
1. **Symptom: two copies of the same prompt disagree.** A string in the code, an edited copy in a dashboard and a
   test fixture all claim to be "the prompt". Check by searching for a distinctive sentence of it; more than one
   hit outside tests is the bug. Fix: one file or record per prompt, everything else reads it.
2. **Prompts in files are the easiest to review.** promptfoo reads prompts from text, markdown, template files,
   chat-format JSON and functions, and from external prompt-management services. Whatever the store, the same
   questions apply: who may edit it, how is an edit reviewed, how is an old version restored. A vendor says the same
   about its own hosted store: OpenAI's prompt-engineering guide tells you to keep production prompts in
   application code (typed inputs, code review, tests, the normal deployment process) and announces that its saved
   prompt objects are being retired, with a migration guide (OpenAI prompt-engineering guide, section on versioning
   prompts in code; re-read the deprecations page for the timeline). A hosted prompt store is a dependency with its own
   lifecycle.
3. **A prompt store outside the repository still needs the repository's discipline:** a diff view, a named
   author per change, a way to pin a deploy to a version and not to "latest". Symptom of missing pinning: behaviour
   changes the moment someone saves in the editor, with no deploy to blame. Two open-source prompt registries show
   the mechanism: MLflow's versions are immutable, carry a commit message and a diff view, and an alias such as a
   production stage points at a version, so switching the alias is the rollback; its reserved latest alias moves with
   every new version, so an application loading it is the unpinned case. Langfuse assigns each version an identifier
   and lets labels mark environments, tenants or experiments, and its SDKs cache prompts client-side, so an edit
   reaches a running service only after the cache refreshes (MLflow prompt-registry pages, Langfuse prompt-management
   pages).
4. **Separate the instruction from the variables.** Template placeholders are filled at call time; the template
   text is the versioned thing, the filled text is data. Log the identifier of the template, not only the filled
   string, or two different templates that render alike cannot be told apart.

## 1.2 What a version includes
1. **A prompt version is more than its words.** It also includes the model identifier, sampling settings,
   the output schema or tool definitions, the few-shot set, and any retrieval or preprocessing step that shapes
   the input. Changing one of those with the text unchanged is a new version. Two provider caching pages list the
   model, tool definitions, output format and reasoning or effort settings as things that alter the rendered prompt
   (Anthropic, OpenAI prompt-caching docs), which confirms the bundle idea for those items; the few-shot and
   preprocessing items remain own guidance. OpenAI's prompt-engineering guide also says different snapshots of a model
   within a family may need different prompting, and recommends pinning production to a snapshot and keeping evaluation
   suites to monitor behaviour when the model or its version changes.
2. **Hash the whole bundle, not just the text.** Symptom of text-only versioning: "same prompt version, different
   behaviour" after a settings or model change. Fix: a content hash over the bundle, stored with each call.
3. **Treat model aliases as moving.** A floating alias is a version change you did not make; pin a dated or
   numbered identifier where the provider offers one and record which one ran (`model-migration-pitfalls` §1). One provider documents
   that its current model identifiers are pinned snapshots and that only older aliases resolve to a dated one; read
   the page of the provider in use (Anthropic models overview).

## 1.3 Tracing and rollback
1. **Log, per call:** prompt identifier, bundle hash, model identifier, settings, and a request identifier you can
   join to the user's complaint. Langfuse's page on linking prompts to traces gives the reason: with the link,
   metrics and evaluations can be read per prompt version. Mind what else the log would hold: prompts and answers can carry personal
   data (retention belongs to `observability-instrumentation`).
2. **Roll back by promoting the previous bundle,** not by retyping it from memory. Keep the last good version
   until the new one has run through a stated observation window. Immutable versions plus a movable alias make this a
   one-step change in MLflow's registry (see §1.1.3).
3. **Promote in steps when traffic allows:** a small share first, with the same metrics as the gate, then the rest.
   Decide before the rollout which result turns it back (own guidance; no figure is suggested here). OpenAI's guide
   names feature flags and configuration in your deployment system for staged releases of prompt changes, and both
   registries above support labels or aliases for experiments.
4. **A version that was never run on the case set is not a candidate.** Promotion needs the rerun of §2.4.
