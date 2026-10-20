# modal-drawer-dialog-ui-pitfalls §3 — Mobile, URL and tests

Own craft knowledge; platform behaviours are remembered, not re-checked (see origin.md).

## 3.1 Mobile and small screens
1. **Symptom: the footer buttons sit under the on-screen keyboard, or the dialog is taller than the viewport.** Fix: size to the visible viewport (dynamic viewport units, not the layout viewport), make the body scroll, keep the actions in a footer that stays visible, and scroll a focused field into view.
2. **Under a narrow width, use a full-screen sheet or a bottom sheet** instead of a centred box; keep a clear close at the top and the primary action reachable by thumb.
3. **A bottom sheet with a drag handle also has a button to close**; a swipe is never the only exit (`accessibility` §7 on modality).
4. **Overscroll and pull-to-refresh behind the sheet are disabled** while it is open; rubber-banding of the page under it is a bug.
5. **Safe areas**: keep actions out of the home indicator and notch zones (`safe-area` env values).
6. **Touch targets** of at least the size your accessibility rule sets (`accessibility` §1), with space between close and primary action.
7. **Hardware or gesture back closes the layer first** (§3.4), not the page.
8. **Test on a real device or emulator, with the keyboard open**, not only at a narrow desktop width.

## 3.2 Orientation and zoom
1. **Landscape on a phone leaves little height**; the dialog body must scroll, and the header must not take a third of it.
2. **Zoomed text (200 percent) must not clip or hide the actions**: no fixed heights on the dialog body (`accessibility` §3).
3. **Do not lock the viewport zoom** to make a dialog fit.

## 3.3 Media and reduced motion
1. **Animations are short and optional**: honour the reduced-motion preference by cutting slide and scale effects to a fade or nothing.
2. **A lightbox names the image and the position** ("photo 3 of 12"), keeps arrow keys for navigation and Escape for close, and returns focus to the thumbnail.
3. **Video or audio in a dialog stops on close**; autoplay with sound is never started by an open.

## 3.4 URL-addressable dialogs
1. **Symptom: a user shares the link to an open dialog and the recipient sees the bare page, or reloads and loses it, or presses back and leaves the site.**
2. **Put the dialog's identity in the URL** (a path or a query value that names the record and the mode) when it is a view people will link to: a record's details, an edit form, an image.
3. **Opening pushes a history entry; closing goes back to it**, so the back button closes the dialog and the URL returns to the page. Avoid pushing an entry on each internal step.
4. **Closing from the close button, Escape or the backdrop uses the same path** (go back when the entry was pushed by this open; replace the URL when the page was loaded directly on the dialog).
5. **A page loaded directly on the dialog URL renders the page behind it and the dialog on top**, or a standalone view when the background is unknown; either way focus goes into the dialog and a close goes somewhere sensible (the parent list).
6. **Permissions and missing records apply**: an unauthorised or deleted record shows the proper error, not an empty dialog (`security-hardening` §3).
7. **Never put secrets or typed form values in the URL**; keep draft state out of it.
8. **Unsaved-change guards apply to back and forward** as well (§2.3); handle the pop event, not only the buttons.
9. **Routers and server-rendered stacks have a pattern for this** (nested or parallel routes, modal routes, an out-of-band swap): use the framework's, and test reload on the dialog URL.

## 3.5 Server-rendered and progressive enhancement
1. **A dialog link without script should still reach a page**: the same URL renders a full view, and script upgrades it to a dialog.
2. **Fragments loaded into a dialog** must re-initialise focus and handlers after the swap (`htmx-protocol-pitfalls`).
3. **A failed fragment request shows an error inside the dialog**, not a blank box.

## 3.6 Tests
1. **Open and close by mouse, keyboard and Escape**; assert focus is inside on open and on the trigger on close.
2. **Assert the page behind is inert**: Tab never reaches it, and the accessibility tree hides it.
3. **Name test**: the dialog has an accessible name and, where relevant, a description.
4. **Dirty test**: type, attempt each exit, assert the confirm; clean form closes without one.
5. **Stack test**: open a popup inside a dialog, press Escape twice; the popup, then the dialog, close in that order and focus lands correctly each time.
6. **Scroll test**: lock and exact restore of the page position, no layout shift, two stacked dialogs unlock only after the last.
7. **URL test**: load the dialog URL directly, reload, press back and forward; an unknown record shows an error.
8. **Small-viewport test**: actions visible with the keyboard open, zoomed text, landscape.
9. **Accessibility checker on the open state** (`a11y-lint-wiring-pitfalls`).

## 3.7 Framework pointers
Facts to re-read in the version you use; none was checked here.
1. **The native dialog element** gives modal behaviour, a backdrop, Escape and an inert page; check browser support and how your styling and animation work with its top layer.
2. **Headless dialog libraries** for React and Vue handle trap, return and scroll lock; verify nested dialogs and a popup inside a dialog, the two usual gaps.
3. **Vuetify and similar kits** have dialog and navigation-drawer components; check the persistent and scrollable options, the return-focus and the stacking order before relying on defaults.
4. **Livewire, Inertia and htmx** have modal patterns and modal-route packages; check that reload and back work on the dialog URL.
