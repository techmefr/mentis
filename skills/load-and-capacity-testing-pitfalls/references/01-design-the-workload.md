# load-and-capacity-testing-pitfalls §1 — Designing the workload

> Part 1 of `skills/load-and-capacity-testing-pitfalls`. Read it when a test is designed.
> Sources, read 2026-10-20: Azure Architecture Center, "Continuous validation with Azure Load Testing and Azure
> Chaos Studio" (CC BY 4.0); mercari/production-readiness-checklist, "Capacity Planning" (MIT). Sentences marked
> "own guidance" are ours and rest on no source read, except where a sentence cites the Gatling documentation
> (read 2026-10-20 for facts only).

1. **Start from the question.** Own guidance: "will it hold at twice the launch traffic", "did this change slow
   the checkout path", "how long can it run before memory grows" are three different tests with different
   shapes. Write the question; a test without one produces a chart and no decision.
2. **Get the target figures from the owner, and list the key scenarios.** The Azure guide has the team identify
   key scenarios, dependencies, expected usage and availability, performance and scalability targets, then turn
   them into measurable thresholds, such as sign-ins expected, requests per second on a given API, or operations
   per second for a background process. Symptom: "make it fast". Fix: one threshold per key scenario, owned by
   the person who owns the product promise (`skills/slo-design` §2).
3. **Test each function in isolation first, then a realistic mix.** The capacity notes order the work: each
   function alone to get a known baseline, then many functions at once from an estimate of real traffic, then
   randomised input. Reason given: isolation gives a baseline free of interactions, the mix reveals the
   interactions, and the odd inputs show behaviour away from the ideal path. Keep that order.
4. **Build the mix from measured traffic.** The notes say to measure the requests the application really gets
   and imitate them, and to refresh the test as the numbers change. Own guidance: take proportions, payload
   sizes and the read/write ratio from production logs or metrics; a uniform mix of the cheap endpoint skews
   everything.
5. **Include the awkward inputs.** The capacity notes warn that bad input can degrade a service, for example by
   pushing useful entries out of a cache and slowing other requests. Own guidance: add cache-miss-heavy keys, a
   few very large payloads, deep pagination and a hot key, and compare the tail with the polite run.
6. **Decide open or closed model on purpose.** Own guidance: a closed model (a fixed number of users, each
   waiting for a reply before the next request) slows its own offer when the server slows; an open model sends at
   a set arrival rate whatever the server does (the Gatling documentation defines the two the same way: arrivals per second for open, concurrent users for closed, and notes that ramping a closed model down does not interrupt users already running). Real internet traffic is mostly open, so a closed test tends to
   understate the tail under stress (own guidance: the documentation read does not say which model fits web traffic). Say which you used and why.
7. **Model think time and sessions only where they exist.** Own guidance: a user journey has pauses and
   dependent calls (log in, then use the token); an API consumed by machines may have neither. Do not invent
   think time to make a number look kind.
8. **Use data that behaves like production data.** Own guidance: an empty table or ten rows makes every query
   fast; a copy that has not got the production distribution (skewed keys, large tenants) hides the slow
   plans. Use anonymised or generated data of the right size and shape, never a raw production copy
   (`business/data-protection` §3 point 5).
9. **Match the environment, and write down the differences.** The Azure guide stresses a production-like
   environment so problems surface early, and sustained artificial traffic because without usage runtime issues
   stay hidden. Own guidance: the same instance sizes, pool sizes, caches, network hops and configuration; where
   it differs (fewer nodes, smaller database), state it next to the result.
10. **Control what else is running.** Own guidance: a noisy neighbour, a backup, a cron or another test on the
    same system moves the tail. Note the time window and silence what you can.
11. **Treat the generator as a system under test.** Own guidance: a load generator saturating its CPU or its
    network cap becomes the bottleneck and the test measures itself. Watch the generator's own CPU and run
    several generators if needed.
12. **Fake or isolate the dependencies you do not own.** Own guidance: never send real traffic to a payment
    provider, an email service or any third party; stub it with the latency profile you measured, and say so, as
    the result is then bounded by the stub.
