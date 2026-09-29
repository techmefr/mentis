# § 5 — RGAA: the French legal standard

> Section 5 of `skills/accessibility`. Read it when the project is French public-sector, or the
> client is French and above the private-sector threshold, or anyone has asked for an accessibility
> declaration — not as a fifth independent topic on top of §1–4.

## 5.0 What RGAA is, and what it isn't

RGAA (Référentiel Général d'Amélioration de l'Accessibilité) is the French government's
operationalisation of WCAG for French law. RGAA 4.1, the current version, takes over WCAG 2.1 level
AA success criteria and adds a **French test methodology** on top: 106 criteria spread across 13
thématiques, and for each criterion an official **test procedure** — not a different accessibility
bar, the same WCAG 2.1 AA bar with a prescribed way to check it
([accessibilite.numerique.gouv.fr](https://accessibilite.numerique.gouv.fr/), RGAA 4.1 reference
document, [PDF](https://accessibilite.numerique.gouv.fr/doc/RGAA-v4.1.pdf)). Concretely: §1–4 of this
block already tell you what "accessible" requires at the component level; RGAA is what to reach for
when the project additionally has to **prove** it, in the specific procedural form French law
recognises.

**The 13 thématiques**: images, cadres (frames), couleurs, multimédia, tableaux, liens, scripts,
éléments obligatoires, structuration de l'information, présentation de l'information, formulaires,
navigation, consultation. **106 criteria total** — this figure is stated consistently across the
official portal and independent trackers reporting on RGAA 4.1
([Handinova](https://handinova.fr/accessibilite-numerique-les-106-criteres-du-rgaa/),
[Alsacréations](https://www.alsacreations.fr/definition/rgaa/)); confirm against the current
official [critères et tests](https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/)
page before citing it in a contractual or legal document, since a version bump changes the count.

## 5.1 The test methodology is the actual difference from "read WCAG and judge"

WCAG success criteria are worded as testable but open conditions ("text has a contrast ratio of at
least 4.5:1") and leave the auditor to construct a test. RGAA attaches to **each of the 106
criteria** one or more official **tests** — reported as roughly 258 detailed tests across the 106
criteria, several per criterion — each with an explicit pass/fail procedure: which tool or manual
step to run, what result counts as compliant, what counts as non-applicable. This matters for two
concrete reasons:

- **Two auditors reach the same verdict.** A WCAG-only review is a judgment call an auditor can
  defend differently each time; an RGAA test is a script a second auditor re-runs and gets the same
  answer from, which is the property a legal declaration needs.
- **"Non-applicable" is a real, recorded outcome**, not a shrug. A criterion with nothing on the page
  it applies to (no video → the multimédia criteria are N/A) is scored, not skipped, and the
  declaration's compliance rate is computed over applicable criteria — silently treating N/A as
  "pass" or leaving it out inflates the published rate.

Never substitute a WCAG-level judgment call for the RGAA test when a declaration is the deliverable:
read the actual test for that criterion at
[accessibilite.numerique.gouv.fr/methode/criteres-et-tests](https://accessibilite.numerique.gouv.fr/methode/criteres-et-tests/)
before scoring it.

## 5.2 Who this legally binds

- **Public sector**: state, local authorities, and public establishments — always bound, this is the
  standard's original scope (loi n°2005-102, décret n°2019-768).
- **Large private companies, under RGAA/loi 2005-102 itself**: article 47 of loi n°2005-102 binds
  private organisations above **€250M average annual turnover in France over the last three
  accounting years** — this is the historical RGAA private-sector threshold and it did **not**
  change with the 2023 texts; the official portal still states it this way
  ([accessibilite.numerique.gouv.fr/obligations/champ-application](https://accessibilite.numerique.gouv.fr/obligations/champ-application/)).
  Ordonnance n°2023-859 (6 September 2023) changed **enforcement** for this same population — it
  created ARCOM's sanction power (§5.4) — not the threshold itself.
- **Don't confuse that with the EAA's much lower threshold** (below): a company under €250M turnover
  can still be bound, but by the EAA, not by RGAA, and the two obligations differ in scope and
  enforcement body.
- **European Accessibility Act (EAA, directive 2019/882)**: a separate, EU-wide regime, transposed
  into French law by **loi n°2023-171 du 9 mars 2023** and applicable **since 28 June 2025**. It
  binds specific categories of private "services" — e-commerce, banking, transport ticketing,
  telecoms, e-books, and a few others named by the directive — **not every private digital product**.
  Its own **micro-enterprise exemption** is what sits at **fewer than 10 employees AND at most €2M
  annual turnover or balance-sheet total**: an organisation has to clear *both* thresholds to be
  exempt, and clearing either one alone is enough to be in scope if it also offers an EAA-listed
  service. This is the figure earlier drafts of this section had mislabelled as an RGAA threshold —
  it is EAA's, and it only reaches EAA-listed services, not RGAA's general private-sector scope
  ([Sorena — microenterprise exemption](https://www.sorena.io/artifacts/eu/accessibility-act/faq/microenterprise-and-disproportionate-burden-decisions),
  [Quertum — EAA in France](https://quertum.net/accessibility-act-in-france-rgaa/)).
- **RGAA and EAA are not the same obligation and not the same enforcement body** — scoping which one
  (or both) applies to a given client means checking the client's turnover against RGAA's €250M line
  *and* separately checking whether it offers an EAA-listed service, rather than reading one
  threshold as if it settled both questions
  ([rgaa-checker.com](https://rgaa-checker.com/blog/risques-juridiques-accessibilite)).

## 5.3 The déclaration d'accessibilité: what's mandatory and what triggers it

A site/app in scope (§5.2) owes three things, not one:

1. **A schéma pluriannuel** (multi-year plan, typically 3 years) stating the organisation's overall
   accessibility strategy.
2. **A plan d'action annuel** (yearly action plan) derived from it, listing what gets fixed this
   year.
3. **A déclaration d'accessibilité published per site/app**, stating: the compliance status
   (conforme / partiellement conforme / non conforme), the audit results and compliance rate, the
   non-accessible content and why, the date of the audit and the RGAA version used, and a contact
   channel for a user who hits a blocker plus the legal recourse (Défenseur des droits) if that
   contact goes unanswered.
4. **A visible mention on every page** of the site/app, in the footer (in practice), linking to the
   declaration — this is a per-page presence requirement, not a satisfied-once compliance step; a
   frontend that drops the footer on some templates (a landing page, an app shell, an error page)
   creates a per-template compliance gap even if the declaration itself is correct.

What triggers the obligation to publish is simply being in scope under §5.2 — there is no separate
"opt-in" step; a site going live in scope without a declaration is already non-compliant on that
axis alone, independent of its actual accessibility level.

## 5.4 Consequences of non-compliance

Reported sanctions under the 2023 decree's strengthened enforcement (ordonnance 2023-859): **up to
€50,000 for technical non-conformity and up to €25,000 for failing to publish the declaration**,
each renewable roughly every 6 months for continued non-compliance
([sk-web.fr](https://sk-web.fr/article/rgaa-obligations-2026)). **Verify current figures against the
ordonnance/décret text or DINUM guidance before quoting an amount** — this reference states what
secondary sources report, not a certified figure, and sanction regimes are exactly the kind of detail
that changes between government updates.

## 5.5 How this maps onto §1–4

RGAA doesn't introduce a different accessibility concern from what §1–4 already cover — it gives the
same concerns (semantics/keyboard §1, ARIA §2, contrast/perception §3, forms §4) an official French
test procedure and a legal packaging. Concretely:

- Building/reviewing a component → still §1–4, same rules, same guardrails.
- Being asked to **audit against RGAA**, produce a **compliance rate**, or write/update a
  **déclaration d'accessibilité** → this section, and specifically 5.1's point that each criterion
  needs its official test run, not a WCAG-level judgment call.
- A criterion's underlying requirement (e.g. "focus visible") is the same rule as §1.3 — don't
  duplicate the technical content here, apply §1–4 and additionally run the RGAA test procedure for
  that criterion when a declaration is the deliverable.

## Guardrails specific to this section
- **Never invent the criteria count, the threshold figures, or the sanction amounts from memory in a
  later pass** — they're versioned facts the government updates; re-verify at
  `accessibilite.numerique.gouv.fr` before restating them, same discipline as §3's contrast
  thresholds (`skills/source-freshness`).
- **Never treat an N/A criterion as silently passing** when computing or reporting a compliance rate.
- **Never publish a declaration whose audit predates the current page** — a declaration states an
  audit date and RGAA version; code that changed since invalidates it.
- This section states thresholds and figures reported by public secondary sources describing the
  2023 decree; it has not been cross-checked line-by-line against the décret/ordonnance's legal text.
  Treat every number above as "confirm before it lands in a contract or a legal document", not as
  settled.
