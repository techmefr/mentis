# brainstorm §2 — Demand evidence, the status quo and the premises

> Section 2 of `skills/brainstorm`. Read it when a feature or an idea rests on "people want this" and nothing yet
> shows it, before the approaches are listed. Not for a bug, a legal obligation or a request whose need is already
> evidenced (a reproduced failure, a contract clause): skip it there. 🟡: rewritten from documentation, not yet
> run on a real request.

**Where it lands.** Brainstorm owns the questions; the answers go where the cycle keeps them (`CONVENTIONS.md`
Rule E): the evidenced need into the problem statement of `spec.md`, what is only assumed into its assumptions,
labelled as such (`skills/spec` §1.8), what is undecided into its open questions. This section produces no
document of its own. Whether the thing should exist at all stays `business/product-ownership`'s call; this is
the questioning that gives it something to decide with.

1. **Ask one question at a time, and skip the ones already answered.** The request or the earlier answers often
   settle a question; asking it again wastes the owner's patience. When an answer is vague, push once more for
   the specific version; after a second push the owner may decline, and that is respected: take what you have and
   record it as not evidenced instead of interrogating.
2. **Interest is not demand.** Separate what people said from what they did. Counts as demand: someone already
   paying or budgeting for it, usage that grew, a workflow built around it, a person who would have to scramble if
   it vanished, a complaint when it broke. Does not count: "that sounds useful", a list of sign-ups, a sponsor's
   enthusiasm, a trend in the market. Ask for the strongest evidence that someone would be upset if it
   disappeared tomorrow. Inside a company the same test reads: a team already running the manual process every
   week, a recurring support request, a workaround an engineer maintains (the internal reading is ours).
3. **Check the first answer before building on it.** Three checks: are the key terms defined well enough to
   measure ("seamless", "better platform" are not); what does the framing take for granted, and is that verified
   (name one assumption and ask); is the pain real or imagined ("people would want" against "three of us lose ten
   hours a week"). When the framing is loose, restate what you understand and let the owner correct it, in a
   minute, not in a debate.
4. **The status quo is the real competitor.** Ask what people do today to solve this, even badly, and what that
   costs them: hours, money, tools taped together, someone doing it by hand. A concrete workflow with a cost is
   the signal. "Nothing, that is why it is a big opportunity" is a warning, not an opening: either the pain is too
   small for anyone to act on or nobody looked. The new thing has to beat the workaround by more than the cost of
   switching to it (the comparison is ours).
5. **Name the person, not the category.** Ask who needs this most: a role, ideally a name, and what they lose or
   gain depending on whether it exists. "Support teams" or "customers" is a filter, not a person. If nobody can be
   named, that is not an assumption to carry along: it is an open question for the owner, written as one.
6. **State the premises before proposing anything.** Write them as numbered statements the owner agrees or
   disagrees with: is this the right problem and could a simpler framing do; what happens if we do nothing (real
   pain or hypothetical); what already in the repository partly solves it; and what the evidence above supports
   and where it has gaps. Mark each premise as evidenced (with the evidence) or assumed. A disagreement changes
   the understanding and sends you back; approaches are listed only after the premises stand.
7. **End with one assignment.** Close the exploration with a single concrete action in the real world that the
   owner can do next, not a strategy: talk to the named person, watch someone do today's workflow without helping
   them, find the actual number. When evidence is missing, the assignment is to get it before the spec is
   written; when it is there, the next stop is the approval of `SKILL.md` step 6.
8. **Say what the evidence supports and what would change your mind.** Take a position on each answer rather than
   a polite "interesting", name the evidence that is still missing, and leave the decision to the operator
   (product choices go back to the dev or the human, as in the guardrail of `SKILL.md`).
