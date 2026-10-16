# support-queue-design-pitfalls §2 — Labels and intake

Labels sort work; intake decides how much work arrives. The failure this section prevents is a taxonomy
built to look complete that nobody applies, on top of an intake that lets everything in.

## 2.1 Labels are axes
1. **One axis per question**: what kind of work (type), what it is waiting on (state), what happens if nobody
   does it (priority), which part (area), whether outsiders may help. An item carries at most one value per
   axis.
2. **Two labels from one axis on one item means nobody decided.** Enforce that invariant by convention or by
   tooling.
3. **State moves the queue; priority starts arguments.** Keep priority as small as you can bear.
4. **A minimal state set** in the source: not looked at, waiting on the reporter, accepted, needs an owner,
   blocked on something external. Pick one vocabulary and write it down.
5. **Delete default labels you will not apply**, and present the taxonomy for approval before touching the
   tracker; one imposed on the people who must use it decays quickly.

## 2.2 Priority by consequence, and the limits of automation
1. **Two or three priority levels, defined by consequence**, not by sentiment, urgency in the wording or the
   customer's tone. "Everything is high" is the failure.
2. **One vendor's public definitions are a usable model**: production failing for the business with direct
   impact on its operation is the top level; a failure with limited business impact is the next; limited or
   moderate problems and general questions about operation come next; a question or suggestion that is not
   time-sensitive and blocks nobody is the lowest. Each level has examples next to it. Write yours with your
   own examples.
3. **Examples carry the definition.** A level without examples is argued about every day.
4. **The support owner may change a priority the customer chose.** Own guidance, not found in the cloned
   page: say it in the policy so it is not a surprise.
5. **Gate labelling on confidence**: apply a label when you are confident; when you are not, apply a "needs
   review" state rather than a guess. A guessed area label sends the item to the wrong owner.
6. **Never let automation apply the top priority.** Route candidates to a human, because that axis has the
   most downstream consequence and the least machine-checkable definition.

## 2.3 Cut intake, in order of payoff
1. **Route usage questions off the tracker** to a forum, chat or help centre, and answer in one or two lines
   anyway so the redirect lands as help. A third arrival of the same question is a documentation defect, not a
   fourth answer.
2. **Validated forms** that require only the fields that change the outcome. Every optional field a reporter
   skips teaches them the form is decorative. Markdown templates enforce nothing.
3. **Disable blank issues** once the forms cover the real categories.
4. **Apply the type automatically** from the form.
5. **Order, with reasons**: routing removes whole categories; forms turn two round-trips into one; the last
   two are cheap but small. The source says to promote forms when bug reports dominate.

## 2.4 Security reports leave the public tracker
1. **Three elements, separate from general triage**: a private intake channel, a named team with a capped
   size, and an embargo path for disclosure to those who must patch first. The source adds that a report filed
   publicly by mistake is an emergency, to be moved to the private channel at once.
2. **The advisory side** (acknowledging, assessing, embargo, announcement) is in `security-advisory-comms-pitfalls`.

## 2.5 Publish the scope of support
1. **List what you do not support**: third-party integrations, customers' custom scripts, unsupported
   platforms, discontinued versions. One vendor's page says such requests cannot be prioritised and points
   the customer to the third party's own resources.
2. **State what you will not do in a security incident**, if that is the case. The same vendor says its
   support answers questions about its features and data but does not investigate or analyse on the customer's
   behalf, cannot revert changes or restore to a point in time, and cannot preserve logs after the fact (log
   streaming has to be set up before an incident). It handles such matters in writing, through tickets.
   Decide your own list; do not copy theirs.
3. **Say it before the incident**, in the same place as the response promise.
