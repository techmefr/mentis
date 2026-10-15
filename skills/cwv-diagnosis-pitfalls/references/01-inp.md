# cwv-diagnosis-pitfalls §1 — INP: find the phase, then the owner

Interaction to Next Paint spans everything between the input and the next frame. Most wasted effort comes from
rewriting the event handler when the time was spent before it started or after it finished.

## 1.1 The three phases
1. **Name the dominant phase from a trace before changing anything.** The reference splits an interaction into
   input delay, processing time and presentation delay, and says plainly not to optimise the handler until the
   trace shows which one dominates.
2. **Each phase has its own evidence and its own kind of fix.**

   | Phase | Evidence to look for | Typical fixes |
   |---|---|---|
   | Input delay | A long task already running on the main thread when the event arrives | Less startup work, split long tasks, delay third parties |
   | Processing time | The event callbacks and the synchronous work attached to the interaction | Remove work, simplify handlers, move heavy computation to a worker |
   | Presentation delay | Style, layout, paint or other main-thread work before the next frame | Touch fewer nodes, lower rendering cost, avoid layout invalidation |

3. **Reproduce on a representative device or a throttled CPU, and repeat the same interaction after the fix.**
   Same interaction, same conditions; then wait for new first-party RUM or CrUX visits before saying the field
   number improved (`webperf-measurement-and-budget-pitfalls` §1).
4. **One tab is not field INP.** A `PerformanceObserver` on `event` entries reports the interactions of the
   current session only. For production, the reference points to the attribution build of `web-vitals`, whose
   INP attribution can name the interaction target, the event type and the Long Animation Frame or script
   evidence available for real visits (`webperf-measurement-and-budget-pitfalls` §2).

## 1.2 Yielding, and the order of paint
1. **Split long work and yield between the pieces.** Process in chunks and give the main thread back between them
   with `scheduler.yield()` where it exists, falling back to a zero-delay `setTimeout`. Choose the chunk size from
   trace evidence: a fixed number of items does not guarantee a short task on a representative device.
2. **A yield only helps if the visible update can paint before the rest of the work.** Show the feedback first,
   for example a loading class on the button, yield, then do the calculation and the final update, and move
   analytics calls to idle time (`requestIdleCallback`, with a `setTimeout` fallback). The reference's own
   caution: confirm the frame in the trace.

   ```js
   button.addEventListener('click', async () => {
     button.classList.add('loading');
     await yieldToMain();
     render(compute());
     scheduleIdle(() => track('click'));
   });
   ```

   Here `yieldToMain` and `scheduleIdle` stand for the two fallbacks above, written once for the project.
3. **A chunked loop is not a fix when the cost is presentation.** If the dominant phase is rendering, splitting
   the JavaScript moves nothing. Own guidance: check the phase of §1.1 first, then choose between yielding and
   touching fewer nodes.

## 1.3 Who owns the delay
1. **Attribute long tasks to a script URL, third parties first.** Delay widgets that are not essential until
   interaction or visibility, but do not make the first interaction pay the whole start-up cost with no feedback.
2. **Profile the state transition before memoising a framework component.** Memoisation is justified only when it
   removes work the trace shows as repeated; applying it everywhere is not a fix.
3. **Large DOM updates cost in two ways.** Reduce the number of invalidated nodes, and avoid forced synchronous
   layout caused by interleaving reads and writes of layout properties.
4. **CPU-heavy work can move to a Web Worker, which has a price.** Measure the serialisation overhead of the data
   you send and receive before calling it a win.
