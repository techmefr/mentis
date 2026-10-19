# reuse-before-write §2 — The ladder

> Section 2 of `skills/reuse-before-write`. Read it after §1, to choose what to write. Stop at the first rung
> that fully works. "Fully works" means the whole §1 list is covered, not that the happy path runs.

1. **Does it need to exist?** Leave out the option, the flexibility and the feature nobody asked for, and say
   so in one line in the closing note (§3). A vague request gets the smallest version that does the core job,
   not the largest reading of it. If the request is so open that the smallest version is a coin flip, that is
   a question for the operator, not a rung.
2. **Is it already in this codebase?** A helper, a component, a service, a pattern. Use it the way the code
   around it does: same call shape, same error path, same file layout. Finding a near match and bending it
   by a parameter beats a second copy; finding one that is nearly right and copying it is how two helpers
   come to disagree later.
3. **Does the language, the framework or the platform do it?** Use that, unless the project already has its
   own wrapper: **a house component beats the native widget**, because the house component carries the
   project's styling, accessibility fixes and tests. A NestJS pipe for parsing and validating a query
   parameter beats a hand-written `if` chain in the controller; Laravel's response helpers for a streamed
   download beat a loop that builds the file in memory.
4. **Does a dependency already installed do it?** Use it. Never add a dependency for a few lines. Two
   limits on this rung, both ahead of it in priority: the project's own policy on packages (cooldown on new
   versions, preferred or banned packages, licences) decides before convenience does, and a package that is
   installed only as somebody else's transitive dependency is not a dependency you may rely on.
5. **Can it be one line a reader takes in at a glance?** Then one line. A one-liner that has to be decoded
   is not short; it is long and compressed. If you would explain it in a code comment, it fails this rung and
   you take the next one (comments are not written here; the explanation is the structure).
6. **Otherwise, the minimum that works.** No wrapper, type conversion, option, config key, boilerplate or
   "for later" scaffolding nobody asked for. Keep values in the shape the platform hands you. Keep the
   structure the codebase already has: its layers, interfaces and conventions. Deletion beats addition.

## Reading the ladder
- **The shortest working diff wins, once the reach of §1 is known.** Before then it only looks shortest.
- **Between two answers of equal size, take the one that is right on the edges** (empty input, zero, the last
  item, rounding, time zones, two requests at once).
- **A rung is not a reason to skip a layer.** If the codebase puts queries in a repository class, "the
  shortest" is still a call into the repository, not a query in the controller.
