---
name: podcast-publishing-pitfalls
description: "Use when a podcast episode or an audio file is about to be published or a show is being moved: an episode feed edited so every episode looks new, an enclosure that does not match the file served, a loudness number nobody measured or sourced, a transcript nobody can find, show notes that say more than the audio, a guest who was not told what is published, a synthetic or cloned voice, or music with no licence on file. A stable feed identity, a fetched and checked enclosure, a measured and sourced loudness figure, a published transcript, notes traced to the transcript, and a pass, fail or unknown pre-publish list."
---

# podcast-publishing-pitfalls

Business layer (`business/README.md`), marketing and communication. What goes wrong when an episode is published
is quiet and cumulative: a title edit that makes players treat the whole back catalogue as new, a file length
that does not match the file, a loudness number copied from memory, a transcript that exists but is linked
nowhere, show notes that claim something the audio never says, a voice used because a tool accepted a sample, a
music track with no licence kept. This block is the checklist around the moment of publishing, in five parts.

What it does not cover: how audio is recorded, edited or generated; the accessibility obligations themselves for
audio and video (`skills/accessibility` §7, which this block links to rather than restates); whether a claim in
an episode or sponsor read is substantiated (`business/marketing-claim-substantiation-pitfalls`); personal data
in a recording (`business/data-protection`); labels and provenance marks on AI-made content
(`business/ai-content-disclosure-and-provenance-pitfalls`); recording the licence of a code dependency
(`business/licence-compliance`); where and when social posts go out (`business/social-publishing`).

It states method only. It names no podcast-platform loudness figure, because none was read on a platform page; it
carries one broadcast figure with its source and date (§2). Voice and music rights (§4) are a method for asking
the right questions, not legal advice, and name no statute. It was written without audio or legal expertise; a
person who owns the show decides (`business/README.md`).

## When
- An episode is about to be released, rescheduled, edited after release or removed.
- A feed is changed: new host, new feed address, renamed files, re-encoded audio.
- A loudness target is being chosen or claimed for a release.
- A transcript, captions file or show notes are being written, generated or reviewed.
- A guest is recorded, a voice is synthesised or cloned, or music or stock sound goes under speech.

## Steps

**Read only the section the task meets.** §5 is the pre-publish list; open it last, before release.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Feed and file: identity that never changes, the enclosure triple fetched, dates, escaping, file names, moving a feed | a feed or an episode file is created, edited or moved | [`01-feed-and-enclosure.md`](./references/01-feed-and-enclosure.md) |
| 2 | Loudness measured, not assumed: which measure, on the final file, one sourced number or none | a target is chosen, a file is exported, or a figure is quoted | [`02-loudness.md`](./references/02-loudness.md) |
| 3 | Transcript as a release artefact, and show notes traced to it; sponsor disclosure; guests; withdrawal | the text that goes with the audio is written or reviewed | [`03-transcripts-and-notes.md`](./references/03-transcripts-and-notes.md) |
| 4 | Whose voice, whose music: consent, scope, disclosure of synthetic voice, licence kept with the episode (method only) | a guest, a cloned or synthetic voice, or music is involved | [`04-voice-and-music-rights.md`](./references/04-voice-and-music-rights.md) |
| 5 | The pre-publish list with pass, fail, unknown | just before release | [`05-pre-publish-list.md`](./references/05-pre-publish-list.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the pre-publish list (§5) with every line marked pass,
fail or unknown and the evidence for each pass (the fetched enclosure, the measurement and its source, the
transcript link, the licence on file); any loudness figure written with its page and date or the words "none
published"; the show notes with a source line (transcript time or file) per claim. The person who owns the show
reads it and releases; nothing here certifies an episode.

## Guardrails
- Set an episode's identifier once and keep it through every re-host, rename and title change. Never regenerate
  it to "refresh" an episode (§1.1).
- Fetch the enclosure and compare size and type to the feed. Never trust the feed text alone (§1.2).
- Measure loudness on the final export, after the last encode, and name the measure. Never write a platform
  loudness number from memory; read the platform's page in the session and cite URL and date, or write "none
  published" (§2.1 to §2.3).
- Publish the transcript where the audio is, or one link away, and review any generated text against the audio.
  Never ship generated text unread (§3.1, §3.2).
- Trace every claim, name, number, link and timestamp in the notes to what is said. Never add to the audio
  (§3.3).
- Tell guests what is published and where, and decide how a published episode is corrected or withdrawn before
  launch. Never leave removal to be invented on the day (§3.4, §3.5).
- Get a recorded yes, for this use, from the person whose voice is cloned, and write the synthetic-voice notice
  where listeners meet it. Never clone a voice because a tool accepts the sample (§4.1, §4.2).
- Keep the licence and receipt for every music or sound item with the episode. Never treat "royalty-free" as
  "cleared" (§4.3).
- Mark each pre-publish line pass, fail or unknown with evidence. Never turn an unknown into a pass (§5).
- Rights and consent items are method only, not legal advice; send them to a person who owns that question
  (`business/data-protection`, `business/ai-content-disclosure-and-provenance-pitfalls`).
- This block was written from public pages and three repositories, never run by us, and without audio
  expertise. Sources and open points are in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten in our words from the RSS 2.0 specification, the Podcast Namespace tag pages, Apple's podcast feed
requirements and feed-move pages, the W3C transcripts page and WCAG 1.2.1 understanding page, the EBU R128 page,
and three skill repositories (Apache-2.0 and MIT), read 2026-10-20. 🟡: never run by us, written without
expertise in the function. Details in [`references/origin.md`](./references/origin.md).
