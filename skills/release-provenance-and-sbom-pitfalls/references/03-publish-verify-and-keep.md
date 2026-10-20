# release-provenance-and-sbom-pitfalls §3 — Publishing, verifying and keeping the evidence

> Part 3 of `skills/release-provenance-and-sbom-pitfalls`. Read it when the release is published or a flaw is
> announced. Source for the SBOM facts, read 2026-10-20: the CycloneDX specification JSON schema and README
> (Apache-2.0). The framework's verification page (digest match, see §2.2) backs point 1; everything else is own guidance and rests on no source read.

1. **Match the published file to the shipped bytes.** Own guidance: after the release is public, download the
   artefact from the place users get it, hash it, and compare with the digest in the SBOM and the attestation.
   Symptom: the registry or a mirror serves a repackaged file. Fix: publish digests beside the artefact and
   compare in the release job.
2. **Publish in the place consumers will look.** Own guidance: attach the SBOM and the attestation to the
   release, or serve them at a stable address next to the artefact, using the conventional file name so tools
   find them. A document that exists only in an internal bucket answers no customer.
3. **Make the SBOM searchable the day a flaw is announced.** Own guidance: store every release's document in a
   place where one query returns "which releases contain component X at version Y". Symptom: an advisory
   arrives and the answer takes days of manual unpacking. Fix: an index keyed by package URL and release.
4. **Answer "are we affected" with a statement.** The schema supports attaching vulnerability findings to
   components and describing completeness. Own guidance: for each announced flaw, state affected, not affected
   with the reason (the code path is absent, the component is not shipped), or under investigation, and update
   it as the facts change. A bare "not affected" with no reason is unusable (`skills/security-advisory-comms-pitfalls`).
5. **Reissue deliberately.** The schema asks for a version bump when a document changes and a unique serial per
   BOM. Own guidance: when a correction is needed after publication, raise the version, keep the serial, and
   note the change in the release; do not replace the file under the same version.
6. **Keep the evidence as long as the support period.** Own guidance: customers and regulators ask about old
   releases. Keep the SBOM, the attestation and the verification procedure for every release still supported,
   and record the date when each leaves support. The legal duty, if any, is a question for the compliance
   owner (`skills/cra-scope-and-role-determination-pitfalls`), not legal advice.
7. **Consume suppliers' SBOMs with the same questions.** Own guidance: when a supplier sends one, check the
   lifecycle phase, whether components carry package URLs and hashes, whether the graph states completeness,
   and whether the document's component matches the file you received. Reject a document that cannot be tied
   to the delivered artefact, and ask for one that can.
8. **Automate the whole chain and test it.** Own guidance: generation, validation, signing, publishing and a
   verification run belong in one pipeline job, tested on a throwaway release before the first real one. An
   evidence step done by hand is skipped under pressure.
9. **A deployed site has no release; give the deployed output an identity anyway.** Own guidance. Symptom: the live
   site cannot be tied to a commit, so "which version had the flaw" and "what was live on that day" have no
   answer, and an SBOM, if one is ever wanted, has nothing to point at. Check: is there a build identifier (a
   content hash, a commit hash, a run number) in the output, and does anything link it to the commit and to the
   pipeline run that published it. Fix: write the commit hash into the output or a public file at build time, and
   keep the run's artefact for as long as you may need to answer. Whether to go further (an SBOM, an attestation)
   is a decision for the owner and not a defect; report it as a decision.

## Checks (own guidance)
1. A job downloads the public artefact and compares its hash with the SBOM and the attestation.
2. One query lists the releases that contain a given component and version.
3. The retention period for each supported release is written down and enforced.
