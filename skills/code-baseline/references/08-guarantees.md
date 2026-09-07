# code-baseline §8 — Guarantees

> Section 8 of `skills/code-baseline`. Read it at the "I think I'm done" moment, over your own diff. The
> other sections and the guardrails stay in `SKILL.md`.

**For every guarantee the change declares, there has to be a reachable execution path that enforces it, and
you have to be able to name it.** If you can't point at the line that makes the declaration true, it isn't
protection — it's a claim the next reader will trust. Wire it or delete it.

1. **The asymmetry is the whole reason.** A *missing* protection is visible: someone eventually asks "wait,
   is this authorised?". A declared-but-unenforced one is invisible **precisely because it is declared** —
   it consumes the attention that would have found the hole. A reviewer who reads a permission check stops
   asking whether deletion is guarded; a reader who sees an interface assumes something implements it; a
   reader who sees a test name assumes the invariant is checked.
2. **Six shapes to check the diff for.** A **contract with no caller** (an interface, an abstract method, an
   event with no listener). A **guard that cannot fire** — the condition is unreachable, or the value it
   reads is never set. A **registration with no counterpart** (a listener for an event nobody dispatches, a
   route to a missing handler, a seeded permission with no check against it). A **switch with no reader** (a
   config key, a feature flag, an option nothing consults). A **claim with no code** — user-facing copy
   announcing a protection, a docblock naming an exception the method cannot throw, a field label describing
   a constraint the validation doesn't apply. And a **test that cannot execute**: skipped, unregistered,
   guarded by an environment condition that is never true, or asserting something the code can't reach.
3. **A comment does not close the gap.** Keeping the declaration and explaining it in a comment or a `TODO`
   fails twice — §1 forbids the comment, and a note doesn't make the guarantee hold. Suppressing the
   analyser's unused-symbol warning is worse: that warning was this check running for free.
4. **Prefer the mechanism the runtime enforces over the sentence you'd have to remember.** Where the
   platform can express the constraint — a type, a config field, a permission, a constraint, a linter rule —
   declaring it there means it holds whether or not the next reader honours the prose. Where it genuinely
   cannot, say which half is enforced and which half rests on trust, rather than writing the sentence and
   implying it's covered. This repo learned that one on itself: twelve of its own agents carried a prose
   *"never edit files"* rule for a month with nothing in their frontmatter denying the tool
   (`references/claude-code-platform.md`, and the correction stamped 2026-09-07 in
   `doc/HOW-WE-WRITE-OUR-AGENTS.md`). The variant to watch for is subtler: **removing a declaration is
   not the same as declaring the absence.** Dropping `agents` from this repo's own plugin manifest left
   `claude plugin details` still reporting 25 agents, because the loader discovers the directory by
   convention — the fix was `"agents": []`, and the way it was found was reading the tool's own
   inventory back instead of trusting the edit (`skills/distributing-blocks`).
5. **Carve-outs — a caller that is legitimately elsewhere.** A published API surface exports for consumers
   outside the repo, so zero in-repo call sites proves nothing. Framework contracts have the framework as
   their caller. A deliberate extension point counts where the variants exist or land in the same milestone
   (§7). A guard at a trust boundary the type system can't reach — a check on a deserialised payload, an
   untyped third-party return — is enforcement, not decoration. And a staged rollout behind a flag is fine
   where the other branch is dated and tracked outside the code.
6. **It binds this diff, not the codebase** (§0). A legacy unenforced guarantee found in passing is flagged
   once, not fixed unprompted — with one exception: copy that promises a user a protection they don't have
   is a defect now, not debt. A human can override any of this ("leave the interface, the second
   implementation lands next sprint"); say once what is unenforced until then, and move on.
