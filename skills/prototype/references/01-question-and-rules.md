# prototype §1 — The question and the shared rules

> Section 1 of `skills/prototype`. The two shapes are §2, what happens afterwards is §3.

## 1.1 Name the question, then pick the shape
1. **Write the question in one paragraph before any code**, visible on the artefact itself (an intro on the page,
   a line at the top of the entry file), not only in a comment. A prototype that answers the wrong question is
   pure waste, and a written question can be checked later by someone who was not there.
2. **Pick the shape from the question.**
   - "Does this logic or state model hold up?" is the logic demo (§2.1).
   - "What should this look like?" is the set of UI variants (§2.2).
3. **When the question is ambiguous and nobody can be asked**, follow the surrounding code (a backend module
   points to the logic demo, a page or a component to the variants) and write that assumption at the top of the
   prototype. The two shapes are very different artefacts, so a wrong pick wastes the whole prototype.

## 1.2 Rules both shapes share
1. **Disposable from the first line, and visibly so.** Put it next to the module or page it concerns, so the
   context is obvious, and name it so a casual reader sees at once that it is a prototype. A throwaway route
   follows the routing convention the project already has; no new top-level structure.
2. **Trivial to run.** One command from the project's task runner, or one file opened by double-click. Starting it
   takes no thought.
3. **No persistence by default.** State stays in memory. Persistence is what a prototype may be checking, never
   something it relies on; if the question is about the database, use a scratch store with an unmistakable
   "prototype, wipe me" name.
4. **No polish.** No tests, no error handling beyond what keeps it runnable, no abstraction layer. The point is to
   learn fast.
5. **Show the state.** After each action in a logic demo, and on each switch in the variants, render the full
   relevant state so a viewer sees what changed.
6. **Do not generalise.** No "what if we later support X". One question.
