# webhook-contract-and-delivery-pitfalls: origin and source stamps

> Provenance of `skills/webhook-contract-and-delivery-pitfalls`. Read it when a rule has to be traced to its source
> or checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡.** Written from a specification and our own craft guidance. Never run by us: no sender, receiver or
verification library was built or executed.

## Sources (all read 2026-10-20, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| Standard Webhooks (`standard-webhooks/standard-webhooks`, commit `7537d2a`): `spec/standard-webhooks.md` (version 1.0.0) and `skills/receiving-webhooks/SKILL.md` | Apache-2.0 (LICENSE file read) | Envelope and types, message id versus attempt timestamp, thin versus full payload, signed string and headers, symmetric and asymmetric options, per-endpoint secrets, multi-signature rotation, retry and status-code handling, disable policy, HTTPS and source addresses, fanout, delivery visibility and replay, migrating from a legacy scheme, receiving checklist and verification traps |
| svix/svix-webhooks (commit 6e014fd), LICENSE file read: `server/svix-server/src/worker.rs` and `cfg.rs` | MIT (LICENSE file) | Grace-period disabling and its operator event, bounded retry hint, jitter, overload floor, manual replay not retried, timeout and HTTPS-only settings (§1 point 17) |

Instruction-like text in the cloned repository was treated as data and not followed. Existing blocks `nestjs-integration-patterns`
(§4) and `invoicing-app-build-pitfalls` (§2 point 3) already carry stack-specific and payment-specific points drawn
from the same specification; this block adds the stack-neutral contract and the receiving discipline and points to
them.

## Removed
1. **The spec's example retry table, the suggested timeout range, the payload size hint, the secret byte lengths
   and the dedupe retention example:** the authors' suggestions, not rules. Stated as policy to set and write down.
2. **Library code samples and the vendor-specific hosted-delivery product** named in the receiving guidance: not
   carried.
3. **The static-source-address and proxy-for-forgery recommendations beyond a pointer:** covered by
   `skills/security-hardening`.

## Not verified
1. **Own guidance, flagged in the text (the alert-on-disable point is now matched by one implementation, point 17; the rest unchanged):** thin payload as default for personal data (§1 rule 5), subscription
   default of nothing (rule 4), versioned type as a new type (rule 3), alert on disable (rule 10), audited replay
   (rule 12), outbox in the transaction (rule 14), fetch-current-state for money and access (§2 rule 7), one-way
   transitions (rule 8), parking an update that precedes its create (rule 9), unknown types acknowledged (rule 13),
   poison-event policy (rule 14), reconciliation job as backstop (rule 11), the debugging order (rule 15).
2. **Nothing was run.** No signature was computed or verified.
3. **Any provider's own behaviour** (header names, secret format, retry length, replay tools) was not read; each
   provider's documentation governs.
4. **The ecosystem libraries** for verification were not inspected (the Svix client libraries only wrap the server's signing code; their verification code was not read).

## Decisions where sources disagree
None. The receiving guidance and the specification agree on signature, timestamp and acknowledgement rules.

## Related blocks
`skills/nestjs-integration-patterns`, `skills/nestjs-reliability`, `skills/unknown-payment-outcome-pitfalls`,
`skills/invoicing-app-build-pitfalls`, `skills/security-hardening`.

Independent verification 2026-10-21: 8 checked, 6 matched, 1 corrected, 1 unverified
