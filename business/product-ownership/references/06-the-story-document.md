# § 6 — The story document

> Section 6 of `business/product-ownership`. Read it when writing or modifying a story. Where an org
> catalogue defines the tracker fields, the presentation charter or the label taxonomy, **it wins** —
> this section is the generic form.

1. **A complete story has a fixed set of sections**, the same in every project so a reader knows where to
   look. Eight, and each answers a different question:
   1. **Title** — a verb plus the business objective, not a feature noun.
   2. **User story** — the need from the user's side, one sentence.
   3. **Context** — why this exists now, what problem it closes.
   4. **Functional scope** — split three ways: **included** (what this delivers), **excluded** (what it
      explicitly does not, so "but I thought..." never happens at review), and **dependencies** (other
      stories, services or data it needs).
   5. **Business rules** — the rules themselves, testable.
   6. **Acceptance criteria** — see section 4.
   7. **Edge cases and errors** — the empty, the invalid, the deleted parent, the missing permission.
   8. **Technical impacts to anticipate** — the functional and data consequences (what gets created,
      modified, synchronised, impacted downstream), the risks and sensitive points (side effects, personal
      data, performance), and the systems or modules touched, named plainly.
   The fixedness is the feature: a reader looking for the exclusions knows they are in the fourth
   section, so a story missing them is visibly missing them rather than merely unclear. A free-form story
   of the same quality cannot be checked at all.
2. **Each piece of information appears once, in the section that owns it.** Context restated in the rules and
   again in the criteria means a developer reads the same thing three times and still cannot tell which copy
   is authoritative. It gets worse on the second edit: one copy is updated, the others are not, and the
   story now contradicts itself with no way to tell which sentence is current.
3. **Describe what the user must be able to do, never the interface.** "Be able to add a session", not where
   the button sits, what the screen looks like, or the order of the blocks. A story that specifies layout takes
   the design decision away from the people qualified to make it (`business/interface-design`), and it dates
   the moment the mockup changes — after which the story is wrong in a way that makes the correct
   implementation look like a deviation.
4. **One presentation charter, applied uniformly.** Which mechanism renders it — panels, headings, a
   template — is the tracker's business, but every story looking the same is what makes a backlog scannable.
   The cost of variation is paid by every reader, every time: each differently shaped story has to be read
   from the top to find out where anything is.
5. **Labels are a taxonomy, not free text.** Never create a new label without explicit confirmation, and
   check for an existing one with near-identical spelling first: two labels for one concept splits every
   filter built on it, silently. Silently is the operative word — the filter still returns results, just
   not all of them, so the dashboard built on it is wrong in a way nobody can see.
6. **Before modifying someone else's story, check the assignee.** If it isn't the person asking, confirm
   explicitly — a rewritten story is someone else's work overwritten. It is also, frequently, a story
   already being implemented against, so the rewrite changes the target after the work started.
7. **Never rewrite a description wholesale to "improve" it**: embedded media (screenshots, recordings) is
   lost with the old body, and it's often the only reproduction evidence. Add a comment instead. The loss
   is not recoverable from the tracker's history in most tools, which is why this is stated as never
   rather than as a caution.
8. **One ticket per problem.** Two bugs in one ticket means one of them gets closed without being fixed —
   the ticket is closed when the first is done, and the second survives only in whoever's memory read the
   description. It also makes the delivery record wrong, which is what anyone estimating the next
   similar work will read.
9. **A small story is not a story with skipped sections.** A one-line bug fix does not need eight sections; a
   feature touching billing needs all eight. Judge which sections are critical *for this story* rather than
   applying the template as a checklist. The judgement is the work: a template applied mechanically
   produces eight headings and no content, which reads as complete and is not.
10. **Write the exclusions when you notice them, not at the end.** The moment somebody says "and of
    course it should also…" during discovery is the moment the exclusion is cheap and obvious; recovered
    a week later at review it is a negotiation. The excluded list is the section most often empty and
    the one that prevents the most rework.
11. **A dependency is named with its state, not just its name.** "Depends on the export API" is not
    actionable; "depends on story X, which is in review" and "needs the finance extract, which nobody has
    produced yet" are two different situations, and only one of them can be started around. An
    unstated dependency state is how a ready story blocks on day one.
12. **The story records the decision, not the discussion.** Alternatives considered and ruled out belong
    in an ADR (`skills/spec`), and the reasoning behind the priority belongs where §2.5 puts it. A story
    that carries the whole debate makes the reader reconstruct the conclusion, and different readers
    reconstruct different ones.
13. **A story that cannot be written without inventing something has found its own finding** (§7.4). The
    missing rule, the undefined status, the unnamed data source: writing a plausible version resolves the
    blockage and creates a requirement nobody decided. Leave the gap visible and ask (§7.5).
