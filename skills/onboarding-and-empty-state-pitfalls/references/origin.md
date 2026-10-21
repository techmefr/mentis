# onboarding-and-empty-state-pitfalls: origin and source stamps

> Provenance of `skills/onboarding-and-empty-state-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No onboarding flow was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: pre-account local flag carve-out in the first-run guardrail, resume check for component-state-only flows, skip versus complete in tour state, loaded-flag and catch checks for empty states, skip-when line.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| W3C ARIA Authoring Practices, modal dialog pattern, read 2026-10-20 | W3C copyright notice with W3C permissive licence (terms not read in full), facts only | focus in, Tab trap, Escape, focus return, safe initial focus (§2.3.5, §2.3.10) |
| W3C WCAG 2.2 Understanding SC 4.1.3 Status Messages, read 2026-10-20 | W3C document licence, facts only | results count as status message (§2.3.2) |
| W3C WCAG 2.2 Understanding SC 1.1.1, 1.4.1, 2.2.1, 2.3.3, 2.5.8, read 2026-10-20 | W3C document licence, facts only | Decorative images, colour not the only means, time-limit options, interaction animation can be disabled, 24 by 24 CSS pixel targets (§2.3.3, §2.3.4, §2.3.6, §2.3.8, §2.3.9) |
| W3C Media Queries Level 5, `prefers-reduced-motion`, read 2026-10-20 | W3C document licence, facts only | `reduce` value (§2.3.8) |

Second pass, read 2026-10-20: WCAG 2.2 full Recommendation (SC 1.3.1, 2.2.1, 2.5.8 text with exceptions re-read), <https://www.w3.org/TR/WCAG22/>, W3C Document License, facts only; HTML Standard single page, <https://html.spec.whatwg.org/> (localStorage getter and SecurityError, alt for decorative images, progress and meter), CC BY 4.0 (WHATWG), facts only.

No permissive source found on onboarding or empty-state design itself, searched: none opened beyond the two W3C pages above; product-design and growth articles were not fetched.

## Own craft, not from a source
First-run routing, checklist model with derived steps, progress persistence, skip and dismiss, tours with versions, sample data flagging and removal, invitations, kinds of empty state, copy, accessibility, performance, measurement, test list and framework pointers.

## Removed
Wizard validation and drafts (`long-and-multistep-form-pitfalls`), vendor onboarding and tour products, growth-marketing sequences.

## Verified on 2026-10-20
Modal tour focus behaviour and the announcement of result messages. One point added (§2.3.10).

## Verified on the second pass, 2026-10-20
6 verified (decorative image rule, colour not sole means, time-limit options, reduced-motion media feature and interaction-animation criterion, minimum target size), 0 corrected, 0 deleted. Flow, persistence, sample-data and copy points are craft, not checkable facts.

## Not verified
1. **Everything outside §1.1.8 (storage failure), §2.3.1 to §2.3.6, §2.3.8, §2.3.9 and §2.3.10 is own knowledge**: section 1 and the rest of section 2 were not checked against any source.
2. **Other accessibility points** (hover and position cues, heading level, focus handling in checklist widgets) are recalled public practice, not re-read; timeouts, status as text, reduced motion and target size were re-read on the second pass.
3. **Framework pointers** name features from memory; no version was checked.
4. **No number** (reminder frequency, checklist length, activation rate) is stated; none was measured.
