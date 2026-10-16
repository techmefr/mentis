# prose-lint-gate-pitfalls §3 — Rule content and limits

> Part 3 of `skills/prose-lint-gate-pitfalls`. Read it when a rule is written or a finding is disputed.
> Sources: the Elastic Vale rules repository and the Grafana writers' toolkit (Apache-2.0), the alex checker
> (MIT); each rewritten in our own words, no word lists reproduced. Points marked own guidance are ours.

## 3.1 What a rule message owes the author
1. **Explain the issue and the next action.** Elastic's authoring notes say a message should name the matched
   term, offer a replacement when one exists, and explain the context for rules that need judgment.
2. **A finding with no replacement is a complaint** (own guidance): where a substitute exists, put it in the
   message; where none does, say what to decide.
3. **Link each rule to the guide text it comes from.** Elastic's rules carry a link to the matching style-guide
   section, so a disputed finding goes to the guide and not to the rule's author.

## 3.2 An inclusive-language family, as checks
1. **Ableist wording.** Elastic ships a rule, at warning level, that flags language defining people by a
   disability. The alex checker covers the same ground with suggested replacements, such as a person-first
   phrase.
2. **Gendered and intolerant wording.** The alex checker flags gendered work titles and proverbs, and offers
   neutral terms; for the primary and secondary pair of a system it suggests terms such as primary and replica.
3. **Condescending wording.** The alex checker warns about words that tell the reader something is obvious or
   that everyone knows it.
4. **Directional language.** Elastic's rule, at warning level, replaces references to text "below" or "above"
   (forward and back references) with "the following" or "the preceding" forms, and replaces left and right
   positions in a page with the label of the element. Grafana's quick reference gives the reason as writing for an
   international audience, and lists "on the left" as the example to avoid.
5. **Link text that says nothing.** Elastic flags "click here" and suggests a verb phrase such as "go to" or
   "refer to"; Grafana's reference asks for the exact title of the linked page as the link text.
6. **These are checks, not accusations** (own guidance, from alex's stated assumption below): the message names
   the term, gives a replacement and moves on.
7. **Let teams tune the family without dropping it.** The alex checker lets a project allow some rules or, the
   other way, report only a chosen few, but not both at once; its profanity check has a sureness threshold, and
   a setting treats a pair of gendered words as an error. Decide the settings once, in the shared file.

## 3.3 What lint does not judge
1. **A linter assumes good intent.** The alex readme says so, and that it ignores a word meant literally, such
   as a quoted pronoun. It matches strings; it does not know why you wrote them.
2. **Its own authors say a person does it better.** The readme's FAQ states that the tool is not very smart and
   exists to help people who also make mistakes. A clean run means no rule matched, nothing more.
3. **A person still reads for meaning** (own guidance): accuracy, clarity, completeness and tone are outside
   what string rules can check. For claims about product behaviour, Grafana's reference for AI writers asks
   that each claim be backed by a source file or page, and marked unverified when it cannot be.
4. **Do not use lint to settle a style argument.** If two reasonable readers disagree about a finding, change
   the rule's level, its filter or its scope in the shared file, not the text of one page (own guidance).
