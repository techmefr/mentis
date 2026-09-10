# § 9 — When the story's author is also the builder

> Section 9 of `business/product-ownership`. Read it where one person writes the story and implements it
> — the configuration this repo's operator actually works in.

1. **This is a configuration, not a violation** — an org can put the epic with one person and the stories
   with the people who will implement them, each also carrying the project-management side of their own
   work. Where it holds, apply §1–§8 unchanged: the discovery, the section set, the criteria and the
   sizing test do not depend on who holds the pen. What changes is only which checks are still in place,
   which is point 2.
2. **What it removes is §7's second pair of eyes, and that has to be replaced deliberately.** A story
   reviewed by its author reads as complete because the author knows what the missing sentence meant. Two
   replacements, and they are not interchangeable: the **epic** above it is the check on *whether this is
   the right work* — if the story cannot be traced to one, that gap is the finding, not a formality; and the
   **fresh-context gate** on the delivered code is the check on *whether it does what the story said*
   (`skills/gate`). §5.4's separation moves to those two, it does not disappear.
3. **Write it for the reader who is not you**, and specifically for the agents that will act on it. A story
   whose scope lives in the author's head produces work that matches the head, not the story — and where
   the implementation is delegated, the story *is* the brief. The exclusions of §6.1.4 and the edge cases of
   §6.1.7 stop being paperwork and become the part that prevents an agent inventing a rule (§7.4).
4. **Escalate rather than decide alone on anything the epic did not settle** — a business rule nobody has
   chosen, a scope change, a refusal. Writing the story does not transfer the decision; it makes you the
   person who noticed it needs making.
5. **The gap between writing and building is where the review used to happen, so put time in it.** Not a
   process — an interval. A story written and picked up in the same hour is a story reviewed by the person
   who is already thinking about the implementation, which is exactly the reader who cannot see what is
   missing. A day later, the same person reads it as a brief and finds the holes.
6. **The criteria are written before the implementation is chosen, and not touched afterwards.** This is
   the one rule the configuration makes easy to break: the honest thing is to notice the criterion was
   wrong and change it as a decision (§4.12), and the tempting thing is to adjust it to what the code now
   does. The second one is undetectable from outside and destroys the only fixed reference the work had.
7. **Where the implementation is delegated to an agent, the story's silence becomes the agent's
   invention.** A human developer asks; an agent fills the gap with something plausible and proceeds, and
   the result is a requirement nobody decided sitting in merged code (§7.4). So the sections that a human
   reader would have skipped — exclusions, edge cases, the refused permission case — are the ones that
   carry the most weight in this configuration.
8. **The estimate is still an estimate, and it is still read the same way** (§8.5, §8.10). Holding both
   roles removes the person who would have pushed back on a number produced without reading the code; it
   does not remove the consequence of one. Read the code, or say the estimate is unavailable.
9. **A story you wrote and cannot make ready is still sent back** — to yourself, out loud (§5.3). The
   check is worth doing explicitly because the incentive runs the other way: nobody is waiting for the
   handoff, so the cost of starting hopefully is invisible until the rework.
10. **The record matters more here, not less.** With one person holding the request, the decision, the
    story and the implementation, nothing is written down as a side effect of a handoff — every trace has
    to be created on purpose. §1.12's finding, §2.5's refusals, §3.11's answers and the ADR for a
    structural decision (`skills/spec`) are the whole institutional memory in this configuration.
11. **Reread the story after the code is done, before merging, as if someone else had written it.** This
    is the closest substitute for §7's missing reader: it will not catch what the author still cannot see,
    but it does catch the criterion quietly rewritten to match the code (point 6) and the exclusion that
    got implemented as an assumption rather than as a decision.
12. **A story that keeps growing during implementation is a sign the interview (§1) was too short, not a
    licence to keep adding scope silently.** Without a second reader to notice the drift, the author is
    the only check — so a criterion added mid-build gets the same one-line justification a scope change
    would get from anyone else (§3's saying-no discipline still applies to yourself).
13. **The estimate revision, when the code turns out harder than expected, is written down with the
    reason, not silently absorbed into extra hours.** In the two-role configuration nobody outside notices
    a slipping estimate until the sprint retro — writing the revision the moment it is known is the only
    way the gap becomes visible before it is history.
