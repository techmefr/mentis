# dpa-review-pitfalls §2 — Posture and overview

> Section 2 of `skills/dpa-review-pitfalls`. Read it when the document is a processing agreement and the review
> is about to start. Sources: `SKILL.md` and `references/dpa-cold-start-profile.md` of the dpa-review skill
> (commit `c225d1f`), re-read 2026-10-16. The skill is built around a Chinese-first output contract and a staged
> state machine; only the gates are kept. Sentences marked "own guidance" are ours.

1. **Fix the posture before the review.** The source asks six things, and we keep them: our role (customer
   or controller, supplier or processor, intermediary, unknown); the jurisdiction in focus; how sensitive the data
   is (ordinary business data, personal data, sensitive or regulated data); the use context (a test, a
   low-risk purchase, a production launch, an enterprise deal, a regulated deployment); our negotiating
   position; and the points we cannot accept. If the user has not given them, ask and stop before reviewing,
   unless the user asks to proceed on assumptions.
2. **An assumption-based review is allowed, and it is labelled.** If the user asks for a quick or urgent
   first pass, say at the top that the posture was incomplete, treat each unknown as unknown, infer only what the
   text itself shows, and warn that the result finds issues but is not fit to support a decision to sign (the
   source's banner says this).
3. **Never invent leverage or a hard constraint.** A hard constraint is a statement the user made. "Not provided"
   is only written once the user has been asked and has answered or skipped. Concerns you spot yourself go in
   a separate list called likely concerns (the source separates the two).
4. **Take our role from the definitions in the document.** Look at how it defines our side: controller,
   processor, service provider, third party, independent controller, joint controller, or a mixture. A word
   such as "Company", "vendor", "platform" or "customer" does not settle it. If several paths exist or the
   main agreement is missing, say the role is uncertain and which document would settle it. The role decides
   which findings are defects (part 3).
5. **Show the role judgment in plain words.** Write it as a sentence the user can confirm or correct ("on its
   face the agreement puts us in the supplier and processor position; the main agreement is not provided").
   Hand the user the posture to confirm before the term review.
6. **Write a data-processing overview before the terms.** A short statement of who is involved and in what
   role, what data is processed and about whom, why, where, and with which further parties. The source makes
   this mandatory before term-by-term review; write each item as stated in the document, mark what the
   document leaves out, and do not fill gaps from what the product probably does (own guidance).
7. **Keep sector facts open.** If the data may be regulated by a sector rule (health, finance, children,
   employment), and the document or the user does not say, mark it unknown and leave signing comfort out
   (part 4). Which rules apply is for counsel.
8. **Ask the operational questions that shape the findings.** The source's playbook questions are useful
   prompts: may the data be used only to provide the service, or also for analytics or product improvement;
   is training of models allowed, opt-in, opt-out or banned; what approval standard applies to subprocessors;
   which transfer mechanism is required; how fast must an incident be notified; what proof of deletion; what
   security evidence (a report, a certificate); what audit right; how may the supplier change the terms. Record
   the user's answers as positions. Do not fill them in with defaults, and note that figures such as
   notification hours listed as options in the source are options, not rules (own guidance).
