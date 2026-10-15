# a11y-lint-wiring-pitfalls §3 — Rules that encode a decision

Most lint rules are yes or no. A few ask the project to choose, and a few of the plugins' own examples or
rules should not be followed. This section is the list of both.

## 3.1 Label association: nesting, `for`, or both
1. **There are two ways to associate a label with a control.** Wrap the control in the label, or give the label a
   `for` (`htmlFor` in JSX) that holds the id of the control. The JSX rule also checks that the label has text
   content.
2. **The two plugins disagree on whether one way is enough.** The JSX rule's page says that wrapping the control
   is the simplest way and that all modern browsers and assistive technology will associate it. The Vue
   `label-has-for` page encourages validating both nesting and id "to fully cover" assistive devices, and its
   rule requires both by default. Decision: neither claim was tested here, so the project chooses the JSX
   `assert` option (`both` or `either`) or the Vue `required` option on purpose, and writes the reason next to
   the config. Own guidance: `both` is the stricter and costs a redundant attribute; take it when the audience
   includes older assistive technology and `either` otherwise.
3. **A label that is a sibling of its control needs `for` and an id.** Nesting is not available there.
4. **Two labels for one input.** The second label, if it sits elsewhere in the page, can only use `for`; the JSX
   page's answer is an override of `assert` to `either` on that label, with an inline rule comment.

## 3.2 Ids for labels
1. **Every id used to associate a label is deterministic on the server and on the client, and unique on the
   page.** The JSX page says an id generated at render time is not a convenience but a defect that should never be
   used, because server and client output then differ. Pass a required id prop down from as high in the tree as
   possible so that uniqueness is guaranteed from one place. The Nuxt side of the same defect is in
   `nuxt-no-hydration-nondeterminism`.

## 3.3 Anchors and buttons
1. **An anchor navigates, so it needs a real destination.** `anchor-is-valid` treats a missing `href`, an empty
   one, a bare `#` and a `javascript:` string as invalid. An anchor without `href` is no longer a hyperlink and
   can neither take keyboard focus nor be clicked as a link.
2. **An action is a `button`.** An anchor with `href="#"`, with a `javascript:` URL or with no `href` that exists
   only to run a handler should be a `button`. The page adds that keyboard users expect an anchor to activate on
   `Enter` and a button on both `Enter` and `Space`, and that rebuilding that with ARIA and CSS recreates what
   HTML already provides (`accessibility` §1).
3. **If the design wants a link look for an action, restyle a button.** The page offers that compromise itself
   and calls it inferior to a link that navigates. Own guidance: raise the design question first.
4. **Mouse events alone never expose functionality.** An element that reacts to hover must be reachable and
   operable by keyboard and touch too; the page adds a click handler for that reason in its example.

## 3.4 Click handlers and autofocus
1. **A click handler on a non-interactive element needs a key handler.** The Vue rule `click-events-have-key-events`
   asks for at least one of `keyup`, `keydown` or `keypress` next to `@click`, for people who cannot use a mouse,
   for assistive technology compatibility and for screen reader users; the JSX plugin has a rule of the same
   shape. Own guidance: treat the lint failure as a prompt to use a native `button`, which carries the key
   handling, the focus and the role (`accessibility` §1), rather than as a prompt to add a key handler to a `div`.
2. **`no-autofocus` flags the attribute, not its value.** The Vue page says autofocus can cause usability
   problems for sighted and non-sighted users alike, and its failing examples include `:autofocus="false"` and
   `:autofocus="undefined"`. Its `ignoreNonDOM` option decides whether your own components are checked; the JSX
   README lists the rule in both presets. Own guidance: where focus really has to move on a view change, do it
   in code after the change and not with the attribute.

## 3.5 Rules and examples not to carry
1. **`no-onchange` is deprecated in both plugins.** The Vue page's own warning says the rule rests on the behaviour
   of old browsers (Internet Explorer 10 and below), which newer browsers and the DOM specification have since
   corrected; the JSX README marks the rule deprecated too. Do not enable it and do not rewrite select handlers
   to use blur because of it.
2. **The Vue `no-aria-hidden-on-focusable` page lists passing examples that hide a focusable element.** Its text
   says to avoid `aria-hidden="true"` on focusable elements, but its passing examples include a button that carries
   both `tabindex="-1"` and `aria-hidden="true"`, and a hidden container around a button or a link with
   `tabindex="-1"`. Decision: that contradicts `accessibility` §2.7, which says never to hide something focusable,
   and the repository's rule wins; do not copy those examples as accepted code.
