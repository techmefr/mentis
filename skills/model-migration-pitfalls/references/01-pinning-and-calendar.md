# model-migration-pitfalls §1 — Pinning and calendar

## 1.1 Know what you call
1. **Inventory every call site:** feature, model identifier string, where the string lives (code, config, a
   prompt store, an environment variable, a third-party tool), pinned or alias, and owner. Symptom of skipping it:
   a retirement notice arrives and nobody can say which services it touches.
2. **Search for the identifier in every repository and every deployed configuration,** including scripts, notebooks,
   evaluation configs and the agent or coding tools your team uses. Forgotten call sites are the usual casualty.
3. **Use the provider's own usage export to find stragglers.** Anthropic documents a console export of usage by API
   key and model, meant for finding use of deprecated models; use the equivalent where it exists, since keys held by
   scripts nobody remembers show up there (Anthropic deprecations page).
4. **Put the model identifier in one place per service** and log it with each call
   (`prompt-versioning-and-change-gating-pitfalls` §1.3), so a behaviour change can be matched to a model change.

## 1.2 Pins and aliases
1. **A floating alias is a silent version change** whenever the provider moves it. Symptom: quality or format
   shifts on a date with no deploy. Where a dated or numbered identifier exists, pin it. What identifiers exist is provider-specific: Anthropic states
   its current identifiers are pinned snapshots and only older aliases resolve to a dated one; OpenAI lists
   deprecations by dated snapshot and maps aliases separately (Anthropic models overview, OpenAI deprecations page).
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
   Both providers read say customers with active use are told by email, so the address on the account matters, and
   a key with no recent use may be missed.
4. **Treat the retirement date as a hard deadline for requests, not for planning:** Anthropic says requests to a retired
   model fail; OpenAI says the model is no longer accessible and its page does not name the error. Know what your
   caller does with either (`failure-classification-before-retry`; Anthropic and OpenAI deprecations pages).
5. **Check what the replacement implies** beyond quality: different limits, price, context size, supported
   features, refusal behaviour. Read the vendor's current migration notes before the run (idea only, not copied
   into your docs).
6. **Dates differ by platform.** Anthropic says its page dates apply to the platforms it operates, while cloud
   resellers set their own retirement schedules. A model reached through a reseller needs that reseller's calendar.
7. **Fine-tuned models follow their base model's schedule** on the OpenAI page; list them in the inventory with the
   base. OpenAI also exposes a shutdown date through its models endpoints, which a script can poll (OpenAI
   deprecations page).
