# release-provenance-and-sbom-pitfalls §2 — Provenance and signing

> Part 2 of `skills/release-provenance-and-sbom-pitfalls`. Read it when artefacts are signed or attested.
> **No source for this section was read**: it is own guidance from general knowledge of supply-chain practice.
> The build-provenance framework's level names and the signing tools' options were not opened; re-read the
> specification in force before quoting any level, field or flag. Where the schema read for §1 says something,
> it is cited as such.

1. **State what each artefact claims.** Own guidance: a signature says "this key vouched for these bytes"; a
   provenance statement says "this builder produced these bytes from this source with these inputs". They answer
   different questions; a release that has only a signature cannot tell a customer which commit or which build
   it came from. Decide which claim you owe and write it in the release notes.
2. **Bind the claim to a digest.** Own guidance: attach the evidence to the cryptographic hash of the exact
   file, not to a name or a tag. Tags move; a digest does not. Symptom: an attestation exists but the artefact
   downloaded by users has a different hash because it was repacked after signing. Fix: hash after the final
   packaging step and sign that.
3. **Prefer short-lived credentials to a stored key.** Own guidance: a signing key kept as a long-lived secret
   in the pipeline is a target and a rotation burden; identity-based, short-lived signing, tied to the
   workflow that ran, removes the stored secret. Whichever is used, a build triggered by an untrusted change
   must not be able to read the key (`skills/ci-workflow-hardening`, `skills/gha-trust-boundary-pitfalls`).
4. **Build in an environment the producer controls, from a known source.** Own guidance: provenance is only as
   strong as the builder: a hosted, ephemeral build that takes pinned inputs and cannot be altered from the
   job's own steps gives a stronger statement than a laptop build. Record the builder, the source revision and
   the dependency lock state. The framework's levels grade this in steps; the level definitions were not read,
   re-read before relying.
5. **Verify once, from outside, and keep the command.** Own guidance: after the first signed release, run the
   verification as a consumer would, from a machine that did not build it, against the downloaded artefact, and
   keep the exact command in the release checklist. Symptom: months of signed releases that no one can verify
   because the identity or policy was mistyped. For the verify step of one hosted attestation action see
   `skills/release-changelog-pitfalls` §3.
6. **Sign the SBOM or bind it as evidence.** The schema read for §1 allows an enveloped signature on the document
   and on its parts in a JSON signature format; own guidance: either sign the SBOM, or attach it to the
   artefact's attestation, so the list cannot be swapped without detection.
7. **Say what you do not attest.** Own guidance: a signature does not mean the code is safe, and provenance does
   not mean the dependencies are free of flaws. State the scope, so a customer does not read "signed" as
   "audited".
8. **Pin and review the tools that sign.** Own guidance: the signing step is itself part of the chain. Pin
   actions and tools by digest, restrict who can change the release workflow, and review a change to it like a
   change to production code (`skills/ci-workflow-hardening`).
9. **Score the repository's own hygiene separately.** Own guidance: automated checkers of a repository's
   practices (branch protection, pinned dependencies, reviews, signed releases) exist; none was read here, so
   their checks are not listed. If you adopt one, treat the score as a to-do list, not a badge.

## Checks (own guidance)
1. The signature or attestation names the digest of the file users download.
2. The verification command is in the checklist and was run from another machine.
3. No signing secret is readable by a build started from an untrusted change.
