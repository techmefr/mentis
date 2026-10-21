# code-review-reviewer-pitfalls §5 — Debt typical of agent-written code

> Section 5 of `skills/code-review-reviewer-pitfalls`. Read it when the change under review was produced by an
> agent, in whole or in large part, or when code works but feels thin. It adds a checklist to §1.5 ("understand every
> line"); it does not change the approval standard. Source, read 2026-10-20: the ai-debt-detector skill of the
> skill-forge-essentials plugin of wshobson/agents (MIT, root licence; the manifest declares MIT for its author).
> Sentences marked "own guidance" are ours. 🟡: never run on a real review.

1. **Review what was not written.** An agent writes toward the case it was shown; the debt sits in the paths it did
   not write. Reading only the diff misses it. Check: for each new function, name the failure that would happen in
   production and look for where the diff handles it.
2. **Failure modes.** Ask of each external call, file operation and parse: what happens on a timeout, a full disk,
   a denied permission, an empty or null input? Symptom: a try block that catches everything and logs, or none at
   all. Check: the handler catches a specific error, does something that a caller can see, and releases what the
   code opened on that path.
3. **Orphans.** List what the change creates and never removes: temporary files, timers and intervals, event
   listeners, subscriptions, open connections, spawned processes. Check: each open or create has a matching close
   or dispose on every path, including the failure path. The source's reminder that garbage collection does not
   close connections, listeners or timers holds in every language with a collector.
4. **Edge inputs.** Empty collection, empty string, null, very large input, non-ASCII text, concurrent calls.
   Own guidance: agents rarely write these cases unprompted; ask for one test per edge or say why it cannot occur.
5. **Invented dependencies and methods.** Check that every import resolves to something in the project's manifest
   and that every call exists in the installed version of the library. Symptom: a plausible name that compiles in
   the author's head and fails at run time, or a package name that exists only because someone registered it after
   models started suggesting it. Check: look the package up in the registry yourself, check its age, owner and
   download history, and open the library's own reference for the method. Own guidance: a new dependency
   introduced by an agent is a decision for a person (`package-manager-supply-chain-pitfalls`), not a diff line.
6. **Deprecated or wrong-version APIs.** An agent often uses the interface it saw most. Check the installed
   version's documentation, and the project's own lint for deprecation warnings.
7. **Drift from the project's patterns.** Does it handle errors the way the neighbouring code does, use the
   project's existing helpers rather than a fresh copy, and put files where the layout puts them? Reinvented
   utilities are the commonest sign (`skills/reuse-before-write`).
8. **Red flags that stop the review.** An empty or log-only catch; resources opened with no cleanup; a to-do about
   handling errors left in the code; an import from a path that does not exist; a timeout set with no abort on
   expiry; a connection taken from a pool and never returned.
9. **Passing the compiler is not evidence.** Compilation shows syntax and types, not behaviour; a green run of
   tests the agent wrote shows agreement with the agent's own idea. Own guidance: ask what test would have failed
   before the change and passes after it (`skills/run-generated-tests`).
10. **When the agent says it is done and shows no check, it is not done.** Ask for the command it ran and its output
    before reading further (`skills/gate`).
11. **Keep the checklist a prompt, not a score.** Own guidance: the source says agents do this at higher rates than
    people; no rate is given in a form we can verify, so none is stated here. Use the list to find specific lines to
    ask about, not to rate the author.
