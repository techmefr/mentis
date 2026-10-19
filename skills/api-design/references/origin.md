# api-design — origin and source stamps

> Provenance of `skills/api-design`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

Rewrite of the `api-and-interface-design` skill from a market generalist dev skill catalogue;
Hyrum's law, the "One-Version Rule" and the final verification checklist are taken as-is,
rewritten to the mentis template.

**Sectioned and deepened 2026-09-08.** The three inline sections moved to one file each under
`references/` and the router became a table of triggers. No section was added: the three are the
lifecycle of a contract — write it, decide what it exposes, change it. Every section and point number
was preserved; nothing outside this block cites them by number, but the guardrails and the checkpoint
now cite the points they enforce.

**This was the thinnest block counted in the depth table: 375 rules words for nine numbered points.**
The reason is worth recording, because it is the same one `skills/spec` had. The block was written as a
checklist of principles an experienced reader already agrees with — contract-first, don't expose
internals, extend rather than fork — and every one of them is uncontroversial when read and useless
under pressure, because the pressure comes from a specific change that looks compatible and is not. So
the depth here is almost entirely a catalogue of those cases.

**What the depth adds.** The additions that were real absences rather than elaborations:

- **§1**: that a schema generated afterwards describes whatever the implementation happened to do,
  including the parts nobody chose — a field nullable because the column is, a shape mirroring the
  database, a name taken from an internal class; that duplicated validation is worse than absent,
  because the two copies diverge and the one that matters is not the one a reader finds; that the cost
  of an inconsistent error format is paid on the *client's* failure path, where it is least visible to
  us; that required, nullable and absent are three states and conflating two of them produces client
  code wrong in exactly one case; that a closed enumerated set makes adding a value a breaking change,
  so the contract has to say which it is; that the error code has to be machine-readable, or an
  interface-text improvement becomes somebody else's outage; that validation failures are part of the
  contract, since a client building a form has to map them onto its own fields; and that identifiers,
  units and time representation are decided once in the contract or by default in the implementation.
- **§2**: the mechanism the law rests on — consumers write code against what they *observe* and have
  no way to tell that from what we documented, so every accident is part of the contract from the first
  integration; that the surface is response times, ordering, default page size, synchronicity, status
  codes and error wording, none of which is in the schema; that an unspecified detail is a choice you
  make once by accident, ordering being the clearest case; that the narrower the surface, the cheaper
  the interface is to keep, which is why this is a design rule and not a warning; that "nobody uses
  it" is a claim about the consumers we can see; that anything undocumented but reachable is reachable,
  authorisation and cost included; that **loosening is compatible and tightening is not**, so a
  validation rule added later breaks callers even though it makes the contract more correct; that a
  default value is part of the contract; and that consumers depend on our *failures* too — a retry loop
  keyed on a status code turns a changed code into a duplicated write.
- **§3**: that a second version is two implementations, two test suites and a migration nobody
  schedules, so the cheaper change is more expensive for as long as it exists; that additive is only
  additive if the consumer tolerates the unknown, which has to be set before the first consumer;
  that **widening a type is not compatible**, because every existing parser was written against the
  narrower promise; that renaming is removal plus addition and there is no compatible rename; that a
  version is a promise to maintain the old one, and one created with no sunset date becomes permanent
  by default; that a change to a field's *meaning* is breaking with the type unchanged and cannot even
  be detected by the consumer; that compatibility is verified by comparing the two schemas rather than
  remembered, since from memory the check passes on the change that broke it; that extension has a
  limit and reaching it is a finding to state rather than another optional field; and that deprecation
  announced only in a document nobody re-reads is a field in full use on the day it is removed.

Router plus sections: 375 → 2,392.

**Status.** The source is unchanged and still stands. The depth is ours, written from the changes that
look compatible and are not — which is what a reviewer needs in order to refuse one, and is a different
thing from this block having been used against a real third-party consumer, which it has not.

**Sections 4 and 5 added 2026-10-02**, from primary sources read that day (rule B: mechanisms rewritten,
no prose copied; every rule traces to a passage that was read, none was recited from memory).

- **§4 (protobuf and gRPC).** The protobuf style guide and the protobuf best-practices page (the
  `protocolbuffers.github.io` content repository; code under BSD-3-Clause per its LICENSE file, the CC BY 4.0
  licence of the site content was not re-verified in the repository and the text is rewritten either way); the
  gRPC guides on deadlines, cancellation, error handling, status codes, retry, health checking, graceful stop,
  wait-for-ready and keepalive (`grpc.io` content repository, CC BY 4.0, code samples Apache-2.0); AIP-155
  (request identification), AIP-158 (pagination), AIP-180 (backwards compatibility), AIP-193 (errors) and
  AIP-194 (automatic retry) from `google.aip.dev` (CC BY 4.0, samples Apache-2.0). Left out on purpose: the
  Java and C++ language-option mechanics, edition-2024 symbol-visibility details (moving fast, version-specific)
  and the per-language example tables. The buf tool is named as the open-source lint and breaking checker but
  its own documentation was not read here; the rule states the check, not the tool's rule categories.
- **§5 (HTTP and OpenAPI).** RFC 9457 (problem details, read in full text); the OpenAPI Initiative's
  best-practices page and the 3.0-to-3.1 and 3.1-to-3.2 upgrade guides (`learn.openapis.org`, CC BY 4.0);
  Spectral's OpenAPI rule reference and CI guide (Apache-2.0); the Zalando RESTful API guidelines chapters on
  pagination, idempotency, status codes, URLs, JSON and security (CC BY 4.0). The OpenAPI specification text
  itself (versions 3.1.2 and 3.2.0) was listed, not read end to end: the Schema Object claims are the upgrade
  guides' claims. Left out: the Zalando proprietary headers and company-specific naming; the OWASP API Security
  list (CC BY-SA, idea only, not read here); the Redocly CLI (not read).

**Status.** Both sections are 🟡 like the rest of the block: written from the standards and style guides,
never run against a real third-party consumer. OpenAPI moves by minor version; re-read the upgrade guide
before trusting point 2 of §5 on a newer one (`skills/source-freshness`).
