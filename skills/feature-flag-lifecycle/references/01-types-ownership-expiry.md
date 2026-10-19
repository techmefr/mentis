# feature-flag-lifecycle §1 — Types, ownership and expiry at creation

> Part 1 of `skills/feature-flag-lifecycle`. Read it before a flag is created.
> Source, read 2026-10-19: Martin Fowler, "Feature Toggles (aka Feature Flags)"
> (https://martinfowler.com/articles/feature-toggles.html). Sentences marked "own guidance" are ours.

1. **Name the type before writing the flag.** Four kinds cover almost everything, and they differ in how long
   they live and how often their decision changes. A release flag hides unfinished or untested work so it can
   merge early; it is transitional. An experiment flag assigns each user to a variant for the length of a test;
   it lives as long as the test needs and no longer. An operational flag lets an operator degrade or disable
   behaviour without a release; most are short-lived, a few stay as long-term kill switches. A permission flag
   decides who sees what by user or plan; it can live for years. The article's two axes (longevity and
   dynamism) explain why the type matters: it sets how the flag is built and how it is cleaned up.
2. **The type fixes the removal trigger.** A release flag goes when the feature is fully out; an experiment flag
   goes when the test is called; an operational flag goes when the risk it covered is gone; a permission flag
   goes when the plan or role does. Writing the trigger down at creation is the cheapest way to make removal
   a task and not a memory.
3. **A flag that does not fit a type is not a flag.** If nothing fits, the change can ship by deploy, or the
   need is configuration or an entitlement. Own guidance: a purely cosmetic change with no risk to roll back is
   the usual example; a flag there is only carrying cost.
4. **Do not keep entitlements under a release flag's name.** A per-user or per-plan rule is permanent by
   nature. Own guidance: it belongs where the account's entitlements live, with the lifecycle of a plan, and
   not in a place where everything is expected to be deleted.
5. **Every flag has a record written when it is created**: the name, the type, a named owner (a person, not a
   channel), the creation date, the expiry date, what the off state does, who is allowed to flip it, and the
   signal that tells them to. The article recommends structured configuration for exactly this metadata,
   including an expiry date per toggle.
6. **Add the removal task to the backlog in the same change that adds the flag.** The article gives this as the
   practice for release flags. A flag without a removal task has already decided to stay.
7. **Make expiry enforceable.** The article describes a "time bomb": a test that fails, or a start-up check that
   refuses to run, once a flag passes its expiry date. Own guidance: a warning that nobody reads is the same as
   no date; the date has to cost something when it is ignored, and the cost should reach the owner first.
8. **One decision point per flag, one place for the decision.** The article separates the toggle point (the
   `if` in the code) from the toggle router (what decides). Keep the point at the edge of the module and move
   the choice behind a named decision, so that scattered conditionals do not multiply and so that the logic can
   change without touching every point. Own guidance: a flag checked in many places has to be understood in all
   of them at removal time.
9. **Keep the inventory small on purpose.** The article treats flags as inventory with a carrying cost and
   suggests a ceiling on how many may exist, so a new one waits for an old one to go. Own guidance: where a
   ceiling is too blunt, the next best thing is a visible list the team reads at planning.
10. **Say who may flip it, and who is told.** A flag that changes production behaviour is a production change.
    The record names who may change it and where the change is logged, so that "what changed at that time"
    has an answer during an incident.
