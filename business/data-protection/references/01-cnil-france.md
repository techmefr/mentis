# § 1 — CNIL: what French regulatory guidance adds on top of bare GDPR

> Section 1 of `business/data-protection`. Read it when the project or its users are French, or a
> French DPO/legal team is the one who will eventually be asked. Not legal advice — a structured
> pointer to CNIL's own published guidance, and the engineering consequence of each point.

GDPR states the law; CNIL (Commission Nationale de l'Informatique et des Libertés), France's
regulator, publishes concrete guidance, recommended figures and enforcement practice on top of it.
Where GDPR says "an appropriate retention period" or "a high-risk processing", CNIL is the body that
has actually published a list, a grid, or a number — and that specificity is exactly what lets an
engineer check a decision instead of guessing at what "appropriate" means. Every figure below is
**CNIL's published recommendation**, not a hard legal ceiling: CNIL itself states that following its
recommended durations creates a presumption of compliance, and departing from them is allowed if the
departure is documented — which is a DPO/legal decision, not one this checklist makes for you.

## 1.1 When a PIA/AIPD is required

CNIL requires a Privacy Impact Assessment (Analyse d'Impact relative à la Protection des Données,
AIPD) whenever a processing operation is "likely to result in a high risk to the rights and freedoms
of individuals." To make that operational, CNIL and the EU G29/EDPB working party published a grid
of **9 criteria** (large-scale processing, systematic monitoring, sensitive data, vulnerable
subjects, innovative use of technology, data matching/combination, and others) — meeting **2 or more
of the 9** is CNIL's own trigger for treating an AIPD as mandatory
([CNIL — Ce qu'il faut savoir sur l'AIPD](https://www.cnil.fr/fr/ce-quil-faut-savoir-sur-lanalyse-dimpact-relative-la-protection-des-donnees-aipd)).
CNIL also separately publishes an explicit **list of processing types that require an AIPD, and a
list that don't**
([CNIL — listes des traitements](https://www.cnil.fr/fr/listes-des-traitements-pour-lesquels-une-aipd-est-requise-ou-non)) —
check a new feature against both lists before reasoning from the 9-criteria grid alone, since a
listed case settles the question directly.

**Engineering consequence:** a feature that combines two previously separate datasets to profile
users, or that adds systematic behavioural monitoring (session replay, granular analytics, biometric
matching), can flip a processing operation past the 2-criteria line without anyone deciding "we're
now doing high-risk processing" — the AIPD trigger is a property of what the feature *does*, not of
whether anyone flagged it as sensitive. Read the 9-criteria grid, and the two published lists,
**before** shipping a feature that combines or monitors, not after.

## 1.2 Retention periods CNIL has actually published

CNIL's practical guide on retention periods
([CNIL — guide durées de conservation](https://www.cnil.fr/sites/cnil/files/atoms/files/guide_durees_de_conservation.pdf),
[CNIL — les durées de conservation des données](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees))
gives concrete figures for common categories, reported consistently across CNIL's own guidance and
secondary trackers:

- **Prospect data** (someone who has not become a client): active-base retention until consent
  withdrawal, or **3 years from the last contact initiated by the prospect** — each new contact from
  the prospect resets the clock.
- **Client data**: for the duration of the commercial relationship, then **up to 3 years from its
  end** (e.g. from the last order), before archiving or deletion.
- **Cookies and trackers**: lifetime capped at **13 months**, with data collected through them kept
  no more than **25 months** (CNIL's cookies recommendation, §1.3).
- **Connection/access logs**: sources diverge between roughly **6 months and 1 year** depending on
  the specific guidance cited (CNIL's own journalisation recommendation vs. commonly cited
  code-de-la-sécurité-intérieure practice) — **this is the one figure in this section not
  independently resolved; confirm the current applicable duration for logs specifically with the
  DPO/legal before hard-coding a retention job around it**, rather than picking whichever number
  looks more convenient.
- **CCTV / employee monitoring / other categories**: CNIL's guide above covers more categories than
  listed here (HR files, video surveillance, etc.) — read it directly for anything not named above
  rather than assuming a category not listed here has no published figure.

**Engineering consequence:** each of these is a job someone has to write, not a comment in a
retention policy document. See `references/02-code-patterns.md` §2.3 for a scheduled-purge pattern —
the point of naming the CNIL figure here is so the job's threshold is traceable to a source instead
of a number someone remembers from a meeting.

## 1.3 Cookie/tracker consent: CNIL's recommandation cookies

CNIL's cookies recommendation and its published FAQ
([CNIL — FAQ cookies](https://www.cnil.fr/fr/cookies-et-autres-traceurs/regles/cookies/FAQ))
establish, among other things:

- **"Refuser aussi facilement qu'accepter"** — refusing has to take the same number of actions as
  accepting. A banner with an "Accept all" button front and center and "refuse" buried two clicks
  deep in a settings panel is exactly the pattern CNIL enforcement has targeted; the practical bar
  reported is a **symmetrical one-click accept / one-click refuse**, not a click-through menu on one
  side only.
- **No pre-ticked consent, no soft opt-out** ("continuing to browse implies consent" is not valid
  consent under the current recommendation) — consent has to be a genuine, informed, specific,
  freely-given action.
- **Non-essential trackers wait for consent.** Strictly necessary cookies (session, load balancing,
  a shopping cart) are exempt from consent but not from information; everything else — analytics,
  ads, most "audience measurement" tools unless configured to CNIL's exemption criteria — is
  non-essential and must not fire before consent.
- **Revocation has to be as easy as granting**, reachable at any time, not only at first visit.

**Engineering consequence:** see `references/02-code-patterns.md` §2.2 for what this means
concretely in a Nuxt app — categorising scripts, blocking non-essential ones until consent, and
giving revocation a real, reachable path rather than only a first-load banner.

## 1.4 Registre des traitements (Article 30)

Article 30 GDPR requires a **registre des activités de traitement** (record of processing
activities) for most organisations (the small-organisation exemption is narrow and doesn't apply to
regular/non-occasional processing, which covers nearly all software products). CNIL's own guidance
on the register
([CNIL — le registre des activités de traitement](https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement))
states it must contain, per processing activity: the purpose, the categories of data and data
subjects, the recipients (including any outside the EU), the retention period, and a description of
the security measures in place; the controller's and DPO's identity and contact details are recorded
once at the register level.

**Engineering consequence:** the register is documentation, not code, but every field in it is a
question this checklist's step 1–4 already asks (what data, why, how long, who receives it). A
feature reviewed against §1–4 of the router `SKILL.md` produces the register's inputs as a
byproduct; a feature shipped without going through that review is a register entry someone has to
reconstruct from the code later, which is markedly harder.

## 1.5 DPO designation: mandatory vs recommended

Under GDPR Article 37 (as CNIL and legal commentary summarise it), designating a DPO is **mandatory**
for: public authorities/bodies (with narrow exceptions); organisations whose core activity requires
**large-scale, regular and systematic monitoring** of individuals; and organisations whose core
activity is **large-scale processing of special-category data** (health, biometrics, etc.) or
criminal-conviction data. Outside those cases, CNIL still **recommends** designating one as good
practice, and many organisations do voluntarily.

**Engineering consequence:** "large-scale" and "core activity" are judged on what the *product*
actually does, not on company size — a small team building a health-tracking app or a
behavioural-analytics platform can cross the mandatory threshold well before it has the headcount
to intuitively expect it. Whether a given product crosses that line is a DPO/legal call (§2 of the
router `SKILL.md`), not one to self-certify from this paragraph.

## Guardrails specific to this section
- **Never treat a CNIL-recommended figure as a hard legal ceiling** — it's a documented default that
  creates a presumption of compliance; a different figure is allowed if the DPO/legal team documents
  why.
- **Never resolve the connection-logs retention conflict (§1.2) by picking a number** — surface it
  to the DPO/legal team as an open question with a stated range, not as a decided figure.
- **Never assume "we're too small for an AIPD/DPO"** — both thresholds are about what the processing
  does, not about company size (§1.1, §1.5).
