# § 1 — Tokens, not values

> Section 1 of `business/interface-design`. Read it when any spacing, size or type value is being chosen
> — while drawing, or while checking a mockup against the scale it claims to use.

Where a design system exists its tokens are the authority and nothing here overrides one. Where none
exists, the rule is "pick a scale and never leave it", which is the part that holds across projects.

1. **One spacing scale, and only its steps.** A value invented between two steps ("14 here, it looked
   better") is how a codebase ends up with forty spacings and no rhythm. If the scale is genuinely
   missing a step, that's a change to the scale — a decision, made once, for everyone. The mechanism is
   that a one-off value has no name, so the next person needing the same gap invents their own one-off
   next to it; what the reader sees six months later is a list of near-identical values in the stylesheet
   and no way to tell which of them were decisions.
2. **One grid step** that every spacing and size is a multiple of. Two documented exceptions exist in
   practice and are worth knowing rather than discovering: typography (line heights don't land on the
   grid) and fixed interactive component heights. Knowing the two exceptions up front is what stops the
   grid from being abandoned the first time it visibly fails: someone hits a line height that cannot be a
   multiple, concludes the grid doesn't work, and stops applying it anywhere.
3. **One type scale** for titles and one for body text, each level meaning a level — not a size picked
   for how it looked in this one card. A size chosen for appearance encodes no hierarchy, so the next
   screen reusing that card has a heading that outranks the page title, and the reader has to work out
   the structure from position rather than from size. Assistive technology reads the heading *level*, not
   the size, which is where the two diverge visibly (`skills/accessibility`).
4. **A fixed set of icon sizes**, chosen from the set rather than scaled freely. A freely scaled icon
   almost never lands on the pixel grid, so what the reader actually sees is a blurred glyph next to a
   crisp one, and the two are the same icon at two sizes nobody can name.
5. **Spacing expresses relatedness**: elements closer together read as belonging together. That's the
   actual function of the scale, and it's why a uniform gap everywhere reads as flat and unreadable. The
   consequence of the uniform gap is not ugliness, it is that grouping has to be inferred: a label and
   its field, and that field and the next label, sit at the same distance, so the form reads as a column
   of unrelated rows and the reader pairs them wrong at least once.
6. A floor on internal padding: content touching the edge of its container reads as broken, at every
   screen size. The case that produces it is a container whose padding was set for the widest layout and
   is then reused in a narrow one, so the failure shows up on the screen the designer looked at least.
7. **Two values from the scale can still be wrong together.** The scale removes arbitrary numbers; it
   does not decide relative order, and a gap *inside* a group that is larger than the gap *between*
   groups is on-scale and still reads as the wrong grouping. This is the one check the scale cannot do
   for you, which makes it worth doing explicitly on any screen with more than one group.
8. **A token is a name, and the name is the part that has to survive.** A value referenced by what it is
   for can be changed once for every place that means the same thing; the same value hard-coded in twelve
   places is twelve edits, and the reader who finds eleven of them ships a screen that is subtly out of
   step. This is why "take it from the scale" and "use the token" are the same rule, and why copying the
   number the token resolves to defeats it entirely while looking identical in the mockup.
9. **Never carry a value across projects.** Every number in a real design system is arbitrary and owned:
   its spacing scale, its type scale, its button heights, its icon sizes. A step remembered from the last
   project is a number with no owner in this one — it will disagree with the local scale by a few units,
   which is exactly the amount that looks like a mistake rather than a choice (rule C: nothing named, no
   house values).
10. **When no scale exists yet, choosing one is the deliverable, not a side effect.** Write down the
    grid step, the spacing steps, the two type scales and the icon set once, before the second screen
    exists, and put them where the implementer will read them. A scale that lives only in the mockup's
    geometry has to be reverse-engineered by measuring rectangles, and the measurement is where the
    forty spacings come from.
