# email-campaign-measurement-and-testing-pitfalls §2 — Conversion, baselines and benchmarks

Once opens and clicks are demoted, the result has to come from somewhere. This section says where, what sits
beside it, and what it is compared with.

## 2.1 Conversion from the system of record
1. **Read the conversion from the system that holds the outcome** (orders, activations, upgrades, logins), not
   from the mail tool's own counter. The mail tool knows who clicked; the system of record knows who bought.
2. **Write the attribution window beside the number**: "purchases within N days of a click" is a different
   figure from "purchases within N days of delivery". Say which and why.
3. **One conversion per program**, defined once. The rules for a single business conversion, the system of record
   and double counts are `business/ad-measurement-pitfalls` §2; the habit of tagged links and their testing is
   §1 there; why two tools disagree is §3 there. Email links need the same discipline.
4. **A flow's result is a statement about its audience as much as its copy** (§2.3).

## 2.2 Guardrails from the same send
1. **Report the unsubscribe rate and the complaint rate of the send** beside every lift. A lift in clicks
   bought with a doubled unsubscribe rate is a loss.
2. **Give the complaint rate its source and denominator** as in
   `business/email-deliverability-and-sender-requirements-pitfalls` §3.2.
3. **No threshold is set here.** The reader and the program's owner choose what change counts as unacceptable
   before the send, and write it down (the same habit as a guardrail in `skills/experiment-design-pitfalls` §1).
4. **Count the list shrinking.** A send that converts well and removes a tenth of the audience changes the next
   send's denominator.

## 2.3 The baseline of an always-on flow is a holdout
1. **A flow that runs continuously needs a baseline that runs continuously**: a random sample of eligible
   recipients who are not mailed, drawn at the same time as the mailed group.
2. **"Last month" is not a baseline** and neither is the organic rate. A conversion rate that looks good
   against the organic rate says the audience chosen by the trigger already converts more often (they signed
   up, they abandoned a basket), not that the copy works.
3. **Holding people out costs something**, and whether to do so for a given programme is the owner's choice.
   The reading of a holdout, and why it beats a before-and-after comparison, is
   `skills/experiment-design-pitfalls` §3.
4. **Say so when there is none.** "No holdout, so this number says nothing about what the flow caused" is a
   legitimate sentence in a report.

## 2.4 Benchmarks: a ladder
1. **First, own history in the same window**, with volume, audience and timing comparable. One vendor guide
   itself says a month-on-month comparison works only if send volume, audience size and timing are similar;
   keep that caveat.
2. **Second, own holdout** (§2.3).
3. **Last, a vendor or industry average, labelled as such**, with who produced it and what they counted. The
   guides quote open and click bands and the figures differ by guide and by industry; none was taken here,
   and an open-rate band is also affected by §1.
4. **Never quote a vendor average as pass or fail.** It can be shown beside the result as context.
5. **A single send is not a trend.** One vendor guide suggests three comparable sends before calling a baseline;
   treat any such count as a convention and write the reason.

## 2.5 Failure patterns
- **Counter from the mail tool taken as the outcome.**
- **No window beside the conversion.**
- **Lift reported without the unsubscribe rate.**
- **Flow judged against the organic rate.**
- **Industry average as the verdict.**
