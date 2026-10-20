# agent-memory-and-state-pitfalls §1 — Writes and poisoning

All points in this file are own guidance.

## 1.1 Who may write
1. **A memory written from outside content is a persistent injection.** Symptom: days later the agent applies a
   rule the user never gave ("always send reports to this address"), traced to a page or mail summarised earlier.
   Check: for each stored entry, find the turn that produced it and see whether the user, or a document, said
   it. Fix: only user statements or an explicit "remember this?" confirmation create entries; content read by
   tools may be summarised for the current run only.
2. **The model deciding by itself what is worth remembering is a write path.** Symptom: entries that restate a
   guess as a fact. Fix: let the model propose, store as a candidate with status "proposed", and promote on
   confirmation or on a second independent occurrence.
3. **Store the source with the entry:** who said it (user, tool, document), when, in which session, and whether it
   was confirmed. Without that, neither a cleanup nor an incident review can separate trusted from untrusted entries.
4. **Subagents and other agents are outside content.** Their output is written only through the same gate as a
   document (`multi-agent-design-pitfalls`).

## 1.2 What is stored
1. **Store facts, not instructions.** Symptom: an entry such as "ignore the usual review" read back as a command.
   Fix: store "the user prefers short reviews" as data, and place memory in the prompt in a clearly labelled
   data section, never in the system instructions.
2. **Never store secrets or raw identifiers.** Symptom: a token or a card number in a notes file that is
   then committed, logged or surfaced to another user. Check: scan the store for key and identifier patterns.
   Fix: refuse the write, keep a reference to where the secret lives.
3. **Summaries drift.** Each summary of a summary loses qualifiers (who, when, under what condition) and can
   invert a claim. Fix: keep the original entry or a pointer to it, re-summarise from originals, and carry the
   date.
4. **A state file for a task is also memory.** A half-finished plan restored after a crash is trusted. Fix:
   store what was done and verified, not what was intended, and re-check cheap preconditions on resume.

## 1.3 Checks
1. Every entry has a source, a writer and a date, or it is deleted by the next cleanup.
2. No entry created from tool or document content lacks a confirmation flag.
3. A scan for key, token and identifier patterns over the store returns nothing.
4. Memory enters the prompt in a labelled data section and never in the instruction part.
