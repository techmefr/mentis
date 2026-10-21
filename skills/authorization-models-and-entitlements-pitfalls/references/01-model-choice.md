# authorization-models-and-entitlements-pitfalls §1 — Choosing the model

Sources: the Check implementation page, the architecture page and the caching page of the OpenFGA repository at 22c4d5d, and the "what is" and tutorial pages of the Cerbos repository at 75f01a9, read 2026-10-20. Everything marked "own guidance" is craft knowledge.

## 1.1 Three families
1. **Role-based: a role is a bundle of actions.** Enough while the question is "what may an editor do". Symptom of outgrowing it: roles named after a resource ("project-7-editor") or multiplying per customer. Check: count roles that differ only by a resource id. Fix: move that dimension out of the role and into a relationship or an attribute (own guidance).
2. **Attribute-based: the decision reads facts about the person, the resource and the context.** Fits "the owner may delete, only while the record is active". The Cerbos tutorial models exactly this: a broad role from the identity system is extended at request time into a more specific one by a condition on an attribute such as the record's owner, so the rule is written once and imported by each resource policy instead of being repeated.
3. **Relationship-based: the decision is a path in a graph of "X is related to Y".** Fits sharing, folders, teams and organisations, where access flows from a parent. The OpenFGA check is a walk from the object and relation through rewrites until the person is found or every path is exhausted. Use it when the question is "does a path exist", not when a single attribute test would do (own guidance).
4. **The families combine.** A role gives broad access, an attribute narrows it, a relationship delegates it. Pick the primary one per resource type, not per application (own guidance).

## 1.2 Relationship rewrites
1. **A relation can be defined by other relations.** "Viewer" can be rewritten as "editor", and "editor" as "editor on the parent folder", which is how hierarchy is expressed without storing every grant at every level.
2. **Combine paths with union, intersection and exclusion.** Union adds ways in; intersection requires two conditions; exclusion removes a group from an otherwise open relation. Symptom of getting this wrong: a blocked user still reads through a second path. Check: write one test per path to a resource, including the exclusion. Fix: express the block as an exclusion in the model, not as a late check in code (own guidance).
3. **A relation that refers to itself through a group must not loop forever.** The OpenFGA implementation remembers the sub-questions already visited on the current path and refuses to ask the same one again. Consequence for modelling: nested groups are allowed, but a data cycle should be rejected at write time where you can (own guidance).
4. **The cost of a check grows with the depth and breadth of the graph.** Deep folder trees and very large groups make decisions slower; the source's own concurrency notes were left unfinished at the commit read, so treat limits as something to measure on your data.

## 1.3 The model is versioned data
1. **A model update creates a new model identifier; the old one never changes.** The caching page relies on this to cache models for a long time without staleness. Consequence: a check can name the model it was written against, and a rollout can be compared before it is switched.
2. **Write the model as a file in the repository and review it like code** (own guidance). Symptom of editing it by hand in a console: nobody can say which version produced yesterday's decision. Fix: model file, a test suite, a deployment step, and the identifier logged with each denial.
3. **Isolate tenants with separate stores or with a tenant in the object name** (the architecture page says stores can separate applications, environments or tenants). Decide which, and test that a person from tenant A is refused on tenant B's object (own guidance; tenant isolation generally is `skills/multi-tenancy-isolation-models-pitfalls`).

## 1.4 Checks (own guidance)
1. For each resource type: the question, the model family, the facts needed, who writes those facts, and the test that fails if the rule is removed.
