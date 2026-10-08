# android-edge-to-edge-insets §3 — The keyboard

The Android developer pages "Set up edge-to-edge", "Set up window insets", "Use keyboard IME animations" and "About
WindowInsetsRulers" (all last updated 2026-10-01), read in full as page text on 2026-10-08, and one Apache-2.0
Android agent skill for the ordering and scaffold rules. The pages say IME insets animate, backported to API 21.

## 3.1 Receiving the keyboard insets
1. **Declare `adjustResize` in the manifest** for the Activity (§1.2); the page says it lets the app receive the IME
   insets and pad its layout when the keyboard appears or disappears.
2. **Pad with `imePadding()` on the container that must move,** or place it with a ruler (§3.4). `imePadding()`
   consumes the part of the insets it applies, so a nested inset modifier applies only what is left.
3. **Test with the keyboard up on the last field of the screen.** A preview does not show it.
4. **For a list that should open and close the keyboard while scrolling,** the page's example combines `imePadding()` and
   `imeNestedScroll()` on the list (the nested-scroll modifier is marked experimental in the sample).

## 3.2 Order and double application
1. **IME insets are applied twice when the same insets reach the content by two routes without consumption.** The
   skill's wrong examples: a parent that pads with `WindowInsets.safeDrawing.asPaddingValues()` (not consumed) and a child
   with `imePadding()`; and a scaffold given `contentWindowInsets = WindowInsets.safeDrawing` whose content uses
   `padding(innerPadding)` and then `imePadding()`. Its right examples: a parent using `safeDrawingPadding()` or
   `windowInsetsPadding(...)` (which consume) with a child `imePadding()`, and `consumeWindowInsets(innerPadding)`
   after the scaffold padding.
2. **Put `imePadding()` before `verticalScroll()` in the chain** (the skill's rule), so the padding shrinks the
   viewport the scroll container works in.
3. **For a list with a text field at the end,** use the trailing spacer described in §2.4 point 2.

## 3.3 Scaffolds
1. **Scaffold's default `contentWindowInsets` does not include the IME** (the skill), so a screen with a text field in a
   default scaffold needs `imePadding()` (after `padding(innerPadding)` and `consumeWindowInsets(innerPadding)`) or a ruler.
2. **With `contentWindowInsets = WindowInsets.safeDrawing`,** `innerPadding` already carries the IME insets; consume
   them and add no `imePadding()`.
3. **Material 2 scaffold:** its insets go through `contentWindowInsets` (§2.3 point 2).

## 3.4 Rulers for the IME
1. **`Modifier.fitInside` with `WindowInsetsRulers.Ime.current` keeps content above the keyboard** regardless of how
   the parents consumed insets; the skill prefers it to `imePadding()` for that reason.
2. **To clear both the keyboard and the navigation bar,** the page's example passes
   `RectRulers.innermostOf(WindowInsetsRulers.NavigationBars.current, WindowInsetsRulers.Ime.current)` to `fitInside`.
3. **The ruler limits of §2.5 apply:** a constrained parent, no use for measurement.
