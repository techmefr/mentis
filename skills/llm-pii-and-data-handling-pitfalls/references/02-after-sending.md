# llm-pii-and-data-handling-pitfalls §2 — After sending

Source: the attack-scenario text of the sensitive-data output scanner of llm-guard (MIT), read 2026-10-20. Points marked "own guidance" are not from a source. Not legal advice.

## 2.1 The vendor
1. **Provider terms differ by tier and endpoint** (own guidance): retention period, whether inputs are used to
   improve models, abuse-monitoring storage, regional processing. Symptom: a free or consumer tier used for
   customer data. Check: read the terms and data-processing agreement for the exact endpoint and plan in use,
   and write down the date read. Fix: choose the endpoint whose terms match the data class; zero-retention
   options exist at some vendors and must be requested and verified, not assumed.
2. **The source names the concern directly:** some providers may train on requests, and personal data sent
   upstream spreads across their storage. Treat "might be trained on" as the default until the terms say otherwise.
3. **Sub-processors and region** (own guidance): who else touches the data, and where. Transfers are in
   `gdpr-international-transfers-pitfalls`.

## 2.2 Our own copies
1. **Prompt and completion logs are a second database of personal data** (own guidance). Symptom: a debug
   flag left on, full conversations in a log service with broad access. Fix: default to ids, token counts and
   outcome; gate full capture by a short-lived switch with an owner; apply `telemetry-sensitive-data-pitfalls`.
2. **Caches repeat data across users** (own guidance). A response or prompt cache keyed without the tenant serves
   one customer's answer to another. Fix: include the scope in the key, or do not cache prompts that carry personal data.
3. **Embeddings are personal data too** (own guidance). A vector derived from a person's text can be inverted
   in part and is linked to the record by id. Fix: store the source reference and the scope with each vector; they
   fall under the same retention and deletion as the text.
4. **Evaluation sets and replays copy production** (own guidance). Symptom: real tickets pasted into a test
   suite in the repository. Fix: use synthetic or redacted cases (§1), and keep real samples in a restricted store
   with an expiry.
5. **Training and tuning sets** inherit all of the above and add memorisation risk: see
   `ml-training-and-evaluation-pitfalls` §3.
6. **The source's leakage framing:** leakage is not only a database breach; a model that overfits its training data
   can reveal information about it. For a hosted model you do not control, the control is what you send.

## 2.3 Deletion and retention
1. **Build the data-flow table before the first deletion request** (own guidance): each place that holds a
   prompt, completion or derivative, its retention, its reader and how to delete one person's data from it.
2. **A deletion must reach logs, caches, vector stores, summaries, evaluation sets and backups' restore
   procedure.** Symptom: erased from the app, still returned by a similarity search. Check: after deletion, search
   every store for a seeded identifier (§3.3). Fix: derivation links at write time (`agent-memory-and-state-pitfalls`
   §2.3).
3. **Backups cannot be edited**; record how long they live and that restored data is re-deleted from the request
   list. The restore side is in `backup-restore-drill-pitfalls`.
4. **Retention is a number with an owner.** "Keep logs for debugging" is not a retention rule.

## 2.4 Checks
1. The data-flow table exists and has no empty cell.
2. The provider terms were read for the endpoint in use, with a date.
3. A seeded identifier test finds no copy after a deletion.
