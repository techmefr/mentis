---
name: a11y-hiding-and-tables-pitfalls
description: "Use when content has to be hidden from sighted users but kept for screen readers (a label for an icon-only control, a skip link), hidden from assistive technology only, or hidden from everyone, and when a data table is marked up: the clip pattern for visually hidden text, making a hidden focusable element appear on focus, display none versus aria-hidden versus the hidden attribute, table captions, and th cells with scope for column and row headers. The general semantics, ARIA and keyboard rules are accessibility."
---

# a11y-hiding-and-tables-pitfalls

A small defensive block for two markup decisions that look finished in a browser and are wrong in a screen
reader. The first is how content is hidden: there are three different audiences (everyone, assistive technology
only, sighted users only) and each has a different mechanism. The second is the markup of a simple data table.
Both come from two short how-to posts of the A11y Project, read at the commit stamped in `references/origin.md`.
The wider rules (names and roles, keyboard order, focus, `aria-hidden` on something focusable, landmarks and
skip links) are in `skills/accessibility` (its §6 also covers tables, at diff level) and are not repeated here. Complex tables with spanned or multi-level
headers are not covered by the source and are not covered here.

## When
- An icon-only button or field needs a text label that sighted users do not see.
- A utility class such as `.sr-only` or `.visually-hidden` is added, or is applied to a link, button or input.
- Content is hidden with `display: none`, `aria-hidden` or the `hidden` attribute, and it is unclear who should
  still get it.
- A table is added or restyled, or a grid of `div` elements stands in for one.

## Steps

**Read the part for the decision in front of you.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Hiding content: the clip pattern, hidden focusable elements, the three mechanisms and their audiences | something is hidden, or a hidden-text class is used | [`01-hiding-content.md`](./references/01-hiding-content.md) |
| 2 | Data tables: caption, header cells, scope, unique headers | a table of data is written or reviewed | [`02-data-tables.md`](./references/02-data-tables.md) |

## Output / checkpoint
For each hidden element: who must still get it (sighted users, assistive technology, both, neither) and the
mechanism chosen for that audience, and for a hidden but focusable element the proof that it appears when it
receives keyboard focus. For each table: its caption and which cells are column and row headers. Evidence is a
Tab-key pass that shows every hidden-but-focusable control becoming visible, and a screen reader or
accessibility-tree read of the table that announces its name and, for a cell, its two headers.

## Guardrails
- Never use `display: none` on content that is meant for a screen reader user (point 1.1).
- Never apply the visually hidden class to a focusable element without a rule that shows it on focus (point 1.3).
- Never use `aria-hidden` expecting it to hide anything visually (point 1.5).
- Never leave a data table without a caption (point 2.2).
- Never use header cells without saying whether they head a column or a row (point 2.3).
- Do not rely on a positioning trick or a negative text indent to hide text; they fail in right-to-left pages
  (point 1.2).

## Origin
Rewritten from the A11y Project posts "Hide content" and "Create accessible data tables" (Apache-2.0 repository
licence), read 2026-10-16. The full provenance, what was removed and what is our own guidance are in
[`references/origin.md`](./references/origin.md). 🟡: never run by us.
