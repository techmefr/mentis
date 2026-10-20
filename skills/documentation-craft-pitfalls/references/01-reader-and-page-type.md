# documentation-craft-pitfalls §1 — Reader and page type

> Part 1 of `skills/documentation-craft-pitfalls`. Read it when a page is planned or a page does two jobs.
> Source, read 2026-10-20: Microsoft Writing Style Guide, "Content planning" and "Reference documentation"
> (CC BY 4.0). Sentences marked "own guidance" are ours.

1. **Start from the reader and the task they arrive with.** The guide's planning questions begin with who the
   audience is and what they want to accomplish, and add that few readers come to see what is new. Symptom: a
   README that opens with the project's history while the reader wants the install command. Check: write the
   reader and their task in one sentence before the first heading; if it needs "and", there are two pages.
2. **Name the business reason as well, and rank it second.** The guide notes every piece has a reason of its
   own beside the reader's. Own guidance: write it in the brief so the page does not drift into promotion, and
   let the reader's task win every conflict.
3. **Pick the page type from what the reader will do with it.** Own guidance, from the craft rather than one
   source: someone learning by doing needs a guided walk with a visible result; someone with a goal needs ordered
   steps and nothing else; someone checking a fact needs a complete, predictable lookup; someone building a
   mental model needs an explanation with the why. Symptom: steps interrupted by three paragraphs of background,
   or a lookup page with a story in the middle. Fix: move the aside to its own page and link it.
4. **Keep one purpose per page and link to the rest.** Own guidance: mixed pages fail every reader a little, and
   cannot be kept true because a code change touches half of them. A link costs one line; a merged page costs
   every future edit.
5. **Give lookup pages one fixed layout.** The guide says consistency is essential in reference documentation:
   a standard design, predictable headings and consistent wording let readers find the detail fast. Its typical
   entry holds a title and short description, the signature, each parameter, the return value, remarks, an
   example, requirements and links to related items. Own guidance: pick the layout once per kind of item and
   reuse it, because a reader who finds one entry learns how to find all.
6. **Describe parameters and values, do not repeat their names.** The guide warns against descriptions that echo
   the name or the type. Symptom: "`timeout`: the timeout". Fix: say the unit, the default, what happens at the
   limit and what is invalid.
7. **Review generated reference text before publishing it.** The guide advises reviewing text generated from
   source comments and removing internal details. Symptom: a published page that explains a private helper.
   Check: read the generated page as the reader, not the file as the author.
8. **Plan for how it will be found and translated.** The guide asks how the reader will find the page, on what
   device, and whether it will be localised. Own guidance: a descriptive title and first sentence are the page's
   search entry; short, literal sentences survive translation.
9. **Decide the success check up front.** The guide asks how success will be measured. Own guidance: for an
   internal page the cheapest honest measure is the question it should stop; note that question in the brief and
   look for it in the support channel later.
