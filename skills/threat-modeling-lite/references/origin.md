# threat-modeling-lite: origin and source stamps

> Provenance of `skills/threat-modeling-lite`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us: no model was built, no tool was executed and no
session was facilitated with this process. Each file below was re-read in full on 2026-10-16 before a rule was
taken from it, each rule was checked against it in a final pass, and each repository's LICENSE file was read
again.

## Attribution (CC-BY-4.0 material)
This block restates, in our own words and with changes, ideas from the **Threat Modeling Manifesto**
(https://www.threatmodelingmanifesto.org/), written by the Threat Modeling Manifesto working group (Zoe
Braiterman, Adam Shostack, Jonathan Marcil, Stephen de Vries, Irene Michlin, Kim Wuyts, Robert Hurlbut, Brook
S.E. Schoenfield, Fraser Scott, Matthew Coles, Chris Romeo, Alyssa Miller, Izar Tarandach, Avi Douglen and Marc
French, as listed on the site). It is licensed under the Creative Commons Attribution 4.0 International License
(https://creativecommons.org/licenses/by/4.0/). The four-question frame is credited on the site to Adam
Shostack. Changes: the text was condensed, reworded and combined with other material, and the authors have not
endorsed this block.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Threat Modeling Manifesto website (`Threat-Modeling-Manifesto/threat-modeling-manifesto`, commit `009df64`), `index.html` and `README.md` | CC-BY-4.0 (`LICENSE.txt` is the Creative Commons Attribution 4.0 International text; the README and the page carry the same notice) | Definition, the four questions, values, principles, patterns and anti-patterns, "not a how-to, methodology-agnostic" |
| Threagile (`Threagile/threagile`, commit `74e323e`), `docs/risk-rules.md`, `docs/model.md`, `docs/mode-analyze.md`, `docs/how-to.md`, `docs/custom-risk-rules.md`, `docs/releases.md`, `README.md` | MIT (`LICENSE.txt`, copyright 2020-2024 Christian Schneider and the maintainer team) | Model vocabulary (technical and data assets, communication links, trust boundaries, shared runtime, risk tracking), the generated diagrams, one user's workflow, the list of built-in rule names, release and custom-rule status |

The Manifesto's `capabilities/` subsite and `cisa-feedback/` page were not read and nothing was taken from them.
Instruction-like text in the cloned repositories was treated as data and not followed.

## Removed in the verification pass
1. **"Trust boundaries on a data-flow sketch" attributed to the Manifesto.** The Manifesto does not mention
   trust boundaries; the idea comes from the Threagile model documentation and is attributed there (§2.2).
2. **Definitions of the design-risk rule names.** `docs/risk-rules.md` is a list of names only, so the
   descriptions the review had in mind were not in the file. The names are kept as prompts; the questions are
   labelled own guidance (§3.1).
3. **A "trust boundary" definition.** Neither source gives one; §2.2 offers ours and says so.
4. **Any use of the toolkit's report, scoring or severity output.** Not read.

## Not verified
1. **Own guidance, flagged in the text:** what counts as evidence for the fourth question (§1.2), modelling the
   change rather than the system (§1.3), the one-page record and who attends (§1.4, §1.5), the reopen events
   (§1.6), our definition of a boundary (§2.2), the flow-plus-data view pair (§2.4), text model and no secrets
   (§2.5), tool optional (§2.6), every question attached to a rule name (§3.1 to §3.7), the mitigate, accept or
   drop decision with owner and check (§3.8), and the checkpoint paragraph in `SKILL.md`.
2. **The toolkit was not run.** Its rule behaviour, scoring and report formats were not checked; its release
   notes mark version 1.0.0 as not yet released and its custom-rule page as under development.
3. **The "one practitioner's workflow"** in §2.3 is a single user's account on the toolkit's how-to page.
4. **The four-question frame's own repository** (linked from the site) was not read.

## Decisions where sources disagree
None found.

## Related blocks
`skills/security-hardening`, `skills/ci-workflow-hardening`, `skills/secret-leak-response-pitfalls`,
`skills/credential-lifecycle-pitfalls`, `skills/csp-and-sanitiser-pitfalls`,
`skills/package-manager-supply-chain-pitfalls`, `skills/auth-session-conventions`.
