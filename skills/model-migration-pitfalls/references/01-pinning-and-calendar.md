# model-migration-pitfalls §1 — Pinning and calendar

## 1.1 Know what you call
1. **Inventory every call site:** feature, model identifier string, where the string lives (code, config, a
   prompt store, an environment variable, a third-party tool), pinned or alias, and owner. Symptom of skipping it:
   a retirement notice arrives and nobody can say which services it touches.
2. **Search for the identifier in every repository and every deployed configuration,** including scripts, notebooks,
   evaluation configs and the agent or coding tools your team uses. Forgotten call sites are the usual casualty.
3. **Put the model identifier in one place per service** and log it with each call
   (`prompt-versioning-and-change-gating-pitfalls` §1.3), so a behaviour change can be matched to a model change.

## 1.2 Pins and aliases
1. **A floating alias is a silent version change** whenever the provider moves it. Symptom: quality or format
   shifts on a date with no deploy. Where a dated or numbered identifier exists, pin it (own guidance; what
   identifiers exist and how long they live is provider-specific, re-read).
2. **Pinning buys time, not safety:** a pinned version is retired on the provider's schedule. The pin is only
   useful if the calendar of §1.3 exists.
3. **Pin in tests as well.** A test or evaluation run on an alias is not reproducible later; record the resolved
   identifier in the result.
4. **Self-hosted models need the same discipline:** weights hash or tag, quantisation, serving software version
   and the sampling defaults of the server, since any of them changes output (own guidance).

## 1.3 The deprecation calendar
1. **Keep a dated list of announced retirements per model in use,** each with its source and the date you read it
   (`source-freshness`). Dates change; an undated line is a rumour.
2. **Set the migration start well before the date,** because the work is a run, a review, a staged cutover and
   an observation window, in that order. Decide the lead time from your own last migration, not from a
   default (own guidance; no figure is suggested here).
3. **Subscribe to the provider's notices** with a named owner and a shared mailbox, not a single person's inbox.
4. **Treat the retirement date as a hard deadline for requests, not for planning:** after it, calls may fail or be
   redirected; know which, and what your caller does with either (`failure-classification-before-retry`).
5. **Check what the replacement implies** beyond quality: different limits, price, context size, supported
   features, refusal behaviour. Read the vendor's current migration notes before the run (idea only, not copied
   into your docs).
