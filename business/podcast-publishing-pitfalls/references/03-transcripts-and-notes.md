# podcast-publishing-pitfalls §3 — Transcripts, show notes, guests, withdrawal

> Part 3 of `business/podcast-publishing-pitfalls`. Read it when the text that goes with the audio is written
> or reviewed. Sources, read 2026-10-20: the W3C WAI transcripts page, the WCAG 2.2 Understanding page for
> success criterion 1.2.1, the Podcast Namespace `transcript` tag page, a show-notes skill repository
> (Apache-2.0) and a transcription skill repository (Apache-2.0). Own guidance is marked. Not legal advice
> (`business/README.md`).

## 3.1 The transcript is a release artefact
1. **Audio-only needs one.** The W3C page states that for prerecorded audio-only content a transcript is
   required at Level A, and the 1.2.1 page describes the alternative as text that gives the same information
   as the audio. The obligations are in `skills/accessibility` §7; this block only makes the transcript a line
   on the release list.
2. **Video with sound is different.** The same W3C page says captions are Level A for prerecorded video with
   audio and a transcript is Level AAA. A video podcast needs captions first; a transcript does not replace
   them.
3. **Put it where the audio is.** The W3C page says make it easy to find: on the same page as the media, or a
   link directly under it; HTML is the usual format and a podcast transcript can be plain paragraphs with
   speaker names. Own guidance: the link goes in the episode's notes, not in a folder.
4. **Say who speaks and what is heard.** The W3C page recommends naming speakers and including non-speech sound
   that is needed to understand the content, with clarifying text clearly separate from the audio, for
   instance in brackets. Timestamps only where they help.
5. **Link it from the feed.** The Podcast Namespace page puts the `transcript` tag on the episode (more than
   one allowed, one per format), with `url` and `type` required, `language` optional (the feed language when
   omitted) and `rel="captions"` meaning a timed captions file. Own guidance: publish the format a person can
   read first.

## 3.2 Generated text is a draft
Own guidance, in line with the transcription skill read, whose workflow ends by validating the output (quality,
speaker labels, segment boundaries): someone reads generated text against the audio before it is published,
and the check is recorded in the list (§5). Names, numbers and product terms are checked first.

## 3.3 Show notes are traced to the transcript
1. **Every claim, name, number, link and timestamp in the notes is found in what is said.** The show-notes
   skill read has one rule worth keeping: summarise only from the transcript and add nothing beyond it. Own
   guidance: keep a source line per item (a time, or a file).
2. **A link in the notes is opened before release.**
3. **Sponsor reads and affiliate links are disclosed in the notes as well as the audio.** Method only, no law
   stated: see `business/marketing-claim-substantiation-pitfalls` for the claims and
   `business/ai-content-disclosure-and-provenance-pitfalls` for labels.

## 3.4 Guests
Own guidance: before recording, tell the guest in writing what will be published, where, in what form (audio,
video, transcript, clips) and for how long. A recording that holds personal data goes through
`business/data-protection`; this block does not restate it.

## 3.5 Correction and withdrawal, decided before launch
Own guidance: write down who may unpublish or correct an episode, what is removed (the file, the notes, the
transcript), and what cannot be recalled (copies players and directories already hold). A correction is a new
file at the same identifier (§1.1), never a new episode, unless the person owning the show decides otherwise.
