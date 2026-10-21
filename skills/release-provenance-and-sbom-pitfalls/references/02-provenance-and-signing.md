# release-provenance-and-sbom-pitfalls §2 — Provenance and signing

> Part 2 of `skills/release-provenance-and-sbom-pitfalls`. Read it when artefacts are signed or attested.
> Read 2026-10-20 for facts only, restated in our words: the build-provenance framework's levels page and its
> artefact-verification page (specification site, licence is a community specification licence, not on our
> creditable list), and the OpenSSF Scorecard checks page (Apache-2.0). The levels page read is the v1.0 one and is
> itself marked retired in favour of v1.2: re-read the specification in force before quoting any level, field or
> flag. The signing tools' options were not opened. Where a point has no citation it is own guidance; where the
> schema read for §1 says something, it is cited as such.

1. **State what each artefact claims.** Own guidance: a signature says "this key vouched for these bytes"; a
   provenance statement says "this builder produced these bytes from this source with these inputs". They answer
   different questions; a release that has only a signature cannot tell a customer which commit or which build
   it came from. Decide which claim you owe and write it in the release notes.
2. **Bind the claim to a digest.** Confirmed in the framework's verification page: a consumer checks that the statement's subject matches the digest of the artefact in hand, because expectations attach to a package name while provenance attaches to one specific artefact, so a name check alone misses a substituted or modified file. The attestation statement format (in-toto statement page, read 2026-10-20, facts only) matches subjects purely by digest, gives every subject a digest set, treats the subject name as the producer's own convention (unset or a placeholder when meaningless) and asks that subjects be treated as immutable. Attach the evidence to the cryptographic hash of the exact
   file, not to a name or a tag. Tags move; a digest does not. Symptom: an attestation exists but the artefact
   downloaded by users has a different hash because it was repacked after signing. Fix: hash after the final
   packaging step and sign that.
3. **Prefer short-lived credentials to a stored key.** Own guidance: a signing key kept as a long-lived secret
   in the pipeline is a target and a rotation burden; identity-based, short-lived signing, tied to the
   workflow that ran, removes the stored secret. (Sigstore signing overview, read 2026-10-20: the keyless flow gets a short-lived certificate binding an ephemeral key to an OpenID Connect identity, and each signing is recorded with a timestamp in a public transparency log; the page gives no validity period and does not say what a verifier must check, so pin the expected identity yourself. The cosign verification page, read 2026-10-20: every keyless example passes both the expected certificate identity and the expected issuer, and a signed file is checked with its bundle; the page does not say what happens when a flag is left out, so supply both and never rely on a default.) Whichever is used, a build triggered by an untrusted change
   must not be able to read the key (`skills/ci-workflow-hardening`, `skills/gha-trust-boundary-pitfalls`).
4. **Build in an environment the producer controls, from a known source.** Own guidance: provenance is only as
   strong as the builder: a hosted, ephemeral build that takes pinned inputs and cannot be altered from the
   job's own steps gives a stronger statement than a laptop build. Record the builder, the source revision and
   the dependency lock state. The framework's levels grade this in steps (v1.0 page): level 1, provenance exists and shows how the
   artefact was built, which catches mistakes and is easy to forge; level 2, a hosted platform generates and signs
   the provenance, which protects against tampering after the build; level 3, a hardened platform protects against
   tampering during the build, with isolated runs and protected signing secrets. The build track does not cover
   source or dependencies. Hosted-platform attestations: the GitHub artifact-attestation concept page (read 2026-10-20) says attestations alone reach build level 2 and a shared reusable workflow can reach level 3; public repositories sign through the public Sigstore instance and write to a public transparency log, while private repositories use the vendor's own instance with no transparency log; and it says generating attestations alone provides no security benefit, so verification is what delivers it (see point 5). Re-read 2026-10-20 on the v1.2 build-requirements page: the three levels are unchanged in substance (provenance naming the output digest; authentic, hosted-platform provenance; unforgeable provenance with isolated, ephemeral builds and signing secrets out of reach of user steps).
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
   actions and tools by digest (a full commit hash for an action, an image digest for a container), because a tag
   such as `v4` is a pointer its owner or an attacker can move, so a pipeline that pins by tag runs whatever the tag
   points to that day. A tag pin is a weaker, common choice: when you keep it, say so, restrict the pipeline's
   token to the least it needs, and let an update bot propose digest bumps for review, which narrows the window
   and does not close it. Check by listing every `uses:` line of every workflow and noting the form of each ref. Beyond that,
   restrict who can change the release workflow, and review a change to it like a
   change to production code (`skills/ci-workflow-hardening`).
9. **Score the repository's own hygiene separately.** Automated checkers of a repository's practices exist; the
   OpenSSF Scorecard checks page lists checks on branch protection, human code review, dangerous workflow patterns,
   token permissions, pinned dependencies, signed releases, an update tool, a security policy and a published SBOM,
   each with a risk level and a score out of ten (signed releases score higher when provenance is also present). If
   you adopt one, treat the score as a to-do list, not a badge. Its stated reasons for pinning by hash: the same
   software in checks and in deployments, a guard if a dependency is later compromised after you vetted the pinned
   one, and a counter to dependency confusion; the trade-off it names is delayed security updates, which an update
   tool offsets (consistent with point 8).

10. **Verify the build inputs, not just the signature.** Confirmed in the provenance and verification pages (v1.0, marked retired; read 2026-10-20): the externally controlled parameters are untrusted and must be compared downstream with expected values, unknown fields should make verification fail, the builder identity must be one the verifier recognises and expects (so correct code cannot be built on an unintended platform), and the canonical source repository and build type are compared too; expectations attach to a package name, formed by trust on first use, by the producer or from the source repository. A check that only validates the signature passes a build of the right code from the wrong place or with a swapped parameter. Dependencies listed in the statement are best-effort complete up to level 3, so do not read the list as a full inventory.

## Checks (own guidance)
1. The signature or attestation names the digest of the file users download.
2. The verification command is in the checklist and was run from another machine.
3. No signing secret is readable by a build started from an untrusted change.
