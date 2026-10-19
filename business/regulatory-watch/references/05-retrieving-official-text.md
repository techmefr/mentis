# regulatory-watch §5 — How retrieving official text fails

> Section 5 of `business/regulatory-watch` (the numbers 1 to 4 of that file are inline in `SKILL.md`). Read it
> when a quoted provision, a date or a version of a legal act is about to be relied on. It adds failure modes
> only; the rules to cite a primary source and to date a claim are in the steps of `SKILL.md`. Sources, read
> 2026-10-16: the `jamarpl21/prawo-pl-eli` repository (MIT, commit `d989570`), file
> `plugins/prawo-eu-eurlex/skills/prawo-eu-eurlex/SKILL.md` (source order, date and consolidation caveats); the
> `emendrix/emendrix` README (MIT, commit `97b7ad5`, v0.1.0); Regulation (EU) 2024/2847 Article 71(2), as
> published in the Official Journal, https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R2847 ,
> read 2026-10-16 (original publication, not a consolidated version). Own observations are marked. Not legal
> advice.

1. **Take the text from the official publisher, never from memory or a snippet.** The Polish skill puts the
   text of an EU provision under one source only (the Publications Office repository behind EUR-Lex) and says
   that when a web search result gives wording, it is re-read at that source before use. The web is for
   case law and commentary and for identifying the act. Own guidance: a portal, a vendor page or a search
   snippet is a lead.
2. **Identify the act by its stable identifier.** The same skill identifies an act by its CELEX number or ELI,
   not by its popular name; a CELEX number encodes the sector, year, type and number. Own guidance: write the
   identifier next to the popular name in any note, so the next reader opens the same act.
3. **One act has several dates, and the general one is not the only one.** Example read in the text:
   Regulation (EU) 2024/2847 applies from 11 December 2027 in general, but Article 14 applies from 11 September
   2026 and Chapter IV from 11 June 2026 (Article 71(2)). Read the application article of the act itself, not a
   summary of it.
4. **A consolidated version has a date, and it is not the entry-into-force date.** The Polish skill notes that
   the date in a consolidated-version identifier is the state of the law on that date, and that the entry-into-
   force and application dates belong to the base act. Own guidance: write which one you read.
5. **An act can be amended after the copy you read.** The same skill warns that dates from the base act may be
   out of date when an amending act exists, since an amendment can move them, and tells the reader to check the
   application article in the latest consolidated version. Own guidance: look for amending acts and the latest
   consolidated text before quoting a date.
6. **End of validity is not the same as partial lapse.** The skill notes that its metadata source can carry the
   end date of the whole act and the lapse dates of single provisions in one property, so a partial lapse must
   not be quoted as the end of the act. Own guidance: for a provision, read whether it is the whole act or a
   provision that is concerned.
7. **The base text is the text before any corrigendum.** The skill notes that the base act's text is the Official
   Journal wording before later corrigenda and points to the consolidated version or to the corrigendum itself.
   Own guidance: a block written from the original text (as several in this repository are) says so and tells
   the reader to read the current text.
8. **Say which language version you read.** Own guidance: the same act exists in many language versions; state
   the one read and, for a disputed wording, compare another.
9. **Record URL, date read and version with every quoted provision.** Own guidance: the version is the
   original publication or a consolidated one with its date. A claim without these three is `[verify]`
   (`SKILL.md`, steps 2 and 3).
10. **"Source not reachable" is not "not found".** Own observation, 2026-10-16: EUR-Lex answered an empty
    HTTP 202 to curl and to a page-fetch tool, and the text was readable only in a real browser. When the
    official source cannot be reached (bot wall, empty page, blocked network), say "source not reachable", mark
    the claim as needing verification, keep it out of any rule, and never fall back to memory. An empty search
    result is a different statement and also not proof that an act does not exist.
11. **An automated difference between versions is a lead.** The emendrix README describes a tool that computes
    a provision-level difference between two versions of an act and explains it with every sentence citing a
    provision that resolves, and states that it is v0.1.0 and may be incomplete, out of date or wrong. Own
    guidance: a person reads the two texts; a summary sentence that cites no provision that resolves is
    discarded.
