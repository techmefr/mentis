# § 5 — Secrets, tests, and the plan-review-apply pipeline

> Section 5 of `skills/terraform-conventions`. Read it when a secret appears in a configuration, when tests are
> written, or when a pipeline is wired. The pipeline's job is to make "what was reviewed" and "what was applied"
> the same thing.

1. **Check the runtime floor before using a feature.** The language gains features every minor release, and a
   suggestion that needs a newer runtime than the project pins fails at init or plan. The ones that matter here:
   `moved` blocks 1.1, `optional` with defaults 1.3, import and check blocks 1.5, the native test framework 1.6,
   mock providers 1.7, ephemeral values 1.10, write-only arguments 1.11 (the vendor's pages for tests, ephemeral
   values and write-only arguments state their own floors; the others are from the secondary guide). OpenTofu
   numbers its releases differently, so read its own documentation for each. Pin the runtime (§4.5) and write the
   floor next to any feature that needs a recent one.
2. **Keep secrets out of state, and out of version control, in this order of preference.** First, do not give
   Terraform the secret at all: the resource reads it at run time from the cloud's secret manager, using an
   identity, so the value never enters the configuration. Second, where the provider offers it, use a write-only
   argument (Terraform 1.11), whose value is sent to the provider and never stored in state or plan; pair it with
   an ephemeral value (1.10) as the source. Third, if neither exists, accept that the value is in state and
   protect the state accordingly (§2.2). Marking a variable sensitive only hides it from output; it does not keep
   it out of state or the plan file. Never put a secret in a variable default or a committed variable file.
3. **A generated password lives in the secret manager from the start.** Let the secret store generate and own it,
   and have the resource reference it; a random-password resource in the configuration writes the value to state.
4. **Choose the test layer by what it must prove.** Static checks (format, validate, lint, a policy or security
   scanner over the configuration) are free and run on every commit. The native test framework (Terraform 1.6) runs
   assertions: by default each run block applies for real and creates real infrastructure, so choose the
   plan-only mode for checks on values derived from inputs, which is fast and free, and the apply mode for
   computed values (identifiers, generated names), which exist only after creation. With mock providers (1.7) the
   logic of a module can be unit-tested without a cloud. Integration tests in real infrastructure run on the
   main branch or on a schedule, in a sandbox account, with resources tagged and cleaned up automatically.
5. **Test a module through its examples.** The minimal and complete examples are the fixtures: they prove the
   documented usage works, and they stay honest because the tests run them. A module without a test is a module
   whose next provider upgrade is a leap of faith (§3.9).
6. **Pipeline stages: validate, test, plan, review, apply,** in that order, and the apply uses the **saved plan**
   produced by the plan stage and shown to the reviewer, never a second plan computed inside the apply job (the
   world may have moved between the two). Pin the runtime and providers, commit the lock file, run the security
   scan on every path that can reach an apply, apply to production only through a protected environment with
   approval, and keep the plan output as the audit record.
7. **Give the pipeline a short-lived identity, not a stored key.** Use the CI system's federation with the cloud
   (an OIDC trust) so each job gets a temporary credential. The trust must pin the audience and the subject to the
   specific repository and branch or environment, with no wildcard across repositories or organisations, since a
   loose subject lets any repository assume the role. Separate roles per environment so a non-production job
   cannot touch production. Fall back to static keys only where federation is unavailable (`devops-conventions`
   §1.3 and `security-hardening` §4 for the secret handling).
8. **Scanners are a gate, not a report.** Run a static scanner over the configuration for the classic defects
   (unencrypted storage, open network rules, public buckets, default networks, overly broad identity grants), fail
   the build on the severities you decided on, and record exceptions by rule with an owner and a date rather than
   by turning the scanner off. A scanner passing is evidence about configuration, not about what is deployed.
9. **Cost and cleanup are part of the test design.** Tests that create real resources need unique names to avoid
   collisions between parallel runs, a tag that marks them as test resources, and a scheduled sweep that removes
   what a crashed run left behind.

**Sources:** the vendor's documentation on testing (`.tftest.hcl`, default apply behaviour, plan mode, mock
providers 1.7), on sensitive data in state (ephemeral 1.10, write-only 1.11, sensitive is stored in state and
plans), on provisioners and on the plan command (saved plans), read 2026-10-02; the open terraform-skill guide
(Apache-2.0) for the pipeline stages, identity-federation subject pinning, scanner-as-gate and drift-alert
practice. Points 3, 5, 8 (exception handling) and 9 are reasoning of ours. The CI-system-specific details
(trust-policy fields per cloud) are deliberately left to the platform's own documentation.
