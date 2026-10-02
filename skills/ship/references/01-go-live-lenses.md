# ship §1 — The data and operations lenses

> Section 1 of `skills/ship`. Read it before the change leaves draft for a release, in addition to the
> concerns the block lists (speed, discoverability, accessibility, secrets and trust boundaries). Each lens ends
> in a verdict per item: **verified** (with the evidence) or **residual** (named, owned, accepted).

1. **Reversal.** For every change that alters stored data or a contract, answer in one sentence how to undo
   it and how long that takes. A schema change follows expand, migrate, verify, contract, so that old and new
   code both work during the rollout (`skills/deprecation-migration`). Run the migration on production-shaped data
   in a dry run and read the statements. A destructive step is its own change with its own approval. "We would
   restore a backup" is an answer only if the restore has been tried and its time is known.
2. **Release switch.** Can the new behaviour be turned off without a deploy (a flag, a config value)? If not, is
   the previous build one command away and has that command been run in a rehearsal? A release with neither is
   a one-way door and is named as one.
3. **Idempotence of what repeats.** A job, a webhook handler, an import, a message consumer will run twice
   sometime. Show where the second run is recognised and ignored, or does no harm. Delivery order is not
   guaranteed either; say what happens when event two arrives before event one.
4. **Authenticity of inbound calls.** A webhook or callback verifies the sender's signature before it parses
   any field it then trusts, and rejects a replayed one.
5. **Configuration validated at startup.** Required settings are named in one place, read once, and validated when
   the process starts; a missing one stops the start with a message that names it. A service that boots
   with a half-set configuration and fails on the first request, at night, is the failure this lens targets. Test
   and live credentials are separated, and a test key cannot reach a live service by accident.
6. **Health that tells the truth.** There is a probe that proves the dependencies the service needs are
   reachable, separated from a cheap "the process is up" probe, and the deploy waits on the right one. A probe that
   always answers yes is worse than none.
7. **Logs that diagnose without leaking.** A failure produces a line that says what failed, for whom, with
   which identifier, without a secret, a token or personal data. Check one real failure path by causing it.
8. **The critical journey, exercised end to end.** The two or three paths whose failure ends the release (sign-in,
   payment, the main write) have been driven for real on the release candidate, not inferred from unit tests. If
   they could not be run, that is a residual item with the reason (`skills/gate` §8.7).
9. **Ownership.** Someone is named who watches the release and who decides to reverse it, and they have the
   access to do it. A rollback plan nobody is allowed to execute is a document.
10. **Watch after the release against a baseline.** Before it goes out, record the numbers that describe a healthy
    service (error rate, latency, queue depth, the count of the business event); afterwards compare at fixed
    intervals for a fixed window and decide at the end of the window. A comparison with no baseline is a feeling.
11. **The verdict is capped by blocking facts, not by a score.** Any of these caps it at "do not release":
    sensitive data without access control; a non-idempotent payment or fulfilment handler; a migration that cannot
    run safely; a secret in a client bundle, a log or the history; no way back for a high-impact change. A
    green pipeline with a blocking fact is blocked; a failing pipeline with no blocking fact is a smaller
    problem. A number between 0 and 100 hides which fact decided it.
12. **Write the residual list into the MR description** (`skills/mr-conventions` §3): item, owner, reason. The
    human who approves reads what was knowingly left.
