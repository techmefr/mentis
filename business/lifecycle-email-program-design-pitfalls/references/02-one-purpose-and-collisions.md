# lifecycle-email-program-design-pitfalls §2 — One purpose per flow, and collisions between programs

A person is not in one program. They can be in a welcome flow, a product-update newsletter, a billing notice and a
re-engagement flow at the same time, each designed by someone who never saw the others. The harm is in the
sum, and nobody owns the sum unless it is written down.

## 2.1 One purpose per sequence
1. **A flow has one purpose.** A welcome that also teaches the product, also sells and also asks for a review is
   three flows in a trench coat: it cannot be measured (which part moved the number?), it cannot be changed
   (editing the middle shifts the timing of the end) and it cannot exit cleanly (the exit that suits the first
   purpose is wrong for the last).
2. **Split a mega-flow into separate flows wired together.** The hand-off between them is a trigger (the first
   flow's goal reached starts the second), written down like any other trigger.
3. **A sequence the product already covers in-app does not repeat it.** The mail supports the in-product path
   and points to it; when both say the same thing in the same hour the person learns to ignore both.

## 2.2 Each message stands alone
1. **Write each message so it still works if the previous one was never delivered.** A bounce, a filter or a
   skipped open is normal; a message that opens with "as I said last time" and carries the only link to the
   key step loses people silently.
2. **One job and one primary action per message**, and the action's destination still has to work on the day
   the message arrives (§4.1).
3. **Messages in one sequence do not look like a system glitch**: distinct subjects, distinct jobs, a clear
   reason each arrives when it does.

## 2.3 The inventory and the frequency rule
1. **Keep one list of every program that can mail a person**: lifecycle flows, newsletters, campaigns, billing
   and account notices, product notifications, anything a team can send from the same sender. Each entry has an
   owner, an audience and a type (§3.2).
2. **Ask the collision question for every new program**: "what else is this audience receiving?" It is a
   question a design checklist asks and its own output format rarely answers; put the answer in the program
   definition (§1).
3. **Set one frequency rule across all marketing programs**, owned by a named person, and decide what happens
   when two programs are due for the same person: one waits, one wins by a stated priority, or they are
   merged. Never let each program apply its own limit and call that a limit.
4. **Do not copy a frequency number from a source.** A cap that suits one audience is wrong for another; set
   the rule from this audience's own behaviour, and review it when complaints or unsubscribes move (measured
   as in `business/email-campaign-measurement-and-testing-pitfalls`).
5. **Transactional and account messages are outside the cap but not outside the inventory.** They are listed so
   the sum is known; whether a given message really is one of them is §3.2.
