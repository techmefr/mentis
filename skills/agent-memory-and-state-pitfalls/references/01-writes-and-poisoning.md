# agent-memory-and-state-pitfalls §1 — Writes and poisoning

Points 1.1.5, 1.2.2, 1.2.5 and 1.2.6 come from framework and vendor documentation re-read on 2026-10-20 (see `origin.md`); the rest is own guidance.

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
5. **A memory shared by several agents is written by all of them.** One agent framework's current documentation says
   the agent edits its own memory as it learns, and offers shared memory repositories that several agents attach;
   so a poisoned or wrong edit by one agent reaches every reader. The same documentation says every edit is a
   commit in a version history, which is the tool for finding the writer and undoing the edit. Fix: give shared
   memory the §2.1 point 4 write rule, keep the writer in the entry, and make memory that only one role should
   change read-only for the others if the framework allows (not found in the documentation read). Source: Letta
   documentation, memory and MemFS pages.

## 1.2 What is stored
1. **Store facts, not instructions.** Symptom: an entry such as "ignore the usual review" read back as a command.
   Fix: store "the user prefers short reviews" as data, and place memory in the prompt in a clearly labelled
   data section, never in the system instructions.
2. **Never store secrets or raw identifiers.** Symptom: a token or a card number in a notes file that is
   then committed, logged or surfaced to another user. Check: scan the store for key and identifier patterns.
   Fix: refuse the write, keep a reference to where the secret lives. Anthropic's memory-tool page says the model
   usually refuses to write sensitive information and, for a stronger guarantee, tells you to add validation that
   strips it before your handler writes the file: the refusal is a habit, the validation is the control.
3. **Summaries drift.** Each summary of a summary loses qualifiers (who, when, under what condition) and can
   invert a claim. Fix: keep the original entry or a pointer to it, re-summarise from originals, and carry the
   date.
4. **A state file for a task is also memory.** A half-finished plan restored after a crash is trusted. Fix:
   store what was done and verified, not what was intended, and re-check cheap preconditions on resume.
5. **An in-process state store dies with the process.** Symptom: "the agent forgot everything" after a restart or
   deploy, or, the reverse, a test passing on a store that production does not have. Check: restart the process
   mid-task and resume. Fix: use a durable store for anything that must survive, and key state per thread or session so
   two runs never share it. LangGraph's stores page calls its in-memory store suitable for development and testing and
   points to database-backed stores for production, and its checkpointer page says the thread identifier is the
   primary key without which state cannot be saved or resumed; Google's ADK documentation says its in-memory session
   service and in-memory memory service lose state on restart (LangGraph and ADK documentation).
6. **File-backed memory is a file-system exposure.** Symptom: a memory path that escapes the memory directory, such as a
   relative path with parent-directory segments, or an encoded one, reads or overwrites a file elsewhere. Check: ask the
   handler for such paths, including percent-encoded ones. Fix: canonicalise every path in every command and refuse
   anything outside the memory root; Anthropic's memory-tool page makes the application responsible for this and lists
   the checks.

## 1.3 Checks
1. Every entry has a source, a writer and a date, or it is deleted by the next cleanup.
2. No entry created from tool or document content lacks a confirmation flag.
3. A scan for key, token and identifier patterns over the store returns nothing.
4. Memory enters the prompt in a labelled data section and never in the instruction part.
