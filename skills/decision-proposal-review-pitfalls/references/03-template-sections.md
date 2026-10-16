# decision-proposal-review-pitfalls §3 — Template sections

These come from two templates, each one project's choice; keep what earns its place for your size of change.
The section lists are examples.

## 3.1 Proposal sections worth keeping (Kubernetes template)
1. **Summary and motivation**: at minimum these two, which are easy if the idea was preflighted.
2. **Goals and non-goals**: what the change is for, and what it is explicitly not for.
3. **Risks and mitigations** and **drawbacks**: a separate "why should this not be done" section.
4. **Alternatives**: other approaches considered and why each was ruled out. They need not be as detailed as
   the proposal, but must express the idea and why it was unacceptable. Rust adds that proposals that are
   disingenuous about drawbacks or alternatives tend to be poorly received. Own guidance: an alternative
   nobody would choose is a strawman; delete it.
5. **Test plan**: what tests at which levels will show it works.
6. **Rollout, upgrade and rollback**: how it is enabled and turned off, how a rollout can fail, which
   signals should trigger a rollback.
7. **Monitoring and troubleshooting**: how an operator knows it is used and working, and known failure
   modes with how to detect them (the template asks for this when targeting a later maturity stage).
8. **Optional**: user stories, infrastructure needed.

## 3.2 Decision-record fields (MADR template)
1. **Decision drivers**: the qualities, concerns or constraints that matter for this decision.
2. **Considered options with pros and cons**: each option with good, neutral and bad points.
3. **Consequences**: good and bad results of the chosen option.
4. **Confirmation**: how compliance with the decision will be checked, for example a review or a test.
5. **Roles**: decision-makers, consulted (two-way communication) and informed (one-way communication).
6. **Status and date** of the last update, and "more information" for evidence and when to revisit.

For the template of an architecture record and for superseding, `documentation-adr` is the reference; the
fields above are another project's ideas to compare with it, not a replacement.
