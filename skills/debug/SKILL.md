---
name: debug
description: Use as soon as a bug, an unexpected test failure or a repeated error shows up during the code step, trace the cause backwards to its origin before proposing a fix, then make the bug structurally impossible rather than locally absent.
---

# debug

Support block for step 6 (`code`). Find the **root cause**, not the symptom, and know the difference:
the place the error appears is almost never the place it started.

## When
During `code`, at the first unexpected error or the second identical failure.

## Steps

### 1. Reproduce, then form one hypothesis
1. Reproduce reliably: an exact command plus the minimal input. A bug you can't reproduce on demand
   can't be shown fixed either.
2. State **a single** hypothesis and verify it (a targeted log or test) **before changing anything**.
   Changing code to see what happens is how a second bug gets introduced next to the first.

### 2. Trace backwards to the origin
The error surfaces deep in the stack; the instinct is to fix it there, which fixes the symptom.

1. **Note where it actually appears**: the real message, the real location.
2. **Find what directly produced it**, then ask **what called that**, then its caller. Follow the
   chain, not the intuition.
3. **Follow the data, not just the calls**: where did this invalid value enter the system? Usually
   several frames above where it finally caused damage.
4. **Stop at the original trigger**: the point before which nothing else caused it.
5. When manual tracing stalls, **capture the call chain at the suspicious operation** rather than
   guessing: log the parameters, the surrounding context, and a captured stack trace, immediately
   before the failing call. In tests, write to stderr — a logger may be suppressed, and then you're
   debugging your own silence.

### 3. Fix at the source, then make the class of bug impossible
Fixing the origin removes this bug. Adding checks along the path removes the next one of its kind.

1. **Fix at the origin.**
2. **Validate at the boundaries the bad value crossed**: at the entry point (reject what's obviously
   invalid), and in the business logic (reject what's invalid *for this operation*, which also catches
   the path that bypassed the entry point, including via a mock).
3. **Guard the context** where the consequence was severe: an operation that must never run outside a
   sandbox refuses to, rather than trusting the caller.
4. **Add or adjust the test that captures the case** — at the origin, not at the symptom, or it'll pass
   again the day the path changes.
5. Validate **where data crosses a boundary**, not inside every function: a check in every frame is
   noise, and noise gets deleted wholesale later.

### 4. Know when to stop
Still looping after more than 2 attempts with no progress → `escalate`. Three failed hypotheses means
the model of the problem is wrong, and more attempts inside a wrong model cost more than asking.

## Output / checkpoint
No checkpoint of its own: resumes `code`. What it owes is the chain — symptom, origin, why the origin
explains the symptom — not just a diff that makes the error stop.

## Guardrails
- **No random fixes, no retry loops.** One hypothesis at a time.
- **Never fix only where the error appeared.** If you can't say why the origin produces this symptom,
  you haven't found it, you've found somewhere the symptom disappears.
- **Never make an error quieter to make it stop**: a swallowed exception, a widened type, a removed
  assertion. Same bug, now undetectable.
- A fix with no test capturing the case is a fix that comes back.

## Origin
Native / internal `systematic-debugging`, rewritten. Sections 2 and 3 are rewrites of
`debugging/root-cause-tracing` and `debugging/defense-in-depth` from a market skills repository (the
companion of the upstream this framework responds to): the backwards call-chain walk, the
stack-capture instrumentation and the layered-validation model are theirs, and they filled a real hole
— our own version said "fix the cause, not the symptom" while offering no technique for finding it.
The "validate at boundaries, not in every frame" limit and the three-failed-hypotheses stop rule are
ours; the source is deliberately silent on over-validation, and unqualified layering would collide
with our standing preference for less logic to maintain.
