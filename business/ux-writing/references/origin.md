# ux-writing — origin and source stamps

> Provenance of `business/ux-writing`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Assembled from public sources: established interface-writing guidance (errors stating cause and next
action, buttons naming the outcome, useful empty states) as published in the major design systems'
content guidelines. Written **without internal UX-writing expertise** and without access to a company
tone-of-voice reference, so it deliberately stops at the mechanical cases where wording causes a
measurable failure and leaves voice to whoever owns it. The consistency link to `domain-modeling`, the
concatenation rule and the "empty vs no-match vs failed-to-load" distinction are ours.

A dedup audit on 2026-08-06 established the boundary with an org design catalogue's own UX-writing
skill: that skill owns the wording rules at design time, inside a mockup, and this block is the
code-time pass on text that reaches a diff without passing through one.

**Sectioned and deepened 2026-09-08.** The five inline sections moved to one file each under
`references/` and the router became a table of triggers. No section was added: the five already covered
the subject. Every section and point number was preserved — `business/release-communication` §2 cites
§4.1 by number — and the guardrails now cite the points they enforce instead of restating them.

**What the depth adds.** The original stated each rule and, in most cases, one clause of justification;
what it did not have is the failure the rule prevents, stated as something the reader does. That matters
here because interface text has no test: a wrong string ships green, and the only evidence it was wrong
is a behaviour — a retype, a second click, a support ticket, an escalation. The additions that were real
absences rather than elaborations:

- **§1**: that a validation message has to name the *rule* rather than the verdict, since "too weak"
  cannot be satisfied without guessing and a requirement appearing only on failure is one the reader had
  to fail to learn; that the message is the only thing that can say what happened to the reader's work
  after a failed save, and silence on that is read as loss; that "you cannot" and "it did not work" are
  not interchangeable, because one of them is retryable; that one cause must produce one message, or the
  reader starts fixing things that were never wrong; and that the catch-all fallback is a string written
  on purpose, with a reference the reader can quote, rather than the framework's default.
- **§2**: that a button's label is what a screen reader announces out of context and what a
  voice-control user has to speak, so a label depending on the surrounding text is unusable in both;
  that the count in a destructive confirmation is the one part a reader can check against what they
  meant to select; that a label is not a hint and a placeholder-as-label disappears the moment the
  reader types; that two controls on one screen never share a label, because twelve "Edit" entries are
  distinguishable only by position; that a label the interface then contradicts costs trust in every
  honest label on the screen; and that a label has to survive being longer after translation.
- **§3**: that a zero is a measurement and not an empty state, so presenting "nothing to measure yet"
  as 0 puts a false datapoint into a decision; that a permission-empty list is a third case, where "add
  your first item" is an instruction the reader cannot follow; that sample content in an empty screen is
  read as real and gets reconciled against; that the empty state's text is the part which reaches
  production untouched, because the developer's fixture data is never empty; and that the same string is
  read by someone who just deleted their last item, so a first-visit-only wording reads as the product
  having forgotten them.
- **§4**: that the form of address propagates into every verb form, so one string written the other way
  cannot be fixed by changing one word; that the existing product is the reference and a better-written
  divergent string costs more than it gains; that the voice extends into transactional email, exports
  and generated documents, which are the strings written furthest from any review; that two words for
  one concept split the codebase's search and the support team's as well as the reader's; and that a
  half-translated screen fails *silently*, since a missing key renders as its source text.
- **§5**: that a plural is not a conditional, because several languages have more than two forms and at
  least one has none; that a key names the string's role rather than its text, or it stops matching what
  it holds at the first rewording; that markup inside a translated string is both a translator hazard
  and a rendering path that will eventually carry user input; that an unnamed interpolated value reaches
  a translator as a guess; that length is part of the string's contract and belongs in the key's
  comment where a hard limit exists; and that a hardcoded user-visible string bypasses the translation
  file, the review and the search at once, which is the most common way consistency breaks after it was
  established.

Router plus sections: 1,005 → 4,217.

**Status.** Unchanged. There is still no internal UX-writing expertise and no tone-of-voice reference
behind this block, and the depth does not change that — it makes the mechanical cases arguable, which is
what a developer needs in order to defend a string in review, and leaves voice where it belongs.
