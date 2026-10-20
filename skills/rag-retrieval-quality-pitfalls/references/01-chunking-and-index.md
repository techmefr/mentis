# rag-retrieval-quality-pitfalls §1 — Chunking and index

## 1.1 Boundaries
1. **A chunk has to answer something on its own.** Symptom: the retrieved passage says "it" or "the above
   table" and the model guesses the referent. Check: read ten random chunks without their neighbours. Fix:
   split on the document's own structure (sections, clauses, rows) rather than a fixed length, and keep the
   heading path with the chunk. The Ragas testset guide makes the same point for its own pipeline: splitting
   follows the document type, for instance statement sections for financial reports, and a custom splitter is
   expected.
2. **Fixed-size splitting cuts through facts** (own guidance). Symptom: the question and its answer sit on either
   side of a boundary and neither chunk ranks. Check: take failing questions, find the answer span in the source,
   see whether a boundary falls inside it. Fix: split on structure first, overlap only as a fallback.
3. **Tables, code and lists need their header with every piece** (own guidance). Symptom: a row retrieved
   without its column names, so a number has no meaning. Fix: repeat the header, or index the table as
   one unit with a description.
4. **Small to retrieve, larger to read** (own guidance): matching on a small unit and handing the model its
   parent section trades precision of matching against context for the answer. Test it on the failing set
   before adopting.

## 1.2 What gets stored with a chunk
1. **A stable identifier, the source document and its version** (own guidance). Without them neither citation
   nor an identifier-based recall check (§2.2) is possible.
2. **Metadata used to filter:** tenant, language, product, date of validity (own guidance). A filter applied
   after the nearest-neighbour search can leave fewer results than requested; check how your store applies
   it (re-read the store's documentation before relying on this).
3. **Permissions travel with the chunk** (own guidance). Symptom: an assistant quotes a document the asker
   may not open. Check: ask a question as a user without access to a known restricted document. Fix: filter by
   the asker's rights inside the retrieval query, not on the answer; never rely on the prompt to hide text
   that was already retrieved.
4. **Dates and supersession.** Symptom: an answer quotes a policy replaced last quarter. Fix: store the
   valid-from and valid-to dates or a "superseded by" link, filter or down-rank on them, and re-index when a
   source changes (`search-index-sync-pitfalls` for the sync side).

## 1.3 Search method
1. **Meaning-based search misses exact strings** (own guidance): product codes, error numbers, names, article
   numbers. Symptom: a question quoting an identifier returns thematically similar but wrong chunks. Fix:
   add keyword search and merge the two lists, then check on identifier questions specifically.
2. **A keyword-only retriever misses paraphrases.** The Ragas improvement guide shows a keyword retriever failing
   to return documents that held the answer for several questions, and the model correctly saying "not in the
   documents". The pipeline was behaving; retrieval was the bottleneck. A retrieval complaint can look like a
   model refusal.
3. **One query is one chance.** The same guide tries an agent that rewrites and repeats its search and decides
   when it has enough, as an alternative to better chunking or vector search. Treat it as an option to test
   after §3.3 puts the failures in retrieval, not as the default; it costs more calls and more places to
   fail (`agent-run-limits-and-guardrail-pitfalls`).
4. **Changing the embedding model invalidates every stored vector** (own guidance). Symptom: after an
   upgrade, new documents retrieve and old ones do not. Fix: re-embed the whole corpus under a new index
   name, compare on the reference set (§2), then switch.
5. **Re-ranking and result count are tunable, not free** (own guidance): more results raise the chance the
   answer is present and the amount of noise the model reads (§2.2). Pick the number by measuring recall and
   noise on the reference set.
