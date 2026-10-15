# locale-negotiation-and-switcher-pitfalls §1 — Negotiation and persistence

Three things can say which language a request wants: the address, a stored choice, and the browser's header.
Without a written order they overrule each other differently on each page.

## 1.1 The order of resolution
1. **Write the order down: URL prefix, then the stored preference, then the `Accept-Language` header, then the
   default.** That is next-intl's order for prefix-based routing, and its domain-based variant has the same
   shape with the domain's own locales. A prefix in the address always wins.
2. **Visiting a prefixed address changes the stored preference.** In next-intl a visit to `/de` takes
   precedence over a cookie or a header and updates the cookie, which is how a plain link to the other
   language becomes a switch. The documented walk-through: `/` is matched to `en` from the header and sent to
   `/en`; the user follows a link to `/de`; the cookie now says `de`; a later request for `/` is sent to `/de`.
3. **Detect from the browser's languages, not from the network address.** Vercel's guidelines say to read
   `Accept-Language` or `navigator.languages` and not the IP. The Nuxt module does exactly this: it reads
   `navigator` in the browser and the header on the server.
4. **A project that wants the URL to be the only authority switches the rest off.** next-intl's
   `localeDetection: false` disables both the header and a stored cookie, leaving only the prefix and a
   matching domain; its `localeCookie: false` turns the cookie off. Own guidance: say which of the two the
   project chose, because a half-way setting is the order nobody wrote down.
5. **With one domain per language, a request for a language the domain does not serve is sent to one that
   does.** next-intl's domain-based routing reads the host from `x-forwarded-host`, falling back to `host`, and
   redirects `en.example.com/fr` to the domain that supports French; the switcher link for another language can
   therefore cross domains.

## 1.2 Matching the header
1. **Match with a distance-based "best fit", not with the strict "lookup" of RFC 4647.** next-intl's middleware
   uses the best-fit algorithm of `@formatjs/intl-localematcher`. Its example: with `en-US` and `de-DE`
   supported, a browser that sends `en-GB` gets the default locale under lookup (subtags are removed one by
   one until something matches, and nothing does) and gets `en-US` under best fit, which weighs regional
   distance.
2. **A simpler matcher may do less.** The Nuxt module matches the configured locale tags against what the
   browser reports, and when no full tag matches, it matches the language code, the letters before the first
   `-`. Own guidance: test the cases that matter to the audience (`en-GB` against an `en-US` catalog, `pt-PT`
   against `pt-BR`) instead of assuming the matcher is the one the other stack uses.

## 1.3 Where to redirect
1. **Redirect by detected language only on the root path.** The Nuxt module recommends `redirectOn: 'root'`, its
   default: detection runs only when the visitor requests `/`, so a crawler that asks for an inner page gets
   that page and not a redirect to another language, and a link to a page in a given language keeps working.
   This is Nuxt module 10.6 behaviour.
2. **With no server, nothing negotiates.** In a static export, next-intl documents that a locale prefix is
   required, the locale cannot be negotiated on the server, translated pathnames are unavailable, and `/` needs
   an explicit redirect to the default locale.

## 1.4 The stored locale
1. **It is a cookie, and its lifetime is a choice.** next-intl sets a session cookie called `NEXT_LOCALE` when
   the user changes to a locale the header would not have given, with no `max-age`, so it ends when the browser
   closes, and with `SameSite=Lax` so it can be set when the visitor arrives from another site. Its docs suggest a
   longer `maxAge` when URLs carry no prefix, so the choice survives a restart.
2. **Inside a cross-origin frame the default attribute is wrong.** The Nuxt module's `cookieCrossOrigin: true`
   changes the cookie from `SameSite=Lax` to `SameSite=None; Secure` (module 10.6).
3. **Cookie lifetime and consent are not settled here.** next-intl's documentation describes its session cookie
   as the compliant default and tells the reader to check the legal position; this block does not repeat the
   claim as a rule (see `references/origin.md`).

## 1.5 A switcher writes the preference
1. **Changing the language must also write the stored locale.** The Nuxt module's guide says that to keep the
   locale across a route change when detection is on, the stored cookie has to be updated explicitly with
   `setLocale()` or `setLocaleCookie()`; otherwise a later navigation can redirect to the old cookie value.
2. **Use the module's switch call, not the underlying i18n library's `locale` setter.** Setting `locale` on the
   Vue i18n instance does not load the messages, run the hooks or update the cookie; `setLocale()` and
   `switchLocalePath()` do (Nuxt module guide).
3. **In next-intl a link carrying the target locale does the same work.** The request to the prefixed address is
   what makes the middleware update the cookie (§1.1). Own guidance: a switcher built on a plain `<a>` to the
   unprefixed address, or on client-side state, skips that request, so test it by changing language and then
   navigating once.
