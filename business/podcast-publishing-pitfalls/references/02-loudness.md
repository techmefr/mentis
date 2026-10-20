# podcast-publishing-pitfalls §2 — Loudness

> Part 2 of `business/podcast-publishing-pitfalls`. Read it when a loudness target is chosen, a file is
> exported, or a figure is quoted. Sources, read 2026-10-20: the EBU R128 page (tech.ebu.ch/publications/r128),
> Apple's podcast requirements page. Own guidance is marked. Not audio-engineering advice
> (`business/README.md`).

## 2.1 Name the measure
1. **Say which measure a number is.** The EBU recommendation uses three: average programme loudness, loudness
   range, and maximum true peak level. Own guidance: a bare "-X" with no measure and no unit is not a target.
2. **Measure the final export.** Own guidance: after the last encode, measure the file that will be served, not
   the session. A lossy encode can change the peak, so re-measure after it and after any re-export.
3. **One setting does not fit two kinds of episode without a check.** Own guidance: a spoken-word episode and a
   music-heavy one are measured separately before sharing one processing chain.

## 2.2 The one figure read, and what it is
1. **Broadcast.** The EBU R128 page gives -23 LUFS as the programme loudness target, and says version 3.0 of
   the recommendation restricted target tolerances to plus or minus 0.5 LU. The page gave no number for the
   true peak ceiling and pointed to related documents (loudness metering, loudness range) that were not read.
   This is a broadcast recommendation, read 2026-10-20; it is not a podcast-platform requirement.
2. **No platform figure.** Apple's requirements page, as fetched 2026-10-20, does not mention loudness and links
   no audio page. No streaming-platform page with figures was read. This block therefore carries no
   podcast-platform number.

## 2.3 How to write a platform figure
1. Open the platform's own current page in the session. Write the figure with the URL and the date read, or
   write "none published".
2. Never take a figure from memory, a forum or a search summary. If the page cannot be read, the line in §5 is
   unknown, not pass.
3. Say which listening context a figure applies to (broadcast, a platform's own playback, a car). Own guidance:
   one number per context, each with its source.
