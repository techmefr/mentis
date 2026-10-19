# chaos-experiment: origin and source stamps

> Provenance of `skills/chaos-experiment`. Read it when a rule has to be traced to its source or checked for
> freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from a published source, never run against a real system by us.

## Sources (read 2026-10-19, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Principles of Chaos Engineering, https://principlesofchaos.org/ | Published site, idea only | Definition, steady-state output as the focus, control versus experimental group, vary real-world events, run in production, automate continuously, minimise blast radius and the experimenter's responsibility to contain fallout |
| alirezarezvani/claude-skills, skill `chaos-engineering` (SKILL.md and its experiment-design and principles references, read in full; commit 19392f7a08264ed00486a251f5b2098321771f94; LICENSE file re-read: MIT, Alireza Rezvani 2025) | MIT | Own-guidance points flagged in the text: abort criteria written first (the source adds it as a fifth principle of its own), one fault, written plan before the run, rollback tested, learning question, stop first and investigate after, write-up with owned follow-ups |

## Removed
1. **Every number**: blast-radius shares, budget percentages, durations, abort thresholds, cadence targets,
   maturity-level timelines and the source's success metrics.
2. **The tool chooser and the fault catalogue tied to named products**, and the three Python scripts and the
   slash command: a runtime and perishable detail, not a method.
3. **The "always run in production from day one" tone**: the principles favour production for authenticity;
   here the step-wise route and the stop conditions in §1 points 6 to 9 temper it, as own guidance.

## Not verified
1. The principles site was read through a fetch tool's summary; the original's wording was not compared.
2. The history, the book list and the maturity model in the source skill were not independently checked and
   are not used.
3. No injection tool's documentation was read; none is named in the rules.
4. Whether any team following this block gets value is unknown: it is the thinnest of the three blocks written
   on 2026-10-19 and the one most worth dogfooding on a real game day before relying on it.

## Related blocks
`skills/slo-design`, `skills/feature-flag-lifecycle`, `skills/failure-classification-before-retry`,
`skills/blameless-incident-review-pitfalls`, `skills/incident-comms-pitfalls`, `skills/dotnet-conventions` §8,
`skills/source-freshness`.
