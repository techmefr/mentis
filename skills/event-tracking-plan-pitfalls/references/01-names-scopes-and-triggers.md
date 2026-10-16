# event-tracking-plan-pitfalls §1 — Names, scopes and triggers

The plan is written so that each event can be implemented, verified and read without asking its author. Items
marked vendor hold for the tag manager and analytics product of the source tool and are carried as its
statements.

## 1.1 Start from the questions
1. **List the questions the data must answer and the decisions it informs before listing events**
   (product-on-purpose). It prevents tracking everything and still missing the one thing needed.
2. **Each event should be meaningful to the business, not merely detectable.** The jtrackingai guide asks for
   events that serve reporting, optimisation, QA or debugging, and rejects vanity events, duplicates and
   low-signal interactions.
3. **Cover the journeys that matter**: primary conversion points, call-to-action intent, lead-capture, signup,
   login and request forms, key funnel transitions and completion, and failures or error states that matter
   to the analysis (jtrackingai).

## 1.2 Names
1. **One name, one event.** Every event name is unique across the plan. If two interactions share a name, either
   they are the same action on different pages and are merged into one event scoped to all pages, with the page
   carried as a property, or they are different intents and one is renamed (jtrackingai).
2. **Do a dedup pass before finalising**: list every name, resolve any that appears twice, and check that a
   merged event still carries enough context to analyse (jtrackingai).
3. **A convention, written down.** Lower-case words joined by underscores, descriptive, in a consistent shape
   such as noun and verb (product-on-purpose gives `noun_verb` or `verb_noun` as the usual choices). Record the
   convention in the spec.
4. **Vendor items for the analytics product of the source tool**: snake case only, a maximum of 40 characters,
   starting with a letter, and no reserved names such as the ones the product sends itself. The source states
   these limits; they were not checked against the product's documentation here.
5. **Prefer the standard event name when it matches the intent** (jtrackingai), and keep the custom ones
   specific to a business action rather than to the element that triggers them.

## 1.3 Do not redefine what is collected automatically
1. **The analytics product collects some events itself** (vendor): page view, session start, first visit, user
   engagement, scroll at a fixed depth, outbound clicks, file downloads, form interactions and embedded video
   progress are in the source's list of automatic ones. Do not define them again as custom events.
2. **If a custom scroll-depth measure is really needed, give it a distinct name** such as scroll depth, not the
   reserved one (jtrackingai). Add it only when there is a clear analysis need.
3. **The configuration tag usually sends the page view already**; a second custom page view event duplicates it
   (jtrackingai, vendor).

## 1.4 Page scopes
1. **Locale-aware.** When URLs carry a language prefix, define one event for the shared business intent and let
   the page pattern accept the optional prefix; do not create one event per language and do not scope the event
   to the default-language path alone. Prefer an explicit list of the discovered locales over a catch-all
   pattern (jtrackingai).
2. **Subdomain-aware.** When login, signup, onboarding, checkout, billing or account flows live on a subdomain
   of the same registered domain, one event for the business intent can span the main site and that subdomain.
   Use patterns that name the host rather than defaulting to the marketing host (jtrackingai).
3. **Shared elements are defined once.** Header, footer and navigation elements that repeat across pages are
   one event with an all-pages scope, defined in one place, and skipped in each page group. An element is
   shared only if it actually repeats across pages; being inside a navigation region is not enough
   (jtrackingai).

## 1.5 Selectors
1. **Text is a discovery hint, not a trigger.** A selector built on visible text, such as a link whose text
   matches a word, helps find the intended element during analysis, but the source states that its tag manager
   does not support it in selector triggers (vendor). It must be replaced with a stable executable selector before
   approval: an id, a stable link target, a data attribute, an accessibility attribute or a stable structural
   selector.
2. **Test the degradation.** If removing the text condition leaves a generic tag or a weak class match, the
   selector must not be approved; either find a structural selector or mark the event for manual resolution.
   Otherwise the trigger becomes over-broad, fires twice or on the wrong element, and cannot be QA'd
   (jtrackingai).
3. **Keep the label as data.** The visible text can still be captured as a property such as link text; it just
   must not be what makes the trigger work (jtrackingai).
4. **Carry forward only what can be explained.** When reusing events from a live setup, keep a click event when
   its structural trigger can be recovered; keep a custom event only when its source (the push, the listener,
   the callback) still exists and is understood; otherwise mark it as an unresolved dependency, not as
   implemented (jtrackingai).

## 1.6 Triggers and properties
1. **A trigger says exactly when the event fires.** product-on-purpose's example: "when the user clicks Submit"
   and "when the form is submitted successfully" are different events with different meanings. Choose the one
   the analysis needs, usually the outcome.
2. **Each property has a name, a type, whether it is required, a description and an example value**
   (product-on-purpose). Untyped properties are how a number ends up sometimes as text and sometimes as a
   count.
3. **Properties support both analysis and QA**, not only implementation convenience (jtrackingai).
4. **Persistent user properties are listed separately**, with when each is set: tier, creation date and the
   like, for segmentation (product-on-purpose).
5. **Common properties are written once** and event-specific ones under each event, so a review reads the
   event table first and the long parameter lists after (jtrackingai's review order).
