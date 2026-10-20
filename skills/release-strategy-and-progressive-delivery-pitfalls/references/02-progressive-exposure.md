# release-strategy-and-progressive-delivery-pitfalls §2 — Progressive exposure

> Part 2 of `skills/release-strategy-and-progressive-delivery-pitfalls`. Read it when a rollout plan is written.
> Facts about rings, stamps and blue-green come from the Azure Architecture Center articles on tenant update
> strategies and on blue-green deployment of a cluster (CC BY 4.0), read 2026-10-20, restated in our words.
> Sentences marked "own guidance" rest on no source read.

1. **Pick the exposure unit before the tool.** The source describes exposing a change to a subset of tenants, or
   to independent copies of the whole application (stamps), in sequence. Own guidance: the unit may be a
   percentage of requests, a tenant, a region or a stamp; choose the one whose blast radius you can name.
   Symptom: a canary of random requests still breaks one big customer every time. Fix: expose by the unit
   that matches who would be harmed.
2. **Order the rings by tolerance for risk.** The source's example sequence starts with your own test tenants
   and volunteers who accept frequent, less validated updates, then early adopters, then the bulk of users with
   less frequent, more tested updates. Fix: write who is in each ring, how they were chosen, and that they
   agreed. Symptom: the first ring is a set of internal users whose traffic never exercises real paths.
3. **State the stop rule as a condition before the first user.** Own guidance: for each ring, name the signals
   read (error rate, latency, a business signal such as completed checkouts), the comparison (against the
   previous version at the same time, not against yesterday), the hold time long enough to see the slow
   failure, and who may halt. Symptom: the rollout goes on because nobody is sure. Fix: a written rule that
   halts on its own, and a person who may halt without asking.
4. **Compare like with like.** Own guidance: a canary and the baseline must see similar traffic. Symptom: the
   canary looks better because it was routed the easy requests, or looks worse because it started cold.
   Fix: route by a stable key, warm it first, compare at the same moment.
5. **Blue-green means two full environments for a short time.** The source describes bringing the new version up
   next to the live one, bringing its state in line, validating, switching traffic, and only then removing the
   old one, keeping the two together for a limited period to bound cost. Pitfalls: the switch is instant while
   state is not (sessions, caches, queued work, the database), and the old environment is destroyed before the
   new one has proved itself. Fix: keep the old one until the stop rule's hold time has passed, and decide
   what happens to in-flight work at the switch.
6. **Know what runs where.** The source says to track which version each tenant or stamp runs, what it is
   eligible for and since when. Symptom: support cannot answer "which version does this customer have".
   Fix: a record per exposure unit, readable by support, kept as part of the release.
7. **Health check is not validation.** Own guidance: a process that answers a ping says nothing about the
   journeys. Symptom: green health, broken login. Fix: a post-deploy check that runs one real critical journey
   against the new version before widening.
8. **Do not mix a rollout with another change.** Symptom: a metric moves and nobody knows whether the cause is
   the release, a flag ramp or an upstream incident. Fix: one variable at a time per ring, and a note of every
   concurrent change in the release record.
9. **Plan the long tail.** Own guidance: a ring that stays on an old version forever is a second product.
   Fix: a deadline for the last ring, and a count of exposure units still behind, reviewed each release.
