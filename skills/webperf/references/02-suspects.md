# § 2 — The usual suspects, in the order they usually matter

> Section 2 of `skills/webperf`. Read it once a measurement points at a cost.

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
   the route actually ships, don't guess from the import list (levers in §4).
7. **Images and fonts.** Unsized images (which also cost layout shift), full-resolution assets
   displayed small, a blocking font (formats and sizes in §5, font loading in §4).
8. **Motion that costs frames.** No raw scroll listener, and no scroll position held in reactive state:
   observe with `IntersectionObserver`, CSS scroll-driven effects, or a passive handler throttled to the
   frame. A `requestAnimationFrame` loop never writes into framework state each tick; it writes to the
   element or a CSS variable, and stops when idle. Animate `transform` and `opacity`; animate a layout
   property only when the layout change is itself the visible effect. A reduced-motion preference is
   honoured everywhere (`skills/accessibility` §3.9). Stacking uses a named z-index scale, not an arbitrary
   large number.
