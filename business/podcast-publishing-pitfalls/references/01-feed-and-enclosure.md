# podcast-publishing-pitfalls §1 — Feed and enclosure

> Part 1 of `business/podcast-publishing-pitfalls`. Read it when a feed or an episode file is created, edited or
> moved. Sources, read 2026-10-20: the RSS 2.0 specification (rssboard.org), Apple's podcast requirements page
> and feed-move page (podcasters.apple.com), the Podcast Namespace `podcast:guid` page. Sentences marked "own
> guidance" are ours. Not legal advice and not platform advice (`business/README.md`).

## 1.1 Identity that never changes
1. **The episode identifier is set once.** The RSS specification calls the item `guid` an opaque string with
   no syntax rules, which readers may use to decide whether an item is new; the publisher is responsible for
   its uniqueness. Apple's requirements page asks for an episode identifier that never changes. Own guidance:
   a rename, a re-host, a re-encode or a title edit never touches it; regenerating it makes players show a
   second copy of the episode.
2. **The permalink flag.** In the specification `isPermaLink` defaults to true, meaning a reader may treat the
   value as an address to open. Own guidance: if the identifier is not an address, say so with the flag set to
   false, so that nothing tries to open it.
3. **The show has its own identifier, once.** The Podcast Namespace page puts `podcast:guid` on the channel
   (one per feed), derived from the feed address at the time it is first assigned (scheme and trailing slash
   dropped, then hashed), and says it normally never changes, even when the address does; a new host should
   find the existing value and carry it into the new feed rather than generate another. If a feed already has
   one, that value wins.
4. **Moving a feed.** Apple's feed-move page, as fetched: the old address answers with a permanent redirect
   (HTTP 301), the new feed carries the `itunes:new-feed-url` tag set to the new feed address (not to the
   mirror address shown in Apple's console), both stay in place for at least four weeks, and every episode
   identifier stays unchanged, since changing them can cause duplicates and misreported analytics. A host that
   manages the feed can do the redirect for you. Own guidance: write the date the move started, and the date the
   redirect may be removed, in the show's notes file.

## 1.2 The enclosure triple, fetched
1. **Three attributes, all real.** The specification requires `url`, `length` (bytes) and `type` (a MIME
   type) on the enclosure, and says the address must be an http address. Apple asks for a unique enclosure per
   episode and ignores a repeated enclosure address.
2. **Fetch it.** Own guidance: request the enclosure address, compare the size in bytes and the type the
   server returns with the feed, and keep the result in the list (§5). The feed text proves nothing about the
   file served.
3. **The server.** Apple asks the host to answer HEAD and byte-range requests, so that artwork shows and
   episodes stream. Own guidance: test both on the real address after every host change.
4. **File names and addresses use ASCII letters and digits** (Apple), percent-encoding anything else.

## 1.3 Dates, escaping, case
1. **Dates.** The specification says RFC 822 with a two- or four-digit year, four preferred; Apple asks RFC
   2822 form with the weekday, a 24-hour time and a timezone offset, no a.m. or p.m. Own guidance: generate
   the date with a library, never by hand.
2. **A future date can hide an item.** The specification says an aggregator may choose not to show an item
   until its date. Own guidance: for a scheduled drop, check the feed after the date, not before.
3. **Escaping and case.** Apple says tags and attribute values are case-sensitive (its example shows a
   category written `Kids & Family`), asks for XML entities and not HTML names such as curly-quote entities, and
   says other characters go in directly as UTF-8. Own guidance: validate the feed after every edit.
4. **Required elements.** The specification requires channel title, link and description. Apple links its
   required-tags and artwork specifications from the requirements page; those two pages could not be read (see
   origin), so check them directly before a new feed goes live.
