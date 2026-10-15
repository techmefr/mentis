# i18n-catalog-workflow-pitfalls §2 — IDs, loading and fallback

The key of a message is also its identity in the vendor's tool and in the translation memory. Changing it, or
failing to find its translation, is a decision the catalog makes for you unless you made it first.

## 2.1 Message IDs
1. **Generated IDs and explicit IDs trade stability against effort; pick one per project.** Lingui's guide
   lists, for generated IDs derived from the source text: no naming effort, duplicates merged so translators
   do not translate the same phrase twice, no collisions as the app grows, smaller bundles, and a search for a
   user-visible string lands in the code. For explicit IDs: full control, loose coupling because the ID stays when
   the text changes (which helps a non-technical person edit text in a translation tool), readable names, and
   stability across versions. Lingui itself says its benefits are greatest with generated IDs; that is the
   vendor's own view of its default.
2. **What changes a generated ID.** The ID is derived from the source message and its context, so editing the
   text, adding a context, or renaming a placeholder variable produces a new ID and a new, untranslated catalog
   entry (Lingui explicit-versus-generated guide, and its translator-friendly guide for the context and variable
   cases). Own guidance: read the catalog diff after any source edit, and expect the old entry to be left behind.
3. **The repository convention is a third style, and it has the same property.** `vue-nuxt-vuetify-conventions`
   §6.2 makes the key the full source sentence, readable in the file. Own consequence: editing that sentence
   changes the key, so the translated entries must be renamed with it or they are lost; do the edit as a catalog
   change, not only as a code change.
4. **Enforce the choice.** Lingui has `require-implicit-id` and `require-explicit-id`; formatjs has `enforce-id`
   (generated IDs matching a pattern, with an allow-list for custom ones) and `no-id` (bans explicit IDs).
   The formatjs docs say they generally encourage generated IDs.

## 2.2 Loading catalogs
1. **Load only the active locale's catalog.** Lingui's dynamic-loading guide imports one catalog at runtime and
   shows the build output with a separate chunk per language, of which only the first is requested at start.
   The Vue and Nuxt form of this rule is `vue-nuxt-vuetify-conventions` §6.16.
2. **The source locale needs a catalog too, in Lingui.** Its guide warns that Lingui drops the default
   messages from the production build, so even the source language has to be loaded; otherwise switching from it
   would need two catalogs. This is Lingui behaviour (6.9.1), not a general rule: check what your library
   strips from a production build before assuming the source text is still there.

## 2.3 Fallback chains
1. **A locale tag is BCP 47 with hyphens, and the chain follows the hyphens.** In vue-i18n (documentation of
   12.0.0-alpha.5, version-bound) `de-DE-bavarian` falls back to `de-DE` and then to `de`, because the library
   splits the tag at `-`. `pt_BR` does not fall back to `pt`, and a trailing `!` (`de-DE!`) turns the
   implicit chain off.
2. **The fallback is a list, and it can be a decision map.** A single `fallbackLocale`, an array such as
   `['fr', 'en']`, or a map keyed by locale. The guide's map sends `de-CH` to French then Italian before the
   default, `zh-Hant` to `zh-Hans`, and its table shows each resulting chain, for instance `pt-BR` going
   through `pt`, `es-AR`, `es` and `en-GB` before `en`. Write the chain you intend, then read it back from such a table.
   The point that this is a different failure from a missing key is `vue-nuxt-vuetify-conventions` §6.21.
3. **Fallback warnings are development-only by default and stay on in development.** vue-i18n prints a
   "not found" warning and a "fall back" warning, off in production by default, and they can be silenced with
   `missingWarn: false` and `fallbackWarn: false`. Own guidance: do not set either to `false` during development,
   it removes the signal that a locale is incomplete.
4. **A key that is the source text can double as its own template.** vue-i18n's `fallbackFormat: true`
   interpolates a missing key's text, so with sentence keys (`vue-nuxt-vuetify-conventions` §6.2) the source
   language needs no entry of its own, and the key's own `{name}` parameters still work. The drawback is the
   one in point 3 of §2.1: the key is the text.
