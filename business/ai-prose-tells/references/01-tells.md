# The tells, the false positives, and what to keep

> Reference for `business/ai-prose-tells`. Read it at the audit step, once a draft exists.

## 1. Catalogue of tells, by family

Judge families, not words. Each entry names the mechanism, so a new variant is recognisable.

1. **Hollow vocabulary.** Words that carry approval and no information: robust, seamless, powerful,
   comprehensive, leverage, streamline, cutting-edge, delve, crucial. Test: can a measurement or a name
   replace it? If yes, replace it; if no, delete it.
2. **Scope inflation.** A small change dressed as a milestone: "a pivotal step toward a better developer
   experience" for a renamed flag. Test: does the sentence size match the diff?
3. **Vague attribution.** "Experts agree", "it is widely known", "best practices suggest". Name who or
   cut it.
4. **Chatbot closure.** "I hope this helps", "let me know if you have questions", "feel free to". It
   belongs to a conversation; a README is not one.
5. **Announced plans.** "In this section we will explore", "Let's dive in", "Below is an overview".
   Start with the content.
6. **Rule of three.** Triplets used as rhythm: "fast, reliable, and scalable". One triplet is normal; a
   triplet in every paragraph is a template.
7. **Negative parallelism.** "Not just X, but Y", "It is not about X, it is about Y". The frame creates a
   contrast nobody asked for.
8. **Staccato.** A run of very short sentences for effect. "It works. It scales. It ships."
9. **False ranges.** "From small teams to large enterprises", "from setup to deployment", where the two
   ends are not a scale.
10. **Actorless passive.** "Errors are handled", "the cache is invalidated". Who does it, and when? Naming
    the actor often exposes that nobody checked.
11. **Generic conclusion.** A final paragraph restating the document, or promising a bright future.
12. **Formatting excess.** Bold on every key phrase, emoji as bullets, a heading over three lines.
13. **Hedging stack.** "may potentially", "could possibly", "it is generally considered". Hedge once,
    where the uncertainty is real, and say what the uncertainty is.

## 2. Clusters, not instances

- Count by family, per paragraph. One family once is silent. Two families in a paragraph is a note.
  Three, or one family repeated past the threshold in the severity table, is a finding.
- A finding quotes the sentence, names the family, and proposes a positive replacement drawn from the
  source, never a synonym.
- A clean paragraph next to a flagged one is evidence the author can write; fix the flagged one in that
  voice.

## 3. Do NOT flag (false positives)

This section is mandatory in a detection block; do not delete it to shorten.

- **Legitimate lists of three** that are three things: three supported platforms, three steps.
- **Technical terms** that happen to be suspect words: "robust" in a statistics context, "leverage" in
  finance, "comprehensive" in a test-plan title that is literally a coverage claim backed by a table.
- **Formal register by convention**: licences, security advisories, legal notices, RFC-style text.
- **Short sentences in a procedure.** Numbered steps are staccato by nature.
- **Conventional headings** in changelogs and READMEs (Added, Changed, Fixed; Installation, Usage).
- **Non-native English** with unusual phrasing. Awkward is not machine-made; do not "correct" a person.
- **Quoted text**, error messages, command output, code.
- **A hedge that carries real uncertainty** and names it.
- **Bold used for the one warning** that must not be missed.

## 4. Signs of human writing to preserve

- A specific detail only the author could know: the failing input, the version, the surprise.
- An opinion with a reason, including a dissent from the common approach.
- Admitted limits: "this does not handle X yet".
- Uneven rhythm: a long sentence next to a short one because the idea needed it.
- Names, dates, numbers, links to the actual issue.

Editing must not sand these off. If the audit would remove a human sign, the audit is wrong.

## 5. The positive requirement

Every document leaving this filter carries at least: what changed or what this is, for whom, and one
specific, checkable detail (a figure with its conditions, a command, an input that used to fail). A
filter made only of prohibitions produces blank prose; the requirement is what keeps the text useful.
