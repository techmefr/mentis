# § 2 — Which container

> Section 2 of `business/interface-design`. Read it when deciding where something lives — a toast, a
> modal, a drawer, a bottom sheet or a page — before it is drawn.

A decision tree, because this is the choice most often made by habit:

1. **Transient feedback, nothing to decide** → a toast/snackbar. It disappears, so nothing important can
   live only there. What the reader sees when this is broken is nothing at all: the toast expired while
   they were looking elsewhere, or a screen reader announced it and moved on, and the reference number
   or the error detail is now unrecoverable. If it has to be readable a minute later, it belongs
   somewhere that persists.
2. **A short blocking action or a confirmation** → a modal/dialog. Blocking is the point; anything the
   user needs to compare against the page behind it doesn't belong here. The observable failure is the
   user dismissing the modal to read the value it was asking about, and losing what they had typed.
3. **Contextual work alongside the page**, where the context must stay visible → a side panel/drawer,
   which becomes a bottom sheet on a small screen. The test is whether the task requires reading the
   page: a panel that covers what it is about is a modal that costs more to build.
4. **A full task, or anything deep-linkable, shareable, or reloadable** → a page. If a user could
   plausibly want to bookmark it or press back, it's a page, and putting it in a modal removes both. The
   consequences are concrete and each of them arrives as a support request: the link a colleague pastes
   opens the list instead of the item, a refresh loses the state, and the back button leaves the app
   rather than closing the layer.
5. **On a small screen, a modal and a bottom sheet look alike and are not interchangeable.** The modal
   interrupts for a blocking action; the bottom sheet is the mobile form of the drawer and shows
   non-blocking context. Choose by **role**, never by appearance — this is the most common wrong pick on
   mobile. The two differ in what dismissing them means: a sheet swiped away has been read, a modal
   dismissed has been refused, and a flow that treats one as the other either loses an answer or asks
   again.
6. A destructive confirmation is never a toast, and a long form is never a modal. The first is
   irreversible action behind a component designed to be missed; the second is a form whose validation
   errors have nowhere to go, on a screen the keyboard covers on mobile.
7. **A container carries a scroll contract, and that is the part that breaks late.** A page scrolls; a
   modal that scrolls hides its own action row; nested scrolling inside a sheet inside a page is
   ambiguous to touch and to a keyboard. So the amount of content is part of the container decision, not
   a detail to be handled afterwards, and "it grew" is the usual reason a modal became wrong without
   anyone changing the decision.
8. **A layer over a layer is a design error, not a technical one.** A modal opening a modal, or a
   confirmation opening over a drawer, leaves no unambiguous meaning for dismiss and no unambiguous
   place for focus to return to. Where the second step genuinely exists, the shape is one container that
   changes step, not two stacked containers.
9. **A container decides where focus lives and what happens when it closes**, which the mockup has to
   say because nothing in the drawing shows it. A blocking layer takes focus and traps it; on close,
   focus returns to what opened it. Left unstated, the implementation leaves focus on the page behind, so
   the next keyboard action goes somewhere invisible and a screen-reader user is returned to the top of
   the document (`skills/accessibility`).
10. **The choice is reversible on paper and expensive in code.** A modal changed to a page after
    implementation means routing, state ownership, back-button behaviour and validation placement all
    move. That asymmetry is the reason this decision is made in this block, in a mockup or in a
    conversation, rather than being left to the person building it — for whom the cheapest option is
    always whichever container the surrounding code already uses.
