# rtl-and-bidi-layout-pitfalls §1 — Direction and layout

A right-to-left page is not an English page with the text aligned the other way. Direction has to be declared
once per locale, the layout has to follow it without a second stylesheet, and the few pieces that carry a
direction of their own (arrows, hidden text, library components) each need a deliberate answer.

## 1.1 Where the direction is set
1. **Direction belongs to the locale entry.** In the Nuxt i18n module (version 10.6, patch 0, version-bound) a locale
   object takes a `dir` value of `ltr`, `rtl` or `auto`, next to its `language` tag; a separate default direction,
   `ltr` unless changed, is used only when `dir` is missing. A right-to-left locale that omits `dir` is therefore
   laid out left-to-right with no warning. Own guidance: set `dir` on every locale entry, including the
   left-to-right ones, so that a missing value is a visible gap.
2. **Take the direction from script data.** When Pontoon asks an administrator for a locale's direction, its
   documentation says to choose right-to-left when the locale's script has the value `YES` for right-to-left in the
   CLDR script metadata file. Own guidance: look that value up when a locale is added instead of maintaining a
   list of right-to-left language names in the project, which goes stale and misses scripts.
3. **The `language` tag and the direction are two fields.** The Nuxt page defines `language` as a BCP 47 tag used
   for SEO and for matching browser locales, and `dir` as the direction of elements and content. Whether the
   module writes either one onto the `html` element was not read here (see `origin.md`).

## 1.2 Logical properties and arrows
1. **One layout serves both directions when sides are logical.** The Impeccable hardening reference replaces
   `margin-left` with `margin-inline-start`, `padding-left` and `padding-right` with `padding-inline`, and
   `border-right` with `border-inline-end`. The rule itself is `vue-nuxt-vuetify-conventions` §6 point 20; the
   pairs are only a reminder of which physical property each logical one replaces.
2. **Directional arrows are mirrored with one rule keyed on the direction.** The same reference flips an arrow
   with a horizontal scale of minus one under `[dir="rtl"]`. It says this for arrows and nothing about other
   icons, so do not generalise it to every icon. Decision: this is consistent with the point 20 of
   `vue-nuxt-vuetify-conventions` §6 against flipping icons by hand per locale, because it is one rule in the
   stylesheet and not a second copy of the template. Own guidance: decide icon by icon whether the picture has a
   direction, and mirror only those that do.

## 1.3 Hidden text
1. **Hide text visually with the clip pattern.** The A11y Project post says that, unlike positioning text off
   screen or using a negative text indent, the clip pattern also works in right-to-left languages. The pattern is
   a zero clip rectangle, a clip path that insets by half on every side, a height and width of one pixel,
   hidden overflow, absolute positioning and no wrapping. The post does not describe how the other techniques
   fail. Own guidance: open every hidden label, description and skip link in the right-to-left build and confirm
   that nothing of it is visible and that no scroll area appeared.

## 1.4 Components
1. **A component library is not right-to-left ready by default.** The GOV.UK language navigation page says that to
   show languages written right to left, such as Arabic, the components and the layouts need changes, and that
   some languages need component changes so that text displays well and assistive technology can read it. Own
   guidance: before choosing or upgrading a library for such a product, open each component the product uses
   with a right-to-left locale.
2. **Test with real right-to-left text, and with mixed text.** The hardening reference lists right-to-left text
   among the special characters to test and, in its verification list, asks for a test with Arabic or Hebrew.
   Own guidance: add one screen per component family rather than testing the home page only.
