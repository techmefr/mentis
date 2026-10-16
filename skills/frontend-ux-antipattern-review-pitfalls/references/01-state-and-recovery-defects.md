# frontend-ux-antipattern-review-pitfalls §1 — State and recovery defects

Categories are read as questions about state and recovery. Each item names the pattern, what to look for and
the usual fix. Responsive, touch and keyboard topics are in `webperf` and `accessibility`.

## 1.1 The axioms behind every finding
1. **Acknowledge every action**: visible feedback within about 100 ms, even when the result takes seconds
   (the source's figure).
2. **Never destroy user input**: not on error, navigation, timeout or refresh.
3. **State survives the unexpected**: refresh, double submit, network loss.
4. **The most recent intent wins**: a stale response never overwrites a newer action.
5. **Explain every constraint**: if disabled, say why; if failed, say how to fix it; if it succeeded, say
   what happened.
6. **Do not fight the platform**: browser conventions, native controls and OS gestures encode a lot of
   settled practice.

## 1.2 Layout stability
1. **Content injected after first paint displaces interactive elements** (images without dimensions,
   late banners, lazy components). Reserve the space: explicit size, aspect ratio, skeleton or minimum
   height.
2. **An element that changes size on hover or focus moves out from under the pointer.** Look for hover or
   focus rules that change padding, margin, font size, width, height or border width. Declare the property on
   the base state (a transparent border) or use a property with no layout effect such as transform, outline
   or box shadow. Put a spinner on or inside a button, not next to it.

## 1.3 Feedback
1. **A primary action with no pending state** (no loading, disabled or pressed state) looks ignored.
2. **An optimistic update that fails must say so.** Look for an update with no rollback handler, or a rollback
   that does not notify. Show what happened and offer a retry.
3. **A long operation needs progress**: the source's threshold is about 5 seconds. Give a determinate
   indicator (percentage, step N of M, bytes) or, if that is impossible, a status message that changes, so the
   user can tell it has not frozen.

## 1.4 Errors and recovery
1. **An error says what failed in user terms, why if known, and what to do.** Raw status codes, exception names
   and "something went wrong" fail this. Look for an error view with nothing to act on.
2. **A disabled control explains the precondition**, or stays enabled and explains on interaction.
3. **Contain errors**: one failed widget or call must not lock the page. Look for the absence of per-section
   boundaries; show an inline error with a retry in the broken region.

## 1.5 Forms and input
1. **Paste is never blocked**, including for passwords, codes and confirmation fields; validate instead.
2. **Required fields are marked before the user interacts**, with a visible mark and the matching attribute,
   not only after a failed submit.
3. **Input hints match the data**: type, input mode, autocomplete, autocorrect and autocapitalize. A one-time
   code field with no hints invites mangled input.
4. **A formatter that rewrites the value on each keystroke must keep the caret position**; otherwise editing
   mid-string breaks. Prefer a masking library that handles it, or format on blur.
5. **A custom input keeps standard editing**: select all, arrow keys, delete, clipboard, undo. Look for
   key handlers that prevent the default without re-implementing it.
6. **A multi-step form survives going back**: look for steps that unmount their state, wizard state held only
   in local component state, and no guard before navigation that discards progress. Persist to session
   storage, the URL or a store, and warn before discarding.

## 1.6 Focus stealing
1. **Do not move focus while the user is interacting elsewhere.** Look for a focus call or an autofocus that
   fires after load from an async event, timer or state change, a live search that re-renders and grabs
   focus, and a focus trap that activates under a user who is typing.
2. **The safe moments**: initial load of a page or dialog, or a direct response to the user's own action.
   `autofocus` on touch devices is in `webperf`.

## 1.7 Notifications and dialogs
1. **Deduplicate and batch notifications.** Look for a toast fired per event in a burst; throttle and show a
   count instead, and offer a mute option.
2. **Floating widgets must not cover content**: give them a minimise control and a position that avoids the
   content, especially on small screens.
3. **A modal closes by the usual means**: a visible close button, the Escape key and a click outside. The
   source allows an exception for a critical confirmation of a destructive action, which then still needs a
   visible, obvious close control.
4. **A destructive action needs a safety net**: a confirmation that names the consequence, or an undo window
   such as a soft delete. For account deletion or bulk removal the source asks for both. Look for send,
   publish and overwrite as well as delete.

## 1.8 Navigation and state in the URL
1. **A redirect for sign-in keeps the original target.** Look for a login flow with no return address and a
   fixed landing page after authentication.
2. **State a user would share, bookmark or recover on refresh lives in the URL**: search, filters, sort,
   pagination. Look for these held only in component state or a store.

## 1.9 Scroll
1. **Scroll position and loaded data are restored on back-navigation.** Look for infinite scroll with no
   caching, or list to detail and back landing at the top; classic pagination is an alternative.
2. **Fixed and sticky elements stack up.** A fixed header, sticky navigation, cookie banner, notification bar
   and chat widget together can leave a fraction of the screen for content. The source's rough limits are
   15 to 20 percent of the viewport on mobile and about 10 percent on desktop; treat those as the source's
   heuristic. Hide on scroll down, merge bars, and let banners be dismissed and stay dismissed.
3. **In-app swipe gestures can conflict with the browser or system ones**: pull to refresh, edge swipe, a
   carousel inside a scrolling page. Contain overscroll, keep targets away from the screen edge and use
   direction and speed thresholds. The overscroll rule for modals is also in `webperf`.

## 1.10 Timing and races
1. **Duplicate submission**: disable the control on first activation and re-enable on completion or error,
   and also give critical operations server-side idempotency, for example idempotency keys. The source says
   client guards alone are insufficient.
2. **A stale response must not overwrite a newer intent**: typing "appl" then "apple" and the slower first
   answer arriving last. Look for async work from user input with no abort, sequence number or check that the
   result still matches the current input.
3. **Session expiry mid-task**: look for a hard redirect to sign-in that loses in-progress work, or a failed
   call with a bare error. The source's four steps: warn before expiry, try a silent refresh, save the work
   before redirecting, restore it and return the user afterwards.

## 1.11 Layering
1. **Define a z-index scale of named layers** (dropdown, sticky, overlay, modal, toast) instead of escalating
   numbers; the source lists 999 and 9999 as the smell.
2. **Overlays that must escape clipping render through a portal or teleport** to the document root or an
   overlay container, because a parent with hidden or auto overflow clips them.

## 1.12 Cumulative decay
1. **An update must not reset preferences.** Look for initialisation that writes defaults over saved
   settings; merge defaults with what is saved, and if an option is retired, tell the user.
2. **Bound every cache.** Look for local storage, IndexedDB or cache usage with no expiry, size cap or
   eviction.
3. **Remove flags and experiments when they conclude.** A flag enabled or disabled for everyone for a long
   time is debt and leaves users on inconsistent UI.

## 1.13 Review discipline
1. **Do not flag style preferences.** Only patterns that harm the user under the axioms count.
2. **Check context first.** A disabled button inside a wizard may be explained by the wizard's own text.
3. **Do not report handled cases.** An existing abort controller, error boundary or framework loading state
   may already cover the pattern; read the implementation, and know what the framework does.
4. **Check the fix against the platform**: a visual cue that removes keyboard access trades one violation for
   another.
5. **Report grouped by pattern with a place in the code**, each with the harm and a fix, and say plainly when
   nothing was found (source workflow).
