# webperf — origin and source stamps

> Provenance of `skills/webperf`. Read it when a rule has to be traced back to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

Sourced from the market: a `webperf` skill in a market generalist dev skill catalogue was the trigger
to write this, alongside web.dev's performance guidance (already the source for the Core Web Vitals
part of `seo`) and the bundle-weight items rewritten from a market open source TypeScript project's
review skill. The ordering of §2 (requests before rendering before bundle) and the
measure-first/re-measure-identically discipline are ours; the "state a marginal win and consider
reverting" rule follows the standing internal preference for simplicity over call-count optimisation.
No dedicated internal performance-engineering experience at this stage.

Motion rules (§2.8) added 2026-10-02 from the redesign checklist of a public design-quality skill
(`taste-skill`, MIT, read that day); reduced motion was already in `skills/accessibility` and is referenced, not repeated.

§4 to §6 added 2026-10-02 after reading the public `Front-End-Checklist` repository (its README and
package metadata declare MIT; the repository carries no licence file, so only the idea of which topics a
frontend review should reach was taken, never a sentence). Every fact was written from primary documents,
none from that repository:
- the HTML Living Standard (the `script` element and `defer`/`async`, `picture`, `img` `srcset` and
  `sizes`, `link` types and `loading`);
- RFC 9111 (HTTP caching) and RFC 8246 (`immutable`);
- web.dev guidance on resource hints, fonts, the back-forward cache, optimising long tasks and images;
- MDN for `font-display`, `IntersectionObserver`, the scheduling API and the `pagehide` event.

Deliberately not taken: a hosted measurement service named as a tool (rule B), a CDN or HTTP-version
checklist (infrastructure, `skills/devops-conventions`), minification and unused-CSS removal (owned by the
bundler), numeric size and time thresholds (recalled figures, `skills/source-freshness`), and speculative
or experimental loading features (the list moves faster than this block).
