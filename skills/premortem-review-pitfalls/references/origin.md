# premortem-review-pitfalls: origin and source stamps

> Provenance of `skills/premortem-review-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from two repositories of documentation, read and rewritten, never run: no decision
was stress-tested with this block. Nothing in it is verified by use. Both repositories are young (their
LICENSE files say 2026) and the rules are each author's practice, not consensus.

## Sources (all re-read in full 2026-10-16, rewritten in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| kharmanskyi/open-steps, `skills/os-what-could-go-wrong/SKILL.md`, `references/premortem-prompt.md` and `references/why-these-rules.md` (commit 4fa744b) | MIT (repository LICENSE file, "Copyright (c) 2026 Pavlo Kharmanskyi") | Independent attacker, brief fields and rules, order for closing gaps, depth, outside view, nine areas, no quota, risk card, cross-cutting findings, five verdicts, report shape, plain-language rules, reasons |
| phuryn/pm-skills, `pm-execution/skills/pre-mortem/SKILL.md`, `pm-execution/skills/strategy-red-team/SKILL.md`, `pm-execution/commands/pre-mortem.md` and `pm-execution/commands/red-team-prd.md` (commit c68487d) | MIT (repository LICENSE file, "Copyright (c) 2026 Pawel Huryn") | Tigers, paper tigers and elephants, launch-blocking, fast-follow and track, action plans, load-bearing claims, steelman then attack, "Fails if", ranking by impact, likelihood and cheapness, kill criterion, cheapest test, no fabrication |

The licence of each repository was verified again from its LICENSE file in this session. kharmanskyi's skill
is written as directives to an agent harness (invoke it always, dispatch an agent, print the report
whole); phuryn's files address the reader as a product manager. Both were treated as practice descriptions
and rewritten as mechanisms; no instruction was executed. kharmanskyi's `scripts/prompt.sh`, the two example
reports and its other skills were not read.

## Rewrite notes
**Sources differ: unsure risks.** phuryn's pre-mortem skill says to default to Tiger when unsure so that risks
are addressed early; kharmanskyi says to publish only risks whose chain is anchored and to accept fewer than
three. The block follows kharmanskyi and routes an unsure item to an Elephant with an investigation step
(§2.3). That routing is our reconciliation.

**Elephants.** phuryn's skill and command define the term differently (not sure it is a problem, against known
and avoided). Both senses are carried and the report names which it means (§2.3).

**Pre-mortem versus red-team.** phuryn separates the two (a pre-mortem narrates a failure that already
happened, a red-team attacks the live assumptions). The block keeps both in one place because they share the
brief and the verdict, and states the difference (§1.1).

**Harness mechanics are not carried.** The fresh-agent dispatch protocol, the language handling, the
mandatory copy of the report into the final message and the allowed-tools list belong to kharmanskyi's tool;
the block keeps the principle (an independent reader, a brief of facts) and not the protocol.

## Removed
1. **kharmanskyi's "Quick look" section list and its card count** (top three to five cards): not carried as
   rules; depth is described in §1.3, not scripted.
2. **phuryn's "launch in 14 days" framing, the "30 days" fast-follow window and "revisit 2 to 3 weeks before
   launch"**: product-launch specifics and numbers of one author, not carried.
3. **phuryn's category list** (technical, user, business, operational, dependencies): superseded by the nine
   areas.
4. **phuryn's optional cross-model second opinion**: a tooling suggestion, not carried.
5. **Further reading links** (product newsletter articles) in phuryn's files: links only, not followed, not
   carried.
6. **Go/no-go checklist and the report templates** of phuryn's command: read, not carried beyond the fields in
   §2.3.

## Not verified
1. **Everything here is unrun.** No decision was attacked with these rules.
2. **No external citation was checked**; neither source cites an outside study for the method.
3. **The other skills** of both repositories were not read, except as listed above.
4. **Written by us, not sourced**: the Output / checkpoint paragraph, the unsure-risk routing, the combined
   treatment of the two Elephant definitions, and the pairing of pre-mortem with red-team in one block.

## Verification pass (2026-10-16)
Every rule in the three references was compared with the attributed kharmanskyi and phuryn files, read in
full in the same session; the "three at most", "no date to be judged by" and "default to Tiger" statements were
re-searched and exist as stated.
- **Corrected:** none needed; no reversed or overstated rule found. The "or both" remark in §1.1 now points to
  what phuryn's command actually offers.
- **Own guidance, already labelled:** the unsure-risk routing and the combined Elephant definition.
- **Not re-verified:** that the method works; no decision was attacked with it.

## Related blocks
`assumption-validation-pitfalls`, `blameless-incident-review-pitfalls`, `experiment-design-pitfalls`.
