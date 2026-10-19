# locale-negotiation-and-switcher-pitfalls §3 — The switcher, the transition and dates

A switcher is read by people who may not read the page's language, and a date is rendered by two runtimes
that may not agree on the zone. Both look correct on the developer's machine.

## 3.1 The switcher
1. **Each option is written in its own language and carries its own `lang`.** GOV.UK's language navigation
   component says to use the native name, such as "Cymraeg" for Welsh, so a speaker recognises the link, and
   its example gives each item a `lang` value. The Nuxt module's switcher example does the same with a `name`
   per locale (`Español`, `Français`).
2. **The landmark label follows the page, the hidden description follows the target.** In GOV.UK's component the
   navigation landmark's label is translated into the language of the page it sits on, and the hidden text of
   each link, such as "change the language to English", is translated into the language being linked to.
3. **Same place, every language.** The component page asks for one consistent location used across the whole
   service in all languages, because some users switch back and forth to check their understanding. After the
   `h1` is its suggestion for a few translated pages; inside the service navigation when the whole service is
   translated. Elsewhere on the page it needs its own heading, visible or hidden.
4. **A switch never costs the user what they entered.** The same page says not to ask for information again
   after a language change.
5. **Offer a language only when the page has the same key information in it.** The component is not for
   a service that cannot give all the same key information in the other language. It does not translate
   content, and the component's status on that page is "trial", dated August 2026, so check the current
   guidance before copying its markup.
6. **A switcher on a dark background still needs contrast.** The component's inverse variant requires a
   background with at least 4.5:1 contrast against white; the colour contrast rules are in `accessibility` §3.

## 3.2 A page transition during a switch
1. **By default the Nuxt module changes the locale as soon as the navigation starts**, so a transition fades the
   old page out with its text already in the new language and fades the same content back in.
2. **Delay setting it.** Set `skipSettingLocaleOnNavigate` to `true` and call `finalizePendingLocaleChange()` in the
   `onBeforeEnter` hook of the transition, globally or per page (module 10.6). The guide adds that scrolling
   can wait for `waitForPendingLocaleChange()` for a smoother result.

## 3.3 Dates and time zones
1. **The time zone is chosen, not inherited.** next-intl's documentation says the default is the time zone of
   the server runtime, and shows three ways to choose one: a fixed value, a user profile setting, or request
   information such as the locale or a cookie. Components rendered on the client inherit the server's value
   when the provider is rendered by a server component. The same point as a rule for Vue is
   `vue-nuxt-vuetify-conventions` §6.10.
2. **Store full ISO 8601 strings and format only at display time.** next-intl's guidance is to keep dates as
   complete ISO 8601 strings (its example ends in `Z`), parse them with the `Date` constructor, and let the
   formatter do the rest.
3. **Guard date and time rendering against a server-versus-client mismatch.** Vercel's guidelines list it as a
   hydration-safety item. When a value is read from the clock in a component, the rule that fixes it is in
   `nuxt-no-hydration-nondeterminism`.
4. **Read "now" once and reuse it for relative times.** A relative time is computed against a reference
   point. next-intl's `useNow` returns a value that is consistent across client re-renders, can start from a
   global value, and a global `now` also helps caching and makes tests repeatable. Own reasoning: one
   reference value per render is also what keeps a relative label from differing between two components on the
   same page.
5. **Turning a month or weekday into a word through a lookup array is a different rule**: see
   `laravel-date-via-localised-accessors`.
