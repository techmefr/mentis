# podcast-publishing-pitfalls §5 — Pre-publish list

> Part 5 of `business/podcast-publishing-pitfalls`. Read it just before release. Own guidance throughout; the
> items point to §1 to §4 for their sources. Not legal advice (`business/README.md`).

Mark every line pass, fail or unknown, with the evidence beside a pass. An unknown stays unknown; it is never
rounded up to a pass.

| Line | Evidence for a pass |
|---|---|
| Feed validates after the last edit (§1.3) | the validator's result and date |
| Episode identifier set once, unchanged by this release (§1.1) | the value, compared to the previous feed |
| Enclosure fetched: size and type match the feed; HEAD and byte-range answered (§1.2) | the fetch result |
| Date format correct; scheduled date checked after it passed (§1.3) | the feed read after the date |
| Loudness measured on the final export, measure named (§2.1) | the measurement and the tool |
| Any platform figure cited with URL and date, or "none published" (§2.3) | the page and the date read |
| Transcript published and linked from the notes and the feed (§3.1) | the link |
| Generated text read against the audio (§3.2) | who read it, on which date |
| Notes traced to the transcript; links opened (§3.3) | the source line per item |
| Sponsor and affiliate disclosure present in notes and audio (§3.3) | the lines |
| Guest told what is published (§3.4); removal path written (§3.5) | the message, the note |
| Voice consent and synthetic-voice notice present (§4.1, §4.2) | the recorded yes, the notice |
| Music and sound licences and receipts on file (§4.3) | the file |

Any fail is fixed or sent to the person who owns the show. The list is the output (SKILL.md); nothing here
certifies the episode.
