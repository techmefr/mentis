# ai-content-disclosure-and-provenance-pitfalls §2 — The metadata

Content credentials are metadata attached to an asset. A publisher mostly needs to know how they get lost
and what they may reveal.

## 2.1 Loss on the way
1. **Embedded credentials are lost for good if the file's metadata is stripped.** Embedding is the most
   interoperable choice and needs no server call, but alone it is brittle (C2PA user-experience
   recommendations, 3.6.1 Embedded Content Credentials).
2. **Own guidance:** upload, resize, compress, screenshot and export can all strip or re-encode metadata.
   Test the chain with one real asset before relying on it, and keep the original file with its
   credentials.
3. **Remote storage can outlive stripping.** A manifest kept remotely can persist and be found again by
   content fingerprint, and it keeps the file smaller (3.6.2). Storing remotely has privacy and
   persistence trade-offs, which the standard says to explain to creators (3.6).

## 2.2 Recovery is not the original
1. **Watermarks and fingerprints can reconnect a stripped file to its manifest** (3.7.1, 3.7.2).
2. **Say that it is recovery.** When provenance was found through a watermark, tell people it was matched
   that way and not through a direct embedded binding (3.7.1). A fingerprint match must be nearly
   identical to the asset and the person should choose among several matches (3.7.2).
3. **Recovered credentials appear among the content's ingredients**, not as the asset's own signature
   (3.7.1).

## 2.3 Recorded versus typed in
1. **Distinguish what a capture or creation tool recorded from what a person entered afterwards**: captions,
   names, rights, a location typed in. Do not present them as equally trustworthy (3.4.1).
2. **The same field can fall on either side.** GPS data signed by a capture device is not the same as
   coordinates entered by hand; trust depends on who signed it and how it entered the record (same
   section).
3. **Use plain labels** such as "Recorded by the capture device" and "Entered by the creator" (same
   section).
4. **Be careful with custom or unfamiliar fields from earlier signers**; their meaning and privacy impact
   may be unclear, so label them clearly or leave them out (3.4.2).

## 2.4 Personal data in a record
1. **Recording personal information is opt-in.** Tell the creator up front what will be recorded and shown,
   with a preview of what viewers will see, and let them change the setting at any time. Opting out must be
   as easy as opting in (3.8.1).
2. **Creators choose which optional information to include**, such as editing history or attribution
   (3.8.2). Some may prefer not to disclose actions; the standard warns that omitting them can reduce trust
   in news, documentation and science, while leaving it to the implementer to decide when AI transparency
   outranks the creator's preference (3.8.3).
3. **Removing a name or location is a redaction**, done by a separate signed update that says the record
   changed and not the asset. Do not edit the record silently (3.5.2).
4. **Own guidance:** a photographer's name, a precise location or a person in a frame are personal data;
   route the choice to `business/data-protection`.

## 2.5 Offer a pause before export
1. **Before the final file is saved or exported, review a preview of the provenance package**, toggle the
   optional parts and decide how it is attached (3.8.5).
2. **Tell people where it is stored**: embedded, remote or both (same section).
