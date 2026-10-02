# safe-refactor §2 — Pinning behaviour that has no test

> Section 2 of `skills/safe-refactor`. Read it when step 2 finds no proof covering the code you are about to move.

1. **Decide the oracle first: the code as it is.** A characterization test records what the code does today,
   not what it should do. Its job is to fail when the structure change alters an observable result, so it
   asserts current outputs even where they look wrong. A wrong-looking output you pinned is a finding to report,
   not a line to fix in the same change.
2. **Pin at the seam you will keep.** Call the code through the public entry point whose signature step 1
   promised to preserve, not through the internals you are about to move; a test coupled to the internals
   dies with the move and proves nothing about it.
3. **Cover the inputs that decide behaviour**, not every input: the empty value, the boundary, the invalid one,
   the case that takes the error path, the case that takes the rare branch. Read the branches of the code you
   will move and make sure each one is reached by at least one pinned case.
4. **Pin the order of effects when order is observable**: which call happens first, what is written before what
   is sent. A test that records calls in sequence on a fake at the boundary is enough; do not mock the logic
   you are moving.
5. **Watch each pinning test fail once.** Break the code on purpose (flip a condition, drop a line), see the
   test go red, restore. A pinning test that cannot fail gives exactly the false safety this step exists to remove.
6. **Commit the pinning tests before the move**, as their own change, so that the move lands on a base where
   the proof already exists and the reviewer can see the proof was not tuned afterwards.
7. **When pinning is not feasible** (time-dependent code with no clock seam, code that talks to a service with
   no fake), say what blocked it and either narrow the refactor to the part that can be pinned or stop and
   escalate. Do not substitute "I read it carefully".
