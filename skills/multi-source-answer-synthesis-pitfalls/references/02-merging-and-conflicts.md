# multi-source-answer-synthesis-pitfalls §2 — Merging and conflicts

> Part 2 of `skills/multi-source-answer-synthesis-pitfalls`. Read it when results from several sources are
> combined. Source: the knowledge-synthesis skill of the enterprise-search plugin of a plugin repository
> (Apache-2.0, re-opened 2026-10-20), rewritten in our own words; its confidence-weight table and ranking weights
> are not carried. Anthropic's search-results page and research-agent write-up are cited where named.

## 2.1 What counts as the same item
1. **Signals that two results are one**: nearly identical text, the same author, timestamps close together, a
   reference to the same entity (a project, a document, a decision), or one source pointing at another ("as
   discussed in the thread", "per the doc").
2. **Merge into one item that cites every place it appeared.** Use the fullest version as the main text and add
   a detail only one source holds.
3. **When the same information exists in several places, prefer the fullest, then the most authoritative, then
   the most recent**, and say which was used. For something that evolves, the most recent wins over the fullest.

## 2.2 What must not be merged
1. **Keep apart items on the same topic that reach different conclusions.** Symptom: one smooth sentence that
   silently adopts one side.
2. **Keep apart the views of different people**, even on the same topic.
3. **Keep apart versions of a decision that changed between sources** and items from different periods. A draft
   and its approved form are two items with a relationship, not one.

## 2.3 Authority and freshness
1. **Rank by authority for the question type.** For a policy: the maintained knowledge base, then published
   documents, then announcements, then conversation. For what happened: meeting notes and the conclusion of a
   thread, then confirming mail, then a mid-thread message. For a status: the tracker, then recent
   conversation, then status documents.
2. **A draft is weaker than a final document; a message in the middle of a thread is weaker than its
   conclusion.** The tiers are the organisation's to set; the structure (authority, finality, age) is what
   carries over. Own guidance: write the tiers down once per organisation instead of re-deriving them per
   answer. Anthropic's research-agent write-up supports putting them in the prompt: its early agents kept choosing
   search-optimised content farms over authoritative but lower-ranked sources, and adding source-quality heuristics to
   the prompts fixed it.
3. **Freshness weighs heavily for status and little for stable policy.** Old material is not wrong for that
   reason, but flag it as possibly out of date for anything that changes.
4. **Do not copy numeric weights for relevance, freshness and authority from any source.** They are one author's
   judgement; if weights are used, set them on this organisation's data and say they are chosen.

## 2.4 Conflicts
1. **Surface a conflict; never silently pick.** State each side with its source and date, then say which is
   likely current and why (later, more authoritative, or final) while leaving the conflict visible.
2. **A later source that supersedes an earlier one is not a conflict to hide**; it is the history of the
   decision, and the earlier discussion may still explain why.
3. **Distinguish a conflict from an omission.** Two sources that say different things disagree; one that says
   nothing is a gap (§3.4).
4. **When agreement is only apparent** (two sources repeating the same original message), count them as one
   origin, not two confirmations. Own guidance.
