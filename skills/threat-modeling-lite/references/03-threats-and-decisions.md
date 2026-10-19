# threat-modeling-lite §3 — Threat prompts, decisions and anti-patterns

> Section 3 of `skills/threat-modeling-lite`. Read it when you ask what can go wrong and record what you will do.
> The prompt names come from the toolkit's `docs/risk-rules.md` (Threagile, commit `74e323e`, MIT), a list of
> rule names with no definitions; the questions attached to them are our own guidance. The decision, pattern and
> anti-pattern wording is restated from the Threat Modeling Manifesto and the toolkit's `docs/model.md`, read
> 2026-10-16.

1. **Use a rule's name as a prompt, not as a finding.** The toolkit lists about forty built-in risk rules by
   name. The file gives no definitions, so each question below is own guidance written from the name alone.
   Walk each boundary crossing and each store in the sketch (§2) against the groups that follow, and write down
   the answers that surprise you.
2. **Identity: Missing Authentication, Missing Identity Propagation, Missing Two-Factor Authentication.** For each
   call across a boundary: who is calling, how is that proven, and does the original caller's identity survive
   the hops, or does a downstream service act on its own authority? Which actions would need a second factor?
   (`skills/auth-session-conventions`, `skills/credential-lifecycle-pitfalls`.)
3. **Data and stores: Unguarded Direct Datastore Access, Unnecessary Data Transfer, Unnecessary Data Asset.**
   Can anything reach the store without going through the service that owns it? Which data crosses a boundary
   that the receiver does not need, and which stored data has no reason to exist?
4. **Secrets: Missing Vault (Secret Storage), Missing Vault Isolation, Accidental Secret Leak.** Where does each
   credential live, who can read it, and which paths copy it into code, images, logs or reports?
   (`skills/secret-leak-response-pitfalls`.)
5. **Boundaries and transport: Untrusted Deserialization, Wrong Trust Boundary Content, Unencrypted Communication,
   Unguarded Access From Internet.** Which parser reads data that came from the wrong side of a boundary, which
   assets share a boundary although their trust differs, and which links cross a network unprotected or are
   reachable from outside with no gate?
6. **Implementation-level classes are not modelled here.** The list also names SQL and NoSQL injection, XSS,
   CSRF, SSRF, path traversal, XXE and similar. Own guidance: note the exposure in the sketch, then hand the
   code-level work to `skills/security-hardening` and `skills/csp-and-sanitiser-pitfalls` instead of enumerating
   attack strings in a design session.
7. **Build and delivery: Code Backdooring, Container Base Image Backdooring, Missing Build Infrastructure, Push
   instead of Pull Deployment, Unchecked Deployment.** Who and what can change what is built and deployed, and
   is the path checked? (`skills/ci-workflow-hardening`, `skills/package-manager-supply-chain-pitfalls`.)
8. **Decide on every finding and record the decision against it.** The toolkit's documentation says some
   identified risks are real and some are accepted, and gives a `risk_tracking` field where the decision is
   documented against the risk's identifier. A rule that fires is not yet a threat. Own guidance: for each item
   write one of mitigate, accept or drop, with the reason, an owner, the check that will show it holds, and for
   an accepted risk who accepted it.
9. **Avoid the Manifesto's four anti-patterns.** The hero threat modeler: it does not depend on innate ability,
   everyone can do it. Admiration for the problem: go beyond analysing to practical, relevant solutions. The
   tendency to overfocus: keep the big picture, since parts of a model can be interdependent, and do not
   exaggerate attention on adversaries, assets or techniques. The perfect representation: several
   representations beat one ideal one (§2.4).
10. **Use the Manifesto's patterns as a quality check.** A systematic approach for thoroughness and
    reproducibility, informed creativity (craft as well as science), varied viewpoints (§1.5), a useful toolkit
    that raises productivity and repeatability, and theory put into practice with field-tested techniques. If a
    session had none of these, say so in the record.
