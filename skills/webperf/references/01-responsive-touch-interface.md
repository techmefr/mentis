# webperf — responsive, touch and interface rules

> Reference of `skills/webperf`. Read it when a page has to work on a phone browser, a touch screen or a dark theme, or when an animation, an image or a long text block is added. Framework-neutral: it holds in Vue, React or plain HTML. Mobile here means the responsive web; a native app has its own rules.

## 1. Animation and motion

1. **Honour `prefers-reduced-motion`.** Parallax, large slides and auto-scrolling are vestibular triggers for some
   readers, and the media query is one block. Provide a reduced variant (a fade, or nothing), not just a shorter
   duration. A muted decorative video loop stops under the same query.
2. **Animate `transform` and `opacity` only.** Width, height, top and margin force layout on every frame and run
   on the main thread, so the animation stutters exactly when the page is busy. Transform and opacity run on the
   compositor.
3. **Never `transition: all`.** It animates properties added later by someone else (a colour on hover, a width
   from a media query), and it forces the browser to watch every property. List the properties.
4. **Set the `transform-origin` on purpose.** The default centre is right for a spinner and wrong for a dropdown
   that should grow from its trigger; the wrong origin reads as a bug to the eye without being identifiable.
5. **An animation stays interruptible.** If a second click arrives mid-animation, the element follows the new
   target from where it is rather than finishing the first one. Locking input until the animation ends turns a
   200 ms effect into a 200 ms freeze on a fast user.
6. **Anything that moves for more than five seconds beside content needs a way to pause, stop or hide it.** A
   carousel that auto-advances is the common case; the control is a requirement, not an extra.

## 2. Touch and pointer

1. **`touch-action: manipulation` on controls.** It removes the double-tap-to-zoom wait that older mobile
   browsers add before a tap fires, so a button responds immediately; pinch zoom is untouched.
2. **A touch target is large enough to hit.** At least 24 by 24 CSS pixels is the WCAG 2.2 minimum
   (`skills/accessibility` §3); 44 by 44 is the comfortable target on a phone. Extend the hit area with padding
   rather than enlarging the icon.
3. **`overscroll-behavior: contain` in modals, drawers and sheets.** Without it, scrolling to the end of the
   sheet continues scrolling the page behind it, which looks like the overlay is not modal.
4. **Set `-webkit-tap-highlight-color` deliberately.** The default grey flash on iOS and Android is either part
   of the design or it is transparent with a visible `:active` state in its place; leaving it to chance gives
   two looks across devices.
5. **A drag, swipe or pinch has a tap and a keyboard alternative** unless the gesture itself is the point.
   During a drag, disable text selection and mark the dragged element `inert`, or the selection fights the
   gesture.
6. **`autofocus` sparingly.** On a phone it opens the keyboard over the content the user came to read, and it
   scrolls the page to the field. Keep it for one primary input on a desktop-first screen.
7. **Hover is a bonus, never the only affordance.** A touch device has no hover: anything revealed on hover
   (a menu, a tooltip, a delete button) needs a tap or focus path as well.

## 3. Safe areas, viewport and layout

1. **Full-bleed layouts respect `env(safe-area-inset-*)`.** A fixed bottom bar placed at `bottom: 0` sits under
   the home indicator on a notched phone; padding it with the inset keeps it tappable. It requires
   `viewport-fit=cover` in the viewport meta to take effect.
2. **Never disable zoom** (`user-scalable=no`, `maximum-scale=1`). A layout that breaks at 200% is the defect;
   zoom is how a large share of users read at all.
3. **Use `dvh`, not `vh`, for full-height sections on mobile.** `100vh` includes the area behind the browser
   toolbar, so the bottom of the section is cut off until the toolbar hides.
4. **Flex or grid over JavaScript measurement.** A measured layout runs after paint and shifts the page;
   `min-width: 0` on a flex child is what lets a long text truncate instead of overflowing.
5. **Avoid horizontal scroll by finding the overflowing element, not by `overflow-x: hidden` on the body.**
   Hiding it removes the symptom and also breaks `position: sticky` in some browsers; the fix is the element
   that is wider than the viewport.
6. **Test with the on-screen keyboard open.** A fixed footer or a modal taller than the remaining space hides
   the field being typed in on a phone; this is the screen the desktop test never shows.
7. **A sticky header, footer or overlay must not cover the focused element.** Set `scroll-padding-top` on the
   scroll container and `scroll-margin-top` on heading anchors so keyboard focus and anchor links land in view.

