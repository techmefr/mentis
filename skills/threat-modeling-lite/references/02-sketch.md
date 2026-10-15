# threat-modeling-lite §2 — The sketch: assets, flows and trust boundaries

> Section 2 of `skills/threat-modeling-lite`. Read it when you draw what the change touches. The vocabulary
> comes from the Threagile model documentation (`docs/model.md`, `docs/mode-analyze.md`, `docs/how-to.md` and
> the README, commit `74e323e`, MIT), read 2026-10-16. Sentences marked "own guidance" are ours. We did not run
> the tool.

1. **List what the change contains, what data it handles and how the parts talk.** The toolkit's model starts
   from technical assets (the things that run or store: services, databases, queues, jobs) and separately
   models data assets (what is stored, processed or sent). Technical assets are linked through communication
   links, and a link records which data assets it sends; an asset records which data it processes and stores.
   Those three lists, assets, data and links, are enough for a lite sketch.
2. **Mark the trust boundaries, and what shares a runtime.** The model can group assets into trust boundaries
   and into shared runtimes, which is how one sketch shows what sits on the same host or container. The
   documentation does not define a boundary. Own guidance: draw one wherever control, identity or privilege
   changes between two parts, including the line between your code and any third party, and between tenants.
3. **Confirm the flow with the owner before reasoning about threats.** One practitioner's account on the
   toolkit's how-to page: generate a starting model, define assets, links and boundaries, look at the generated
   data-flow diagram, then interview the project owner to make sure the flow is accurate, and only then review
   the risks. A wrong sketch makes every later answer wrong, so the check is cheap insurance. This is one user's
   workflow, not the toolkit's rule.
4. **Draw it more than one way if it helps.** The Manifesto lists a "perfect representation" as an
   anti-pattern: there is no single ideal view, and extra views may show different problems. The toolkit
   itself generates a data-flow diagram of technical assets and a separate data-asset diagram of data and its
   relationships. Own guidance: a flow view and a "where does this data live" view are the useful pair.
5. **Keep the model as text beside the code, and keep secrets out of it.** The toolkit keeps its model as a
   YAML file edited in the IDE and offers includes to split a large one into several files. Own guidance: a
   text model diffs and reviews like code; put no credentials, customer data or production hostnames in it, use
   names and categories.
6. **The tool is optional.** The toolkit checks a model against a set of built-in risk rules and produces
   reports. Its release notes list version 1.0.0 as not yet released, and its custom-rule page says the feature
   is under development and carries a "needs to be confirmed" note. Own guidance: a whiteboard photo or a plain
   diagram in the repository is enough for a lite session; use the tool only when the team already has it.
