# programmatic-video-pitfalls §4 — Choose the approach, then the tool, then read the licence

> Part 4 of `skills/programmatic-video-pitfalls`. Read it when an approach, a framework or a template is being
> chosen. Sources, read 2026-10-20: the video skill of an MIT marketing skills repository (read in the clone);
> the licence file, the terms page and the fundamentals page of a frame-based React video framework, and the
> credits and licence of an Apache-2.0 HTML-to-video framework (clone). The React framework's pages came
> through a fetch tool that returns a small model's digest, not the verbatim page. Sentences marked "own
> guidance" are ours. Licence texts change: this is a record of what was read on the date, not a ruling.

## 4.1 The approach first
1. **Decide what kind of video the need calls for before naming a tool.** The marketing skills repository lists
   this as the first common mistake ("starting with tools, not strategy"). Own wording of the choice, by what
   the picture has to show:
   - a title, a callout, a chart, a user interface rebuilt to be animated: drawn by code, because the text
     stays sharp, is editable and can be re-rendered with new data;
   - a real product doing a real thing: a screen recording, with code adding titles and highlights on top;
   - a scene that cannot be filmed: generated footage, accepting that what it shows is invented;
   - the same person saying many versions of a script: a recorded presenter or an avatar service, whose terms
     and consent requirements have to be read;
   - a few seconds of looping motion on a web page: not a video project at all (`skills/webperf` §5,
     `skills/web-animation-pitfalls` §1).
2. **Readable text and real interfaces do not come from a generative video model.** The marketing skills
   repository says such models handle readable text poorly and that specific products are for programmatic
   drawing instead. Treat it as a claim of that source, not tested here, and as a reason to try text and
   interface in code first. If any generated or synthetic media ends up in the output, follow
   `business/ai-content-disclosure-and-provenance-pitfalls`.
3. **One-off or template?** A video made once is cheaper to build by hand than to generalise; a video that will
   be re-rendered with new data is where drawing it in code pays. Own guidance: write which of the two this is
   before building a template.
4. **Do not copy a tool comparison table into a decision.** The same repository carries model and plan tables
   with prices; they date within months and the source gives none for its own date. Read the vendor's page when
   deciding.

## 4.2 The licence gate for a framework
1. **Read the licence before adopting a framework, record the conditions in a sentence with the date, and read
   it again when the team or the use changes.** The two frameworks read are licensed differently, which is the
   point of the gate.
2. **Remotion, as its own pages say on 2026-10-20 (digests):** the licence file lists who may use it free of
   charge as an individual, a for-profit organisation of up to three employees, a non-profit or not-for-profit
   organisation, or someone evaluating it who is not yet using it commercially; free use includes commercial
   video and image creation and modifying it for your own use. Anyone else needs a Company License. Copying or
   modifying the code to sell, rent, licence, relicense or sublicense your own derivative is not allowed. The
   file never calls it open source, and states that the licence "will slightly change" in version 5.0 without
   saying how. The terms page adds, as the digest has it: free use for an organisation or team of up to three
   people, where headcount counts all personnel including part-time staff and contractors who jointly operate
   it on one project; a non-profit must actually qualify, and government bodies, educational institutions,
   commercial subsidiaries and trade associations are excluded without written permission; running a rendering
   service that lets end users bring their own code is not allowed without prior written approval; licensing
   is per use case; and the Company License has several kinds that differ by how it is used (the terms page
   names per-render and per-seat kinds and an enterprise kind; prices are on the vendor's page and are not
   recorded here). The file says "employees" and the terms say "people", so the two pages are not worded
   identically: **read both, and ask the person who owns licences before relying on either.** State it as
   source-available with a free tier and a paid one, never as open source.
3. **An open-source licence is a different kind of answer.** The HTML-to-video framework read is Apache-2.0
   (full text in its licence file), which allows commercial use, modification and redistribution under stated
   conditions, including keeping notices and the licence text with any copied file. Its credits file also lists
   a media toolkit under MPL-2.0 used in its editor and a speech model under a Creative Commons attribution
   licence that its tooling downloads on request. Reading the licence of the framework does not settle the
   licence of what you bundle or download with it.
4. **A timeline or animation library inside the project has its own licence.** The HTML framework's credits
   record that the animation library used in its templates is under a proprietary no-charge licence and "not an
   OSI open-source licence"; `skills/web-animation-pitfalls` §1 holds the one-sentence record of it. Do not
   assume the framework's licence covers the library.
5. **None of this is legal advice.** The block states what the pages said; whether a particular company's use is
   allowed is a question for whoever owns licences, and it goes to them early (`business/licence-compliance`).
6. **A skill or template repository with no licence file is idea-only.** Copy nothing from its text; rewrite
   the idea (rule B in `CONVENTIONS.md`).

## 4.3 What the template ships
1. **Fonts, sounds, images and footage in a template carry their own licences.** In the HTML framework's tree
   read this session: the fonts in one style preset and in one registry block ship with SIL Open Font License
   text beside them; the credits file lists further fonts as OFL 1.1 with their licence text, a high dynamic
   range environment image as CC0, and two registry blocks that load their fonts from a font service at run time; the bundled
   sound effects are credited to a stock site under that site's content licence, which the credits file
   summarises as allowing use in videos without attribution; and the credits file lists six texture images as
   "origin to be confirmed with the author". Test fixtures in the repository carry their own source notes.
2. **So an asset whose origin is not recorded is not cleared.** Own guidance: for each font, sound or image that
   ends up in a delivered video, write the source and licence next to it; an asset whose licence is unknown is
   replaced, not shipped.
3. **A font fetched at run time breaks §1.3 and is a data transfer to its host.** Bundle the file if its licence
   allows it, and keep the licence text with it.
4. **A voice, a face or a musical work is not covered by the framework's licence either.** Music, a cloned
   voice or a person's likeness need their own permission; where personal data is involved,
   `business/data-protection` comes first.
