# § 8 - Redesigning an existing interface

> Section 8 of `business/interface-design`. Read it when the screen or product already exists and is being
> improved, restyled or rebuilt, before touching it.

1. **Detect the mode first: keep or redo.** Ask which. "Improve" and "start over" call for different
   amounts of change, and guessing wrong either wastes the existing work or ignores it.
2. **Audit before touching.** Read the code and the live screens. Record the brand tokens already in use
   (colour, type, spacing, radius), the structure, and what each element does. Sort every element into
   "works" (the reader uses it, it carries information) or "filler" (decoration, repetition).
3. **Preservation rules.** What the product's users or other systems rely on survives unless the owner
   says otherwise. Keep the stack and its styling method; improve inside them. A restyle is not a
   rewrite.
4. **Levers, ordered by risk, lowest first:** typography; spacing and rhythm; colour; motion;
   recomposition of the layout. Stop at the first lever that reaches the goal.
5. **Targeted evolution or full redo.**
   - Few findings, a coherent system already present: evolve, one lever at a time.
   - Findings across tokens, structure and content, or a system that never existed: redo, but still keep
     the list in point 6.
   - A redo is proposed with its list of what changes and what stays, never started silently.
6. **Never change silently:** URL slugs, navigation labels, form field names, the logo, legal text,
   analytics events and the identifiers their tracking depends on. If one must change, name it, say why,
   and ask.
7. **Show the difference.** Report each change against the audit finding it answers; a change with no
   finding behind it is taste, and goes back to the owner (§0.4).
8. **Score the existing design before deciding.** For an honest keep, refine or redo verdict, rate the
   current interface on ten questions, 0 to 3 each, and attach evidence to every score: a file and line,
   or a screen and element. The questions come from a public body of design principles, restated: does it
   do something new where novelty helps (innovation), is it useful, is it well made to look at
   (aesthetics), is it understandable without instruction, is it unobtrusive and leaves room for the
   person's own work, is it honest about what the product does, will it still hold up in years rather than
   weeks, is it right down to the last detail, is it frugal with attention and resources, and does it use
   as little design as the job needs.
   - 0 = absent or harmful, 1 = weak, 2 = sound, 3 = exemplary.
   - **A score without cited evidence is not given**; write "not assessed". Impressions are not evidence.
   - Verdict: **keep** when no question scores under 2; **refine** when a few score 1 and the structure
     holds, listing each with its fix (point 5, targeted evolution); **redo** when usefulness,
     understandability or honesty score 0 or 1, or when scores of 1 are spread across most questions
     (point 5, full redo, with the list of point 6).
   The grid is a way to keep an argument about taste honest, not a number to report as quality. The verdict
   goes to the owner with the evidence (§0.4).
9. **Strategic omissions on a site or app being rebuilt.** Before calling the restyle done, check the
   things users and search engines rely on that a visual pass tends to drop: a real not-found page, a skip
   link and visible focus, form validation and its messages, the cookie or consent surface where required
   (`business/data-protection`), the redirects for every URL that changed (`skills/seo`), print and
   reduced-motion behaviour, and the social preview image. Each missing item is a finding under §0.13.
