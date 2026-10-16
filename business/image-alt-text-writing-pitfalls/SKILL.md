---
name: image-alt-text-writing-pitfalls
description: "Use when alt text is written or reviewed for images in posts, pages, newsletters or decks: deciding whether an image needs text at all (decorative, informative, active), how context changes the wording, phrasings to avoid, caption duplication, logos and linked images, charts and other complex images, and why generated or keyword text fails."
---

# image-alt-text-writing-pitfalls

Business layer (`business/README.md`), communication. `business/social-publishing` says alt text must be on
every image and `skills/seo` lists it as a check; neither says how to write it or when to leave it empty.
This block is the writing side: the few mistakes that make alt text useless to the people who depend on it.

Accessibility standards and their criterion numbers were not opened here. For a conformance claim, cite the
standard itself (WCAG, or RGAA in France), not this block.

## When
- Publishing or reviewing images on a page, a social post, a newsletter or a deck.
- Setting up a content workflow where editors fill an alt field.
- A tool proposes to generate alt text automatically, or an SEO checklist asks for keywords in it.

## Steps

**Read only the part the task meets.**

| Part | Covers | Read it when | File |
|---|---|---|---|
| 1 | Attribute versus text, and the three kinds of image: decorative, informative, active | deciding whether an image gets text | [`01-attribute-and-three-kinds.md`](./references/01-attribute-and-three-kinds.md) |
| 2 | Writing the text: context, phrasings to avoid, captions, logos, keywords | an image needs text and you are drafting it | [`02-writing-the-text.md`](./references/02-writing-the-text.md) |
| 3 | Complex images, audio and video, and who must write it | a chart, a video or a generated description is involved | [`03-complex-media-and-authorship.md`](./references/03-complex-media-and-authorship.md) |

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: for each image, a decision (decorative, informative
or active) and either an empty attribute or a text written by someone who looked at the image in its
page, with no caption copy and no keyword string; a text equivalent next to each chart; captions or a
transcript for audio and video.

## Guardrails
- Never omit the attribute; decorative images get an empty one (part 1).
- Never write alt text without looking at the image where it is used (parts 2 and 3).
- Never copy the caption into the alt text, and never stuff keywords (part 2).
- Never lengthen the alt attribute to carry a chart; put a text alternative beside it (part 3).
- Never publish machine-generated alt text unreviewed (part 3).
- This block is a method from public accessibility guidance, never run by us on a real content set. A
  second human read, ideally by someone who uses a screen reader, is warranted. Sources and open points are
  in [`references/origin.md`](./references/origin.md).

## Origin
Rewritten from three posts of the A11Y Project site (Apache-2.0 repository, individually authored posts,
attributed) and the accessibility page of the Microsoft style guide (CC-BY-4.0), read 2026-10-16. 🟡:
never dogfooded. Details in [`references/origin.md`](./references/origin.md).
