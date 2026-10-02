# § 2 — HTML semantics: what a crawler and a screen reader read the same way

> Section 2 of `skills/seo`. Read it when a diff touches headings, links, images or how content reaches the HTML.

1. A single `<h1>` per page, an `h1 > h2 > h3` hierarchy with no arbitrary level skipping for a visual
   effect (the visual is handled in CSS, not by changing the tag).
2. Real text content in the HTML served (SSR/SSG), never only injected client-side after hydration for
   content that has to be indexed: a crawler that doesn't run JS sees nothing.
3. Internal links as real `<a href>` tags (navigable, crawlable), never a `<div onClick>` simulating a
   link, with anchor text that describes the destination rather than "click here"/"read more" repeated
   across a page. An outbound link to content we don't vouch for (user-generated content, a comment, an
   unmoderated submission) carries `rel="nofollow ugc"` — otherwise the page passes its own trust to
   whatever the untrusted content links to.
4. A descriptive `alt` attribute on meaningful images, empty (`alt=""`) on purely decorative ones: never
   absent.

