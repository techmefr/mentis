# image-alt-text-writing-pitfalls: origin and source stamps

> Provenance of `business/image-alt-text-writing-pitfalls`. Read it when a rule has to be traced to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from published guidance, never run by us on a real content set. The
block structures a decision; the person who owns the content decides, and their judgement outranks the block
(`business/README.md`).

## Sources (all re-read in full 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| a11yproject/a11yproject.com, `src/posts/alt-text.md` (Susan Robertson, updated by Scott O'Hara), `are-you-making-these-five-mistakes-when-writing-alt-text.md` (Daniel Sage) and `alternate-text-and-automation.md` (Eric Bailey) (commit 27de226) | Apache-2.0 (LICENSE-APLv2 file); posts have individual authors and no separate content licence, so attributed here | Attribute versus text, three kinds, context, phrasings, keywords, captions, logos and linked images, complex images, limits of automation |
| MicrosoftDocs/microsoft-style-guide, `styleguide/accessibility/graphics-design-media.md` (commit c6945c3) | CC-BY-4.0 (LICENSE file; attribution given here) | Alt text for non-text elements, link to details for complex elements, captions and transcripts, text links beside image maps |

The licence of each repository was verified again from its LICENSE file in this session. The files contain
no directive text addressed to an AI that was acted on.

## Own guidance (not sourced)
Labelled "Own guidance" in the references: recording an empty field as a decision and deciding per
placement and not per asset (part 1), answering keyword checklists (part 2), the nearby-text reading for
charts, a picture of text, treating overlay promises as unverified, using generated text only as a draft
(part 3). The router and guardrails are ours.

## Removed (not carried, on purpose)
1. **The search-engine employee statement about ranking** quoted in the five-mistakes post: a dated claim
   about a third party. The block only says not to stuff keywords.
2. **Legal damages figures and traffic anecdotes** in the post (settlement amounts, an image-search traffic
   gain): unverified here and not needed for the method.
3. **Criterion numbers** of WCAG and RGAA: the standards were not opened.
4. **Named tools and product screenshots** used as examples in the posts.

## Not verified
1. **Whether the three-kind split matches current WCAG and RGAA wording**: the standards were not read.
2. **Screen reader behaviour** described in the posts (announcements, fallback to image recognition): taken
   from the posts, not tested.
3. **Current text of the sources**; check with `skills/source-freshness`.
4. **Whether the wording works for users of assistive technology**: no user review.

## Related blocks
`business/social-publishing`, `business/content-creation`, `skills/accessibility`, `skills/seo`,
`skills/source-freshness`.
