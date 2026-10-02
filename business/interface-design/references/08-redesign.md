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
