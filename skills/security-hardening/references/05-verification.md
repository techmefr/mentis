# § 5 — Verification

> Section 5 of `skills/security-hardening`. Read it before claiming a boundary is done. This is the
> evidence the block's checkpoint owes.

1. Replay the boundary with a **hostile value**, not just an invalid one: a quote and a
   semicolon where a name goes, a `../` in anything path-shaped, a script tag in anything rendered.
   The distinction is the whole point: an invalid value exercises the validation, and a hostile one
   exercises what happens when the validation is wrong — which is the case you are actually claiming
   cannot happen.
2. Replay the new endpoint **as a user who shouldn't have access** and as one who should, and confirm
   the refusal is clean rather than a crash or an empty success. A crash is an information leak and an
   availability bug; an empty success is indistinguishable from a genuinely empty result, so the caller
   cannot tell they were refused and neither can your test.
3. **Observed, not reasoned about.** The evidence is the response you got — the status, the body, the
   absence of the row — and a boundary declared safe by reading the code is a boundary whose framework
   behaviour was assumed. This is the same rule the pipeline's gate applies to everything else, and it
   is the one most often skipped here because the happy path already works.
4. **A test is worth more than a replay, because it runs again.** A manual hostile-value replay proves
   today's code; the same case written as a test proves it after the next refactor, which is when the
   guard gets moved or removed. Where the boundary is worth checking at all, it is worth one test.
5. **Assert the absence, not only the refusal.** A negative test that checks the status can pass while
   the response body still carries the record, and a leak test that only counts rows can pass while a
   field it never looked at is present. Name the value that must not appear.
6. **Verify the whitelist by its edges.** The interesting cases are the value one step outside the
   allowed set, the value that differs only by case or encoding, the empty value and the absent one —
   and, for anything with a bound, one over it. A whitelist tested only with a legal value has been
   tested for the happy path.
7. **Check what got logged while you were testing.** The hostile value you just sent is the fastest way
   to find out whether the boundary writes input into a log, an error tracker or a trace, which is a
   different exposure from the one you were testing and one nothing else in this list would surface
   (`skills/observability-instrumentation` §2).
8. **Never run a hostile-value replay against a shared or production environment.** Local or preview
   only: the payload is designed to do something, the system it reaches is not yours to break, and the
   log entries it leaves get read as a real incident. This is `seraph`'s rule and it applies at writing
   time just as much as at audit time.
9. **A tool's pass is a floor, not a result.** A scanner or a linter finds the shapes it knows and says
   nothing about the authorisation your domain requires, the field a serialiser should not have
   included, or the ownership check nobody wrote. Green tooling with no negative test is an unverified
   boundary with a badge.
10. **State what you did not verify.** A boundary whose replay was skipped — no preview environment, a
    dependency not available, a case that needs data you do not have — is a known gap, and naming it is
    the difference between an open item and a silent assumption. Anything else makes the checkpoint's
    evidence a claim rather than a record.
