# platform-engineering-golden-paths-pitfalls §3 — Adoption, measurement and maturity

Sources: the CNCF Platforms White Paper (measurement and challenges sections) and the Platform Engineering Maturity Model (introduction and "how to use this model") at tag-app-delivery commit cadc776, and the adoption pages of the Backstage documentation at commit 64ab86e, read 2026-10-20. "Own guidance" marks craft knowledge.

## 3.1 The adoption curve
1. **Adoption has known milestones and a known plateau.** The Backstage adoption pages describe: a proof of concept, first users, a group that really adopts it, then a plateau in catalogue coverage or active users, then leadership asking about continued value, then a crossroads between doing the work and replacing the tool. Symptom: enthusiasm fades because "another file to maintain" is overhead. Fix: plan for the plateau in advance, and reduce the cost of joining (reuse an existing inventory to seed entries, generate the file from a template).
2. **Get something real in front of leadership early.** The pages recommend a real proof of concept, metrics defined for what you want to move (onboarding time, time to production for a new service, time to mitigate incidents) and lower adoption barriers.
3. **Expect the weeks after a general launch to be slow.** The launch page says so, and to remove friction rather than force adoption. Set up a visible feedback channel (a chat room, a form or office hours) in the launch announcement.
4. **Announce the problem solved, not the feature list.** The launch page contrasts "you no longer chase ownership across five tools" with "we launched a catalogue", and recommends a short live demo with a proof-of-concept team member co-presenting, because peer endorsement carries more weight.
5. **Spend little time on appearance.** The customisation page warns against months on the theme; get close enough and iterate.
6. **Prefer existing plugins or components to building your own early on** (the same page). A custom build needs justification by a clear gap.
7. **Inner sourcing needs groundwork before it is invited:** a starting template for new plugins, style guides, and review capacity. Without it contributions create friction for both sides (the plugin-ownership page).

## 3.2 What to measure
1. **Three families:** user satisfaction and productivity, organisational efficiency, and product delivery (the white paper's grouping). Pick a few from each, not all.
2. **User side:** active users and retention, capabilities provisioned, and a satisfaction survey. Counts of registrations alone say nothing about value (own guidance).
3. **Efficiency side:** time from request to a usable database or test environment; time to build and deploy a brand-new service into production; time for a new person's first change to land (the paper lists these). These are the self-service claim made measurable.
4. **Delivery side:** the paper points to the four delivery metrics (deployment frequency, lead time for changes, time to restore, change failure rate) and says product success is the real measure. Treat them as team-level indicators the platform can influence, not as platform scores (own guidance).
5. **Take a baseline before the platform changes anything.** Symptom: a report that cannot say if a number improved. Fix: measure the manual process once, even roughly (own guidance).
6. **Use the smallest viable effort at first.** The paper says simple surveys and analysis of usage may be most valuable initially.
7. **Report the metric that moved with the one that did not,** and the reason (own guidance).

## 3.3 Maturity models
1. **A maturity model is a list of things to work on, not a score.** The model's introduction quotes the idea that the outcome of an assessment is the list of skills to acquire next, not the level reached.
2. **Aspects are assessed and evolved independently** (the model's own statement), though improving one may need a minimum in another. Symptom of one overall level: a team polishing the portal while provisioning is still by ticket.
3. **Each level costs more funding and time, so the top is not a goal in itself.** Ask whether your organisation would benefit from the qualities of the next level before paying for it.
4. **The model's four levels are named provisional, operationalized, scalable and optimizing,** repeated across several aspects (read from the page headings; the descriptions were not read in full). Use the level names to talk, and re-read the tables before an assessment.
5. **Check your starting context with the organisation's wider cloud-native maturity** (the model recommends it, own guidance on how).

## 3.4 Checks (own guidance)
1. A one-page plan: users interviewed, first capabilities, baseline numbers, launch channel, plateau plan, owner of the catalogue data.
