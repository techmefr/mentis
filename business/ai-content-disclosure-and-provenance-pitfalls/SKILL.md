---
name: ai-content-disclosure-and-provenance-pitfalls
description: "Use when a publisher decides how to label AI-assisted content or handles provenance data on images, video and text: wording of an AI label (generated, edited, enhanced), disclosure text that must be true, keeping credentials through upload and export, recorded versus typed-in information, personal data in provenance records, advisory use of AI-text detectors, and never stripping marks."
---

# ai-content-disclosure-and-provenance-pitfalls

Business layer (`business/README.md`), communication. For publishers and editors, not for people who build
provenance tooling. `business/content-creation` says a person reads and owns what goes out under their name;
this block covers the label and the metadata that travel with the content, where the common failures are a
label that says too little, wording that claims too much, and credentials lost at upload.

Whether a disclosure is legally required, and by when, was not verified here. The AI Act, platform terms
and advertising rules were not opened: ask the owner of legal and compliance, and cite the official text,
not this block.

## When
- Choosing or writing the words of an "AI-assisted" label for a page, a post, an image or a video.
- Publishing images or video that carry embedded credentials, or sending them through a tool that
  re-encodes them.
- Deciding what a provenance record may show about a person.
- Someone proposes to run an AI-text detector as a publish gate, or a tool that removes marks.

## Steps

**Read only the part the task meets.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | The words: what the AI did, verifiable context, true claims, vendor-neutral, disclose when unsure | writing a label or a disclosure sentence | [`01-the-words.md`](./references/01-the-words.md) |
| 2 | The metadata: loss on upload, storage choices, recovery, recorded versus typed-in, personal data, redaction | credentials travel with an asset | [`02-the-metadata.md`](./references/02-the-metadata.md) |
| 3 | Detectors and marks: advisory only, never evade, the human owner | a detector or a stripping tool is proposed | [`03-detectors-and-marks.md`](./references/03-detectors-and-marks.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: label wording that says what the AI did and to which
part, a disclosure sentence whose every claim happened, a decision on how credentials are kept through the
publishing chain, a preview of any personal data a provenance record will show, and a note that detector
output was advisory. The owner of the content decides.

## Guardrails
- Never use a bare "made with AI" label when the part the AI touched is known (part 1).
- Never write a disclosure that claims a review, a check or an author that did not happen (part 1).
- Never publish an AI-edited or AI-enhanced claim without context on how the AI affected the content (part 1).
- Never assume embedded credentials survive an upload or export; check and keep the original (part 2).
- Never show personal data in a provenance record without the person opting in after a preview (part 2).
- Never use an AI-text detector as a publish gate or to justify stripping marks (part 3).
- Never remove, hide or evade a provenance mark or watermark (part 3).
- This block is a method from one standards body's user-experience guidance and one small MIT design note,
  never run by us. A second human read, including legal, is warranted. Sources and open points are in
  [`references/origin.md`](./references/origin.md).

## Origin
Rewritten from the user-experience recommendations and the AI-and-machine-learning guidance of a content
provenance standard (CC-BY-4.0 specification repository, attributed) and from one design note of a small MIT
content-pipeline plugin, read 2026-10-16. 🟡: never dogfooded. Details in
[`references/origin.md`](./references/origin.md).
