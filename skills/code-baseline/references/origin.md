# code-baseline — origin and source stamps

> Provenance of `skills/code-baseline`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**An org skill catalogue's cross-language rule set (14 skills: no comments, no ticket references, no AI
attribution, file size limit, no god classes, no generic exceptions, external APIs behind an owned client,
parsed files as typed manifests, distinct concepts as distinct types, layered architecture, test new
features, run generated tests, diff coverage, plus one on not exporting the catalogue itself)** — read in
full, then extracted, de-identified and rewritten generically, with everything naming an internal repository,
package or channel deliberately left out (rule C). The catalogue-export rule was **not** carried over: it
governs that catalogue's own distribution, not code.

The layered architecture rule was **not** duplicated here: it already lives in `skills/archi` and
`skills/domain-modeling`, and the per-stack blocks carry the language form of it.

**Deepened 2026-08-06.** A first pass wrote this block from the skills' descriptions alone. Reading the
bodies added what mattered most and what a summary loses: **§0's scope stance** (new code only, legacy
untouched, bundled versus drive-by cleanup, flag-don't-fix, and the user's local override — a coherent
posture that appears in every one of those skills and that the descriptions never state), plus the exclusion
lists, carve-outs and anti-pattern catalogues throughout. Stamped 2026-08-06.

**§7 added 2026-08-11** from the same catalogue's `extend-dont-override`, a 15th skill added there after
this block's original mining pass (confirmed absent from the "14 skills" counted above). Read directly
from the installed plugin rather than from a description alone, since the source itself is short enough
that the body is the whole rule: the preference order (config key → config file → override hook → whole-file
replace → fork) and the "state why no narrower option worked" discipline are taken as-is and rewritten
generically, with the source's Railpack/`php.ini` worked example left out (rule C — a specific vendor tool,
not a mechanism worth naming here).
