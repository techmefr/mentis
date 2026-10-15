# locale-negotiation-and-switcher-pitfalls §2 — URLs and alternate links

The rule that every multi-language page needs `hreflang` is in `seo` §1.5. What goes wrong is the input to it:
tags that are not tags, a base address that is not absolute, and a URL strategy under which the addresses
are not different.

## 2.1 What hreflang is built from
1. **Each locale needs a full language tag, not a short code.** The Nuxt module generates its alternate links
   from a `language` value on each locale object (`en-US`, `es-ES`) and uses it for the `lang` attribute of the
   page; its guide lists that option as a requirement for every locale (module 10.6).
2. **The base address must be set and absolute.** The same guide requires `baseUrl` so the alternate URLs are
   fully qualified. next-intl reads the host from `x-forwarded-host` and falls back to `host` to build its
   links, so, own reasoning, a proxy that drops those headers would produce wrong ones.
3. **Several locales of one language need a chosen catch-all.** The Nuxt module adds a language-only alternate
   for each group such as `en-*`, defaulting to the first locale of the group; `isCatchallLocale: true` on
   another locale changes it, and a locale whose `language` is plain `en` is used without any setting.

## 2.2 URL strategy and generated links
1. **Under "never prefix", the address is the same for every language and generated alternates stop.**
   next-intl documents that alternate links are disabled when the prefix is never shown, because URLs may not be
   unique per locale, and tells the reader to write the links by hand or list them in a sitemap with
   `alternates`. Own guidance: a crawler needs a distinct address per language, whatever the visitor sees.
2. **Opt out of the generated `Link` header when it would lie.** next-intl's `alternateLinks: false` is for
   pages that exist in only some locales and for paths held in a CMS; the alternates are then supplied from a
   sitemap or the metadata API. Own reasoning: a generator that lists every configured locale for every page links to pages
   that do not exist.
3. **The strategy is chosen once.** That is `vue-nuxt-vuetify-conventions` §6.18; the extra point here is the
   consequence for crawlers in point 1.

## 2.3 x-default and canonical
1. **`x-default` points at the address that does the choosing.** next-intl's generated header includes it and
   says the entry is reserved for language selection and detection, which in its setup answers with a
   temporary redirect to the best locale. Own guidance: it is the one address allowed to redirect by language,
   which is the root rule of §1.3 seen from the search engine.
2. **The canonical address excludes tracking parameters.** The Nuxt module generates a canonical link per page,
   chooses the unprefixed address when both a prefixed and an unprefixed version of the default locale exist,
   and leaves query parameters out unless they are listed in `canonicalQueries`.
3. **The page language is a document property.** The same module sets the `lang` attribute of the document
   from the locale's `language`, and a Vue layout may pass `dir` from the same head data.

## 2.4 The middleware has to run on the right paths
1. **Run on pages, not on files.** next-intl's matcher excludes paths that start with `/api`, `/_next` and the
   like, and any path with a dot, because that usually means a static file. A route where a dot is expected,
   such as `/users/jane.doe`, needs its own matcher entry or it is not localised.
2. **Unprefixed addresses must be matched too** when the strategy omits the prefix for the default or for every
   locale, or those pages never reach the middleware.
3. **Exclude third-party endpoints that are rewritten to another host.** next-intl names analytics paths of a
   hosting provider as an example of requests that must not be rewritten by accident.
