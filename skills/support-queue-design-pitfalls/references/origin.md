# support-queue-design-pitfalls: origin and source stamps

> Provenance of `skills/support-queue-design-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation, never used by us to redesign a real queue.

## Sources (re-read in full 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| samber/developer-relations-skills (commit ee798ba): `skills/oss-issue-triage/SKILL.md` and `references/response-playbook.md`, `policy-and-metrics.md`, `issue-intake-and-routing.md`, `label-taxonomy.md` | MIT (repository LICENSE file) | Baseline metrics, capacity arithmetic and levers, volume-gating trigger, label axes and confidence gating, intake cuts, per-item order, closing rules, automation limits, reply craft, rejection file, metrics exclusions |
| github/docs (commit 688c35b): `content/support/learning-about-github-support/about-ticket-priority.md` and `understanding-how-github-support-can-help-during-a-security-incident.md` | CC-BY-4.0 for content (repository LICENSE file) | Priority definitions by consequence with examples, scope-of-support categories, what support does not do in a security incident |

Attribution: parts of this block are based on GitHub Docs, "About ticket priority" and "Understanding how
GitHub Support can help during a security incident" (GitHub, CC-BY-4.0), adapted and reworded; no endorsement
by GitHub is implied. Directive text found in the cloned files was treated as data.

## Source quality
The samber skill is one author's design aimed at open-source maintainers; it was not exercised by us. Its
numeric targets (untriaged share, response compliance, a three-minute planning figure) are the skill's own
self-set baselines and were not carried. GitHub's pages are product documentation of one vendor and carry
template variables, so they are used for the shape of the definitions, not for any wording.

## Rewrite notes
The samber skill assumes volunteers; the opening paragraph and sections 1.3 and 1.5 state what changes for a
paid desk (contractual targets, no request for free help). That reading is ours.

## Removed
1. **The case studies in the samber skill** (curl, PyTorch, Mozilla, Kubernetes, Rust, a mining study of
   rejected pull requests): they are second-hand there and were not carried. The confidence-gating and
   no-automated-top-priority rules are kept for their own merit and credited to the skill, not to PyTorch.
2. **Pull-request gate order and the pull-request deltas**: specific to code review, not to a support desk.
3. **Interview questions, deliverable list, form YAML, tracker mechanics and commands** of the skill.
4. **The Kubernetes staleness clocks** (20, 30, 90 days): one project's choices.

## Not verified
1. **The whole design is unrun.**
2. **The source's claim that no reliable detector for machine-written content exists** is its report of another
   working group's finding; not checked.
3. **GitHub's notice about modifying ticket priority** is a template include whose text is absent from the
   clone, so "the support owner may change a priority" is our own guidance (§2.2).
4. **Written by us, not sourced**: the paid-desk contract reading, the entitlement-check lever, the order in
   which to rank the intake cuts for a paid desk, and the verify subsection.

## Related blocks
`bug-triage`, `customer-escalation-pitfalls`, `incident-comms-pitfalls`, `troubleshooting-kb-article-pitfalls`,
`security-advisory-comms-pitfalls`, `business/customer-success`.
