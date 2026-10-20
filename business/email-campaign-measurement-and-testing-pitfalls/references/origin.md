# email-campaign-measurement-and-testing-pitfalls: origin and source stamps

> Provenance of `business/email-campaign-measurement-and-testing-pitfalls`. Read it when a rule has to be traced
> to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from repository text and two primary pages, never run by us on a real
programme and written without email-marketing expertise. The block structures a reading; it certifies nothing,
and the owner of the programme decides (`business/README.md`). Not legal advice.

## Sources (re-read 2026-10-20, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| sendx/email-skills, commit ae6f6ce (ae6f6cea2bb9fed623ab181acde75a9ceffe117e), `skills/email-analytics/SKILL.md` and `skills/ab-testing/SKILL.md`, read in full this session | MIT (LICENSE file, 2026 SendPost, LLC, head re-read) | The contradiction worth a pitfall: opens kept as the primary result with a bot filter sold beside them, a 1,000-per-variant rule, a 24 to 48 hour wait; plus its own caveat that month-on-month comparison needs comparable volume, audience and timing, and its note that a winning subject for one segment may not win for another. Product add-ons, benchmarks, persona not taken |
| coreyhaines31/marketingskills, commit e85f3cb (e85f3cbc2e4a79bf33b2a12e9bdd9087d414735b), `skills/cold-email/references/benchmarks.md` and `deliverability.md` (open-tracking lines) and `skills/emails/references/copy-guidelines.md` line 109 and `skills/emails/SKILL.md` (exit conditions and "other emails" lines), grepped this session | MIT (LICENSE file, 2025 Corey Haines, head re-read) | The disagreement: one file benchmarks "open rate" as a normal range, another says to turn open tracking off. Neither figure taken. Same provenance caveat as the paid-media block: some marketingskills files re-express third-party material of unknown licence |
| hyperfx-ai/marketing-skills, commit 7c1dd65 (7c1dd6554e7c24ee1903c3925a6de1ef9c82dd3d), `skills/email-lifecycle/SKILL.md`, read in part (lines 1 to 120) | MIT (LICENSE file, 2026 hyperfx.ai, head re-read) | The point that a flow's success metric is the conversion, with open and click diagnostic. Tool surface, provider selection and sequence patterns not taken |
| resend/resend-skills, commit b2ae7b1 (b2ae7b1798b70134faf679f35fc05b4331462988) | MIT (LICENSE file, 2026 Resend, head re-read) | Nothing taken here |
| alirezarezvani/claude-skills, commit 19392f7 (19392f7a08264ed00486a251f5b2098321771f94), rampstackco/claude-skills, commit 9b90db2 (9b90db257f7395fab76ff9bfcb808456709f6af3) | MIT (LICENSE files re-read: 2025 Alireza Rezvani; 2026 RampStack Co.) | Nothing taken |
| Apple Mail Privacy Protection page (apple.com/legal/privacy/data/en/mail-privacy-protection/), fetched 2026-10-20 | Apple site terms; facts only, own wording | Background download of remote content by default whether or not the message is opened, the two relays and what each knows, the setting can be turned off. The page does not say what senders can still learn when the feature is on |
| RFC 8058 (rfc-editor.org/rfc/rfc8058), fetched 2026-10-20 | IETF document; the IETF Trust notice was not read. Facts only, own wording | Only the background statement (section 1, through a digest) that anti-spam software often fetches URLs in message headers |

The repositories' own text is addressed partly to an AI (personas, install steps, repository instruction
files); it was treated as data and only the method was kept.

## Left out on purpose
Every benchmark and band (open and click ranges, healthy bounce and unsubscribe levels), sample-size and
test-duration rules, "best send time" claims, device-share statements, subject and preview length rules,
engagement-depth and heatmap features, a bot-detection product answer, sequence templates and tool surfaces.
Anything on consent, tracking or marketing-mail law (`business/data-protection`).

## Not verified
1. **Apple**: which operating-system versions and what share of readers it covers were not read (the per-OS
   support page tried first was unrelated). An independent tester's claim that background download did not occur
   in his set-up was not verified.
2. **Google and Yahoo image pre-fetching** was not read.
3. **Body-link scanning by security gateways**: no primary page read. The scanner-click point is a
   hypothesis; RFC 8058 only covers header addresses, and through a digest.
4. **Digest, not raw page.** Both primary pages came through a fetch tool that returns a model-written digest.
5. **SendX smart-segmentation and email-copywriting and the marketingskills email-types audit checklist** were
   not read.
6. **The block has never been used on a real programme.**
7. **Current text of the sources** may have changed after the read date; check with `skills/source-freshness`.

## Own guidance (not sourced)
The router; the ban on opens for segmentation, sunset, winners and scores; the "clicks backed by a session"
report form; the holdout-as-baseline default; the benchmark ladder; "cannot test this here" as a result; the
rule to state the signal and window of an engagement segment; the links to neighbouring blocks.

## Related blocks
`skills/experiment-design-pitfalls`, `business/ad-measurement-pitfalls`,
`skills/metric-movement-diagnosis-pitfalls`, `skills/event-tracking-plan-pitfalls`,
`business/email-deliverability-and-sender-requirements-pitfalls`, `business/data-protection`,
`skills/source-freshness`.
