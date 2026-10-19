# § 10 - Data screens and multi-step flows

> Section 10 of `business/interface-design`. Read it when the screen is a dashboard, a table, a filtered
> list or a wizard. §3 gives the states these screens need; this section gives the decisions that make the
> content worth displaying. §7.8 states the principle; this is the working detail.

## Dashboards and summary screens

1. **Name the decision before drawing a widget.** "What will the person do differently after reading this?"
   Each tile, chart and table is placed to answer one named question. A tile without a question is
   removed, not restyled.
2. **A figure carries its meaning with it.** Every number shows what it counts, over which period, against
   what comparison, and where it comes from (§3.12). A bare figure invites the reader to supply the
   comparison, and they supply the wrong one.
3. **A chart is chosen by its question.** Comparing categories, showing change over time, showing parts of
   a whole and showing a relation are different questions with different forms; choose the form from the
   question, not from what looks rich. A form that cannot be read without a legend lookup is a poor fit.
   For colour use in charts and labelled axes, use the project's charting rules where they exist.
4. **An alarm has an owner and an action.** An alert tile that turns red tells the reader something is
   wrong; it must also say what, since when, and what the next step is (§3.6). Otherwise it becomes
   wallpaper.
5. **Order by importance of the decision, not by data source.** The tile the reader needs first sits first;
   the order of the database tables is not an information architecture.

## Tables and lists

6. **A column earns its width.** Each column answers something a reader of this table needs. Identifier
   columns the reader never uses, repeated columns and columns identical in every row are removed or moved
   to a detail view.
7. **Alignment follows content.** Text left-aligned, numbers right-aligned in equal-width figures so
   digits line up, and the header aligned with its column. Mixed alignment forces the eye to guess where
   a value starts (`01-tokens.md` §1.14).
8. **Sorting and filtering state is visible.** The active sort shows its column and direction. Every
   applied filter is shown as a removable item near the results, with a count of results, and a single
   action clears them all. A filter that narrows silently produces the empty state that looks like lost
   data (§3.5).
9. **The state of a list is addressable.** A filtered, sorted, paged view is something a colleague pastes
   in a message; the state therefore lives in the address, not only in memory (§2.4).
10. **Row actions are named by the row.** An action repeated on every row must be distinguishable by name
    for keyboard and screen-reader users (`business/ux-writing` §2.8). Destructive row actions follow §2.6.
11. **Selection is explicit.** If rows can be selected, the screen states how many are selected and what
    the bulk actions will apply to, including rows on other pages. A bulk action whose scope is unclear is
    a bulk accident.
12. **A table on a narrow screen is a decision, not a squeeze.** Either the table scrolls inside its own
    region with the key column pinned, or each row reshapes into a stacked item that keeps the same
    information. Shrinking the text until the columns fit is neither (`skills/responsive-layout`).

## Multi-step flows (wizards, onboarding, checkout)

13. **One decision per step.** A step asks one thing, or a small group of related things. A step that asks
    five unrelated questions is a page with a "next" button.
14. **Show position and what is left.** The person knows which step this is and roughly how many remain;
    steps are named by what they do (§7.7), not "Step 2".
15. **Going back loses nothing.** Answers survive a return to an earlier step and a reload where the data
    is not sensitive. A flow that discards input on "back" teaches people to avoid it.
16. **Show a summary before the irreversible step.** The final step lists what will happen and what it
    costs, with edit links back to the step that holds each item. The confirm button states the outcome
    (`business/ux-writing` §2.1).
17. **Skippable means skippable.** An optional step has a visible way past it; a step that cannot be
    skipped says why.
18. **Errors are met where they happen.** Validate at the step, say what to fix (`business/ux-writing`
    §1), and never reveal at the last step a problem that belonged to the first. Mark the
    recoverable state of a long flow (saved draft, resume link) in the design.
19. **The flow has an exit.** A way to leave that says whether progress is kept. Abandonment is a normal
    path, and it needs a state like any other (§3).
