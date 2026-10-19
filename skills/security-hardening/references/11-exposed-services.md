# security-hardening §11 — Exposed services: probing, defaults, bind address and the width of a control

> Section 11 of `skills/security-hardening`. Read it when you stand up or review a service that holds other
> systems' credentials or spends money on a caller's behalf (an API gateway, a proxy for model providers, a tool
> server, an internal admin tool), or when someone asks "is this protected?". Primary source: OWASP API Security
> Top 10 2023, API5 Broken Function Level Authorization and API8 Security Misconfiguration, read 2026-10-19 at
> https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization and
> https://api-security.owasp.org/editions/2023/en/0xa8-security-misconfiguration . The default-credential,
> junk-credential and bind-address points rest on one project's documentation (see `origin.md`) and on the OWASP
> pages only for their general principle; they are marked "own guidance".

1. **Probe the route that spends or changes something, never the listing route.** Authorisation is decided
   per function, not per service: API5 describes endpoints that differ only by method or path where one has
   the check and its sibling does not. A refusal on a read-only catalogue or a login page proves only that
   one function is guarded. Test the endpoint that costs money or mutates state, from outside the network
   path the operator normally uses.
2. **Probe with no credential and with a valid one, and compare.** Own guidance: some services, when a check
   is switched off, treat an invalid credential as "anonymous" instead of rejecting it, so sending a junk
   token returns the same success as sending nothing and says nothing about protection. The probe pair is
   (no credential, valid credential); an invalid one is a third case worth a separate look, not the test.
3. **A refusal where you expected acceptance, or the reverse, is a finding, not noise.** If the listing says
   "unauthorised" and the action says "bad request" or "model not found", the request reached the logic
   behind the guard: anonymous traffic is accepted.
4. **A placeholder password in an example environment file is a publicly known password.** Own guidance,
   consistent with API8's insistence on a repeatable hardening process: a file people copy and edit leaves the
   placeholder live whenever the editing step is skipped. Ship the template with the value empty so the first
   start forces a choice, or make the service refuse to boot while the placeholder is set; a comment above the
   line saying "change me" is the weakest of the three.
5. **A service that holds third-party keys and sees every prompt must not listen on a non-loopback interface
   with authentication off, silently.** Own guidance. Default the bind address to loopback; when the operator
   opens it, require authentication, and at minimum log a warning at start. Say in the runbook which of
   "refuse" or "warn" the project chose: a warning does not stop an exposed instance, it only leaves a log
   line.
6. **A proxy in front does not make the service safe unless the proxy itself enforces authentication.** A
   reverse proxy that only terminates TLS forwards anonymous traffic as faithfully as any other. API8 asks
   for requests to be processed uniformly across the whole chain; state in the runbook which layer owns
   authentication and test through the public address.
7. **Stored third-party keys are encrypted at rest, and a missing encryption key is a boot failure or a loud
   state, never a silent plaintext fallback.** Own guidance. Ask which mode a deployment is in; do not assume.
8. **Management routes that start processes or change configuration are reachable from loopback or an
   authenticated administrator only.** API5's prevention is a default-deny, role-based check on every
   administrative function, applied from one shared module rather than route by route.
9. **A control is only as wide as its wiring.** A guardrail that masks, filters or blocks (content filter,
   data masker, injection screen, budget check, audit hook) runs where it was attached, not where its name
   suggests. Typical gaps: the streamed variant of a response skips the post-response step; media,
   embedding, search and other secondary routes never enter the shared pipeline; a hook that throws is
   swallowed and the request proceeds. API8's uniform-processing principle is the same point at the proxy
   layer. Method: (a) list every route and every response path (streamed, non-streamed, error); (b) mark
   which ones the control reaches; (c) send the hostile or oversized case down one it should not reach and
   observe; (d) write down whether the control fails open or closed when it breaks. A control that fails
   open is a best-effort filter, and the document that describes it must say so.
10. **A heuristic screen has stated false negatives and is never the only boundary.** Pattern-based
    detection of hostile input (injection phrases, secrets in output) misses what it was not written for;
    keep the structural controls of §1 to §3 underneath it, and do not let its presence replace a
    permission check.
