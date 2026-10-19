# android-edge-to-edge-insets §2 — Applying insets once

The Android developer pages "Set up window insets", "Use Material 3 insets" and "About WindowInsetsRulers" (all last
updated 2026-10-01), read in full as page text on 2026-10-08, and one Apache-2.0 Android agent skill for the
adaptive-scaffold, list and Material 2 rules. The page says the inset types animate with the IME, backported to API 21.

## 2.1 Choose one mechanism per component
1. **Inset padding modifiers consume the part they apply.** `windowInsetsPadding`, `safeDrawingPadding`,
   `systemBarsPadding` and `imePadding` automatically consume the inset they pad, so a nested one pads only
   what is left. That is what prevents double padding. `consumeWindowInsets` consumes without padding, for use
   with inset-size modifiers, and also accepts a `PaddingValues` that came from another source.
2. **Prefer the modifiers to turning `WindowInsets` into raw `PaddingValues` yourself.** `asPaddingValues()` returns
   values unaffected by consumption, and the page tells you to prefer the padding and size modifiers because of the
   phase timing in §2.2. Choose a single method per component, as the skill requires, to avoid double padding.
3. **Use a `Scaffold` where one exists.** It hands the insets to you as `PaddingValues` but does not apply them to the
   content. For a list, pass them as `contentPadding` and call `consumeWindowInsets(innerPadding)` on the list, as the
   page's example does. Inside a scaffold, avoid rulers, padding modifiers and size modifiers on top of that, or the
   padding is applied twice (the page).
4. **Outside a scaffold, pad with a modifier** such as `safeDrawingPadding()` or `windowInsetsPadding(WindowInsets.safeDrawing)`.
   `safeDrawing` keeps content out of everything the system draws over; `safeGestures` and `safeContent` extend that
   to gesture zones and both together.
5. **To make an element exactly as tall as a bar,** use an inset-size modifier (`windowInsetsTopHeight`,
   `windowInsetsBottomHeight`, `windowInsetsStartWidth`, `windowInsetsEndWidth`), not a measured constant.

## 2.2 Timing
1. **Inset values arrive after composition and before layout,** so a value read in composition is one frame late.
   The built-in modifiers delay their reads to the layout phase so values are used on the frame they change. That is
   the page's reason to prefer them to raw values (`compose-correctness` §2 on phases).

## 2.3 Bars and adaptive scaffolds
1. **Material 3 components handle their own insets:** `TopAppBar` and its variants (top and horizontal sides),
   `BottomAppBar` and `NavigationBar` (bottom and horizontal), `NavigationRail` (vertical and start), `ModalBottomSheet`
   (bottom) and the drawer sheets (vertical and start). Do not add a second inset on top. The `windowInsets` parameter
   can be replaced, or disabled with an empty `WindowInsets(0, 0, 0, 0)`.
2. **Material 2 components do not handle insets themselves.** From `androidx.compose.material` 1.6.0 the page says to
   use the `windowInsets` parameter on `BottomAppBar`, `TopAppBar`, `BottomNavigation` and `NavigationRail`, and
   `contentWindowInsets` on `Scaffold`; otherwise apply the insets as padding. The skill adds that padding the parent
   of a bar stops its background drawing into the system bar area, so pass the insets to the bar itself.
3. **Adaptive scaffolds do not pass padding to their content.** A navigation suite scaffold manages the insets of its
   own rail or bar, and neither it nor a list-detail scaffold propagates `PaddingValues`. Apply insets to each
   screen or component inside (a list's content padding, a floating button's padding). Do not wrap the scaffold in
   `safeDrawingPadding` or a similar modifier: it clips the screen and defeats edge-to-edge (the skill's rule).

## 2.4 Lists
1. **Give a scrollable list the inset as `contentPadding`, never as `Modifier.padding()` on its parent.** Parent
   padding clips the content and stops it scrolling behind the bars, which is the point of edge-to-edge.
2. **Where the keyboard can hide the last text field,** the page's caution is to use a trailing `Spacer` sized with
   `windowInsetsBottomHeight(WindowInsets.systemBars)` in a list that has `imePadding()`, not `contentPadding`:
   `imePadding()` consumes insets as it grows, so the spacer shrinks and is zero once the keyboard is taller than
   the bars. This is the source tension with point 1, which is the skill's rule for a list without text fields.
3. **Check both ends.** The first item must clear the top bar and the last must clear the bottom bar and any
   floating button; a floating button outside a scaffold takes `safeDrawingPadding()`.

## 2.5 Rulers
1. **`WindowInsetsRulers` work in the placement phase and bypass the consumption chain,** so they give the correct
   absolute positions of the system bars and cutouts whatever the parents did; the page says they help when an ancestor
   consumed insets wrongly. `Modifier.fitInside` and `fitOutside` take a ruler such as `SafeDrawing`, `Ime`,
   `NavigationBars`, `StatusBar` or `DisplayCutout` (`fitOutside` is not offered for `SafeDrawing` or `Ime`). The skill
   prefers them for deeply nested components with excess padding.
2. **Rulers cannot be used for measurement,** because the positions exist only at placement.
3. **The parent must be constrained.** The composable needs a size modifier such as `fillMaxSize`, the parent must not
   depend on the child's size, and a scrolling container such as `verticalScroll` can give unexpected behaviour
   because its constraints are unbounded.
