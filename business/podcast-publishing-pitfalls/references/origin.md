# podcast-publishing-pitfalls: origin and source stamps

> Provenance of `business/podcast-publishing-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from public pages and repository text, never run on a real show by us and
written without expertise in audio, podcasting or law. The block structures a release checklist; it certifies
nothing, and the person who owns the show decides (`business/README.md`).

## Sources (read 2026-10-20, rewritten in our own words, no text copied)

Web pages were read through a fetch tool that returns a model-written digest of the page, not the raw page; a
fact below is "as fetched". Repositories were cloned read-only in the session and deleted afterwards.

| Source | Licence or terms | What it gave |
|---|---|---|
| rssboard.org/rss-specification (fetched 2026-10-20) | CC BY-SA 1.0 per the page's own licence line; facts only, no text kept | opaque item identifier and its uniqueness, `isPermaLink` default, enclosure `url` / `length` / `type`, date format and the future-date remark, required channel elements |
| github.com/Podcastindex-org/podcast-namespace, `docs/tags/guid.md` and `docs/tags/transcript.md` (fetched 2026-10-20) | repository licence not read; facts only | channel-level `podcast:guid` assigned once and carried through a host move; episode-level `transcript` tag, attributes, `rel="captions"` |
| podcasters.apple.com/support/823-podcast-requirements (fetched 2026-10-20) | Apple site terms; facts only | RSS 2.0, public feed, HEAD and byte-range, unique enclosure, never-changing episode identifier, ASCII file names, date form, case and entity rules; absence of any loudness statement |
| podcasters.apple.com/support/837-change-the-rss-feed-url (fetched 2026-10-20) | Apple site terms; facts only | permanent redirect on the old address, the new-feed tag on the new feed, four weeks minimum, identifiers unchanged |
| w3.org/WAI/media/av/transcripts/ (fetched 2026-10-20) | W3C page, copyright line "© 2026 W3C" with its permissive-licence reference; facts and structure only | transcript kinds, speaker names, non-speech sound, placement, HTML, timestamps, level for audio-only and for video with audio |
| w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html (fetched 2026-10-20) | W3C terms; facts only | 1.2.1 at Level A, a text transcript as an alternative for audio-only |
| tech.ebu.ch/publications/r128 (fetched 2026-10-20) | EBU site terms; facts only | -23 LUFS programme loudness, the three measures, tolerance of plus or minus 0.5 LU in version 3.0, no true-peak number on the page |
| forcequit/shownotes-skill, commit 5f29cd2cab970c4f3dbcc3b8bb457799474b7fc4: `shownotes/SKILL.md` (read in full) | Apache-2.0 (LICENSE re-read this session: full text) | one idea: summarise only from the transcript and add nothing. The service, endpoints and email step are not taken. No file or text copied, so the NOTICE terms do not apply |
| openai/skills, commit 49f948faa9258a0c61caceaf225e179651397431: `skills/.curated/speech/SKILL.md` (grep of the disclosure and custom-voice lines, plus its accessibility reference), `skills/.curated/transcribe/SKILL.md` (workflow and validation lines) | Apache-2.0 (per-skill `LICENSE.txt` re-read this session; the repository root has none) | the AI-voice disclosure line and the habit of validating generated transcripts. No file or text copied |
| elevenlabs/skills, commit 269e5f0e5a4cf296a8a38beb166245b89d5e2c1c (grep for consent, clone and cloning, then the voice-changer line) | MIT (LICENSE re-read this session: "Copyright (c) 2024 ElevenLabs") | only the observation that the voice-conversion skill suggests cloning from a sample with no consent step |
| NoizAI/skills | No LICENSE file | Idea-only; nothing taken and nothing re-read this session |

## Removed
1. **Every vendor parameter**: model ids, voice names, rate limits, character limits, cloning-strength scales,
   streaming settings and formats. They expire and are runtime.
2. **Every podcast-platform loudness or bitrate figure.** None was read on a platform page in the session; the
   Apple requirements page carries none; figures remembered from elsewhere were not written.
3. **The show-notes skill's service, endpoints, protect flag and email-summary step**: dependence on one
   third-party site (rule B).
4. **Everything legal.** No statement of what a regulator or a court requires; no named statute; the earlier
   review's FTC item (not read from the page) is not used.
5. **Runtime podcast pipelines and stub skills** met in the earlier review (synthetic two-host generation, a
   template-only studio skill).

## Not verified
1. **Apple's required-tags page** (its address is a script-rendered help page that returned no content) and the
   **artwork specification** (the artwork page reached described channel placements and gave no feed-image
   specification). Nothing in this block states a tag requirement, an explicit-content rule or an image size.
2. **ITU-R BS.1770** and the EBU documents on loudness metering and loudness range were not read; this block
   defines no measurement procedure and names the measures only as the EBU page does.
3. **Any streaming platform's loudness or audio-quality page.** None read, so no figure.
4. **Platform content policies on cloned voices and music**, and **any primary source on music licensing**
   (recording versus musical work, sync versus master): not read. §4 is a question list, not verified.
5. **The repository licence of the Podcast Namespace** was not read; only facts are used.
6. **The full RSS 2.0 text** beyond the digest (language and ASCII rules).
7. **The fetch tool returns a digest**, so figures such as the redirect period were not checked against raw HTML.
8. **Nothing was tested on a real show.** No claim that this list reduces errors was measured.
9. **Current text of the sources** may have changed after the read date (`skills/source-freshness`).

## Own guidance (not sourced)
The stable-identifier discipline as a rule about regeneration, the permalink-flag advice, the fetch-and-compare
check and the server test (§1); the measure-naming, final-export, re-measure and two-kinds-of-episode advice and
the way to write a platform figure (§2); the transcript-as-release-line, link-from-the-notes, generated-text
review, source line per note item, guest briefing and withdrawal plan (§3); all of §4 beyond the two sourced
lines; the pass, fail, unknown list (§5); the guardrails.

## Related blocks
`skills/accessibility`, `skills/source-freshness`, `business/data-protection`,
`business/ai-content-disclosure-and-provenance-pitfalls`, `business/marketing-claim-substantiation-pitfalls`,
`business/licence-compliance`, `business/social-publishing`, `business/video-brief-and-storyboard`.
