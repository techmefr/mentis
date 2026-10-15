# terraform-ci-delivery-pitfalls §3 — Drift and reproducibility

Two different things are called drift here: the pipeline producing a different plan from the one on a laptop, and
the real infrastructure drifting from the code. The causes and the answers differ.

## 3.1 The CI plan differs from the local plan
1. **Usual causes** (terrashark): an unpinned runtime or provider, a missing or stale lock file, an apply job that
   plans again instead of using the stored plan (§1.1), and different credentials or authentication between the
   plan and the apply.
2. **Diagnose in this order** (terrashark): compare the runtime versions local versus CI, diff the lock file in the
   pull request, check that the apply consumed the stored plan file, check that the policy stage ran on this path.
3. **Pin the runtime and provider ranges and commit the lock file**, so CI and laptop resolve the same versions;
   the pinning decision itself is in `terraform-refactor-identity-pitfalls` §3.2 (terrashark; terraform-skill).
4. **A runtime or provider upgrade is its own change**, reviewed with its lock file diff, not folded into a
   functional change (terrashark; terraform-skill).

## 3.2 Detecting drift in real infrastructure
1. **Run a scheduled `plan -detailed-exitcode` and alert on drift.** The exit codes are `0` for no changes, `1` for
   a failed plan and `2` for changes, which is drift (terraform-skill).
2. **Never make the schedule an auto-apply.** `apply -auto-approve` on a cron silently reverts out-of-band changes
   and is listed as a model mistake (terraform-skill). A human reviews the alert and applies deliberately.
3. **Add a verify job after every apply** that runs `plan -detailed-exitcode`; a change after an apply means the
   apply did not converge (terrashark's verify stage; terraform-skill's idempotency check).
4. **Common causes of drift** (terraform-skill): manual console changes, other tools, resources deleted outside
   Terraform, provider API changes. `plan -refresh-only` shows the difference and `apply -refresh-only` records it
   in state without changing infrastructure.
5. **The alert path is the part to test.** terraform-skill's scheduled job runs the plan, treats exit code `2` as
   drift and sends it to a chat, a pager or an issue tracker; nothing in the sources fixes which. Whatever the
   channel, inject one out-of-band change and watch the alert arrive with no apply behind it.
