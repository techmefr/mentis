# Cross-cutting review axes

> **Single source for what a review looks at beyond correctness and stack conventions.** The readers
> (`aragorn`, `gimli`, `legolas`, `frodo`, `boromir`, `theoden`, `samwise`, `faramir`) each carry their own
> correctness list and their own convention set — that part is stack-specific and stays with them. These axes
> are not: an inaccessible button, an unvalidated input reaching a query, new behaviour with no test and a
> swallowed error are the same defects in every language.
>
> Companion to `references/mr-review-plumbing.md`: that file is the transport, this one is the checklist.
> **Neither restates a rule.** Each axis names the block that owns it, and a finding cites that block rather
> than paraphrasing it.

## How to use it

After the reader's own priority list, **one sweep of the diff** against the axes that apply. Three rules govern
the sweep, and they matter more than the list itself:

1. **Every axis has an entry condition. If the diff doesn't meet it, the axis produces nothing** — and you say
   nothing about it. A review that mentions accessibility on a diff with no markup in it is noise, and it
   teaches the author to skim the next one.
2. **The bar is the same as for any other finding**: a touched line, verified against the real code, with the
   concrete consequence. "Think about accessibility here" is not a finding. "The close button is an icon with
   no accessible name, a screen reader announces it as 'button'" is.
3. **The sweep must not double the comment count.** These axes exist to catch what the correctness pass
   structurally cannot see, not to pad. If an axis yields five findings on one diff, the top two go out and the
   rest goes in the closing message as a single remark about the pattern.

Where an org catalogue or a project package (`test-casebook`) is installed and covers an axis, it is the
authority for that axis and the block below is the fallback. Rule A holds either way: the axis works on a plain
repo with nothing installed.

## The axes

### 1. Accessibility — `skills/accessibility`
**Entry condition**: the diff renders markup for real users (a component, a page, a template, a mobile
screen). Internal scripts, dev tooling and back-office-only glue are out.

The four sections of that block are the reference. In a *diff*, these are the ones that actually recur:
- an interactive `div`/`span` with a click handler instead of a native `button`/`a` — invisible to the keyboard;
- an icon-only control with no accessible name;
- a field whose label is a placeholder, or an error shown visually but never associated with the input;
- focus removed (`outline: none`) with nothing replacing it, or a modal/dropdown that doesn't trap and restore
  focus;
- a state carried by colour alone.

**Never a nit.** An accessibility finding names who is locked out — keyboard user, screen-reader user — because
that is what moves it above a style remark. And per that block's golden rule, a wrong `role`/`aria-*` is worse
than none: don't propose ARIA where the native tag was the answer.

### 2. Security at the trust boundary — `skills/security-hardening`, `skills/auth-session-conventions`
**Entry condition**: the diff carries user input toward a query, a template, a filesystem path, a shell or an
outbound call; or it adds an endpoint, an upload, or anything touching authentication, sessions or permissions.

A security finding must trace **the path from input to sink** — which parameter, through which call, reaching
what. Without that path it's a guess, and a wrong security comment is the most expensive kind. Authorisation is
the half most often missed: a new endpoint that validates its input perfectly and never checks *who* is
calling. Secrets never land in a log or a URL.

### 3. Tests owed — `skills/code-baseline` §6, `skills/testing-anti-patterns`
**Entry condition**: the diff adds behaviour or fixes a bug. A refactor with no behaviour change doesn't owe a
new test; a bug fix always does, because it's the only proof the bug is gone.

Two distinct findings here, and they need different wording:
- **No test.** Name the behaviour that is untested, not the coverage number.
- **A test that reports safety it doesn't have** — mock theatre, a timing guess, an assertion on the mock
  rather than the effect, a test that passes against the pre-fix code. `testing-anti-patterns` lists the
  shapes. This one is worth more than the missing-test finding: everyone can see an absent test.

Where `test-casebook` (or its backend siblings) is installed, its doctrine and its plan-before-tests gate are
the authority, and the selector rules come from it.

### 4. Cost on a hot path — `skills/webperf`, plus the stack's own conventions
**Entry condition**: the diff adds a query inside a loop or a request path, loads a relation lazily where it's
iterated, or adds weight to something already rendered on every page.

