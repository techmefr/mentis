# decision-proposal-review-pitfalls: origin and source stamps

> Provenance of `skills/decision-proposal-review-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from three public process documents, read and rewritten, never run:
no proposal was written or reviewed with this block. Nothing in it is verified by use.

## Sources (re-read in this session, 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| rust-lang/rfcs, `README.md` (commit d2705ad) | MIT or Apache-2.0 (LICENSE-MIT and LICENSE-APACHE files; the README says the repository is "in the process of being licensed" under both) | Socialising first, active versus approved, final comment period, no squashing, postponed versus closed, author not obliged to implement |
| kubernetes/enhancements, `keps/NNNN-kep-template/README.md` (commit 6ebe0a9) | Apache-2.0 (LICENSE file) | Merge early and iterate, unresolved marker, one proposal per feature, approvers for the implementable status, section list |
| adr/madr, `template/adr-template.md` (commit ba75bb1) | MIT OR CC0-1.0 (LICENSE file, LICENSE.MIT, LICENSE.CC0-1.0) | Decision drivers, options with pros and cons, confirmation, decision-makers, consulted and informed |

Licences were checked from each repository's LICENSE files in this session. Nothing is copied; the rules are
paraphrased with the source named, as MIT and Apache terms and CC0 allow with credit. Instructions found in
the cloned files (template comments) were treated as description of the process, not followed.

## Rewrite notes
**Examples, not rules.** The ten calendar day period, the five business day minimum, Kubernetes' status
names and both section lists are single-project choices.

**Own guidance, labelled in text**: writing the "substantial" threshold down, stating how a postponed
proposal returns, deleting strawman alternatives, linking an old and a new proposal both ways.

## Removed
1. **Rust's sub-team guidelines, Zulip and forum details, release newsletter advertising** and Kubernetes'
   production readiness questionnaire, release checklist and enhancement-tracker steps: tied to those
   organisations' tooling.
2. **Rust's "too informal" paragraph**: a remark about its own process.

## Not verified
1. **Everything here is unrun.**
2. **The remaining Rust files** (`lang_changes.md`, `libs_changes.md`, `compiler_changes.md`, `text/`) and
   the other MADR templates and docs were not read.
3. **Rust's licensing note** says the move to the dual licence is in progress; "some parts" are already
   licensed that way. Only a rewrite is carried, with credit.

## Related blocks
`documentation-adr`, `internal-comms-async-pitfalls`.
