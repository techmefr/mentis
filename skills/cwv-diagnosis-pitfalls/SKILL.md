---
name: cwv-diagnosis-pitfalls
description: "Use when a Core Web Vital is poor or a performance trace is being read: splitting INP into input delay, processing and presentation delay before touching a handler, yielding long work so the visible update can paint, attributing long tasks to scripts, reading a layout shift score and its shifted nodes, reserving slots for banners, consent and validation messages, font fallback metrics, animating without layout, and finding which LCP subpart dominates before preloading anything."
---

# cwv-diagnosis-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the moment a vital is red and a fix is about to be written. `seo` §3
states the three page rules (reserve space, prioritise the LCP image, no long task on interactions) and
`webperf-measurement-and-budget-pitfalls` says which instrument may support a claim; neither says how to find the
cause. The three sections share one premise: **each vital is a sum of parts, and a fix applied to the part that
is not dominant changes nothing, so the trace decides before the code does**.

## When
- Field INP, CLS or LCP is poor, or a trace shows a slow interaction, a layout shift or a late hero image.
- Someone proposes a fix (memoisation, a preload, a font swap) with no trace behind it.
- A banner, consent bar or validation summary is about to be added to a page that is already stable.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | INP: the three phases, yielding and paint order, long task ownership, framework, DOM and CPU causes | an interaction is slow | [`01-inp.md`](./references/01-inp.md) |
| 2 | CLS: score and victims, media, dynamic slots, fonts, animation | content moves after it was shown | [`02-cls.md`](./references/02-cls.md) |
| 3 | LCP: candidates, subparts, the usual causes and their evidence | the largest element appears late | [`03-lcp.md`](./references/03-lcp.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the dominant INP phase was named from a trace of the same
interaction on a throttled CPU (§1), the shifted node and the content that caused the shift were both named from
the trace and the slot was tried with the longest translation (§2), and the LCP subpart that dominates was
named before any preload was added and measured again under the same conditions (§3). A fix reasoned from the
source without a trace is a hypothesis, not a result.

## Guardrails
- Never edit an event handler before the trace says which phase dominates (§1.1).
- Never claim a yield helped without seeing the frame that paints before the remaining work (§1.2).
- Never add a banner, consent bar or validation summary above visible content without a reserved slot (§2.2).
- Never copy font override values from another font pair (§2.2).
- Never preload an image because the page is slow; preload it when the trace shows it was found late (§3.2).
- Never attach a millisecond saving to a fix without measuring the subpart before and after (§3.1).
- This block states the guidance of the reference pages read on the date in
  [`references/origin.md`](./references/origin.md). Nothing was run while writing it.

## Origin
Rewritten from three Core Web Vitals reference pages of the Web Quality Skills collection (MIT), read
2026-10-16. 🟡: never run by us; open points are in [`references/origin.md`](./references/origin.md).
