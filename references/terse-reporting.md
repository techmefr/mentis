# Terse reporting: what an agent returns to the operator

> **Single source (rule B).** Every agent that hands back a report cites this file from its `TRACE`
> section instead of describing its own format. Written 2026-08-14, alongside the input-side pass:
> shrinking what an agent reads does nothing about what it writes, and a review that finds four things
> was returning two pages.

**This governs the report, not the artefact.** A report is what the operator reads once and acts on: a
review recap, a gate verdict, an audit, a research answer. An artefact is what someone else reads later:
code, an MR comment, an ADR, a spec, a changelog. Artefacts keep their own register — an MR comment is
short and direct because that is its style rule, not because tokens are expensive.

## The format

1. **Verdict first, one line.** What you concluded, before anything else. `PASS`, `NEEDS_WORK`,
   `4 findings, 1 blocking`, `nothing found`. The operator must be able to stop reading there.
2. **Then one line per item**: `file:line — the fact — the consequence`. The fix only when it fits on
   the same line.
3. **Then the artefact paths**, if you wrote any (payload file, dump, report).

Nothing else. No third-level structure, no per-item paragraph, no closing summary.

## What never appears in a report

- **A preamble.** No "I analysed the 12 files of the diff", no "here is what I found". The findings are
  what you found.
- **A restatement of the instruction.** The operator wrote it; they know what they asked for.
- **A justification of a finding that a click verifies.** You cite `file:line`, that is the
  justification.
- **A method narrative.** How you got there matters only when the result is surprising or when you had
  to work around something — then it is one line, at the end, not a walkthrough.
- **A count of what you did.** Files read, greps run, tools called: none of it is a result.
- **A closing offer.** No "let me know if you want more detail". The operator asks when they want more.

## Where terseness must not cut

The register drops the connective tissue, never the meaning. Three things always survive intact:

- **Negation and polarity.** "nothing found on the parsing path" must never compress to "parsing". A
  dropped negation inverts a verdict, and a gate that reports the opposite of what it found is worse than
  a gate that says nothing.
- **The verdict word itself**, spelled out. Not an emoji, not a colour, not an implication.
- **The uncertainty marker.** "confirmed", "worth digging into", "speculative" is information; flattening
  three confidence levels into one flat list is a loss, not a saving.

If a finding genuinely needs three sentences to be understood, it gets three sentences. The rule removes
what carries nothing, not what is hard.

## The one thing that stays long

**Evidence stays quoted in full.** A test output, an error message, a log line, a diff hunk: cite it as
it is. The whole doctrine is default = failure, and a paraphrased proof is not a proof.
