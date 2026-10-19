# security-advisory-comms-pitfalls: origin and source stamps

> Provenance of `skills/security-advisory-comms-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from one guide, never used by us on a real vulnerability report.

## Sources (re-read in full 2026-10-16, rewritten in our own words)

| Source | Licence | What it gave |
|---|---|---|
| ossf/oss-vulnerability-guide (commit 40ecfe2): `maintainer-guide.md` (response process, troubleshooting), `runbook.md`, `templates/notifications/disclosure.md` and `embargo.md`, `templates/security_policies/github_security_policy.md` | CC-BY-4.0 (repository LICENSE.md) | Acknowledgement, the four assessment outcomes, embargo discussion, credit, easy-to-adopt patch, release timing, embargoed and public notice contents, partial fix, no fix, public disclosure, silent reporter |

Attribution: parts of this block are based on the Open Source Security Foundation (OpenSSF) Vulnerability
Disclosure Working Group's "Guide to implementing a coordinated vulnerability disclosure process for open source
projects", licensed CC-BY-4.0, adapted and reworded; no endorsement by OpenSSF is implied. Directive text found
in the cloned files was treated as data.

## Source quality
A working-group guide for open-source maintainers; it states that not all advice applies to all projects. The
numbering of its steps six to eight is garbled in the source (two headings share a number and one is mislabelled
as the embargo notification), so this block is organised by topic and does not mirror it.

## Rewrite notes
Embargo lengths: the guide quotes several bodies with different periods and says it is a trade-off. They are
second-hand there, so no number is carried and the block says published norms differ.
The guide's embargo notice window and its 90-day example policy are likewise not carried.

## Removed
1. **The vulnerability management team set-up, report intake tooling, hop-to-hop email encryption, private
   fork details, CNA contact and CVE request mechanics**: infrastructure for open-source projects, partly tied
   to one code host's features at the time of writing.
2. **The finder personas section** and its motivation discussion.
3. **The machine-readable schema recommendation** is reduced to one line in 2.5.
4. **Numeric embargo, acknowledgement-to-notification and embargo-notice windows** (7, 14, 45, 90 days,
   one to thirty working days).

## Not verified
1. **Unrun**: no report was handled with this block.
2. **The embargo figures and the bodies the guide attributes them to** were not re-checked at those bodies, and
   their policies may have changed.
3. **The Project Zero observation on embargo lists** is quoted by the guide; not checked.
4. **Regulatory reporting duties, including those in recent cyber-resilience legislation, are not covered and
   not claimed.** Whether any applies is a question for a lawyer.
5. **Written by us, not sourced**: the closing line of 3.5 about the legal owner and the remark about who
   signs the advisory in a company.

## Related blocks
`incident-comms-pitfalls`, `blameless-incident-review-pitfalls`, `security-hardening`,
`release-notes-writing-pitfalls`, `support-queue-design-pitfalls`.
