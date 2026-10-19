# ai-content-disclosure-and-provenance-pitfalls: origin and source stamps

> Provenance of `business/ai-content-disclosure-and-provenance-pitfalls`. Read it when a rule has to be
> traced to its source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from published guidance, never run by us on real content. The block
structures a decision; the person who owns the content decides, with legal and compliance where a law may
apply (`business/README.md`).

## Sources (all re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| c2pa-org/specifications, built pages `2.2/ux/UX_Recommendations.html` (sections 3.2 to 3.8) and `2.4/ai-ml/ai_ml.html` (section 9) (commit ca167c7) | CC-BY-4.0 (repository LICENSE file, titled Attribution 4.0 International; attribution given here) | Source disclosure wording, verifiable context for AI-edited claims, created versus gathered assertions, redaction by update, storage choices, watermark and fingerprint recovery, consent and preview |
| indranilbanerjee/contentforge, `research/2026-08-13-disclosure-provenance-design.md` (commit 8eb6b72) | MIT (LICENSE file) | True and vendor-neutral disclosure wording, disclose when uncertain, advisory review aid, no removal of marks |

The licence of each repository was verified again from its LICENSE file in this session. The pages state the
standard's UX recommendations as recommendations; the block carries them as such. The AI-and-machine-learning
section was read; it describes how tool builders mark model output, so no rule for publishers was taken
from it. The repositories contain no directive text that was acted on.

**Young source, unreviewed.** The contentforge note is from a small plugin and was not reviewed by us beyond
reading it. Only its mechanics are kept (true wording, default to disclose, advisory detectors, no
evasion).

## Own guidance (not sourced)
Labelled "Own guidance" in the references: naming the part the AI touched, keeping a record of who reviewed
what and why a disclosure was left off, testing the upload chain, treating photographer and location data as
personal data, not relying on detector accuracy figures, who decides on a stripping tool, and the label not
replacing the human owner. The router, guardrails and the links to `business/content-creation` and
`business/data-protection` are ours.

## Removed (not carried, on purpose)
1. **Legal articles, applicability and grace dates** for AI disclosure: not opened. The block points to the
   official text and the owner of legal and compliance.
2. **The design note's claim that a named vendor embeds statistical watermarks in its text output from a
   given date**, and the paper figures on detection rates: external claims not verified here.
3. **Any watermark-removal or invisible-character cleaning feature** of other repositories: deliberately not
   carried.
4. **Technical specification detail** of the standard (manifest formats, assertion types, model fine-tuning
   and versioning sections): the block is for publishers, not tool builders.
5. **Brand and trademark guidance** of the standard ("Content Credentials" naming and localisation rules).

## Not verified
1. **Whether the labels work for readers**: no reader testing.
2. **Platform behaviour**: which platforms strip metadata on upload was not checked; the block tells you to
   test.
3. **Current text of the sources**; check with `skills/source-freshness`.
4. **Legal duties** around AI disclosure and provenance: left to a legal-verification pass.

## Related blocks
`business/content-creation`, `business/social-publishing`, `business/data-protection`,
`business/legal-documents`, `business/licence-compliance`, `skills/source-freshness`.
