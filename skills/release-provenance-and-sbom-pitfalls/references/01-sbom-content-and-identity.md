# release-provenance-and-sbom-pitfalls §1 — SBOM content and identity

> Part 1 of `skills/release-provenance-and-sbom-pitfalls`. Read it when an SBOM is produced or read. Source, read
> 2026-10-20: the CycloneDX specification repository, JSON schema for version 1.7 and its README (Apache-2.0).
> Facts are the schema's own descriptions, restated. Sentences marked "own guidance" are ours and rest on no
> source read.

1. **Say which stage the data was captured at.** The schema has a lifecycles field naming the phase: design,
   pre-build, build, post-build, operations, discovery, decommission, and explains that different data exists at
   different phases (resolved versions and where they came from are known at build; what actually sits on a
   running system is known later). Symptom: an SBOM built from a manifest lists a range, the artefact ships a
   different version. Fix: take the document from the build or from the built artefact and record the phase.
2. **Describe the thing the document is about.** The metadata holds a component field for what the BOM
   describes, plus timestamp, the tools that made it, the manufacturer or authors and the supplier. Own
   guidance: fill the described component with name, version and a digest of the shipped file, so the document
   points at exactly one artefact.
3. **Give each document an identity and bump it on change.** The schema says every BOM should have a unique
   serial number in the UUID format, even if its content has not changed, and that a modified BOM should have
   its version incremented by one, a consumer facing several with the same serial taking the highest version.
   Own guidance: a new build gets a new serial; a correction to the same build keeps the serial and raises the
   version. Symptom: two different documents with the same serial and version.
4. **Use stable identifiers, not just names.** A component can carry a package URL, a CPE, a software-heritage
   identifier, an OmniBOR id or a SWID tag, and a hash list. Own guidance: a package URL is the usual key for
   matching a component to an advisory feed; a name and version alone match poorly across ecosystems. Add
   hashes for the files you ship. Symptom: a vulnerability scanner reports "no match" on a component known to
   be vulnerable because it was listed by display name only.
5. **Reference by `bom-ref` and keep it unique.** Every component, service and composition may carry a
   reference identifier, unique within the document, and the dependency graph points to them. Own guidance:
   generate the identifiers from the package URL so they are stable between runs and diffs stay readable.
6. **Know what the dependency graph says and does not say.** The schema says a component that has no dependencies
   of its own must appear as an empty entry, and that a component missing from the graph may have unknown
   dependencies, so an absence must not be read as "dependency-free". It recommends compositions to state which
   parts of the graph are unknown. Symptom: a consumer concludes a library has nothing beneath it. Fix: record
   an aggregate (complete, incomplete, unknown and the variants the schema lists) for each assembly and each
   dependency set, or write down that the graph is direct dependencies only.
7. **Separate direct from transitive, and runtime from build tooling.** Components have a scope and an
   "external" flag for what is expected from the environment rather than shipped. Own guidance: do not list the
   compiler and test tools as shipped components; list them, if at all, under another scope or in a
   build-stage document.
8. **Record licences and suppliers if you will be asked.** The component fields include licences, the
   organisation that supplied it, the group, the publisher and a copyright notice. Own guidance: licence data
   in an SBOM is as good as the registry metadata it was read from; a licence field left unknown is better
   than a guessed one (`skills/oss-compliance-programme`).
9. **Validate the document against the schema.** The schema is the reference for the format and each version
   exists as JSON, XML and protocol-buffer forms. Own guidance: validate in the pipeline before publishing; an
   invalid document is silently ignored by some consumers. Use the conventional file names and the registered
   media type so tools find it (`bom.json`, or a file ending `.cdx.json`).
10. **Vulnerability reports and exploitability statements share the format.** The README lists vulnerability
    disclosure and exploitability exchange documents among the supported uses; the schema's vulnerabilities
    field attaches findings to components. Own guidance: the useful move for a producer is to state, per
    announced flaw, whether the product is affected and why, so customers need not guess (§3.3).
11. **A lockfile is not the list of what shipped.** Own guidance. Symptom: an SBOM or a "what are we exposed to"
    answer is built from the lockfile, which lists every development tool and every package that never reaches the
    output, while the shipped bundle contains only a subset, possibly with versions inlined at build time. Check:
    list what the shipped bundle or image really contains (the build output, its bundler metadata, the image's
    package database) and diff it against the lockfile: components only in the lockfile are build tooling, to be
    left out or put under another scope (§1.7); components only in the bundle have no declared source and need one.
    Fix: generate the document from the built output, and state when it was generated from the lockfile only.

## Checks (own guidance)
1. The document names its lifecycle phase and the digest of the artefact it describes.
2. Every component with a package URL has it; none is identified by name only.
3. The graph states its completeness; no consumer can read an absence as a fact.
4. Serial and version are unique across everything published for the product.
