# § 1 — Input: validate at the edge, on a whitelist

> Section 1 of `skills/security-hardening`. Read it as soon as a diff has data you don't control
> reaching something that acts on it. Point 3 is what §2.1 cites for identifiers that cannot be
> parameterised.

1. **Validate at the boundary, once, against an explicit shape** (a DTO, a schema), and let the inner
   layers trust the validated type. Checks scattered through the call chain get skipped by the one
   path nobody thought about. The reason the boundary is the right place is that it is enumerable — you
   can list the entry points — where the set of call paths through the inner layers is not, so a
   scattered check can only ever be verified by reading everything.
2. **Whitelist, don't blacklist.** Enumerate what's allowed; a denylist of bad values is a promise to
   have thought of everything. It is also a promise that ages: the payload shapes change, the encodings
   change, and the denylist stays exactly as clever as the day it was written while looking like a
   control the whole time.
3. **Validate what the value *is*, not just its type.** A string that will be used as a sort column,
   a file path, a redirect target or a hostname must be checked against a known set of legal values,
   not merely confirmed to be a string. Each of those four is a different exploit with the same cause:
   a value that passed a type check and then went somewhere the type says nothing about.
4. **A validated value has to be the one that is used.** Validating a copy, or validating and then
   re-reading the raw request further down, means the guard and the use are looking at two different
   things — and the second read is the one that reaches the query. Pass the validated object on; never
   pass the request.
5. **Reject, don't repair.** Stripping the dangerous characters out of a value produces something that
   passed validation and was never legal, and the transformation is where the interesting bugs live:
   removing one pass of an encoding leaves a second, and truncating to a length limit can cut a
   multi-byte character in half. Refusing is one branch and is testable.
6. **A whitelist that lives in one place is a whitelist that can be reviewed.** The same set of legal
   sort columns duplicated in three handlers will diverge, and the copy that gains an entry is not the
   copy the reviewer read. Name it once and reference it.
7. **Every field is validated, including the ones the client is not supposed to send.** Binding a
   request straight onto a model or an entity accepts whatever the payload contains, so a field the
   interface never shows — a role, an owner id, a price, a status — is writable by anyone who guesses
   the name. The shape is the allow-list of *fields*, not only of values.
8. **Size and count are part of the shape.** An unbounded string, an unbounded array, a page size taken
   from the query string and a nesting depth taken from the body are each a way to spend the server's
   memory or time with a well-formed request. Bounds belong in the schema, where they are visible, not
   in a comment about reasonable use.
9. **Validate the content type as well as the content.** A handler that parses whatever arrives will
   accept a body in a format the caller chose, and the parsers differ in what they coerce, what they
   allow twice and what they allow to be absent — so the format is part of the contract and an
   unexpected one is a rejection.
10. **A value from another system is still untrusted.** A webhook body, a queue message, an imported
    file, a response from a third-party API and a value read back out of your own cache all cross a
    boundary; that a system is internal says who wrote the code, not what data is passing through it.
    This is the point that gets skipped, because the trust boundary is invisible in the call.
11. **Never let the error message do the attacker's work.** A validation failure that echoes the
    rejected value into a log line, an error page or a template has moved the payload somewhere new,
    and one that explains exactly which check failed enumerates the rules for free. Say the field and
    the rule (`business/ux-writing` §1.6); don't reflect the input.
