---
name: interface-design
description: Use when producing or auditing a mockup, or deciding an interface's shape before it's coded — which container a piece of UI belongs in, which states a data-driven screen must plan, the design-token discipline (one spacing scale, one type scale, one icon set), button hierarchy and sizing, chips versus buttons, icon-text coupling, and how to gather visual references from a story. The design-time counterpart of skills/accessibility and business/ux-writing, which stay on the rendered code and the words.
---

# interface-design

Business layer (`business/README.md`), design. Sits **before** step 6: these are decisions made in a mockup
or in a conversation, where changing them costs a rectangle rather than a refactor.

**Relation to a design system.** Every number in a real design system is arbitrary and owned — its spacing
scale, its type scale, its button heights, its icon sizes. This block therefore states **the discipline and
the decision trees, never the numbers**: where a design system exists, its tokens are the authority and no
value here overrides one. Where none exists, the rule is "pick a scale and never leave it", which is the part
that actually holds across projects (rule C: nothing named, no house values).

**Boundaries.** How text is exposed to assistive technology and to the keyboard, in the shipped code →
`skills/accessibility`. The words themselves → `business/ux-writing`. What the screen is for → `skills/spec`
and `business/product-ownership`.

## When
When a screen is being designed or audited before implementation; when a UI element's shape is being chosen;
when a mockup arrives and has to be checked before someone builds it.

## Steps

### 1. Tokens, not values
1. **One spacing scale, and only its steps.** A value invented between two steps ("14 here, it looked
   better") is how a codebase ends up with forty spacings and no rhythm. If the scale is genuinely missing a
   step, that's a change to the scale — a decision, made once, for everyone.
2. **One grid step** that every spacing and size is a multiple of. Two documented exceptions exist in
   practice and are worth knowing rather than discovering: typography (line heights don't land on the grid)
   and fixed interactive component heights.
3. **One type scale** for titles and one for body text, each level meaning a level — not a size picked for
   how it looked in this one card.
4. **A fixed set of icon sizes**, chosen from the set rather than scaled freely.
5. **Spacing expresses relatedness**: elements closer together read as belonging together. That's the actual
   function of the scale, and it's why a uniform gap everywhere reads as flat and unreadable.
6. A floor on internal padding: content touching the edge of its container reads as broken, at every screen
   size.

### 2. Which container
A decision tree, because this is the choice most often made by habit:
1. **Transient feedback, nothing to decide** → a toast/snackbar. It disappears, so nothing important can
   live only there.
2. **A short blocking action or a confirmation** → a modal/dialog. Blocking is the point; anything the user
   needs to compare against the page behind it doesn't belong here.
3. **Contextual work alongside the page**, where the context must stay visible → a side panel/drawer, which
   becomes a bottom sheet on a small screen.
4. **A full task, or anything deep-linkable, shareable, or reloadable** → a page. If a user could plausibly
   want to bookmark it or press back, it's a page, and putting it in a modal removes both.
5. A destructive confirmation is never a toast, and a long form is never a modal.

### 3. Every state, not the happy path
1. **Loading and error are always required** as soon as the screen fetches data. No exceptions — the network
   is not optional.
2. **Empty is required** wherever the data can legitimately be empty (a list, a search, a filtered table),
   and the empty state carries an explanation and the action that would fill it.
3. **Success/feedback is required** wherever the user performs an action: silence after a click is
   indistinguishable from a failure.
4. A mockup that shows only the populated screen is an incomplete mockup, not a mockup plus details — those
   three states are where the implementation questions come from, and answering them in code means answering
   them by guesswork (`skills/accessibility` §forms, `flutter-conventions` §4,
   `react-nextjs-conventions` §5.6 for the code-side form of the same rule).

### 4. Buttons and chips
1. **One primary action per autonomous context** — per page, per modal, per panel. Two primaries means the
   hierarchy is undecided, and the user has to make that decision instead.
2. Below it, a fixed ladder (secondary, outlined/inline, link with icon, link only) used for its meaning, not
   for variety.
3. **Size is driven by the container, not by importance**: a button in a compact toolbar is small because the
   toolbar is compact, not because the action matters less.
4. Full-width is for a constrained container (a drawer, a bottom sheet, a narrow form), not a way to add
   emphasis on a wide page.
5. **A chip is not a button.** Chips come in distinct kinds — filter, selection/choice, input, and
   informational/status — and mixing them is what makes a filter bar unreadable. A status chip that looks
   clickable will be clicked.
6. Each chip kind keeps its own fixed height, font size and padding; a chip resized by hand stops matching
   every other chip on the screen.

### 5. Icon and text together
1. **The icon's size drives the text's**, not the reverse — text set to match a large icon reads as a heading
   it isn't.
2. A **bare** icon and a **framed** icon (one in a padded container) are two different objects with two
   different spacing rules; treating them the same is the recurring mistake.
3. A fixed gap between an icon and its label, from the spacing scale.
4. An icon next to visible text is decorative: it is hidden from assistive technology rather than read twice
   (`skills/accessibility`).
5. An icon-only control needs an accessible name, and it needs a tooltip for sighted users too — a glyph
   nobody recognises is not a label.

### 6. Gathering references
1. Start from what the story actually says, and extract keywords in separate registers rather than searching
   the story's title: **the screen type or UI pattern**, **the components involved**, **the domain and
   context**, and **the intended tone/ergonomics**.
2. Search in the language the design community publishes in (English), whatever the project's language.
3. Infer the tone from the domain rather than from taste — an approval workflow in a financial back office
   and a consumer onboarding flow have different correct answers.
4. References inform, they don't decide: a pattern copied from a product with different constraints imports
   those constraints. Say what was borrowed and what was rejected — that sentence is worth an ADR line
   (`skills/documentation-adr` §4) when it's a trade-off someone will revisit.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes before implementation starts: every value taken from a
scale rather than invented, a stated container choice, all required states drawn, one primary action per
context, and chips typed by kind. A mockup missing any of these produces implementation questions that get
answered by guesswork at step 6.

## Guardrails
- **Never invent a spacing, size or type value outside the scale.** If the scale is wrong, change the scale.
- **Never ship a data-driven screen without its loading, empty and error states.**
- **Never put a destructive confirmation in a toast, or a long form in a modal.**
- **Never guess an accessibility threshold** — a specific number cited from memory is exactly the failure
  `skills/source-freshness` exists for. Defer to `skills/accessibility` and its cited standard.
- Where a design system exists, **its tokens and components win** over anything here; this block is the
  discipline, not the values.
- This block reviews interfaces, it doesn't write code, and it doesn't rewrite a designer's intent: a
  disagreement about intent goes back to the designer.

## Origin
**An org design-system skill catalogue (10 skills: foundations and grid, spacing scale and rhythm, buttons,
chips, containers decision tree, icon-text coupling, screen states, mockup accessibility, mockup UX writing,
inspiration search from a story)** — rules extracted, de-identified and rewritten generically, with **every
house value deliberately left out** (grid step, pixel sizes, spacing steps, type scale, component heights)
because those are owned per design system and a copied number is a wrong number in the next project
(rule C). The two overlapping subjects were **not** duplicated: mockup accessibility stays with
`skills/accessibility` (which cites its standard) and mockup copy stays with `business/ux-writing`; this
block cross-references both instead of restating them. Mechanisms rewritten, no copied text. Stamped
2026-08-06.
