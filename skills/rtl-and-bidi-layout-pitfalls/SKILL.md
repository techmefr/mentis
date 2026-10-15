---
name: rtl-and-bidi-layout-pitfalls
description: "Use when a product adds or reviews a right-to-left locale such as Arabic or Hebrew, or mixes scripts of both directions in one sentence: direction set per locale and taken from script data, logical CSS properties, mirroring directional arrows with one rule, visually hidden text that survives right-to-left, design-system components that are not right-to-left ready, isolating each formatted value inside a message, and testing with a pseudo right-to-left locale before translations exist."
---

# rtl-and-bidi-layout-pitfalls

Step 6 of the pipeline (`WORKFLOW.md`), for the two ways a right-to-left locale breaks a page that works in
English: the layout (what sits on which side) and the text (where a value from one direction lands inside a
sentence of the other). `vue-nuxt-vuetify-conventions` §6 (point 20) already says that a right-to-left locale is a
layout property and not a mirrored stylesheet; this block adds the settings, the one allowed mirroring rule, the
hidden-text pattern and the message side. The two sections share one premise: **direction is data attached to a
locale, a message and a value, and everything that guesses it from the page or the characters guesses wrong
somewhere**. This is a short block built on a thin set of sources, listed in
[`references/origin.md`](./references/origin.md) together with what was left out for lack of a file to read.

## When
- A right-to-left locale is added, or a design is reviewed for one.
- A sentence contains a name, a number, a price or a code in a script of the other direction, and punctuation or
  order looks displaced.
- A hidden label, skip link or description appears in the wrong place once the page is right-to-left.
- A component library is chosen for a product that will ship in Arabic or Hebrew.

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Layout: where direction is set and where it comes from, logical properties, arrows, hidden text, components | a page or component is made to work right-to-left | [`01-direction-and-layout.md`](./references/01-direction-and-layout.md) |
| 2 | Text: spillover, isolating each value, direction metadata, formatter marks, a pseudo right-to-left locale | values of one direction sit inside sentences of the other | [`02-bidirectional-text.md`](./references/02-bidirectional-text.md) |

## Output / checkpoint
Each rule was exercised, not read off the file: the page was opened with a real right-to-left locale and with the
pseudo locale, every screen was checked for sides, arrows and hidden text (§1), and one sentence per message that
holds a value was rendered with a left-to-right name, a number and a price inside right-to-left text and the
punctuation stayed next to the right word (§2). A page seen only in English is not verified.

## Guardrails
- Never hard-code a list of right-to-left languages when the script data says it (§1.1).
- Never mirror every icon; mirror directional arrows with one rule keyed on the direction (§1.2).
- Never hide text by positioning it off screen or with a negative indent (§1.3).
- Never assume a component library is right-to-left ready (§1, last subsection).
- Never join formatted pieces into a sentence yourself, and never strip the invisible direction marks a formatter
  added (§2.1).
- Never infer the direction of a value by looking at its characters (§2.1).
- This block states guidance and library behaviour as of the sources read on the date in
  [`references/origin.md`](./references/origin.md). The MessageFormat 2 specification and the Pontoon page were
  used for facts only, in our own words. Nothing was run while writing it.

## Origin
Rewritten from the hardening reference of the Impeccable skill (Apache-2.0), the hide-content post of the A11y
Project (Apache-2.0 file, no separate content licence: all rephrased), the bidirectional text section of the
Unicode MessageFormat 2 specification (facts only), the Lingui pseudo-locale configuration (MIT), the Nuxt i18n
locale options (MIT), the Pontoon new-locale documentation (BSD-style licence) and the GOV.UK language navigation
page (MIT), read 2026-10-16. 🟡: never run by us; open points are in
[`references/origin.md`](./references/origin.md).