## 4. Typography and content

1. **`font-variant-numeric: tabular-nums` for numbers that are compared or that change** (prices, counters,
   tables, timers). Proportional digits make a ticking counter jitter and a column of amounts misalign.
2. **`text-wrap: balance` (or `pretty`) on headings.** It avoids a single orphan word on the last line, which
   is the most visible typographic defect on a narrow phone.
3. **A text container handles long content.** `truncate`, `line-clamp-*` or `overflow-wrap: anywhere`, and
   `min-width: 0` on a flex child. Test with a short, an average and a very long user-generated value, plus the
   empty string: the empty state is a design, not a blank box.
4. **Use the typographic characters.** `…` not `...`, curly quotes, a non-breaking space between a number and
   its unit (`10&nbsp;MB`) and inside a keyboard shortcut, so the unit never wraps onto its own line.
5. **Dates, numbers and currencies go through `Intl`**, never a hardcoded format string: the formatted width
   differs per locale, and a column sized for one locale's date overflows in another's.
6. **Brand names, code tokens and identifiers take `translate="no"`**, so a browser translator does not turn a
   product name into a common noun.

## 5. Images, video and fonts

1. **Every `<img>` has explicit `width` and `height`** (or an `aspect-ratio`): without them the browser cannot
   reserve space and the page jumps when the image arrives, which is the layout shift Core Web Vitals counts.
2. **Below-the-fold images `loading="lazy"`; the one above-the-fold hero image `fetchpriority="high"`** and never
   lazy. Lazy-loading the largest visible image delays the very metric it was meant to protect.
3. **Serve a size and a format suited to the display.** `srcset` and `sizes` (or the framework's image
   component), modern formats with a fallback; a 3000-pixel photograph displayed at 320 wastes the connection
   of exactly the device that has the least of it.
4. **A short animation is a video, not a GIF.** `<video autoplay muted loop playsinline>` is a fraction of the
   weight, and `playsinline` is what stops iOS from forcing fullscreen. Keep a still poster for
   `prefers-reduced-motion`.
5. **Preload the one font that gates first paint**, with `font-display: swap` and `crossorigin`; every other
   font loads without a hint. A preload for each weight competes with the content it is meant to speed up.

## 6. Dark mode and theming

1. **`color-scheme: dark` on `<html>` for a dark theme** (or `light dark` when it follows the system): it makes
   the browser's own controls, scrollbars and form fields match instead of staying light inside a dark page.
2. **`<meta name="theme-color">` matches the page background**, so the mobile browser chrome blends with the
   page; give it one value per scheme with the `media` attribute.
3. **A native `<select>` gets an explicit `background-color` and `color`**, because on Windows dark mode its
   list popup otherwise renders dark text on a dark background.
4. **A hover, active or focus state has more contrast than the resting state**, not less; a hover that dims the
   control reads as disabled.

## 7. Navigation and state

1. **URL reflects state.** Filters, tabs, pagination, an opened panel and the sort order belong in the query
   string, so a reload, a back button and a shared link all land on the same view. If a piece of UI has
   `useState`/`ref` and a user would want to send it to a colleague, it should be in the URL.
2. **A link is an anchor.** Navigation through a click handler on a `div` or `button` breaks Cmd/Ctrl-click,
   middle-click and "copy link address", and is invisible to crawlers and screen readers.
3. **A destructive action asks first or can be undone.** A confirmation dialog or an undo toast; an immediate,
   irreversible delete on a control sitting beside a harmless one is how a mis-tap becomes data loss.
4. **Warn before leaving a form with unsaved changes** (`beforeunload` or the router's navigation guard), and
   only while the form is actually dirty.

## 8. Forms on a phone

1. **The right `type`, `inputmode` and `autocomplete`.** `type="email"`, `inputmode="numeric"` for a code,
   `autocomplete="one-time-code"` or `"postal-code"`: the phone then opens the matching keyboard and fills from
   the device. A free-text field for a phone number makes the user switch keyboards.
2. **`spellcheck="false"` on emails, codes and usernames**, and no autocapitalisation on them
   (`autocapitalize="off"`), or the keyboard "corrects" what the user typed correctly.
3. **Errors appear next to the field and focus moves to the first one on submit**; the submit button stays
   enabled until the request starts and shows a spinner while it runs. A button disabled until the form is valid
   gives no reason why it is disabled.
4. **A placeholder is an example, not a label** (`skills/accessibility` §4), ending in `…` when it shows a
   pattern.
