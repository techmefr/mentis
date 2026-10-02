# § 6 — Structured data, dates and social previews

> Section 6 of `skills/seo`. Read it when a page type gets JSON-LD, when a date or an author is published,
> or when a page is meant to be shared and previewed. §4.1 says when structured data earns its place; this
> section says what each type owes and what makes it wrong. Which properties a search feature requires,
> and which features are still shown at all, are the search engine's current documentation: read them on
> the day, because that scope has been narrowed more than once and a block that recites it is wrong
> without anyone noticing (`skills/source-freshness`).

## Structured data

1. **Markup describes what the page shows.** The data in the JSON-LD matches the visible content, word for
   word where it names things. Marking up content a visitor cannot see, or a rating nobody gave, is a
   violation of the engine's guidelines and risks losing the enhancement entirely.
2. **Only on pages that can be indexed.** A page excluded from the index carries no structured data
   (§5.10). Data is placed once per entity, on the page that is the entity's home.
3. **The syntax is valid first.** One `script` of type `application/ld+json` per block, parseable JSON, a
   `@context` of schema.org, a `@type`, and nested entities in the shape the vocabulary defines. The
   parse is a build check; the engine's rich-result tester is a manual step for a person, never a
   dependency.
4. **One line per type that earns its place.** For each, the required and recommended properties are
   read from the engine's page for that feature at writing time.
   - `Article` (or its subtypes): headline, image, publication and modification dates, author.
   - `Product`: name, image, and `offers` with price, currency and availability; review and rating
     properties only from genuine, visible reviews.
   - `Review` and `AggregateRating`: attached to a real reviewed item, never to the page's own
     organisation as self-service.
   - `VideoObject`: name, description, thumbnail and upload date, on the page where the video plays.
   - `Organization`: name, URL, logo and the profiles that really belong to it (`sameAs`); once, on the
     home or about page.
   - `WebSite`: name and URL; any search-box enhancement is a current-support question.
   - `FAQPage`: only real questions that are answered on the page; the enhancement's availability has
     been restricted by the engine, so it is not a default.
   - `BreadcrumbList`: one list item per level with position, name and URL, equal to the visible trail
     (`skills/accessibility` §8.12).
   - `Person`: for an author who has a page of their own; never an invented name.
5. **Authors and organisations are published only when a page exposes them.** A byline links to an author
   page that states who the person is; the organisation data is the one the legal pages state. Structured
   data does not create credibility the page does not show (§7).

## Dates

6. **The publication date never moves; the modification date moves for a substantive edit.** Correcting a
   typo is not a modification, and a refreshed date with no change is an attempt to look fresh that
   engines discount. The date in the data, the visible date, the `Last-Modified` header and the sitemap's
   `lastmod` tell one story, and they are generated from one stored value, not typed in four places.

## Social previews

7. **The Open Graph set is complete.** The protocol's four base properties (title, type, image, URL) plus a
   description and an image alternative text; `og:url` is the canonical URL (§1.2), not the address
   with tracking parameters. A card type for the platforms that read their own tag.
8. **The preview image is reachable and sized for its consumer.** An absolute, secure URL that returns a
   success without authentication, an aspect ratio and minimum dimensions read from each platform's
   documentation on the day, and text inside the image kept short and away from the edges where crops
   happen (and present in the description too, `skills/accessibility` §6.12).
9. **Previews are cached by the platform.** After a change, the new image appears only after the platform
   is asked to re-read the URL; a share-card change is released with that step, and the image URL changes
   when the image does.

## Mechanical checks

```
grep -rn 'application/ld+json' src
grep -rnE 'property="og:(url|image|title|type)"' src
```

- Extract every `ld+json` block from the rendered pages, run it through a JSON parser, and verify the
  `@context`, the `@type` and the properties the engine documents for that type.
- Compare `og:url` with the canonical, request `og:image` and expect a success status.
- Compare `datePublished` and `dateModified` with the visible text, the `Last-Modified` header and the
  sitemap `lastmod` for the same URL.
- Intersect pages carrying structured data with pages carrying `noindex`: the result must be empty.
- Compare names, prices and ratings in the data with those in the rendered text.
