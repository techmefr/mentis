# § 6 — When a pattern stops earning its place

> Section 6 of `skills/design-patterns`. Read it when reviewing a pattern that is already in the code —
> during `review`, an `architect` audit, or any change that has to work around one. The catalogue says
> when to add; nothing says when to take one out, which is why they accumulate.

1. **The deletion test is the only one that settles it: inline the pattern in your head and see whether
   the code reads better.** If collapsing the interface, the registry and the two implementations back
   into one function makes the code shorter and the path obvious, the pattern is ceremony and removing
   it is a normal change. This is `over-engineering-review`'s net-line test run in reverse, and it is
   the version that applies to code somebody already merged.
2. **A pattern's cost is paid at reading time, by someone who did not write it.** The concrete costs are
   worth naming because they are invisible to the author: "go to definition" lands on an interface
   instead of behaviour, a grep for the domain word finds the abstract class and not the case that
   matters, and the stack trace passes through a dispatch table so the frame that mattered is three
   levels from the one that failed.
3. **A one-implementation interface is the most common dead pattern**, and it usually got there
   honestly: there were two implementations, one was deleted, and the seam stayed. It now costs a file, a
   registration and an indirection, and it buys a swap nobody is going to make. Deleting it is not a
   refactor with risk — it is the removal of a claim.
4. **The branches collapsing back to one is the signal to re-check, and nothing announces it.** A
   Strategy introduced for four providers when two are decommissioned is now an `if`; a state machine
   whose middle states were removed by a product change is now a boolean. Nobody gets a notification
   about this, so it belongs in the audit that reads the whole area rather than in the diff that touched
   one file.
5. **A pattern whose justification was performance has to be re-measured, not remembered.** Pools, caches
   and Flyweight-shaped sharing were justified by numbers at a moment in time, on a runtime version that
   has since changed. The honest state is either a current measurement in the ADR or the pattern's
   removal — "it was faster in 2023" is not a reason, and it is the reason most often given.
6. **A pattern is not the migration plan.** An interface added "so we can swap the store later" is a
   claim that the swap will fit the shape guessed today; when the swap actually happens, the second
   implementation needs behaviour the interface never exposed, and the interface is reshaped anyway. The
   cost of the wait is nothing, so wait: the second implementation is what tells you the shape.
7. **Growing a pattern to fit a case that does not share its axis is how it becomes unreadable.** The
   new provider needs one extra parameter, so the interface grows one; the next needs a different one,
   so it grows again — and now every implementation ignores half its own signature. At that point the
   honest options are two abstractions or none, and the one that is never right is a single interface
   satisfied by nobody.
8. **A pattern with a test per implementation and none for the dispatch is untested where it fails.**
   The interesting bugs live in the seam: an unknown key with no branch, the default chosen when the
   input was absent rather than invalid, a registration missing after a rename. Each implementation
   passing its own tests is exactly compatible with the wrong one being selected every time.
9. **When the pattern goes, its justification goes with it** — the ADR line, the class name that carried
   it, and any doc that told the next reader to work that way (§5.8). A deleted structure with a
   surviving justification is a trap: the next person implements the pattern again, from the document,
   and the review that should catch it has the document as evidence in favour.
10. **A framework upgrade is the natural moment for this pass**, because it is when a hand-rolled
    structure most often becomes redundant: the container gains the lifetime you emulated, the queue
    gains the retry you wrote, the language gains the sum type your class hierarchy stood in for. The
    upgrade note is the place to record which ones were checked, so the next upgrade does not start from
    nothing.
11. **Removing a pattern is a change like any other, and it is reviewed like any other.** It needs a
    test that passes before and after, one commit that does only the removal, and a sentence saying what
    it bought — not an apology for the original decision, which was usually right when it was made and
    stopped being right afterwards. Treating removals as embarrassing is why they do not happen.
12. **The count that matters is how many patterns a newcomer has to learn to change one thing.** One
    well-earned abstraction on a path is fine; three stacked on the same path means the person fixing a
    typo in a message reads four files. When that is the answer, the area is a `simplify` candidate
    whatever each individual pattern's original justification was.
