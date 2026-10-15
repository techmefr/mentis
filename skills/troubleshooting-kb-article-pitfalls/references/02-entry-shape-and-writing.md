# troubleshooting-kb-article-pitfalls §2 — Entry shape and writing

What the reader arrives holding decides the shape, and six parts decide whether they leave unblocked.

## 2.1 Choose the shape from what the reader arrives with
1. **Error reference entry**: the product emits a stable identifier and the reader arrives with an exact
   string.
2. **Troubleshooting how-to**: symptoms without a code; the reader arrives with a description of
   misbehaviour.
3. **Known-issues entry**: the cause is confirmed and the fix is not shipped; the reader arrives suspecting it
   is not their fault.
4. **The shapes are not ranked.** The evidence picks the shape. A coded error written as prose loses the string
   match; a symptom forced into a code table loses the diagnosis.
5. **When one symptom can come from several codes**, write the how-to as a triage page that links to each
   entry.

## 2.2 The six parts, in order
1. **Message**: the error text verbatim in a fenced block, copied from a real run, with only the genuinely
   variable parts replaced by obvious placeholders.
2. **Applies to**: versions, platform, plan, configuration. Without it the reader cannot tell whether the entry
   is about their case.
3. **Cause**: one or two sentences on what actually went wrong.
4. **Fix**: numbered executable steps, branched per cause, ordered by how often each check is the real cause
   per minute of the reader's time. A ten-second check that is never the cause still costs a step. Several
   causes give several cause and remedy pairs, in order of fall-back.
5. **Confirm it worked**: the output or state that proves it. "It stopped erroring" also describes a second
   failure hiding the first.
6. **Still stuck**: where to escalate and what to attach.

The source calls parts 5 and 6 its own additions and the ones teams drop first.

## 2.3 Writing rules
1. **Keep cause and fix separate.** A reader who knows the cause skips to the steps; one who is guessing needs
   to confirm the cause before running commands.
2. **Write in the reader's vocabulary.** They know the symptom, not your subsystem names.
3. **Never call a fix "simple", "easy" or "just one step".** It is not working for them now, so the word
   reads as blame.
4. **Each cause and remedy pair stands alone**, so it still makes sense when scanned or when lifted out of the
   page.
5. **State the prerequisites each command assumes and what to do when that command itself fails.** Steps
   written on a healthy machine routinely fail on the reader's broken one.

## 2.4 Template

```
Title: the exact error string

Applies to: versions, platform, plan

Message
  the error text, verbatim

Cause
  one or two sentences

Fix
  If CAUSE A: numbered steps
  If CAUSE B: numbered steps

Confirm it worked
  the output or state that proves it

Still stuck
  watched channel, what to attach
```

## 2.5 Verify
Check each draft for the six parts in this order and for the two words in §2.3.3 ("simple", "just"). Read the
fix as someone who has only the page.
