---
name: webperf
description: Use when a page or a screen feels slow, or before shipping a feature that adds weight to the frontend, diagnose from a measurement rather than from intuition. Complements seo (which covers Core Web Vitals as a ranking factor) and the per-stack frontend conventions on the runtime cost of the code itself.
---

# webperf

Step 6 of the pipeline (`WORKFLOW.md`), and a diagnosis step whenever something is slow. `seo`
covers Core Web Vitals because search ranking depends on them; this block is about the runtime cost
itself, including on screens no crawler will ever see (an authenticated dashboard, an internal admin
table).

## When
When a page/screen is reported slow, or before shipping a feature that adds a dependency, a chart, a
large table, or a new route. Not as a routine pass over code nobody has complained about: unmeasured
optimisation is how simple code becomes complicated for nothing.

## Steps

### 1. Measure before touching anything
1. **Reproduce the slowness and get a number.** Which page, which interaction, how long, on what
   connection and what device class. "The list is slow" isn't actionable; "the list takes 4s to first
   render with 500 rows" is.
2. **Find where the time actually goes** before forming a theory: network waterfall (how many
   requests, which ones block), main-thread work, render count. The bottleneck is regularly not
   where it feels like it is.
3. **Write the number down.** Without a before, there's no after, and "it feels faster" is how a
   change that made things worse gets shipped.

### 2. The usual suspects, in the order they usually matter
1. **Requests that didn't need to happen.** The same data fetched by several components, a request
   fired per row, a call repeated on every keystroke with no debounce. Fewer requests beats faster
   requests.
2. **Requests in sequence that could be parallel.** A waterfall where each call waits for the
   previous one's result, when only the last one actually depends on it.
3. **Payload size.** An endpoint returning entire objects when the screen shows three fields; a
   relation loaded and never used. This is usually a backend fix, and usually the biggest win.
4. **Rendering the whole thing.** Hundreds of rows mounted at once when a dozen are visible. Paginate
   or virtualise before optimising the row component.
5. **Work repeated on every render.** A computation, a sort, a filter or an object built inline
   instead of derived once. Cheap per call, expensive multiplied by renders.
6. **Bundle weight.** A whole library imported for one helper, a heavy dependency pulled into the
   initial route instead of the one screen that needs it, an icon set imported wholesale. Check what
   the route actually ships, don't guess from the import list.
7. **Images and fonts.** Unsized images (which also cost layout shift), full-resolution assets
   displayed small, a blocking font.

### 3. Confirm, and keep the honest comparison
1. **Re-measure the same scenario, the same way.** Same page, same data volume, same throttling. A
   comparison against a different dataset proves nothing.
2. **State the win as a number**, and if it's marginal, say so and consider reverting: complexity
   added for a 3% gain is a net loss on a codebase someone has to maintain.
3. **Check you didn't move the cost.** Caching that makes the second load fast and the first slower,
   or a frontend win paid for by a heavier query, is a trade to make deliberately, not by accident.

## Output / checkpoint
A before number, the identified cause, the change, and an after number measured the same way. No
performance change shipped on "it feels faster".

## Guardrails
- **Never optimise without a measurement.** Intuition about performance is wrong often enough that
  guessing routinely makes code more complex and slower.
- **Simplicity outranks micro-optimisation** here as everywhere: a marginal gain that costs
  readability is refused. Minimising the logic to maintain is the standing priority.
- Don't cache to hide a query problem: it turns a slow page into a slow page with stale data.
- A perceived-performance change (skeletons, optimistic UI) is legitimate but it's a different claim:
  don't report it as a latency improvement.

## Origin
Sourced from the market: a `webperf` skill in a market generalist dev skill catalogue was the trigger
to write this, alongside web.dev's performance guidance (already the source for the Core Web Vitals
part of `seo`) and the bundle-weight items rewritten from a market open source TypeScript project's
review skill. The ordering of section 2 (requests before rendering before bundle) and the
measure-first/re-measure-identically discipline are ours; the "state a marginal win and consider
reverting" rule follows the standing internal preference for simplicity over call-count optimisation.
No dedicated internal performance-engineering experience at this stage.
