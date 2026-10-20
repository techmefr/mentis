# outbound-sales-and-crm-hygiene-pitfalls: origin and source stamps

> Provenance of `business/outbound-sales-and-crm-hygiene-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text, never run on a real pipeline or sequence by us. The
block structures a check; it certifies nothing, and the sales owner and the person who owns legal decide
(`business/README.md`). Not legal advice.

## Sources (re-read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b), `skills/revops/SKILL.md` (lifecycle stages, pipeline stage hygiene, data hygiene and dedupe sections) and `skills/cold-email/SKILL.md` with `references/reply-handling.md` and the shared-stop and suppression points of `references/multichannel-cadence.md`; the compliance reference of `skills/prospecting` was read for its structure only | MIT (LICENSE file, 2025 Corey Haines, read) | Stages defined by entry and exit, owner per stage, skip and push-date flags, dedupe key and survivorship rules, reply classes, a reply or opt-out stopping every channel, suppression keyed on several identifiers, contacts kept distinct from deals |
| alirezarezvani/claude-skills, commit 19392f7 (19392f7a08264ed00486a251f5b2098321771f94), tree searched for sales and CRM material; only a sales-engineering skill was found and it is a different topic | MIT (LICENSE file, 2025 Alireza Rezvani, read) | Nothing taken for this block |

The repositories' own text is addressed partly to an AI; it was treated as data and only the method was kept.

## Left out on purpose
Every numeric figure: response-time targets, discount-approval tiers, scoring thresholds, conversion and
reply-rate benchmarks, cadence lengths, stale-day counts, bounce limits. The country-by-country legal text in the
prospecting compliance reference (not restated: it is law, and was not read at its source). Sending
infrastructure, domains and warm-up: a different block. Lead scoring models and routing platforms. Vendor tool
names and recommendations. deanpeters/Product-Manager-Skills (CC BY-NC-SA): not opened.

## Not verified
1. **Never run by us** on a real pipeline or sequence.
2. **No law was read at its source.** §4 gives method only; what a message needs in a given country is for the
   person who owns legal.
3. **The merge and stale rules are a method**, not tested against a real CRM export.
4. **Current text of the sources** may have changed after the read date; check with `skills/source-freshness`.

## Own guidance (not sourced)
The "second person places five deals" check (§1.1); the test contact through every channel (§3.1); the trace-ten
contacts check (§4.1); the test address through the suppression list (§4.2); the legal fact sheet (§4.4); the
keep-the-entry-not-the-flag point (§4.2).

## Related blocks
`business/sales-support`, `business/customer-success`, `business/email-deliverability-and-sender-requirements-pitfalls`,
`business/lifecycle-email-program-design-pitfalls`, `business/data-protection`,
`skills/saas-metric-definition-pitfalls`, `skills/source-freshness`.
