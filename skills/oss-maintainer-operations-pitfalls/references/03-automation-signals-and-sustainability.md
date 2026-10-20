# oss-maintainer-operations-pitfalls §3 — Automation, signals and sustainability

> Part 3 of `skills/oss-maintainer-operations-pitfalls`. Read it when tooling is chosen, project health is
> reviewed, or a maintainer is overloaded. Sources, read 2026-10-20: Open Source Guides, "Best Practices for
> Maintainers", "Metrics" and "Maintaining balance for open source maintainers" (CC BY 4.0). Sentences marked
> "own guidance" are ours and rest on no source read.

1. **Let machines do the repeatable checks.** The guide recommends requiring tests and other automated checks
   on every change and using tools for routine upkeep: automated releases, reviewer suggestions, review helpers,
   closing issues whose author never replied, and daily dependency update proposals. Own guidance: automate a
   task only after a person has done it by hand enough times to write its rule, and give each bot an owner.
2. **A bot's rule is written and visible.** Own guidance: a closing or labelling bot whose rule is not in the
   contributing file feels arbitrary to the person it acts on. Name it in the file, say what it does and how
   to undo it. Symptom: reporters complaining that "the bot closed my issue". Fix: a link to the rule in the
   bot's closing message.
3. **Measure to understand people, not to score them.** The metrics chapter groups useful numbers by the question
   they answer: discovery (how many people find the project and from where), usage (whether they use it),
   retention (contributor counts, first-time and repeat contributors, open versus opened issues and pull
   requests, types of contribution) and maintainer activity (how long an issue stays open, how long a pull
   request takes to merge, whether stale items are closed). Pick a few that bear on a decision you have to
   make; the chapter's closing advice is to use numbers to learn about people.
4. **Read a rising open count as a request for help.** The guide says too many open issues or pull requests
   suggests the project needs help with triage and review. Own guidance: treat the trend, not the absolute
   count, as the signal, and pair it with the age of the oldest unanswered item.
5. **Know what unbalances you.** The balance guide lists causes: users write mostly to complain and rarely to
   thank; not saying no; working alone; too little time or money; conflicting demands, for instance an employer
   whose interests differ from the community's. It also asks you to name your own motivation for maintaining
   the project, since that decides what you can drop.
6. **Watch for the signs and act early.** Own guidance: dread at opening notifications, snapping at newcomers,
   a backlog you avoid and sleep you lose are the early signals. The cheapest responses come first: narrow the
   scope, shorten the reply promise, hand a module over, or pause.
7. **Use the community and boundaries to sustain it.** The guide suggests leaning on the community to share the
   load, having several points of contact so that one person can rest, exploring funding, resting outside the
   project, and setting limits as simple as a sentence about what you will and will not work on.
8. **It is allowed to pause.** The guide says it is fine to stop for a while and to put yourself first. A pause
   is announced, with a date to review it and a named person for anything urgent; an unannounced silence reads
   as abandonment.
9. **Make the pause or exit cheap to execute.** Own guidance: archive the repository or mark it unmaintained
   with a note on forks, rather than letting issues pile up under a project nobody reads. Link to this block's
   hand-over file from §2.

## Checks (own guidance)
1. Each bot is named in the contributing file with its rule and its owner.
2. The metrics reviewed each cycle are written down with the decision each one informs; any that informs none
   is dropped.
3. There is a written statement, kept current, of what the maintainers will not do.
