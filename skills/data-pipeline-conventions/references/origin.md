# data-pipeline-conventions — origin and source stamps

> Provenance of `skills/data-pipeline-conventions`. Read it when a rule has to be traced back to its
> source or checked for freshness (`skills/source-freshness`), never to apply a rule.

Sourced from established dbt conventions (staging/intermediate/marts layers, schema tests), the DAMA-
DMBOK data quality dimensions (completeness/accuracy/consistency/timeliness), and the classic SCD
patterns in dimensional modelling (Kimball). Mechanisms rewritten, no copied text. Market research, no
internal production feedback at this stage.

**§1.4–§1.5 added 2026-09-07** from an org BI skill for handling supplied accounting files, read for its
handling discipline rather than its format knowledge: never write back over the file someone handed you, and
confirm a destructive transformation before applying it rather than reporting it afterwards. §3.1 already
held the raw-layer version of the first at pipeline scale; what was missing was the ad-hoc case — one file,
one request, no scheduled run — which is where an agent actually meets it. The regulatory file format itself,
the ERP export specifics and the internal instance names stay out (rule C).

**Sectioned and deepened 2026-09-08.** The four inline sections moved to one file each under
`references/` and the router became a table of triggers. No section was added. Every section and point
number was preserved: §1.4 and §1.5 are the two points the 2026-09-07 addition above cites by number,
and §3.1 is the raw-layer rule §1.4 refers to at file scale. The guardrails, which had drifted into a
mixed bulleted-and-unbulleted list, were straightened into one list citing the points they enforce.

**This was the last single-file block counted in `CATALOG.md`'s depth table.**

**What the depth adds.** The original stated the right rules for a subject where none of the failures
announce itself: a non-idempotent pipeline produces a plausible total, a skipped validation produces
figures somebody acts on, a missing grain produces a sum that double-counts, and a full reload works
right up to the volume where it does not. The additions that were real absences rather than
elaborations:

- **§1**: that idempotence covers the *whole run* — an upsert followed by a log append, a counter or a
  notification is not idempotent, and it is the side effect rather than the data that duplicates; that
  a partial run has to leave a state you can resume from or discard, since failing halfway is the normal
  case and the usual response is a re-run; that a run keyed on the wall clock cannot be backfilled,
  which turns a one-line fix into a manual reconstruction; that late-arriving and corrected records are
  expected, so a forward-only window silently stops matching the source; that the reproducible unit is
  the code *plus* its inputs and configuration, which is what makes the traceability in point 2 real
  rather than nominal; that a schema change in the destination is a migration whose breakage lands on
  the consumer's next run; and that a green sample says nothing about cost, timeout, memory or locks,
  which is the specific mistake worth stating twice.
- **§2**: that failing loudly is a choice with a cost, and where blocking is unacceptable the shape is
  a quarantine with a published count rather than a silent skip; that the *number* of failing rows is
  what makes an alert actionable, since one rejected row and a third of the file are different
  incidents; that a validation with no owner gets loosened at the first inconvenient hour and stays
  loosened; row counts in, out, rejected and deduplicated as the cheapest check and the one catching
  the largest class of silent failures; that reconciling against the source needs a second connection
  and different credentials, which is why it gets skipped; that duplicates are defined by a business
  key somebody has to choose, and deduplicating on the wrong one deletes real data irrecoverably; that
  a check reading the pipeline's own output passes on any consistent error; and that a quality check is
  code which needs to be forced to fail once, or it reports green forever.
- **§3**: that the raw layer is what makes every later mistake a re-run rather than a request to a
  source that may no longer hold the data; that the missing grain surfaces as a plausible, stable,
  wrong number after a join fanned out; the test for historisation being whether any question is asked
  about the past, since an in-place `UPDATE` makes last year's revenue change every time a price does;
  that a rule duplicated across two models diverges at the first change and surfaces as two defensible
  dashboards; that a model's name is read by people holding a business question, whose fallback is
  whichever table looked closest; that reusing the source's key lets a renumbering upstream silently
  rewrite your history; that a deletion upstream is an event and not an absence, or a historical count
  changes retroactively with the evidence gone; and that a model has to be *readable* under pressure,
  which makes the tiering a legibility rule as much as a maintenance one.
- **§4**: what the "unless" in point 1 is actually doing — a full reload is simpler and idempotent for
  free, which makes it right for a small table and wrong at the volume that arrives without anyone
  changing the code; that incremental is only correct if you can say what "new" means, and the usual
  failure is a pipeline that runs cheaply and quietly stops picking things up; that cost is a number to
  measure and record rather than a feeling, and the expensive step is usually not the one anybody would
  guess; that a full reprocessing has a blast radius beyond its cost, since it rewrites what other jobs
  are reading; that the expensive part is usually the *shape* of the query and each such shape defeats
  the chosen layout invisibly; that row-by-row work fails at volume with an out-of-memory kill halfway,
  which is exactly the partial run §1.7 has to classify; that a pipeline growing with its data becomes
  an incident on a schedule unless the duration is alerted on; and that optimising before the output is
  verified means debugging two things at once.

Router plus sections: 749 → 3,212.

**Status.** Unchanged: 🟡, market research with no internal production feedback, and the depth does not
change that. What it changes is that a reviewer can now say what each rule costs when it is skipped,
which is what the rules need in order to survive a schedule. `business/data-analytics` continues to own
the landscape the pipeline runs against.
