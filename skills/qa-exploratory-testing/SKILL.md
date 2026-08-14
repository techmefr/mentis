---
name: qa-exploratory-testing
description: Use when a feature is coded and gated but not yet merged: manual exploratory testing of a real user journey on the running app. Distinct from tdd and from gate.
---

# qa-exploratory-testing

A step complementary to `review` (8), before `ship` (10): the QA eye, not the dev eye. `tdd` (5)
writes the tests we knew we had to write; this block looks for what we didn't think to test.

## When
After `gate` (7, automated tests green) and alongside `review` (8), on any feature that touches a
real user journey: not on an internal refactor with no user-facing surface.

## Steps

### 1. Charter: frame the exploration, don't improvise blindly
1. Define the **charter** in one sentence: which area/journey to explore and why (e.g. "the payment
   form, network-error angle"): without a charter, the exploration goes everywhere and never
   converges.
2. Timebox the session (30-60 min): exploratory testing with no time limit never ends and drifts off
   topic.

### 2. Techniques: beyond the happy path already covered by tdd
1. **Boundary testing**: limit values (0, negative, max, empty, very long) on every field/parameter of
   the journey.
2. **State and navigation**: browser back button, refresh in the middle of a multi-step flow,
   double-click on a submit button, duplicated tab on the same session.
3. **Simulated external errors**: network cut/slow, third-party API returning an error or timing out:
   does the journey degrade cleanly or does it break?
4. **Persona switching**: the same journey replayed with a different role/permission (not logged in,
   missing permission, different agency) to check that no unintended access leaks.

### 3. Non-regression: what worked before doesn't break elsewhere
1. Check the adjacent journeys (not only the one modified) when the diff touches a shared
   component/service.
2. Compare the before/after behaviour if there's any doubt, rather than relying on the memory of "how
   it used to work".

### 4. Driving the browser: reconnaissance before action
1. **Never act on a selector you haven't seen.** Read the rendered page first
   (`read_page`, which hands back element refs), then click/type against those refs: a
   click on a guessed selector or on raw coordinates is what makes a session
   non-reproducible.
2. **Wait for the page to settle before reading it.** On any app that fetches after
   mount, the DOM read too early is a different DOM: a "the field is missing" finding
   observed before the load finished is a false positive, not a bug.
3. **Separate the two phases explicitly**: a reconnaissance pass (read the state,
   note the refs) then an action pass (interact, re-read to confirm the effect).
   Interleaving them is how you end up reporting the consequence of your own
   mis-click.
4. A finding whose reproduction sequence can't be replayed from the refs observed
   goes back to step 5 of the LOOP as "to be reproduced", never straight into the
   report as a bug.

## Output / checkpoint
Every bug found is reported with: the exact journey to reproduce it, observed vs expected result,
severity (blocking/major/minor). No bug reported without a precise reproduction sequence.

## Guardrails
- Never replaces `tdd`/`gate`: it's a human-driven complement on what the automation doesn't think to
  test, not a first-level safety net.
- Timeboxed: beyond the allotted time, we stop and report the state reached, no session that stretches
  out indefinitely.
- A bug found here and judged minor doesn't block `ship` by default: it's for the human to weigh
  priority vs deadline, not for the agent to decide alone.

## Origin
Sourced from established exploratory testing techniques (James Bach/Michael Bolton: session-based test
management, charter, timeboxing) and classic boundary testing (ISTQB). Mechanisms rewritten, no copied
text. Market research, no dedicated internal QA production feedback at this stage. Section 4
(reconnaissance before action, wait for the page to settle before reading the DOM) is a rewrite of the
discipline in Anthropic's official `webapp-testing` skill, transposed from Playwright to our Browser
pane tooling.
