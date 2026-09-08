# code-baseline — origin and source stamps

> Provenance of `skills/code-baseline`. Read it when a rule has to be traced back to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**An org skill catalogue's cross-language rule set (14 skills: no comments, no ticket references, no AI
attribution, file size limit, no god classes, no generic exceptions, external APIs behind an owned client,
parsed files as typed manifests, distinct concepts as distinct types, layered architecture, test new
features, run generated tests, diff coverage, plus one on not exporting the catalogue itself)** — read in
full, then extracted, de-identified and rewritten generically, with everything naming an internal repository,
package or channel deliberately left out (rule C). The catalogue-export rule was **not** carried over: it
governs that catalogue's own distribution, not code.

The layered architecture rule was **not** duplicated here: it already lives in `skills/archi` and
`skills/domain-modeling`, and the per-stack blocks carry the language form of it.

**Deepened 2026-08-06.** A first pass wrote this block from the skills' descriptions alone. Reading the
bodies added what mattered most and what a summary loses: **§0's scope stance** (new code only, legacy
untouched, bundled versus drive-by cleanup, flag-don't-fix, and the user's local override — a coherent
posture that appears in every one of those skills and that the descriptions never state), plus the exclusion
lists, carve-outs and anti-pattern catalogues throughout. Stamped 2026-08-06.

**§7 added 2026-08-11** from the same catalogue's `extend-dont-override`, a 15th skill added there after
this block's original mining pass (confirmed absent from the "14 skills" counted above). Read directly
from the installed plugin rather than from a description alone, since the source itself is short enough
that the body is the whole rule: the preference order (config key → config file → override hook → whole-file
replace → fork) and the "state why no narrower option worked" discipline are taken as-is and rewritten
generically, with the source's Railpack/`php.ini` worked example left out (rule C — a specific vendor tool,
not a mechanism worth naming here).

**§8 added 2026-09-07** from the same org cross-language rule set, whose 15 skills at the last count are now
18 — a bodies pass over the three that were not in the original mining plus a re-diff of the rest. Two of the
three were already covered and stayed out: wrapping a disk-loaded file in a typed object is §4.13–§4.18 (the
source states it as its own rule; ours had already reached it from the boundary side), and the
no-unsolicited-documentation rule had already been mined into `skills/documentation-adr` on 2026-08-11. The
third had no home anywhere in the repo and is now §8: every guarantee a change declares needs a reachable
line enforcing it, with the six shapes to check for and the carve-outs where the caller is legitimately
outside the diff. It earns a section rather than a bullet because it is a **different kind of check** from
§1–§7 — those govern how a line is written, this one runs over the finished diff and asks what executes.
Point 4 is ours rather than the source's, and cites this repo's own failure: twelve agents carried a
prose-only tool prohibition for a month with nothing in the frontmatter enforcing it. The house default
stack, the skill-export rule and the layer-architecture rule stay out (rule C, and covered per-stack).

**Depth pass 2026-09-08 — all eight sections.** The last of the five sectioned blocks, and the one where the
pass had least room: this block was already the deepest in the repo, so most of the work was adding the
failure modes the sections were *silent* on rather than explaining rules that already carried their
reasons. Every original point is kept verbatim. Before → after: §3 errors 241 → 920 words, §5 domain types
249 → 932, §7 customising a third party 310 → 932, §1 comments 348 → 979, §2 size and shape 448 → 974, §4
boundaries 509 → 1,085, §6 tests owed 549 → 1,095, §8 guarantees 805 → 1,274. Router plus the eight
sections: 3,459 → 8,191.

What was genuinely absent, by section. **§3** had the naming argument end to end and stopped at the throw:
catch narrowly or you catch your own bugs; an empty catch is a decision that has to look like one;
log-and-rethrow at every layer reports one failure five times; preserve the cause when wrapping; a failure
crossing a process boundary loses its type, so the contract is a stable code rather than a class name;
inside a transaction a throw *is* the rollback; the failure path has cleanup obligations; and no secret in a
message, because the message goes somewhere with different readers than the request had. **§5** had the
divergence argument and none of the primitive-obsession cases: two ids of the same primitive type are
interchangeable to the compiler, a validated value is validated once, the unit belongs in the type, money
is an amount and a currency and never a float, a boolean pair encoding one state admits the impossible
combinations, and a nullable field carrying two meanings carries neither — plus the wire format and the
storage shape both being distinct from the domain type, and a note on where to stop, since a codebase that
wraps every string is unreadable for a different reason.

**§4** owned the client and not its policy: set the timeout explicitly, an external call fails in five ways,
retry only what is retryable with backoff and an idempotency key, decide what happens when the dependency
is down, credentials never into a log, and — the one worth the most — **test the client at the transport
layer, not by mocking the client**, since a test that fakes your own client exercises none of the
status-to-exception mapping that justifies the client existing. The webhook receiver, which §4.11 had
listed only as a place a client is overkill, gained its own three rules: verify the signature before
trusting a field, deduplicate by event id, acknowledge fast and process asynchronously.

**§7** gained the upgrade economics behind its ladder, compose-before-you-change, the copy as a fork of
whatever guarantee that file carried, the version pin an override implies, why editing inside the dependency
directory produces a bug only one machine has, runtime monkey-patching as the invisible tier, upstreaming as
the cheapest override, an exit condition for a fork, and an assertion on the behaviour the override buys.
**§1** gained the docblock's actual job (the contract, not the signature), the comment-in-a-diff as a missing
rename, `TODO` as a decision left to nobody, the section divider as a file asking to be split, where a
durable "why" belongs, the external-bug workaround resolving through §7.4 plus a test, the comment-shaped
things that are not comments, and the scope note that the rule binds this diff rather than licensing a
sweep. **§2** gained a function's much lower ceiling, the parameter-count and boolean-parameter shapes, the
branch chain over a type, dead code, the rule of three, the coupling hub, and the statement that the line
count is a proxy for cohesion.

**§6** was reframed around what it actually owns — the *debt*, not the doctrine, which stays in `skills/tdd`
— and gained what does not discharge it: a test that has never failed, a test of the implementation rather
than the behaviour, a test that reads the real clock, a suite whose tests depend on each other, a bugfix
test never seen red, and the refusal path plus the failure path as behaviour that is owed. **§8** gained
five: enforced-on-the-happy-path-only is not enforced, a guarantee expressed twice will disagree unless one
is named authoritative, a guarantee that must be opted into is the one that gets forgotten, a guarantee can
expire, and the habit that found every example in point 4 — verify by reading the system's answer, not your
own edit.

Twenty-four intra-block `§N.M` references were re-checked one by one against the new numbering, including
the one in this file: the citation reading `§4.6–§4.9` for wrapping a parsed file now reads `§4.13–§4.18`.
