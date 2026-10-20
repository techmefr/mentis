# llm-pii-and-data-handling-pitfalls §3 — Isolation and proof

Source: documentation of the sensitive-data output scanner of llm-guard (MIT), read 2026-10-20. Points marked "own guidance" are not from a source. Not legal advice.

## 3.1 Who can be in the context
1. **Authorise before retrieval, not after generation** (own guidance). Symptom: an answer quotes a document the
   asker may not open. A model told "do not reveal other users' data" is not an access control. Fix: filter
   the candidate documents by the caller's rights, then rank; see `rag-retrieval-quality-pitfalls` §1.2.
2. **One tenant per context** (own guidance). Mixing two customers in one prompt for efficiency lets output,
   or an injection, cross the boundary. Fix: batch only within a tenant.
3. **Service accounts widen rights silently** (own guidance). An assistant that queries with its own broad
   account answers with its rights, not the user's. Fix: pass the user's identity through to the data layer.

## 3.2 Output side
1. **A sensitive-data output scanner exists** in the source: it reuses the detection of the input anonymiser,
   takes a list of entity types, and can replace what it finds. Use it as a second layer for what the model could
   emit from its context, with the same limits as §1.3.
2. **Output can still carry identifiers the detector does not know** (own guidance), and rendering paths that
   send data out are in `llm-app-prompt-injection-and-exfiltration-pitfalls` §2.

## 3.3 Proof
1. **Seed and trace.** Create test records with unique, recognisable identifiers (own guidance), run the real
   feature, then search for the identifiers in: the provider request body capture of a test environment, logs,
   caches, vector store, evaluation fixtures, exports. The table in the checkpoint is filled from this result,
   not from the design.
2. **Cross-tenant probe.** As tenant 2, ask for tenant 1's seeded identifier by name and by description.
   Success: absent from the answer and from the retrieved set.
3. **Deletion probe.** Delete the seeded subject and repeat the search; any hit is a missed copy.
4. **Redaction regression.** Keep the labelled sample from §1.3 as a repeatable case; a detector or model change
   re-runs it (`llm-eval-regression-pitfalls`).

## 3.4 Checks
1. Seeded identifiers are searched in every store of the table, before and after deletion.
2. The cross-tenant probe passes by retrieved set, not only by answer text.
3. Authorisation is applied in the retrieval query, in code.
