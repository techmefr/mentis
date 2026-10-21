# rag-retrieval-quality-pitfalls §2 — Retrieval evaluation

## 2.1 The reference set
1. **Cover the query types the product gets.** The Ragas testset guide separates single-hop questions (one
   source) from multi-hop (several sources), and each can be specific (a fact) or abstract (an explanation).
   Symptom of a set with only specific single-hop questions: a green dashboard and unhappy users asking
   "why did X change".
2. **Generated questions are a start, not a verdict.** Ragas builds test questions from a graph of chunks, so
   the questions inherit the wording of their source chunk and flatter lexical retrieval (that second half is
   own guidance). Read a sample, add real user questions from logs once they exist, and keep the generated
   ones labelled as such.
3. **Each question carries what a correct retrieval would contain.** Either the passage identifiers (cheap to
   compare, brittle when you re-chunk: identifiers change) or a reference answer used as a proxy (cheaper to
   write, judged by a model). Ragas offers both, noting that annotating reference passages is time-consuming,
   which is why its model-based recall uses the reference answer instead.
4. **Include questions with no answer in the corpus.** Without them nothing measures the "not found"
   behaviour of §3.1.

## 2.2 Retrieval metrics
1. **Recall asks "was the needed information retrieved".** Ragas defines the model-based version as the share
   of the reference answer's claims that the retrieved text supports, and the identifier version as the share of
   reference passage identifiers found. Both need a reference. Low recall means a retrieval problem; no
   prompt change can recover it.
2. **Precision at rank asks "were useful chunks placed first".** The Ragas description is the average of
   precision at each rank, weighted by relevance; its worked example scores the same irrelevant chunk far
   lower in first place than in second. Low precision with high recall means the answer is present but buried.
3. **Noise sensitivity asks "does an irrelevant or partly relevant chunk change the answer".** In Ragas it is the
   share of the answer's claims that are wrong, measured with relevant chunks or with irrelevant ones, and
   lower is better. Use it when recall is fine and answers are still wrong.
4. **Compute these per question and read the worst ones,** not only the mean (own guidance): a mean hides the
   handful of questions where the answer was never retrieved.
5. **Re-read the metric definitions of the version you run.** The Ragas pages mark an older metric interface
   for deprecation; names and arguments move (re-read before relying).

## 2.3 Judging with a model
1. **Model-based metrics are measurements with their own error.** The Ragas judge-alignment guide says to align
   the judge with a domain expert's labels before using it to steer improvements, because a misaligned judge
   sends every improvement the wrong way. Do that on a labelled sample, as in `llm-eval-regression-pitfalls` §2.
2. **Whose judgment is the ground truth** matters: the guide recommends the principal domain expert (a lawyer
   for legal answers, for instance), not a convenient annotator.
3. **The real value is in reading the failures.** The same guide says the judge is secondary to examining the
   data and the failure patterns. Keep a written list of the patterns found.
4. **A model judge needs the same inputs every run,** so evaluate stored outputs when the question is about the
   judge, and regenerate only when the question is about the pipeline.

## 2.4 Judging a change
1. **Change one stage at a time and name the metric it should move** (own guidance): a new chunking should move
   recall or precision, a new prompt should move faithfulness (§3.1). A change that moves a metric of another
   stage is a surprise to investigate, not a win.
2. **Keep the reference set frozen between two runs you compare,** and re-index under a new name rather than
   in place so the old index is still there to compare against.
3. **Report retrieval metrics and the final answer score side by side** with the number of questions, so a
   reader sees which stage moved.
