# android-edge-to-edge-insets: origin and source stamps

> Provenance of `skills/android-edge-to-edge-insets`. Read it when a rule has to be traced to its source or checked
> for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from documentation, never run by us. No app was built and no device or emulator was used.

**Fold-in note.** Meant to be folded into `kotlin-android-conventions` (or a Compose reference next to
`compose-correctness`) when PR 118 lands.

## Sources (read 2026-10-08, rewritten, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| developer.android.com: Set up edge-to-edge, About window insets, Set up window insets, Use keyboard IME animations, Use Material 3 insets, About WindowInsetsRulers, About system bar protection (all last updated 2026-10-01) | Android docs: CC BY 4.0 for text, code Apache 2.0 (facts only, rewritten) | §1, §2, §3 |
| developer.android.com: Android 16 and Android 17 behaviour changes | same | §1.1 point 3, §4 |
| One Apache-2.0 Android agent skill on edge-to-edge (LICENSE.txt read, file last-updated stamp 2026-08-24) | Apache-2.0 | dialog, adaptive-scaffold, Material 2 parent-padding, icon-colour, `SOFT_INPUT_ADJUST_RESIZE`, `imePadding` order and Scaffold-IME rules, marked "the skill's" in the text |

The pages were downloaded and read as page text, and every rule was compared with that text in a second pass.

## Re-verified against page text in the second pass
Enforcement at SDK 35 and the bar behaviour; `enableEdgeToEdge()` defaults; `adjustResize` purpose; the contrast
enforcement switch; status-bar protection by an overlapping gradient composable; insets list and the safe types; padding
consumption, `consumeWindowInsets`, size modifiers, phase timing; the Scaffold `PaddingValues` and its warning about
extra approaches; Material 3 and Material 2 component rules; rulers (placement phase, no measurement, constrained
parents, the table of rulers); the Android 16 large-screen and opt-out details; the Android 17 sentence.

## Corrected or removed in the second pass
- **Corrected:** the IME double-padding rule. A parent that applies `safeDrawingPadding()` consumes the insets, so a child
  `imePadding()` is fine; the double application comes from unconsumed raw `PaddingValues` or an unconsumed
  `innerPadding`. The first version had it backwards.
- **Corrected:** "prefer modifiers over raw values because of consumption"; the page's reason is phase timing.
- **Corrected:** the list-spacer rule now states the page's caution about text fields in a `LazyColumn`.
- **Removed:** the launcher-Activity advice for `adjustResize`, "gesture navigation has no contrast enforcement", "do not copy
  inset values into state", and "put the ruler modifier on a bounded container inside a scroller": none is on a page or in
  the skill.
- **Removed:** Android 17 "keyboard not restored after rotation": the Android 17 page says nothing about it.
- **Removed:** library version numbers for `androidx.activity` and Compose: no page read states them (only Material 2
  1.6.0 for `windowInsets`).

## Not verified
1. **Scaffold default IME handling, `imePadding` before `verticalScroll`, the `SOFT_INPUT_ADJUST_RESIZE` deprecation,
   `decorFitsSystemWindows = false` for full-screen dialogs and the SDK 29 rule for contrast enforcement** are the skill's
   statements; no developer.android.com page read states them, and nothing was run.
2. **Source tension kept:** the insets page says to use a trailing `Spacer` rather than `contentPadding` for the last text
   field in a `LazyColumn`; the skill says list insets go in `contentPadding`. Both are written, scoped as each source
   scopes them.
3. **Whether the system icon colours follow the theme with the `WindowCompat` form** of `enableEdgeToEdge` is the skill's
   claim; the page says only that `enableEdgeToEdge()` adapts them.
4. **Nothing was compiled or run;** every API-level statement is the page's.

## Related blocks
`compose-correctness` (state and effects in Compose).
