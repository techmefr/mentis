# agent-memory-and-state-pitfalls §2 — Scope, expiry and forgetting

Points 2.1.5 and 2.2.5 come from the LangGraph documentation (see `origin.md`); the rest is own guidance.

## 2.1 Scope
1. **One flat store for everyone leaks.** Symptom: user A's preference or fact appears in user B's answer.
   Check: ask as B about something only A said. Fix: every entry carries user, tenant and, where relevant,
   project; every read filters on them before any similarity ranking.
2. **A filter applied after the nearest-neighbour search can return nothing or the wrong set.** Re-read how the
   store applies filters (`rag-retrieval-quality-pitfalls` §1.2); prefer separate collections per tenant when
   the isolation matters more than convenience.
3. **Scope the memory to the task, not only to the person.** A coding preference of one repository applied to
   another is a wrong answer with a true source. Store the project key and read the project's entries first.
4. **Shared team memory needs its own write rule.** A fact one member inserts is read by all; apply §1 and show
   who wrote it.
5. **Scope by namespace, and watch prefix reads.** In one framework a memory is keyed by a tuple such as the user id
   plus a label, and a search on a shorter prefix also returns everything below it. Symptom: a read on a short prefix
   returns several users' entries. Check: query with the shortest prefix your code can build. Fix: always build the full
   user key, never a prefix, before a read. Source: LangGraph stores guide §1.
6. **A result limit silently drops entries.** In the same framework a search returns ten items by default and cuts the
   rest without an error, in a backend-dependent order. Symptom: the agent "forgets" a fact that is stored. Check: store
   more entries than the limit and ask for the oldest. Fix: set the limit deliberately, page through, or rank before
   cutting. Source: LangGraph stores guide §1.

## 2.2 Expiry and contradiction
1. **Facts go stale** (address, role, tool version, "currently working on"). Symptom: confident answers
   about the past. Fix: give each entry a kind with its own lifetime (identity: long, status: short), a review
   date, and show the date when the entry is used.
2. **Contradiction is the normal case.** Symptom: two entries saying opposite things, the agent picks the
   one that ranks higher. Fix: on write, search for a conflicting entry; mark the older superseded rather than
   storing both; on read, the user's current message beats any entry.
3. **Unbounded growth degrades retrieval and cost.** Symptom: each session adds entries and answers get slower
   and vaguer. Fix: a cap per scope, merge near-duplicates, and expire by last use, not only by age.
4. **Use of a memory should be visible.** When an answer relies on an entry, say so ("you told me on that date
   that..."), so a wrong memory is spotted and corrected by the person it concerns.
5. **Retention is your job.** The documentation read shows checkpoints accumulating over long conversations with a cron
   style deletion as the suggested mitigation and no documented automatic expiry for stored items. Fix: schedule the
   cleanup yourself and test it. Source: LangGraph persistence guide §2.

## 2.3 Forgetting
1. **Deleting the entry is not deleting the memory.** Copies live in embeddings, summaries built from it,
   caches, exports and backups. Check: after a deletion, ask for the fact in a fresh session and search the
   vector store and summary entries for it. Fix: record derivation links at write time so a deletion
   cascades through summaries and embeddings.
2. **Provide a way to list and delete one's own memories** and a full reset; the person must be able to
   see what is kept. Retention of personal data is in `llm-pii-and-data-handling-pitfalls`.
3. **A deletion request ends in a test, not a log line.** Report forgotten only after the fresh-session check passes.

## 2.4 Checks
1. A read without scope keys fails closed in code, not by convention.
2. Each kind of entry has a lifetime and a review date.
3. A deletion test is part of the suite and covers summaries and embeddings.
