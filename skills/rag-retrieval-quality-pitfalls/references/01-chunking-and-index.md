# rag-retrieval-quality-pitfalls §1 — Chunking and index

## 1.1 Boundaries
1. **A chunk has to answer something on its own.** Symptom: the retrieved passage says "it" or "the above
   table" and the model guesses the referent. Check: read ten random chunks without their neighbours. Fix:
   split on the document's own structure (sections, clauses, rows) rather than a fixed length, and keep the
   heading path with the chunk. The Ragas testset guide makes the same point for its own pipeline: splitting
   follows the document type, for instance statement sections for financial reports, and a custom splitter is
   expected.
2. **Fixed-size splitting cuts through facts.** Product documentation treats overlap between fixed-size chunks
   as the usual way to keep continuity, and offers structure-aware splitting (sentences, sections, headings) as
   the alternative; the Azure AI Search chunking page also notes that a too-large overlap setting can end up
   producing no visible overlap on short pages. Symptom: the question and its answer sit on either
   side of a boundary and neither chunk ranks. Check: take failing questions, find the answer span in the source,
   see whether a boundary falls inside it. Fix: split on structure first, overlap only as a fallback.
3. **Tables, code and lists need their header with every piece.** Symptom: a row retrieved
   without its column names, so a number has no meaning. Fix: repeat the header, or index the table as
   one unit with a description. A managed knowledge-base product does this on its own for parsed tables and
   figures: it attaches the whole table or page to the matching chunk and returns that instead, but only when
   the table or page is 10,000 characters or fewer, so a long table still arrives in pieces (Amazon Bedrock
   knowledge bases, chunking page, section "Tables and figures in parsed content").
4. **Small to retrieve, larger to read:** matching on a small unit and handing the model its
   parent section trades precision of matching against context for the answer. One managed product ships
   this as "hierarchical chunking": it retrieves child chunks and replaces them with their parent chunks, and
   its documentation says the number of results returned can then be lower than requested. Test it on the
   failing set before adopting.

## 1.2 What gets stored with a chunk
1. **A stable identifier, the source document and its version.** Without them neither citation
   nor an identifier-based recall check (§2.2) is possible. The citation features of two vendors confirm the
   first half: a citation carries the source and title you supplied with the content (Anthropic search-results
   page) or the file identifier and file name (OpenAI file-search guide), so a chunk stored without them
   cannot be cited. The version half is own guidance.
2. **Metadata used to filter:** tenant, language, product, date of validity. A filter applied
   after the nearest-neighbour search can leave fewer results than requested: the pgvector README says that
   with approximate indexes the filter is applied after the index scan, which returns a limited candidate list
   (40 by default for its HNSW setting, so a condition matching 10 percent of rows leaves about 4 on average),
   and offers iterative scans, a partial index or partitioning as remedies. Azure AI Search exposes the choice
   as a filter mode: pre-filtering guarantees k results if they exist, post-filtering can return fewer, and
   the default depends on when the index was created. Check which behaviour your store has and test with a
   selective filter (store behaviour differs by product, re-read its documentation).
3. **Permissions travel with the chunk.** Azure AI Search documents the pattern: a field holding the group or
   user identifiers on each document, and a filter on it added to every query; the identifier is only a string
   used in a filter, with no authentication in the index itself, and hiding the field from results is not a
   protection. Symptom: an assistant quotes a document the asker
   may not open. Check: ask a question as a user without access to a known restricted document. Fix: filter by
   the asker's rights inside the retrieval query, not on the answer; never rely on the prompt to hide text
   that was already retrieved.
4. **Dates and supersession.** The Bedrock knowledge-base page shows filtering on a last-modified time to
   keep to recent documents, which only helps if the source system fills that field correctly. Symptom: an answer quotes a policy replaced last quarter. Fix: store the
   valid-from and valid-to dates or a "superseded by" link, filter or down-rank on them, and re-index when a
   source changes (`search-index-sync-pitfalls` for the sync side).

## 1.3 Search method
1. **Meaning-based search misses exact strings:** product codes, error numbers, names, article
   numbers. Anthropic's contextual retrieval article says embeddings can miss exact matches while keyword
   (BM25) search is effective on unique identifiers and technical terms, with an error-code query as its
   example, and reports that combining both beat embeddings alone. The Azure AI Search page on creating a
   vector index likewise says similarity search is not especially helpful for product names, versions or
   addresses, where keyword search or filters fit better. Symptom: a question quoting an identifier returns thematically similar but wrong chunks. Fix:
   add keyword search and merge the two lists, then check on identifier questions specifically.
2. **A keyword-only retriever misses paraphrases.** The Ragas improvement guide shows a keyword retriever failing
   to return documents that held the answer for several questions, and the model correctly saying "not in the
   documents". The pipeline was behaving; retrieval was the bottleneck. A retrieval complaint can look like a
   model refusal.
3. **One query is one chance.** The same guide tries an agent that rewrites and repeats its search and decides
   when it has enough, as an alternative to better chunking or vector search. Treat it as an option to test
   after §3.3 puts the failures in retrieval, not as the default; it costs more calls and more places to
   fail (`agent-run-limits-and-guardrail-pitfalls`).
4. **Changing the embedding model invalidates every stored vector.** Azure AI Search defines the embedding
   space of an index as all its vector fields filled by the same embedding model, and says that changing or
   deleting existing fields often needs a full rebuild. Symptom: after an
   upgrade, new documents retrieve and old ones do not. Fix: re-embed the whole corpus under a new index
   name, compare on the reference set (§2), then switch.
5. **Re-ranking and result count are tunable, not free:** more results raise the chance the
   answer is present and the amount of noise the model reads (§2.2). Anthropic's article reports that passing
   20 chunks beat 10 and 5 in its test, with the caveat that extra text can distract the model and the right
   number depends on the use case; OpenAI's file-search guide says limiting results reduces tokens and
   latency but may lower answer quality. Pick the number by measuring recall and noise on the reference set.
6. **The requested count is a ceiling.** Symptom: fewer chunks come back than asked for, and a test written
   as "exactly N results" fails or a prompt template assumes N. Cause: post-filtering (§1.2.2) and, in a
   managed product, children collapsed into their parent or chunks sharing one attached context returned as
   one result (Bedrock knowledge-base pages). Fix: treat the count as a maximum in code and in tests, and log
   how many came back.
