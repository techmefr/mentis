# release-changelog-pitfalls §3 — Build provenance attestations

Sources: the README of actions/attest-build-provenance at 9d57eef, read in full 2026-10-16. It is a short file; it does not list workflow permissions, inputs or failure messages, so none are stated here.

## 3.1 What an attestation is
1. **It binds a subject to a statement about how it was built.** The subject is a named artifact together with its digest; the statement is a SLSA build provenance predicate in the in-toto format.
2. **It is signed with a short-lived certificate issued by Sigstore,** which means (own reading) no long-lived signing key has to be kept.
3. **It is then uploaded to GitHub's attestations API and associated with the repository whose workflow produced it.**

## 3.2 Plan and visibility decide whether it can exist
1. **Public repositories:** attestations are available on all current GitHub plans.
2. **Private and internal repositories:** they need a GitHub Enterprise Cloud plan. On the Free, Pro and Team plans only public repositories qualify, and the legacy Bronze, Silver and Gold plans have none.
3. **Own guidance:** check the plan before adding the step to a private repository's workflow, since a step that cannot work there is a defect found only when someone tries to verify a release. The README does not say how the action fails, so do not assume it fails loudly.
4. **The signing infrastructure follows visibility:** a public repository uses the public-good Sigstore instance, and a private or internal one uses GitHub's private Sigstore instance.

## 3.3 Use the generic action for new work
1. **From version 4, this action is only a wrapper around `actions/attest`.** Existing workflows may keep using it, and new ones should use `actions/attest`, whose own README holds the usage (not read here).
2. **Documentation for earlier versions of the wrapper is kept at an older tag,** which the README links; a workflow still on an old version should be read against that tag.
3. **Own guidance:** pin whichever action is used by commit, as in `ci-workflow-hardening`, and migrate the wrapper to the generic action on the next change to the workflow instead of as a separate project.

## 3.4 Verify what was produced
1. **The command-line tool has an `attestation verify` command** for checking an artifact against its attestation; the README links its manual.
2. **Own guidance:** run it once against a real artifact from the first workflow run, from a machine that did not build it, and keep the command in the release checklist. An attestation nobody has verified is a claim with no reader.

## 3.5 Checks (own guidance)
1. Confirm the repository's visibility and plan against 3.2 before the step is added.
2. After the first run, verify the attestation of one artifact and note the repository identity it reports.
3. Search the workflows for the old wrapper action and list them for migration.
