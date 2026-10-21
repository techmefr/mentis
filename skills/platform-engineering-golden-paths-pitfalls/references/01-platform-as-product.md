# platform-engineering-golden-paths-pitfalls §1 — The platform as a product

Sources: the CNCF Platforms White Paper (the latest-version page) at tag-app-delivery commit cadc776, and the adoption pages of the Backstage documentation at commit 64ab86e, read 2026-10-20. "Own guidance" marks craft knowledge.

## 1.1 Users first
1. **Symptom: a platform that engineers describe as something done to them.** Cause: built from the platform team's idea of what teams need, announced by mandate. The white paper says teams that ship features without feedback, or rely on top-down mandates for adoption, meet resistance and lose the promised value. Check: can the team name five user teams, what each asked for, and what changed because of it. Fix: interviews, issue tracking, surveys and watching real usage, the methods the paper lists, before the first roadmap.
2. **Put someone with product responsibility on the team from the start.** The paper recommends product managers to share roadmaps and carry user needs. Without one, the loudest request or the favourite technology becomes the roadmap (own guidance on the consequence).
3. **Marketing and advocacy are part of the job.** The paper lists announcements, demos and regular feedback sessions. A capability nobody knows exists is not adopted.
4. **A platform serves the common case first.** It should support the use cases most teams share before the needs of one team (the paper's attribute "platform as a product"). Symptom: months spent on one team's special workflow. Check: how many teams use the capability this quarter.

## 1.2 The thinnest layer
1. **The platform team provides capabilities; it does not have to implement them.** The paper says managed providers or other internal teams can run the services and the platform is the thinnest layer giving a consistent experience over them; its example of a minimal platform is a page of links and procedures. Symptom: a team operating its own database service because "the platform" must. Fix: buy or reuse, own the interface and the experience.
2. **The team's own cognitive load is a constraint.** The paper lists reuse of open-source toolkits for documentation and templates, and staffing that matches the number of users. A platform team of three serving forty teams needs a very small surface (own guidance on the arithmetic).
3. **Secure and compliant by default.** The paper makes it an attribute: the default path already satisfies the organisation's rules, so a team does not have to choose to comply (own guidance on how: checks in the template and the pipeline).

## 1.3 Optional and composable
1. **Teams must be able to use part of the platform and bring their own for the rest.** The paper's example: a team needing a graph database that the platform does not offer provisions its own. Symptom of the opposite: workarounds, shadow tooling, and an exemption process that is the real platform. Fix: document the exit, and what the team takes over (support, patching, compliance) when it leaves a path.
2. **Self-service is the scaling mechanism.** A user should obtain a capability, for example a database with its locator and credentials, through a command or a form without a ticket (the paper's example). Symptom: a queue of requests that equals the platform team's capacity. Check: measure the time from request to use (§3.2).
3. **Hide complexity, keep visibility.** Users need not run the services, but must be able to configure and observe them as needed (the paper states both). A black box that cannot be debugged moves the work back to the platform team as support.

## 1.4 What to build first
1. **Frequently needed, undifferentiated capabilities first:** pipelines, databases and observability are the paper's examples. Symptom of starting elsewhere: a clever feature few teams use.
2. **Start with a few engaged, skilled teams** and use their detailed feedback, then let them advocate (the paper's advice, and the Backstage adoption pages say to pick key stakeholders and iterate closely with them). Symptom of launching to everyone at once: noise, and no team to hold up as proof.
3. **Show leadership the link to delivery.** The paper warns that infrastructure seen as a cost gets constrained, and tells platform teams to demonstrate impact on product teams' value streams. Prepare the case with a measurable baseline (§3.2).

## 1.5 Checks (own guidance)
1. Per capability: user teams, the request that created it, the manual step it removed, owner, support path, exit path, and the number of teams using it.
