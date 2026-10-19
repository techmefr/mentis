# ai-content-disclosure-and-provenance-pitfalls §3 — Detectors and marks

## 3.1 Detectors are advisory
1. **A review aid that spots visible patterns in AI-style prose is advisory.** The design note's review
   sheet highlights surface and structural patterns for a human reviewer, and its thresholds are never
   wired into a publish gate (indranilbanerjee contentforge, design note of 2026-08-13, component B).
2. **State what the aid is not.** The note says it detects visible style and structure and has no
   relationship to any statistical watermark (same note, "What it is NOT").
3. **Own guidance:** a detector score is never the reason to publish, to reject, or to accuse a writer. It
   points a human at passages to read.
4. **Own guidance:** do not rely on a detector's reported accuracy figures. The note cites a paper for them
   and they were not checked here.

## 3.2 Never evade marks
1. **Do not remove, hide or evade provenance marks or watermarks.** The design note's first decision is no
   removal or evasion feature, and that its text-polishing tool is for quality and is never to be marketed
   as a watermark tool (same note, "Why").
2. **A stripping or cleaning tool used to avoid labelling is a decision for the content owner and for
   legal**, not a formatting step. Own guidance.

## 3.3 A label does not replace the human
1. **A label says how the content was made; it does not say a person stood behind it.** Own guidance: the
   named author or owner still reads the text and answers for it (`business/content-creation`).
2. **A disclosure sentence is true only if its claims are** (part 1), so the label is the last step, never
   a substitute for the review.
