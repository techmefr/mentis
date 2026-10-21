# secret-leak-response-pitfalls §2 — The response

> Section 2 of `skills/secret-leak-response-pitfalls`. Read it when a credential has leaked or a scan
> reports an active one. Source: Kingfisher at commit `8244f7b` (its defender-workflow, secret-revocation
> and baseline pages), read 2026-10-15; its commands are named only to show the shape and are version-bound.
> The first action on a real leak is to tell the credential's owner; this section is what you do with them.

1. **Work in this order: scan, validate, alert, map, contain, remove, rescan.** Kingfisher's workflow scans
   the repository and its history, validates the detected credentials against the provider, alerts on the
   active ones, maps access when the impact is unclear, then revokes or rotates, removes the credential from
   source and scans again. Skipping to "remove the line" leaves a live credential; skipping validation
   spends the owner's time on dead ones. Containment (revoke or rotate) comes before cleanup. GitHub's guide to removing sensitive data says the same: revoke or rotate first, because rewriting history is costly and does not reach forks, old clones, cached views or pull request references.
2. **Act only on what you are authorised to act on.** The source says to run scans, validation, impact
   mapping and revocation only against repositories, accounts and provider APIs you are authorised to
   access. Validation and mapping make authenticated requests with the leaked credential. Own guidance: a
   credential found in someone else's repository or in a third party's log is reported to its owner, not
   validated.
3. **Alert narrowly and keep the full report.** The source filters notifications to findings whose
   validation succeeded (`only-active`), suppresses an alert with no findings, and keeps inactive,
   unavailable, skipped and inconclusive findings in the report without paging anyone. Sending alerts to a
   restricted channel is part of the design, and its webhook URLs are credentials (§1.9). Do not combine
   an active-only policy with turning validation off, since without validation nothing is known to be
   active. Alert delivery is best-effort, so a failed webhook is a warning and CI monitoring still matters.
   To handle noise, add known findings to the baseline rather than loosening the alert policy.
4. **Map the impact when the credential's reach is unclear.** Validation says a credential is accepted;
   mapping (the source calls it blast radius) collects identity, permissions and reachable resources for
   supported providers, which separates a low-impact development key from one that reaches production. It
   makes more authenticated requests, so the authorisation rule in §2.2 applies to it as well, and a mapping
   failure does not make a finding inactive.
5. **Pass the credential on standard input, not on the command line.** The source says passing the value
   on standard input keeps it out of shell history and the process argument list, and shows `revoke` and
   `validate` taking `-` for it. Its reports contain ready-to-run commands only when unredacted, and that
   output contains the credential, so review it only in a protected terminal and never paste it into a
   shared shell, a ticket or a chat. With redaction on, those commands are omitted.
6. **Revoking does not remove the copies.** The source says revocation does not remove the credential from
   history, forks, logs, caches or artifacts, and that the follow-up is: remove it from current source,
   clean retained copies where appropriate, rotate dependent workloads, and review the provider's audit
   logs for use between exposure and revocation. Treat the exposure as starting at the push, not at
   discovery (`skills/security-hardening` §4.6, `skills/ci-workflow-hardening` §3.5).
7. **An unknown outcome is not a success.** In the source's revocation behaviour, a custom HTTP mutation is
   never retried, and a 429 after a mutation was submitted is an unknown outcome, since it may already have
   been applied. For AWS, a lost response after IAM may have accepted a change is reported as an unknown
   outcome (`revocation_status: unknown` in JSON), not as failure and not with a more destructive fallback.
   Verify the key's state with separately authorised credentials before trying again, and do not retry a
   permission failure expecting a different answer. Whatever tool you use, record "unknown" in the incident
   notes as unknown.
8. **Never fall back to ambient credentials when revoking.** The source states Kingfisher never falls back
   to ambient AWS credentials implicitly; the responder opts in to a named profile, or to the SDK's default
   chain for an instance or workload role, and names the target user. Own guidance: a tool that revokes
   with whatever credentials the shell happens to hold can act as the wrong principal.
9. **Prefer the reversible action, and know what survives it.** In the AWS flow the default is to
   deactivate the key, which is reversible; deleting is irreversible and must be chosen explicitly.
   Deactivating or deleting a long-term key does not invalidate STS sessions already created from it, which
   stay usable until they expire or are revoked separately, and temporary credentials cannot be revoked
   through the access-key APIs. Check the provider's documentation for what its own revocation leaves
   alive.
10. **Revocation can break a running workload; coordinate it.** The source says to confirm the affected
    workload and likely impact first, that some providers need extra captured values, and that some
    credentials cannot be revoked through the tool, in which case you disable or rotate in the provider's
    console. It offers a revoke action only when it can identify the exact key, and says a remediation
    shortcut should never guess which key to disable; a credential you cannot identify exactly is rotated
    by its owner.
11. **Prove the old value is dead, then rescan.** The source re-validates the revoked credential to check it
    is no longer accepted, then reruns the original scan; the old string may still be reported as detected
    but inactive if it remains in history, and it should no longer pass the active-only filter. Record the
    rescan as the closing evidence.
