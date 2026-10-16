# laravel-blade-view-pitfalls §1 — Components and composition

> Part 1 of `skills/laravel-blade-view-pitfalls`. Read it when a component, an include or a shared piece of view
> data is written. Sourced from `.ai/laravel/skill/laravel-best-practices/rules/blade-views.md` in
> `laravel/boost` (commit `f1411f9`), read 2026-10-16. Sentences marked "own guidance" are ours.

1. **Spread the attribute bag on the component's root element.** Writing the root as a tag that renders
   `$attributes->merge([...])` lets the caller add attributes, and the merge combines the component's defaults
   with what the caller passed; class values get special merging (the source's wording), so a caller's class is
   added to the default and not a replacement. The source's example builds a default class from a prop on a
   `div` and prints the slot or message inside. Own guidance: a component whose root does not print the bag
   silently drops the caller's `id`, `data-` and `aria-` attributes.
2. **Push a script from a repeated component once.** If a component renders repeatedly on a page, a plain push
   adds its script on every render. The source says to use a consistently named once-only push block, so the
   content is added once per rendered response. Own guidance: the name is the key, so two components that
   mean the same script must use the same name and two that do not must use different ones.
3. **Use a component when the interface should be explicit.** The source: a Blade component fits a reusable
   interface that benefits from explicit props, an attribute bag or slots; an include still suits a small
   partial that deliberately uses the current view's data. When an include would share variables
   implicitly, pass an explicit data array so the partial's dependencies are visible. Own guidance: an
   include that reads six variables from the surrounding view is a component that has not been declared.
4. **Give a nested component a parent's prop with the aware directive.** The directive lets a nested component
   read a prop that was explicitly passed to an ancestor. The source adds the limit: it does not expose the
   ancestor's default prop value unless that value was passed through the attribute bag. Own guidance: a
   nested component that needs a parent's default must receive it as its own prop; do not rely on the
   directive for defaults.
5. **A view composer is for data a named view always needs, and only views.** The source says to use a composer
   to centralise data that one or more named views need every time they render, to keep the composer
   compatible with every view it targets, and to avoid broad wildcards when views need different data shapes.
   It also says a composer runs when the framework renders the matching view and does not supply data to JSON,
   streamed or other non-view responses. Own guidance: data an API response needs belongs in a resource, not in
   a composer; and the view list of a composer is part of the review.
6. **Answer a partial request with a fragment.** A route can return a full view or a named fragment of it, for
   clients such as htmx or Turbo: the source's example returns the dashboard view with a conditional fragment
   method that picks the named fragment when the request carries the client's marker header (it uses the htmx
   one). Own guidance: the page keeps working for a request without the header, so test both answers.
