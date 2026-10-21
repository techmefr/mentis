# podcast-publishing-pitfalls §2 — Loudness

> Part 2 of `business/podcast-publishing-pitfalls`. Read it when a loudness target is chosen, a file is
> exported, or a figure is quoted. Sources, read 2026-10-20: EBU R 128 (2023 text, tech.ebu.ch/docs/r/r128.pdf)
> and its supplement 2 on streaming (r128s2.pdf), ITU-R BS.1770-5 (itu.int recommendation PDF), Apple's podcast
> requirements page. Own guidance is marked. Not audio-engineering advice
> (`business/README.md`).

## 2.1 Name the measure
1. **Say which measure a number is.** The EBU recommendation uses three: average programme loudness, loudness
   range, and maximum true peak level. Own guidance: a bare "-X" with no measure and no unit is not a target.
2. **Measure the final export.** Own guidance: after the last encode, measure the file that will be served, not
   the session. A lossy encode can change the peak, so re-measure after it and after any re-export.
3. **One setting does not fit two kinds of episode without a check.** Own guidance: a spoken-word episode and a
   music-heavy one are measured separately before sharing one processing chain.

## 2.2 Figures read, and what they are
1. **Broadcast target (EBU R 128, 2023 text).** Programme loudness is normalised to -23.0 LUFS. Where that
   cannot be attained in practice, as in live programmes, the recommendation allows 1.0 LU either way, and says
   deviation towards the limit must not become routine. A 0.2 LU tolerance is allowed in quality-control
   workflows for measurement error. The revision history shows a 0.5 LU tolerance introduced in version 3
   (2014), live programmes excepted; the current body text states 1.0 LU for the non-attainable case, so quote
   the current text, not the history line. A deliberately lower target is allowed if clearly indicated.
2. **Maximum true peak (EBU R 128).** A programme's true peak must not exceed -1 dBTP during production,
   measured with a meter following ITU-R BS.1770, tolerance 0.3 dB; distribution systems or data reduction can
   need a lower ceiling. This corrects the earlier note that no ceiling was given.
3. **These are broadcast figures.** EBU R 128 is addressed to broadcasters. Its streaming supplement (R 128 s2)
   notes that streaming and podcast services usually use a higher target than broadcast, recommends streaming
   programmes unchanged at -23.0 LUFS with correct loudness metadata, and gives an interim distribution range
   of -20.0 to -16.0 LUFS only where the broadcaster controls the dynamic treatment and no metadata is used.
   That range is an EBU statement about its members' streams, not a podcast-platform requirement.
4. **No podcast platform figure.** Apple's requirements page, as fetched 2026-10-20, does not mention loudness and
   links no audio page. Spotify's help page on loudness normalisation (read 2026-10-20 as a digest) is about
   music playback: it names a reference level based on ITU-R BS.1770, gives true-peak advice for lossy encodes,
   and lists listener volume settings, but does not say whether it applies to podcasts, so it is not used as a
   podcast target. A second Spotify page (audio specifications) returned a not-found page, YouTube's help
   addresses tried returned 404, and an Apple page tried was the wrong page. This block carries no platform
   number; a platform's figure is quoted only with its page, per §2.3.

## 2.2a What the standard measures (ITU-R BS.1770-5)
1. **LKFS and LUFS are the same unit.** R 128 says so in a footnote. A mismatch in the name is not a mismatch
   in the number.
2. **Gating decides the number.** The algorithm applies a frequency weighting, averages power over 400 ms blocks
   overlapping by 75 percent, then drops blocks under an absolute threshold of -70 LKFS and then under a
   relative threshold 10 dB below the level measured after the first. Symptom: two tools report different
   programme loudness on one file. Check whether both use the gated method. Fix: use one BS.1770-compliant
   meter and record its name.
3. **Peak-sample is not true peak.** A meter reading only sample values can miss the peak between samples; the
   recommendation estimates true peak by oversampling (four times at 48 kHz) before taking the maximum, and its
   informative attachment warns that plain sample meters can under-read. Symptom: a clean-looking export clips
   after lossy encoding or on playback. Check: measure dBTP with an oversampling meter on the final export.
   Fix: lower the ceiling and re-export.
4. **A short file gives a weak range.** R 128 advises against quoting loudness range for a programme under one
   minute, because too few three-second windows exist. Do not quote a range for a short trailer.

## 2.3 How to write a platform figure
1. Open the platform's own current page in the session. Write the figure with the URL and the date read, or
   write "none published".
2. Never take a figure from memory, a forum or a search summary. If the page cannot be read, the line in §5 is
   unknown, not pass.
3. Say which listening context a figure applies to (broadcast, a platform's own playback, a car). Own guidance:
   one number per context, each with its source.
