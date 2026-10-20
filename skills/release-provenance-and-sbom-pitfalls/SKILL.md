---
name: release-provenance-and-sbom-pitfalls
description: "Use when you ship software and must say what is inside it and how it was built: generating a software bill of materials (SBOM) for a release, reading one a supplier sent, or adding build provenance and signatures to artefacts: an SBOM produced from the wrong stage, components with no stable identifier, a dependency graph that reads as complete when it is not, a document that is regenerated with the same serial, provenance nobody verifies, and a published file that does not match the shipped bytes. CycloneDX is the worked example; provenance terms are own guidance and unverified."
---

# release-provenance-and-sbom-pitfalls

The producer's side of supply-chain evidence: the list of components inside a release, and the proof of where and
how the artefact was built. The usual failures: an SBOM generated from the source manifest when the shipped
artefact contains something else, components that cannot be matched to a vulnerability feed because they carry
no stable identifier, a dependency list that looks complete and silently is not, a new document with the old
identity, provenance generated and never checked, and a file attached to a release that describes a different
build. The three sections share one premise: **evidence is worth what a stranger can verify from the shipped
artefact alone**, so each point is about being able to match the document to the bytes.

The block owns no generator, signer or registry and names none as required. CycloneDX is the worked example
because its schema was read; the provenance part is own guidance, not read from a source. The consumer's side
(what to trust when installing) is `skills/package-manager-supply-chain-pitfalls`. Attesting a build in a hosted
workflow (its §3, build attestations) is `skills/release-changelog-pitfalls`. Whether and why an SBOM is a legal duty (for example under
the EU Cyber Resilience Act) is `skills/cra-scope-and-role-determination-pitfalls`, and not legal advice. How a
release is cut and announced is `skills/package-release`; the exposure window of a pipeline is
`skills/ci-workflow-hardening` and `skills/gha-trust-boundary-pitfalls`.

## When
- A release needs an SBOM, or a customer, regulator or auditor asks for one.
- An SBOM from a supplier arrives and has to be read or checked.
- A build pipeline is asked to emit provenance or sign what it publishes.
- A vulnerability is announced and you must answer "are we affected" from release evidence.

**Skip when** nothing is distributed as a versioned artefact: a website or service deployed straight from a pipeline has no release, so an SBOM per release, signatures and a retention period are not applicable and are reported as "not applicable: reason". What still applies is the pinning of the pipeline's own actions (§2.8), the comparison of a lockfile with what the deployed bundle really contains (§1.11) and a build identifier for the deployed output (§3.9).

## Steps

**Read only the section the task meets.** They are independent.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | What an SBOM must contain to be useful: identity, components, identifiers, dependency graph, completeness, lifecycle stage | an SBOM is produced or read | [`01-sbom-content-and-identity.md`](./references/01-sbom-content-and-identity.md) |
| 2 | Provenance and signatures: what they claim, what to bind, keys, the builder, what verification means | artefacts are signed or attested | [`02-provenance-and-signing.md`](./references/02-provenance-and-signing.md) |
| 3 | Publishing and keeping the evidence: matching bytes, reissuing, vulnerability answers, retention, checks | the release is published or a flaw is announced | [`03-publish-verify-and-keep.md`](./references/03-publish-verify-and-keep.md) |

## Output / checkpoint
For each release: an SBOM tied to the exact artefact (its digest in the document or beside it), generated at a
stated lifecycle stage, with a stable identifier for every component that has one, a declared completeness for
the dependency graph, a unique serial and an incremented version on every reissue; provenance or a signature
bound to the same digest and verified once from a clean machine; and both stored with the release for as long
as the support period lasts.

## Guardrails
- Generate the SBOM from the artefact or the build, not only from the source manifest. Never ship a document you
  cannot match to the shipped bytes (§1.1, §3.1).
- Give every component its stable identifier, and state where the graph is incomplete. Never let an absent
  dependency list read as "no dependencies" (§1.4, §1.6).
- A changed document gets a new version, or a new serial for a new build. Never publish different content under
  an unchanged identity (§1.3).
- Verify what you sign, from a machine that did not build it. Never publish an attestation nobody has checked
  (§2.5).
- Keep long-lived signing keys out of the build, or use short-lived credentials. Never leave a signing key where
  a pull request build can read it (§2.3).
- Treat the SBOM as data to answer questions with, not as a trophy. Never store it where no one can search it
  when a flaw is announced (§3.3).
- The provenance part of this block is unverified own guidance; every numeric level or threshold must be re-read
  from the specification in force before it is quoted. Nothing was run while writing it.

## Origin
Rewritten from the CycloneDX specification schema (Apache-2.0), read 2026-10-20, plus own guidance flagged in the
references. The build-provenance framework (SLSA) and signing tools were **not read**; their terms are used from
general knowledge and marked "re-read before relying". Provenance, what was removed and not verified:
[`references/origin.md`](./references/origin.md). 🟡: never dogfooded.
