# api-change-classification-pitfalls: origin and source stamps

> Provenance of `skills/api-change-classification-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from two published sets of API guidelines, read and rewritten, never
run: no real change was classified with this block. The two sources are established, but they disagree in
places (part 3) and the stricter reading chosen is ours.

## Sources (re-read 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| aip-dev/google.aip.dev, `aip/general/0180.md` "Backwards compatibility" (commit 615875b) | CC-BY-4.0 for content, Apache-2.0 for code samples (repository LICENSE.md) | Three kinds of compatibility, adding, removing and renaming, moving, types, string length, resource names, semantic changes, defaults, serialising defaults, enums |
| same, `aip/general/0185.md` "API versioning" (read for the versioning and deprecation paragraphs) | CC-BY-4.0 (same repository) | Major version, concurrent versions, deprecation period, stability channels, the 180-day beta recommendation |
| microsoft/api-guidelines, `graph/GuidelinesGraph.md`, section "API contract and nonbackward compatible changes" and "Versioning and deprecation" (commit a7022a2) | CC-BY-4.0 (the repository's `license.txt` and the README badge) | Definition of breaking, lists of breaking and non-breaking changes, versioned elements, the stable-surface support windows |

**Attribution (CC-BY-4.0).** Google API Improvement Proposals, AIP-180 and AIP-185, Google LLC, and the
Microsoft REST API Guidelines for Microsoft Graph, Microsoft, both licensed under Creative Commons Attribution
4.0 International (https://creativecommons.org/licenses/by/4.0/). Rewritten and condensed by us; no endorsement
by either organisation is implied.

The licences were verified again from the repository files in this session. Text found inside the cloned
files was treated as data and not followed.

## Rewrite notes
**The sources disagree** on the length and format of opaque strings (AIP-180: incompatible; Graph:
non-breaking) and list different items (pagination, performance and error codes only in Graph). The block
takes the stricter reading and says why (part 3). That choice, and the condition under which Graph's relaxation
is safe, are ours.

**Overlap with `api-design`.** Optional fields, rename as remove plus add, type widening, meaning changes and
deprecation announcement are already in part 3 of `api-design`; this block repeats the rename point only as
the source states it and adds the classification checklist around it.

## Removed
1. **Protobuf-specific mechanics beyond a mention**: file moves and oneofs are noted in one point; the rest of
   the AIP family (field behaviour, presence, resource types, long-running operations, client-library
   signatures) was not read.
2. **The Graph annotation items** (changing OData annotations, the open-type annotation): schema-language
   specifics.
3. **The AIP interface-based and release-based versioning strategies** and the header names they use: not a
   classification rule.
4. **Microsoft's separate deprecation guideline** (linked by the Graph file): not opened.

## Not verified
1. **Everything here is unrun.** No schema diff or contract was classified with these rules.
2. **The numbers** (36 and 24 months, 180 days) are the sources' own policies for their own platforms and were
   not checked against the originals beyond the files read.
3. **Written by us, not sourced**: the Output / checkpoint paragraph, the premise, the stricter-reading choice
   and the condition for the relaxation, the pre-release labelling advice, the performance-threshold advice,
   and every point marked own guidance in the references.
4. **The OData model-versioning text** that the Graph file names as the minimum bar was not opened.
5. **The pattern pages** of the Graph guidelines (for example the one on extensible enumerations) were not read.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed text, reopened in this session.
- **Corrected:** none needed on re-check beyond wording.
- **Reversed or overstated rules found:** none.
- **Not re-verified:** that other organisations' guidance agrees with either source.

## Related blocks
`api-design`, `deprecation-migration`, `api-contract-and-schema-fuzz-pitfalls`, `business/release-communication`.
