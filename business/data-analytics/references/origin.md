# data-analytics — origin and source stamps

> Provenance of `business/data-analytics`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

§§1-4 generalised from the org catalogue's two BI landscape skills — a
real BI team's reference material for a landscape of several independent SQL Server instances (a shared
CRM, one database per business entity on an ERP instance, a referential/uniformisation instance, and a
views-only restitution instance), plus a usage guide to its main tables. The real instance names, host
names, entity counts, the ERP's actual French table/column names and the concrete crosswalk table's
real columns are left out per rule C — this block keeps the underlying mechanism: independent
same-schema instances defeat identifier portability, a central crosswalk table is the fix, a usage
guide is a different artefact from a schema dump, `UNION ALL` consolidation across many instances is a
named tradeoff not a free win, and the same read-only/no-assumed-value/traceability invariants the
source stated as absolute.

§3.3 (layered modeling) and §2.4 (data-quality dimension vocabulary) added 2026-08-11 from public
sources, no internal data-engineering expertise behind them: the staging/intermediate/mart layering is
established `dbt`-ecosystem analytics-engineering practice (a source table never queried directly from a
mart, business logic confined to the intermediate tier); the six-dimension vocabulary (accuracy,
completeness, consistency, timeliness, uniqueness, validity) is the commonly-cited core of the
DAMA-DMBOK data-quality framework. §5 (KPI/dashboard discipline) added the same day from published
dashboard-design and KPI-management practice: the decision test against vanity metrics, the
single-source-of-truth rule, and the 5-9-items cognitive-load observation behind "fewer, well-defined
KPIs beats a wall of tiles." Stamped 2026-08-11.

**Sectioned and deepened 2026-09-08.** The five inline sections moved to one file each under
`references/` and the router became a table of triggers. No section was added. Every section number and
every point number was preserved, which matters more here than in most blocks: `agents/oracle` walks
§1 to §5 by number as its report structure, and §2.4, §4.3, §5.2 and §5.3 are cited by point from that
agent, from this block's own guardrails and from three business blocks — `investor-relations`,
`sustainability-esg` and `people-ops`, each citing one of the four points above.

**What the depth adds.** The original was a good set of defaults stated as rules, and it was almost
silent on the part that makes them usable: what a wrong answer looks like. That gap matters more in this
block than in a code block, because none of these failures raise an error — every one of them returns a
plausible number. The additions that were real absences rather than elaborations:

- **§1**: that a name match fails in both directions and only one of them is visible, so a heuristic
  match has to be quantified rather than shipped as a figure; that "which system wins when two
  disagree" is a governance question with an owner, and answering it silently produces a number that
  contradicts somebody's existing report; that two sources hold two different *populations*, so a
  difference in counts reads as data loss and is really two questions; that several refresh cadences
  make "today's figure" a mix of ages; and that a permission-scoped account returns a smaller entirely
  valid-looking answer with nothing in the result set marking it as partial — the one landscape fact
  that cannot be discovered by reading the schema.
- **§2**: that the dimension chooses the check, which is the actual reason the vocabulary in point 4 is
  worth the discipline — uniqueness is found by counting distinct keys, consistency only by querying two
  systems, timeliness by reading a load timestamp and not the data at all, and named vaguely they all
  get the same non-check; that a usage guide records what a table is *not* for, since the trap is the
  table that answers approximately; that the **grain** is the fact that decides whether a join fans out
  and a sum double-counts and is invisible in a column list; that a table with several date columns
  needs the filtering one named; and that a guide inferred from the schema is a hypothesis while a
  guide confirmed by the owning team is a fact, which decides whether a surprising result means the
  query is wrong or the note is.
- **§3**: that a consolidation has to carry the source instance as a real column, since dropping it
  destroys the one fact that makes a wrong figure diagnosable; that identical schemas do not guarantee
  identical conventions, so a status, currency or unit populated differently per instance makes the
  union a sum of different questions; that a consolidated figure needs a completeness statement, because
  an unreachable instance returns successfully with its rows missing and nothing distinguishes that from
  a real drop in the business; that business logic inside the union is applied N times and drifts
  between branches; and that a new consolidated layer beside the old views is two answers to one
  question rather than a migration.
- **§4**: that a number without its filters is not traceable at all, and that unstated filters are the
  most common source of a disagreement that gets mistaken for a data-quality problem; that the query is
  the record, not the number, because re-deriving a figure from memory reliably produces a slightly
  different one; that a rate whose numerator and denominator come from two systems moves for reasons
  neither explains; that an extract is a copy which leaves its source's access controls behind
  (`business/data-protection`); and why substituting zero is the worst default — zero is a legitimate
  value, so the reader cannot distinguish "none" from "not recorded".
- **§5**: that a metric with no target cannot be read, so the dashboard stops being opened; that any
  figure someone is accountable for becomes a target, and the cheapest way to move a proxy is usually
  not the work it stands for, which makes naming that exposure part of defining the metric; that a
  dashboard shows its own freshness or its numbers are assumed live; that changing a KPI's definition is
  an event with two defensible handlings and no silent one; that a drill-down which does not reconcile
  with its tile destroys confidence in the tile that was correct; and that a KPI is a claim someone will
  repeat outside the dashboard, detached from the filters that qualified it.

Router plus sections: 1,804 → 4,520.

**Status.** Unchanged: 🟡, and the reason is unchanged too. There is still no in-house data-engineering
expertise behind this block, so the depth makes the defaults arguable rather than proven — which is
precisely what `agents/oracle` needs in order to report by mechanism instead of by assertion, and is a
different thing from the status, which only a real analytics engagement moves.