**No perf finding without either a measurement or a mechanically certain cost.** A query inside a loop is
certain. An unbounded list rendered whole is certain. "This might be slow under load" is not, and `webperf`
exists precisely to say measure first. On the backend stacks the N+1 shape belongs in the reader's own
correctness list; what this axis adds is the frontend and payload side.

### 5. Diagnosability — `skills/observability-instrumentation`
**Entry condition**: the diff adds a failure path someone will one day have to diagnose — a new integration, a
job, a queue consumer, a retry, a `catch`.

The question that block asks is the one to ask here: **when this fails at 3am, what does the person on call
have to go on?** A swallowed exception is the base case, and it is a correctness finding as much as an
observability one. Its opposite is also a finding: a log per loop iteration, or a payload logged whole with a
token inside it.

### 6. Contract and compatibility — `skills/api-design`
**Entry condition**: the diff changes a shape someone outside this file consumes — an endpoint, a response
body, an event payload, a public export, a schema, a column another service reads.

Hyrum's law is the argument: every observable behaviour ends up depended on, so a field renamed or removed is a
break even when no test fails in this repo. Extension over breakage, and if a break is genuinely intended, the
finding is that it isn't flagged anywhere, not that it exists.

### 7. What can be deleted — `skills/over-engineering-review`
**Entry condition**: none, it's cheap and it always applies. Dead code the diff leaves behind, an abstraction
introduced for one caller, an unrequested anticipation, stdlib reinvented.

This axis **lists and scores only** — it never proposes a refactor of code the diff didn't touch. The scope
stance in `skills/code-baseline` §0 governs: new code only, legacy untouched unless asked.

### 8. Words the user reads — `business/ux-writing`, and the stack's i18n rule
**Entry condition**: the diff adds or changes user-visible text — a label, an error, an empty state, a
confirmation.

A hard-coded string where the project has translation keys is a finding on the mechanism. Beyond that: one word
per action across the product, one form of address, and an error that says what to do rather than what the
system failed at. Wording remarks are the most bikesheddable thing in a review — one comment, on the string
that actually misleads, and nothing on the rest.

## Which axes apply, by reader

| Reader | Stack | Axes to sweep |
|---|---|---|
| `aragorn` | Nuxt/Vue | 1 accessibility, 3 tests, 4 cost, 7 deletion, 8 words |
| `legolas` | React | 1 accessibility, 3 tests, 4 cost, 7 deletion, 8 words |
| `faramir` | Flutter/Dart | 1 accessibility, 3 tests, 7 deletion, 8 words |
| `gimli` | PHP/Laravel | 2 security, 3 tests, 5 diagnosability, 6 contract, 7 deletion (+ 1 accessibility when the diff renders templates) |
| `frodo` | Node/TS backend | 2 security, 3 tests, 5 diagnosability, 6 contract, 7 deletion |
| `boromir` | Go | 2 security, 3 tests, 5 diagnosability, 6 contract, 7 deletion |
| `theoden` | C#/.NET | 2 security, 3 tests, 5 diagnosability, 6 contract, 7 deletion |
| `samwise` | Python | 2 security, 3 tests, 5 diagnosability, 6 contract, 7 deletion |

A reader whose correctness list already covers an axis item (secrets in storage for `faramir`, N+1 for `gimli`,
test doctrine for `legolas`) doesn't report it twice — the axis is there to catch the gap, not to duplicate.

## Origin
Written 2026-08-06 from real use: after several MR reviews run through these agents, the reviews came back
sound on correctness and conventions and **silent on accessibility and everything else cross-cutting**. The
cause was structural, not a lapse — `skills/accessibility`, `security-hardening`, `webperf`,
`observability-instrumentation`, `testing-anti-patterns`, `api-design`, `over-engineering-review` and
`business/ux-writing` existed and were cited by the *pipeline* steps, while the eight review readers were
written with a three-item list (correctness, reuse, conventions) and cited none of them. A block nobody reads
at review time is a block that doesn't exist at review time.

Same extraction discipline as `mr-review-plumbing.md`: one file, eight citations, no copy. The entry conditions
and the volume cap are the part that came from use — the first instinct was to hand every reader the full
checklist, which produces a review that comments on everything and is therefore read as commenting on nothing.
