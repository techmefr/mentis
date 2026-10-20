# agent-memory-and-state-pitfalls §3 — Tests and diagnosis

All points in this file are own guidance.

## 3.1 Tests to run against the real store
1. **Planted false memory.** Put an instruction-like sentence in a page or document the agent summarises. Then
   open a fresh session and check that no entry was created from it, and that behaviour is unchanged. Success is
   judged on the store and on actions, not on what the model says.
2. **Boundary crossing.** Create entries as user A in tenant 1; as user B (same tenant) and as user C (tenant 2),
   ask for them directly and indirectly. Success: no entry, no paraphrase.
3. **Ageing.** Insert an entry past its review date and ask a question that depends on it. Success: the agent
   flags it as possibly stale or ignores it, per the rule written in §2.2.
4. **Contradiction.** State a fact, later state the opposite. Success: one active entry, the older superseded,
   and the answer follows the newer.
5. **Reset and delete.** After a reset, the fresh-session check from §2.3 passes.

## 3.2 Diagnosing odd behaviour
1. **List what the run loaded from memory before touching the prompt or the model.** Symptom: behaviour no
   instruction explains. Check: log the entries injected at start (ids, sources, dates). Fix: remove or correct
   the entry, then find the write that created it.
2. **Bisect memory like context.** Run with memory empty, then with half of it. If the symptom disappears, the
   cause is an entry; see `agent-context-hygiene-pitfalls` for the diagnosis habits that apply inside a context.
3. **Check the writer, not only the entry.** One poisoned entry means the gate in §1.1 has a hole; closing the
   hole matters more than deleting the entry.

## 3.3 Checks
1. The four tests of §3.1 exist as repeatable cases, not as a one-off session.
2. A trace of memory loaded per run is available when a complaint arrives.
3. The cause of a bad entry is fixed at its write path.
