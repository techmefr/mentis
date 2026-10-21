# multi-source-answer-synthesis-pitfalls §1 — Planning the search

> Part 1 of `skills/multi-source-answer-synthesis-pitfalls`. Read it when a question has arrived and the sources
> are being chosen. Source: the search-strategy skill of the enterprise-search plugin of a plugin repository
> (Apache-2.0, re-opened 2026-10-20), rewritten in our own words; points marked own guidance are ours. Where
> Anthropic's engineering write-up on its multi-agent research system is cited, it is a product team's account,
> used for facts and practices only.

## 1.1 The question type decides the order
1. **Classify the question before the first query.** A decision, a status, a document, a person, a policy, a
   date and an open exploration each live in different places. Symptom: a status question answered from a wiki
   page written months ago. Anthropic's write-up of its research agent gives the extreme case: an agent searching the
   web for context that exists only in a chat tool is doomed from the start, and its fix was explicit heuristics,
   such as examining every available tool first, matching the tool to the user's intent and preferring a specialised
   tool over a generic one.
2. **Start where that type is usually settled.** A decision: conversations that end in a conclusion, mail
   confirmations and meeting notes. A status: the tracker and recent activity. A document: the shared store and
   the wiki. A policy: the official knowledge base first, then conversations that confirm or contradict it. A
   person: assignments, authors and collaborators. A date: a broad time range.
3. **Search the other sources too when the answer matters.** The first source is where to look first, not the
   only place. Own guidance.
4. **Keep the ordering as a default, not a law.** It reflects common practice, not measurement; an organisation
   that records decisions in a tracker should start there.

## 1.2 Build the queries
1. **Extract the parts**: the terms that must appear, the people and projects named, words that signal intent
   (decide, status, deadline), constraints (period, author, place) and anything to exclude.
2. **Use meaning-based search for concept questions and exact search for known names, quoted phrases and
   filters.** Use both when unsure.
3. **Vary the vocabulary.** The same thing is called by an abbreviation, a project code name and a plain
   description; an exact search for one misses the other two. Symptom: "nothing found" for something everyone
   discussed.
4. **Translate filters into each source's own syntax** rather than assuming a filter works the same everywhere.

## 1.3 Ambiguity and empty results
1. **Ask one focused question only when the readings differ enough to change which sources are searched or what
   the answer says.** A list of the distinct candidates is better than an open "what do you mean".
2. **Do not ask when a useful answer can cover the interpretations.** Return both, labelled.
3. **An empty result widens before it reports.** Drop the date filter, then the source or place filter, then the
   less important terms, keeping the core entity. Say when the answer came from a widened query. The same write-up
   describes the opposite failure that makes widening necessary: agents default to long, specific queries that return
   little, and improved once told to start short and broad, look at what exists, then narrow.
4. **When a source is down, skip it and say so.** A rate limit or an outage is a fact to report, not a reason to
   present a partial search as complete.
5. **Run independent searches together** where the tools allow; the wait should be about the slowest source, not
   the sum. Anthropic's write-up reports that running its sub-searches in parallel, and letting each use several
   tools at once, cut research time sharply on complex queries. It also reports the cost of vague delegation: a
   one-line instruction made sub-agents misread the task or repeat each other's searches, so give each search a
   distinct objective and scope.

## 1.4 Record what was searched
1. **Keep a list of the sources searched, the terms used and any source skipped or empty**, so the final answer
   can state it (§3.4). Own guidance.
