# § 4 — The loading path: what blocks the first paint, and what can wait

> Section 4 of `skills/webperf`. Read it when a measurement shows a late first render, a late largest
> element, or a long main-thread task during load, and before adding a script, a stylesheet, a font or a
> third-party origin to a page. It is a list of levers ordered by how much rendering they hold up, not a
> checklist to apply unmeasured: each lever below is pulled only after §1 names the cost it removes.

## The order of the levers

1. **A script in the head blocks parsing unless it says otherwise.** A classic script with no attribute
   stops the parser, fetches, runs, and only then lets the document continue. `defer` keeps document
   order and runs after parsing; `async` runs whenever it arrives and so suits only scripts with no
   ordering dependency; a module script is deferred by default. Choose per script and write the reason
   down in the pull request, not in the code: a script that other scripts need goes `defer`, a
   self-contained one goes `async`, and an inline blocking script has to justify itself against a
   measurement (HTML Living Standard, the `script` element).
2. **A stylesheet blocks rendering, by design.** The browser will not paint before the stylesheets it
   found in the head are ready, which is correct: the alternative is a flash of unstyled content. The
   levers are therefore size and number, not a trick to make it "non-blocking": split a stylesheet that
   only a rare route needs and load it on that route, scope a print or wide-screen sheet with a `media`
   attribute so it does not block the common case, and keep a script that reads computed style from
   running before the sheet it depends on is applied.
3. **Resource hints are a budget, not a free upgrade.** Each hint spends bandwidth or a connection on a
   guess, and a page full of hints has none of them prioritised.
   - `preload` for the one or two resources the browser discovers late and the first render needs: the
     image of the largest element when it is set from CSS or script, and a font the first paint uses.
     A preload nothing uses within a few seconds draws a console warning; that warning is the test.
   - `preconnect` for an origin the page certainly needs early and cannot avoid, such as the origin that
     serves the fonts or the media. It opens the connection only; use it for few origins.
   - `dns-prefetch` is the cheaper fallback for an origin that may be needed.
   - `prefetch` for the next likely navigation, at idle priority; a wrong guess costs bytes on the user's
     connection, so it is not applied to a metered or data-saving context.
   The project fixes a ceiling on the number of hints and a script counts them (mechanical checks below).
4. **Fonts are loaded by decision.** Serve the compressed web-font format every current browser
   supports, and subset the files to the scripts the product actually writes. Declare how the text
   behaves while the font loads with `font-display`: showing fallback text at once and swapping when the
   file arrives avoids invisible text, at the cost of a reflow that a metrics-matched fallback
   (`size-adjust`, `ascent-override`, and their siblings) reduces. A font used only by one route is
   loaded by that route. Self-hosting removes a third-party connection and puts the cache policy in our
   hands; whether the privacy side of a hosted font service matters is `business/data-protection`'s
   question, not this block's.
5. **A third-party script is a dependency with no code review.** It runs with the page's full privileges,
   costs main-thread time on every visit, and can fail or change under us. For each one, in order: is it
   needed at all; can it load after the page is interactive (`async`, or injected on idle); can a static
   facade stand in until the visitor interacts (a video poster instead of the player, a click-to-load map
   instead of the embed); does it appear only after consent where consent is required
   (`business/data-protection`); is it pinned and integrity-checked (`skills/security-hardening`). Measure
   the page with and without it before keeping it.
6. **Defer work as well as bytes.** Code that only an interaction or a scroll position needs is imported
   at that moment: a dynamic `import()` on the first click, or when an `IntersectionObserver` reports the
   section near the viewport. The same holds for iframes and heavy components below the first screen
   (`loading="lazy"` applies to them as well as to images). The first screen is never lazy: lazy-loading
   the largest element delays exactly what the page is judged on (`skills/seo` §3.1).
7. **Layout reads and writes are not interleaved.** Reading a layout property (an offset, a client size,
   a computed style) after a write forces the browser to recompute layout synchronously; doing that in a
   loop over many elements is the classic source of a long task. Read everything first, then write
   everything, or batch writes in the next frame. A framework's reactive system already batches its own
   writes; the problem returns the moment code reaches around it into the DOM.
8. **A long task is cut, not endured.** Work that holds the main thread for long blocks input. Split it
   into chunks and yield between them: `scheduler.yield()` where the engine offers it, with a fallback to
   a zero-delay task or `requestIdleCallback` where it does not. Support for the scheduling API is a fact
   that moves; read the current compatibility table at the time of writing rather than assuming
   (`skills/source-freshness`). Moving the work to a worker is the stronger fix when it does not touch the
   DOM.
9. **Do not break the back-forward cache.** A page that can be restored instantly from the browser's
   in-memory snapshot is faster than any load, and the commonest thing that prevents it is an `unload`
   handler: use `pagehide` or `visibilitychange` for what has to run when leaving. `Cache-Control:
   no-store` on the document, an open connection a page keeps, and a few other conditions also exclude a
   page; the browser's developer tools report the exact blocker per page, and that report is the
   source, not a list kept here.
10. **Weight is measured once and then held.** Bundle size, stylesheet size and the transfer weight of a
    route are measured on the real build, written to a versioned budget file, and compared in the
    pipeline so growth is a decision rather than a drift. The figure comes from the project's own
    baseline and its audience's connection, never from a number remembered from an article
    (`skills/source-freshness`). Duplicate copies of a dependency in the bundle (two versions pulled by two
    parents) are found by asking the package manager why a package is present, and fixed in the lockfile.
11. **Count the document too.** A very large DOM costs memory, style recalculation and layout time on
    every interaction; the lever is rendering less (§2.4), not trimming wrappers for their own sake. The
    node count is read from the rendered page and compared with the project's own baseline.
12. **First paint metrics are cause-finding, not targets.** The first contentful paint tells you whether
    the delay is before anything shows (server, redirects, blocking resources) or after (the largest
    element). Use it to split the problem before applying any lever above, and report the user-centred
    Core Web Vitals (`skills/seo` §3) as the outcome.

## Mechanical checks

These are hints for reading, never verdicts: an empty result proves nothing and a hit is a place to look.

```
grep -rnP '<script\b(?![^>]*(defer|async|type="module"))[^>]*\bsrc=' src
grep -rnE "addEventListener\(['\"]unload|onunload|beforeunload" src
grep -rnE 'rel="(preload|preconnect|prefetch|dns-prefetch)"' src | wc -l
grep -rnE '@font-face' src
grep -rnE 'loading="lazy"' src
pnpm why <package>
```

- The first lists blocking classic scripts; the second the handlers that cost the back-forward cache
  (`beforeunload` is allowed when it is conditional on unsaved edits, so each hit is read); the third is
  compared with the project's ceiling; the fourth is followed by reading each block for `font-display`
  and a compressed format; the fifth is filtered to images above the first screen, where it should be
  empty.
- Bundle and stylesheet weight: run the bundle analyser the project already has and fail the pipeline
  when the report exceeds the versioned budget file.
- DOM size, long tasks and layout reads are measured in a headless browser with the developer tools
  protocol (a trace of the load), because they exist only at runtime.
