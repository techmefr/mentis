# prototype §2 — The two shapes

> Section 2 of `skills/prototype`. Read the one that matches the question chosen in §1.1.

## 2.1 The logic demo
For "does this state model feel right": a business rule, a transition table, a data shape, the surface of an
API not yet written.

1. **One self-contained page**, plain markup, style and script, no framework, no bundler, no server, so that
   a designer or a domain expert can open it by double-click and it survives being sent around.
2. **Put the logic in a small pure module inside it**, with no reference to the page. Choose its form by the
   question: a reducer when actions are discrete events, an explicit state machine when "which action is legal
   now" is part of the question, a few pure functions when there is no current state, a small class only when the
   logic really owns ongoing state. The page calls the module and never the reverse, which is what lets the
   validated module be lifted out later.
3. **Write for a non-developer.** Labels and buttons use the domain's words, not the code's. Top to bottom: the
   question and a one-line explanation, the current state as a readable panel (not a raw dump) redrawn after
   every click, one always-available button per action, and guided scenarios.
4. **Guided scenarios** each hold a plain description of the situation and what to watch for, then the ordered
   buttons to press. Starting one resets to a known initial state, so it runs the same way every time.
5. **Choose the scenarios for the awkward cases**: the happy path, a tricky edge case, an attempt at something
   that should be illegal. Restrained style, no animation.
6. **Hand it over and listen for "that should not be possible"**: those remarks are the bugs in the idea, which is
   what the prototype is for. New actions and scenarios can be added.
7. **Own example.** For a subscription model, the scenarios would be "pause, then change plan, then resume",
   "cancel during a free period" and "reactivate an expired plan", and the demo's value is the first moment
   a reader says the plan price after resuming is not what they expected.

## 2.2 UI variants
For "what should this look like": several structurally different versions of one screen.

1. **Prefer to host them on an existing page.** Variants on the real route, chosen by a URL parameter, face the
   real header, data and density; a lone empty route makes every variant look fine. Existing data loading and
   access control stay, only the rendering swaps. Something with no page yet that would naturally live inside one
   still counts as this case.
2. **A new throwaway page only when nothing could host it**, named so the word "prototype" shows in the path or
   file name, after checking that an existing page really cannot embed it.
3. **Default to three variants, never more than five**; beyond that they stop being distinct.
4. **They must differ in structure**: layout, information hierarchy, primary affordance. Variants that differ in
   colour or copy are a tweak. If two drafts come out alike, redo one with an explicit ban on the shared pattern.
5. **Each variant is free to discard the shared layout**; a shared small part such as a header is fine.
6. **A small switcher** fixed at the bottom of the screen: previous, current label, next, wrapping around,
   updating the URL parameter so a variant is shareable and survives reload, with the arrow keys too except while a
   text field has focus, and visibly unlike the design under test.
7. **The switcher is absent from a production build**, so that a stray merge cannot ship it.
8. **Read-only by default.** If a variant must mutate, point it at a stub: the question is the look, not the
   backend.
9. **Listen for the mix**: the useful feedback is usually "the header from one and the sidebar from another".
