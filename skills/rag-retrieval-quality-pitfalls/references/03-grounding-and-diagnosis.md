# rag-retrieval-quality-pitfalls §3 — Grounding, citations and diagnosis order

## 3.1 Grounding
1. **Grounded means every claim can be inferred from the retrieved text.** Ragas defines faithfulness exactly
   so: split the answer into claims, check each against the retrieved context, and take the share supported.
   Its own example: a right country and a wrong date give one supported claim out of two.
2. **Faithful is not correct.** An answer can be fully supported by a retrieved passage that is outdated or
   wrong (§1.2). Faithfulness checks the answer against the context, not against the world; correctness needs
   a reference.
3. **Relevant is not faithful.** The Ragas answer-relevancy metric rebuilds likely questions from the answer and
   compares them with the real question; the page states it does not evaluate factual accuracy. A fluent
   answer to the right question can still invent its content.
4. **Decide what happens with nothing.** Symptom: confident answers to questions the corpus cannot answer.
   Fix: when retrieval returns nothing, or nothing above a relevance floor you chose on the reference set,
   return "not found" or ask a clarifying question instead of calling the model (own guidance). Check with
   the no-answer questions of §2.1.
5. **An instruction to answer only from the documents is a request, not a control** (own guidance): measure it
   with faithfulness on the reference set.

## 3.2 Citations
1. **A citation is a claim about a claim.** Symptom: the link exists, the sentence is not in the page. Check:
   for a sample, open each cited passage and mark whether it supports the sentence it is attached to.
2. **Let the system supply the citation, not the model** (own guidance): attach the identifiers of the chunks
   that were in the context, then have the model select among those identifiers; reject any identifier not
   in the context. A model that writes a URL or reference from memory will invent plausible ones.
3. **Cite at the unit a reader can check:** the passage or page, not only the document title (own guidance).
4. **Cited and retrieved are different sets.** An answer can use a chunk it did not cite or cite one it did
   not use. Compare the cited identifiers with the claim-level check of §3.1 on a sample (own guidance).
5. **Show the date and version of the source** (own guidance) so a reader can judge staleness (§1.2).

## 3.3 Diagnosis order
Work through the stages in this order and stop at the first that fails. Each step names the evidence.
1. **Look at the trace of the failing question first.** The Ragas improvement guide ties every result row to a
   trace so a person can see what was retrieved and generated; do the same (what query, which chunks in
   which order, what prompt, what answer). Without it every step below is a guess.
2. **Corpus.** Is the answer in the indexed documents at all, in a current version? If not, it is a content or
   ingestion problem (§1.2); no tuning will fix it.
3. **Retrieval.** Is a chunk holding the answer among the retrieved ones? If not: boundaries (§1.1), search
   method (§1.3), query wording, filters, permissions that excluded it.
4. **Ranking and cut-off.** Present but below the cut-off or buried? Look at rank and result count (§2.2).
5. **Context assembly.** Was the chunk in the prompt whole, in a usable place, without conflicting chunks
   beside it? Noise sensitivity (§2.2) points here.
6. **Generation.** Everything needed was in the context and the answer is still unsupported or wrong: now it is
   a prompt or model problem, measured by faithfulness (§3.1), and the change goes through
   `llm-eval-regression-pitfalls`.
7. **File the result** with the stage and the evidence, add the question to the reference set, and fix in the
   stage where it was found. In the Ragas worked example the failures were retrieval failures although the
   model's refusals looked like the visible symptom, which is why generation is last.
