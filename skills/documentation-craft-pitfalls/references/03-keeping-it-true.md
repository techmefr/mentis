# documentation-craft-pitfalls §3 — Keeping it true

> Part 3 of `skills/documentation-craft-pitfalls`. Read it when a page is reviewed, or will outlive its author.
> Source, read 2026-10-20: Microsoft Writing Style Guide, "Final publishing review" (CC BY 4.0). Most of this
> part is own guidance from the craft and is marked so; it rests on no measured source.

1. **A page is a claim about the system, and claims go stale.** Own guidance: every statement about behaviour,
   a path, a flag, a version or a command is a claim that a code change can falsify without touching the page.
   Symptom: a reader follows the page, fails, and stops trusting every page. Fix: list the falsifiable claims
   when the page is written, so the next editor knows what to recheck.
2. **Prefer a claim a check can read over a claim a person must remember.** Own guidance: generate the part that
   mirrors code (an option table, a command list, a schema) from the source; run snippets and commands in CI or
   in a script before release; check links. A statement nothing can verify gets an owner and a date instead.
3. **Run the steps as a stranger.** Own guidance: a person who did not write the page, on a clean machine or a
   clean checkout, follows it literally. Every place they stop is a missing prerequisite or an unstated
   assumption. This is the single most revealing review and the one most often skipped.
4. **Give every page an owner and a reason to be revisited.** Own guidance: the owner is a team or a role, not a
   departed person (in a one-maintainer repository the owner is that maintainer, said once in the file that
   states how to contribute); the trigger is an event (a release, an incident, a dependency upgrade), not a calendar
   reminder nobody answers. A page with neither is a candidate for deletion.
5. **Delete or mark what is no longer true, do not leave it.** Own guidance: a wrong page is worse than none,
   because the reader cannot tell. Mark the page deprecated with the date and the replacement link, or remove it
   and redirect.
6. **Write a runbook for the person at three in the morning.** Own guidance: state the symptom that makes you
   open the page, the first safe action, how to confirm it worked, how to roll back, who to wake and what not to
   touch. Keep background out of the path; link it. A runbook step that needs judgement names the decision and
   the signal that settles it.
7. **Execute a runbook before it is needed.** Own guidance: a runbook nobody has run since it was written is a
   hypothesis. Run it in a rehearsal after each significant change to the system, and record what was wrong. For
   restore procedures see `skills/backup-restore-drill-pitfalls`; for the review after an incident see
   `skills/blameless-incident-review-pitfalls`.
8. **Get a second opinion from someone far from the work.** The guide advises asking a person removed from the
   project to read as the customer, and removing whatever trips them up however attached you are to it.
9. **Read it aloud and read it back to front.** The guide suggests reading the text aloud, then sentence by
   sentence backward, and leaving it a day before rereading; edits jump out. Own guidance: for a short page this
   catches more than a second proofread of the same pass.
10. **Try removing things.** The guide says to remove words, sentences, headings and whole sections and keep the
    removal if nothing is missed, and to avoid repeating the opening summary or later notes verbatim. Check: a
    section whose deletion nobody notices was decoration.
11. **Do not duplicate a fact across pages.** Own guidance: state a fact once, in the page that owns it, and link.
    Two copies drift at different speeds and the reader finds the stale one.
12. **Say what was not verified.** Own guidance: "not tested on Windows" or "numbers from a 2024 run" in the page
    costs one line and saves the reader an afternoon.
13. **Make the doc change part of the code change.** Own guidance: a behaviour change that leaves its page for
    "later" ships a false page today. Check: the review of a change that alters a command, a default or an error
    lists the pages it touches, or says none do. Fix: the page edit travels in the same change, reviewed by the
    same person.
14. **Review accuracy and wording as two passes.** Own guidance: a subject expert checks that the statements are
    true, a reader far from the work checks that they can be followed, and one person doing both misses the
    second. Symptom: a page that is correct and that nobody can follow. Fix: name which pass each reviewer owns.
15. **A claim about privacy, security or behaviour has to match the shipped code and every other page.** Own
    guidance. Symptom: one page says "no tracking", "no cookies" or "works offline" while another page, or the
    code, describes analytics, a stored identifier or a network call; the opener and the footer are the usual
    places for the older sentence. Check: search all pages for the absolute words (no, never, always, only,
    offline, nothing is sent) and for each hit search the code and the other pages for the thing denied; where the
    sentence is generated, fix the generator, not the output. Fix: state what is collected, by what, and what is
    not, in one place, and link to it from every page that mentions it.
16. **Commands, addresses and pins must agree across pages and with the pipeline.** Own guidance. Symptom: one
    page says install with one command and another with a different one that behaves differently; a dev-server
    address that omits the path prefix the site is served under; a "pinned" version that is a moving alias; a
    command table missing steps the pipeline runs; the same procedure written twice with small differences. Check:
    for each task (install, run, test, add an entry) list every page that describes it and compare command,
    address and version; compare the command table with the pipeline's steps; confirm that a stated pin is an
    exact version, not a range or an alias; confirm a generated section has a check in the pipeline that fails
    when it is out of date. Fix: one page owns each procedure and the others link to it (§3.11).
