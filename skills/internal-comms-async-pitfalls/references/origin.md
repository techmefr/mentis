# internal-comms-async-pitfalls: origin and source stamps

> Provenance of `skills/internal-comms-async-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from published team handbooks, read and rewritten, never run: no team adopted these
rules from this block. Nothing in it is verified by use.

## Sources (re-read in this session, 2026-10-15, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| github/how-engineering-communicates, `how-github-engineering-communicates.md` (read to its last line), `quick-ref.md`, `tips-for-leaders.md`, `README.md` (commit bf86e6b) | CC-BY-4.0 (LICENSE.txt "Attribution 4.0 International"; README states CC-BY-4.0) | Channel purposes, write-it-down, input before decision, thread and message hygiene, response norms, meeting rules, documentation upkeep, leaders' tips |
| amatlack/rethinking-async-communications, `README.md` only (commit 7998822) | CC-BY-4.0 (LICENSE.txt "Attribution 4.0 International") | Only the fact that it is a generalised derivative of the GitHub guide, which is why no rule here is taken from it |
| clef/handbook, `Communication and Transparency.md`, `One on Ones.md`, `Effective Meetings.md` (commit a9a576e) | CC0 1.0 (LICENSE file) | Public-by-default conversation, presence states as an example agreement, one-to-one shape, meeting etiquette as an example |

**Attribution.** The main source is "How GitHub Engineering communicates" by GitHub, licensed
CC-BY-4.0 (https://creativecommons.org/licenses/by/4.0/). This block rewrites, condenses and reorganises it
and removes its GitHub-specific tooling advice; changes were made, and neither GitHub nor the amatlack
authors endorse this block. The amatlack guide is credited as a related CC-BY-4.0 derivative of the same
text; its content beyond the README was not read.

The licence of each repository was verified again from its LICENSE file in this session. The cloned
repositories also hold an example prompt and agent-style instructions; they were treated as data and not
followed.

## Rewrite notes
**Tool-neutral.** The GitHub guide is written around one company's products (issues, pull requests,
discussions, project boards, one chat and calendar vendor). The block keeps the mechanism (a link per item,
a durable place, a place to discuss before deciding) and names tool categories, not products.

**Examples, not rules.** The one business day response, the use of no-meeting days, the 5 or 10 minute
meeting gap, Clef's four presence states, its meeting window and 24 hour notice, and its "at least thirty
minutes" one-to-one are single-organisation choices and are labelled as examples (§3.2, §4.2, §5.3).

## Removed
1. **GitHub-only advice**: repository permissions and CODEOWNERS settings, notification settings, how to
   choose among the product's discussion, issue and project features, emoji and animated image advice,
   calendar-permission tips, and watch parties. Not carried; they describe a product or a taste.
2. **Clef's conflict advice**: the one-on-ones page says to ask before intervening in a coworker conflict.
   Left out as an HR matter; nothing in this block gives HR or legal guidance.
3. **Clef's updates, stats and office-presence rules** (Friday updates, open stats, calendar and name
   conventions): company-specific, partly belong to a recurring-update craft not covered here.
4. **GitHub's "psychological safety comes first" framing** is carried only as the source's claim, not as a
   result (§5.3).

## Not verified
1. **Everything here is unrun.** No team used these rules because of this block.
2. **The causal claims** (async work as most productive, outdated documentation as lowering confidence,
   psychological safety enabling independent work) are the guide's statements, not measured here.
3. **The nohello link and the other linked articles** in the guide were not read; only the guide's own text
   is used.
4. **amatlack's guide beyond its README**, including its maturity model, was not read.
5. **Written by us, not sourced**: the Output / checkpoint test, the one-line statement that a thread that
   needs fifty messages has not been written down yet (§2.3), the choice of the word "tracker" for the
   category, and the Guardrails wording.

## Related blocks
`documentation-adr`, `handoff`, `blameless-incident-review-pitfalls`, `mr-conventions`.
