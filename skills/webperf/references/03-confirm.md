# § 3 — Confirm, and keep the honest comparison

> Section 3 of `skills/webperf`. Read it before reporting a win.

1. **Re-measure the same scenario, the same way.** Same page, same data volume, same throttling. A
   comparison against a different dataset proves nothing.
2. **State the win as a number**, and if it's marginal, say so and consider reverting: complexity
   added for a 3% gain is a net loss on a codebase someone has to maintain.
3. **Check you didn't move the cost.** Caching that makes the second load fast and the first slower,
   or a frontend win paid for by a heavier query, is a trade to make deliberately, not by accident.

