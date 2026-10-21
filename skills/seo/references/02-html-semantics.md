# § 2 — HTML semantics: what a crawler and a screen reader read the same way

> Section 2 of `skills/seo`. Read it when a diff touches headings, links, images or how content reaches the HTML.

1. One clear main heading, usually the first visible `<h1>` (Google's title-link page names it as a source for the
   title shown), and an `h1 > h2 > h3` hierarchy with no level skipped for a visual effect (the visual is handled in
   CSS, not by changing the tag). Correction from the sources: Google's starter guide says that for Search the number
   and the order of headings do not matter, so a single `h1` and an unbroken order are readability and accessibility
   rules (`skills/accessibility`), not ranking requirements; a second `h1` is not an SEO defect.
2. Real text content in the HTML served (SSR/SSG), never only injected client-side after hydration for
   content that has to be indexed. Google renders JavaScript in a later phase, cannot index what is absent from the
   rendered HTML, and recommends server-side or pre-rendering because not every bot runs JavaScript (its JavaScript
   SEO basics page); a crawler that does not run scripts sees nothing.
3. Internal links as real `<a href>` tags (navigable, crawlable), never a `<div onClick>` simulating a
   link, with anchor text that describes the destination rather than "click here"/"read more" repeated
   across a page (Google: appropriate anchor text helps people and engines understand the target; it discovers links
   only in `<a>` elements with an `href`). An outbound link to content we don't vouch for (user-generated content, a comment, an
   unmoderated submission) carries `rel="nofollow ugc"`. Google's page on qualifying outbound links defines `ugc` for user-generated content,
   `sponsored` for paid placements (preferred over `nofollow` for them) and `nofollow` for the rest, and accepts
   several values together; the trust-passing rationale is not stated there.
4. A descriptive `alt` attribute on meaningful images (Google's starter guide: a short, descriptive text on the
   `img` element), empty (`alt=""`) on purely decorative ones: never absent (own guidance for the decorative case,
   see `skills/accessibility`).

