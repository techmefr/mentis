---
name: interface-design
description: Use when producing or auditing a mockup, or deciding an interface's shape before it is coded: containers, states, design tokens, button hierarchy, chips versus buttons.
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

## §0 Settle the mode first: producing, or auditing?
The same rules read differently depending on which you're doing, and getting this wrong wastes the whole pass.
**If it isn't explicit, ask, and don't start until it's settled.** Production is the usual need.

- **Producing** — you apply each rule as you build: plan every mandatory state, take every value from the
  scale, choose the container from the tree. The output is the mockup.
- **Auditing** — you flag, you don't redesign. The output is a list: the screen or component concerned, the
  rule broken, and what's missing. An audit that silently rewrites the designer's intent isn't an audit.

**Numeric thresholds are the one thing never answered from memory.** A principle is stable and always
applies; an exact number (a contrast ratio, a minimum target size) is defined by a standard and changes. Cite
it from the standard or flag the point as to be verified — never state a figure you're recalling
(`skills/source-freshness`, and `skills/accessibility` which cites its standard).

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
5. **On a small screen, a modal and a bottom sheet look alike and are not interchangeable.** The modal
   interrupts for a blocking action; the bottom sheet is the mobile form of the drawer and shows non-blocking
   context. Choose by **role**, never by appearance — this is the most common wrong pick on mobile.
6. A destructive confirmation is never a toast, and a long form is never a modal.

### 3. Every state, not the happy path
**Scope first**: this applies only to a screen or component that **loads or displays dynamic data** — a list,
a table, a dashboard, search results, a detail fetched from a server. A purely static screen (an information
page, an empty form with no loading) is out of scope, and demanding states on one is noise that gets the whole
checklist ignored.

Each state has its own **obligation condition** — they are not four boxes to tick:
1. **Loading — mandatory as soon as data is fetched.** No exceptions; the network is not optional.
2. **Error — mandatory as soon as data is fetched**, covering network, server and permission failures.
3. **Empty — mandatory only where the data *can* be empty** (a list, a search, a filtered table). Not
   required for data that is always present.
4. **Success — mandatory only where there is a user action to confirm** (saving, sending). Not required on a
   read-only screen: silence after a click is indistinguishable from a failure, but there was no click.

Two quality rules on top, and they're where these states usually fail:
5. **An empty state offers a way out.** Never stop at "no data": say why it's empty and offer the exit —
   create the first item, clear the filters, change the search.
6. **An error message says what to do.** Never stop at "an error occurred": point at an action — retry, go
   back, contact support.

**Deliberately not decided here**: the *visual* form of each state — skeleton versus spinner, the exact
anatomy of an empty state, whether success is a toast, inline or a redirect. That's a level of specification
below this one, and pinning it at mockup time over-constrains the implementation. The code-side blocks own
the mechanics (`flutter-conventions` §4, `react-nextjs-conventions` §5.6, `skills/accessibility` for how the
state is announced).

A mockup showing only the populated screen is an incomplete mockup, not a mockup plus details: these states
are where the implementation questions come from, and leaving them out means they get answered by guesswork at
step 6.

### 4. Buttons and chips
1. **One primary action per autonomous context** — per page, per modal, per panel. Two primaries means the
   hierarchy is undecided, and the user has to make that decision instead.
2. **A modal, a drawer or a bottom sheet is an autonomous context**: it carries its own primary button,
   independently of the page underneath. That's what "per autonomous context" means, and it's the part people
   get wrong when they count primaries per screen.
3. Below it, a fixed ladder (secondary, outlined/inline, link with icon, link only) used for its meaning, not
   for variety.
4. **Size is driven by the container, not by importance**: a button in a compact toolbar is small because the
   toolbar is compact, not because the action matters less.
5. Full-width is for a constrained container (a drawer, a bottom sheet, a narrow form), not a way to add
   emphasis on a wide page.
6. **A chip is not a button.** Chips come in distinct kinds — filter, selection/choice, input, and
   informational/status — and mixing them is what makes a filter bar unreadable. A status chip that looks
   clickable will be clicked.
7. Each chip kind keeps its own fixed height, font size and padding; a chip resized by hand stops matching
   every other chip on the screen.

### 5. Icon and text together
1. **The icon's size drives the text's**, not the reverse — text set to match a large icon reads as a heading
   it isn't.
2. A **bare** icon and a **framed** icon (one in a padded container) are two different objects with two
   different spacing rules; treating them the same is the recurring mistake. A framed icon's visual weight
   comes from its container, so the pairing rule is not the bare one with padding added.
3. A fixed gap between an icon and its label, from the spacing scale — **and the gap differs depending on
   whether the icon sits before or after the text**, because the optical distance isn't symmetric. Two cases,
   two values, both from the scale.
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
block cross-references both instead of restating them. Mechanisms rewritten, no copied text.
**Deepened 2026-08-06.** The first pass wrote this block from the catalogue skills' descriptions. This pass
read the **bodies**, which is where the reasons, the exclusion lists, the carve-outs and the anti-pattern
catalogues live — a description states the rule, a body states when it doesn't apply. What that added here: the **production-versus-audit
mode** discipline (§0) that every one of those skills opens with and no description mentions, the caution
principle on numeric thresholds, the scope limit on screen states (dynamic data only) with a per-state
obligation condition rather than four boxes, the two quality rules on empty and error, the deliberate refusal
to fix the visual form of a state at mockup time, "a modal is an autonomous context so it carries its own
primary", and choosing modal versus bottom sheet by role rather than by appearance. Stamped 2026-08-06.
