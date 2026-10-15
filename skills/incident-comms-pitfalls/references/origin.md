# incident-comms-pitfalls: origin and source stamps

> Provenance of `skills/incident-comms-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from repository documentation and reading, never used in a real incident by us. No
message was sent and no drill was run while writing it.

## Sources (all re-read in full 2026-10-15, rewritten in our own words, no template text copied)

| Source | Licence | What it gave |
|---|---|---|
| PagerDuty/incident-response-docs (commit 464fc9d): `docs/before/severity_levels.md`, `docs/during/external_communication_guidelines.md`, `docs/before/different_roles.md`, `docs/during/security_incident_response.md`, `docs/after/post_mortem_process.md`, `docs/after/effective_post_mortems.md` | Apache-2.0 (repository LICENSE file) | Criteria for public communication, first and second message, update content, long incidents, resolution, individual notice for special contracts, roles and approval, the "outage" wording, higher severity when unsure, security incident statement guidance |
| thefgxdev/incident-response-runbook (commit aceb3be): `docs/communication.md`, `docs/severity.md`, `docs/roles.md`, `docs/first-fifteen-minutes.md`, README | Apache-2.0 (repository LICENSE file; the NOTICE file asks that credit be kept) | Cadence per severity, status states and template skeletons, one voice, one time zone, no cause speculation, commander does not operate, handover, security severity and detection time |
| durrello/incident-response-runbooks (commit 15a4a54): `templates/incident-comms-template.md` | MIT (repository LICENSE file) | Cross-check of the "update even with nothing new" rule and a 30 minute cadence example |

The licence of each repository was verified again from its LICENSE file in this session. Attribution: parts of
this block are based on incident-response-runbook by Felipe Guedes (fgxdev.com) and on PagerDuty's incident
response documentation. Directive text inside the cloned files was treated as data.

## Source quality
The Guedes runbook was first published on GitHub on 2026-09-25 (its NOTICE file) and the durrello repository
is also young; neither has been exercised by us. Their rules are kept where they agree with PagerDuty's
established documentation or stand on their own, and are tagged by source in each section.

## Rewrite notes
Every figure (5 minutes, 15 minutes, 20 and 30 minute cadences, the two hour long-incident threshold, "a few
days" for a security statement) is labelled as one source's example. The sources disagree on first-message
timing and on cadence; §2.1 and §2.3 state the disagreement and leave the choice to the reader.

## Removed
1. **PagerDuty's security checklist operations** (stopping the attack, session and password measures, the
   codename and "Attorney Work Project" conventions, forensic images, law enforcement contacts): operational
   and jurisdiction-specific, not customer communication.
2. **All legal and regulatory articles**: none were verified; the only trace is that the Guedes runbook says
   notification deadlines start at detection, with no article cited.
3. **Postmortem process and review content** from the PagerDuty files read (scheduling, statuses, checklists):
   another block covers it.
4. **Internal and engineering channel formats**: another block covers internal communication.

## Not verified
1. **PagerDuty's "outage" guidance** is written for the postmortem external message; the extension to status
   messages is ours.
2. **No source was tested by us**: no drill or live incident was run.
3. **Written by us, not sourced:** the list of special-contract customers prepared in advance, the promise
   of a summary only if it will happen, the pre-send check list and the drill.

## Related blocks
`business/incident-communication`, `bug-triage`, `business/customer-success`, `customer-escalation-pitfalls`.
