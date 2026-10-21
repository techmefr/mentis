# settings-and-preferences-page-pitfalls: origin and source stamps

> Provenance of `skills/settings-and-preferences-page-pitfalls`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** No settings page was built, run or tested while writing it. Read date: 2026-10-20.

Dogfood 2026-10-20: one static read on a real project, nothing run; fixes: scale note (one constants module on a small page), single-source default check, mixed save models labelled, loading-default flip, skip-when line.

## Sources (rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| W3C ARIA Authoring Practices, switch pattern (w3.org/WAI/ARIA/apg/patterns/switch/), read 2026-10-20 | W3C copyright notice with W3C permissive licence (page links the W3C Software License and the WAI permission page; terms not read in full), facts only | role, checked state, Space and optional Enter, constant label, fieldset or group (§2.3.2, §2.3.5, §2.3.10) |
| W3C ARIA Authoring Practices, modal dialog pattern, read 2026-10-20 | same W3C notice, facts only | focus in, Tab trap, Escape, focus return, least destructive initial focus (§2.3.6) |
| W3C WCAG 2.2 Understanding SC 4.1.3 Status Messages, read 2026-10-20 | W3C document licence, facts only | status role without focus move, alert misuse as failure (§2.3.3, §2.3.11) |
| W3C ARIA Authoring Practices, search landmark example (w3.org/WAI/ARIA/apg/patterns/landmarks/examples/search.html), read 2026-10-20 | same W3C notice, facts only | search element or search role, unique label only if several (§2.3.7) |
| W3C WCAG 2.2 Understanding SC 3.1.2 Language of Parts and SC 2.3.3 Animation from Interactions, read 2026-10-20 | W3C document licence, facts only | language marking and exceptions (§2.3.8), reduced motion as a technique, level AAA (§2.3.9) |

Third pass, read 2026-10-20: WCAG 2.2 full Recommendation, <https://www.w3.org/TR/WCAG22/> (W3C Document License, facts only): SC 3.2.2 On Input (§1.1.9, added), SC 3.3.4 Error Prevention (§1.6.3), SC 3.3.2 and 2.5.3 (§2.3.1), SC 4.1.3, 3.1.2 and 2.3.3 re-checked. CSS Media Queries Level 5, <https://www.w3.org/TR/mediaqueries-5/> (W3C Document License, facts only): prefers-color-scheme has light and dark only and light covers no preference (§1.2.2). WAI-ARIA 1.2 and the ARIA Authoring Practices pages (switch, modal dialog) re-opened in full. EUR-Lex was tried for the consent text and returned no content, so §2.5.2 stays unsourced.

No permissive source found on settings-page design itself (autosave, scope, defaults, reset), searched: none opened beyond the three W3C pages above; product and design-system documentation was not fetched.

## Own craft, not from a source
Autosave against explicit save, defaults and the unset-against-default distinction, registry, scope and precedence, reset semantics, dangerous settings, structure and search, states, accessibility, performance, privacy handling, test list and framework pointers.

## Removed
Long-form validation and drafts (`long-and-multistep-form-pitfalls`), admin dangerous-action patterns (`admin-back-office-pitfalls`), flag rollout (`feature-flag-lifecycle`), vendor settings products.

## Verified on 2026-10-20
Switch semantics and keys, group markup, modal dialog focus behaviour (one correction: initial focus on the least destructive action, not tab order), status messages. Two points added (§2.3.10, §2.3.11). Second pass 2026-10-20 (all through a summarising fetcher): §2.3.7 corrected (label needed only when several search landmarks), §2.3.8 and §2.3.9 verified against WCAG 3.1.2 and 2.3.3 (the latter is Level AAA).

## Not verified
1. **Everything outside §1.1.9, §1.2.2 (appearance example), §1.6.3, §2.3.1 to §2.3.3, §2.3.5, §2.3.6, §2.3.10 and §2.3.11 is own knowledge**: sections 1.x, 2.1, 2.2, 2.4 to 2.7 were not checked against any source.
2. **Other accessibility points** (labels and descriptions) are recalled public practice, not re-read.
3. **Framework pointers** name features from memory; no version was checked.
4. **Privacy and consent points** are method only, not legal advice; the rule that applies depends on jurisdiction and activity.
5. **No number** (debounce delay, undo window) is stated; none was measured.

Independent verification 2026-10-21: 15 checked, 14 matched, 1 corrected, 0 unverified
