# blameless-incident-review-pitfalls §1 — Frame and language

Most of what makes a review useless is decided before the first fact is written: what the review is for, and
the words used to describe a cause.

## 1.1 What the review is for
1. **Learning, not blame.** Adhorn's template says an incident analysis helps a team find why its picture of
   the system was incomplete; the point is to extract the lesson from an expensive event, not to assign fault.
2. **Contributing factors, not a single root cause.** Adhorn: complex systems do not have single root causes,
   they have several factors that accumulate and combine, and a "5 Whys" chain can reach an oversimplified
   conclusion. **The sources differ**: PagerDuty asks the review to identify "the underlying cause" and also
   says a mistake is rarely rooted in one person and there are usually several contributing factors. This
   block carries the adhorn stance and keeps PagerDuty's demand that the review drill past what went wrong.
3. **Look for the second story.** The first story is "someone made a mistake". The second asks why the action
   made sense given what the person knew, the time pressure and the information at hand (adhorn).
4. **Never stop at "human error" or "process failure".** Adhorn calls these symptoms, not explanations.
   PagerDuty's version: if someone deployed a change that broke things, the finding is that the system
   allowed a breaking change to be deployed (a script without rate limiting, documentation out of date).
5. **No naming and shaming** (PagerDuty).
6. **Question the assumptions, not only the defect.** Adhorn separates fixing the specific problem from
   questioning the assumptions and mental models that made it possible, and says to push toward the second.

## 1.2 Words that keep the review honest
1. **Prefer the wording on the right** (adhorn's language list):

   | Instead of | Write |
   |---|---|
   | root cause | contributing factors |
   | human error | systemic conditions |
   | "who made the mistake?" | "what about the system made this outcome likely?" |
   | framing an issue as a failure | unexpected behaviour, a surprise |

2. **"Outage" only for an outage.** PagerDuty: customers read "outage" as fully unavailable and assume the
   worst, so use "incident" or "service degradation" unless it really was a full outage.
3. **Precise failure vocabulary.** Adhorn contrasts "database performance problem caused outage" with a
   description of the mechanism: a table lock from a maintenance operation blocked application queries, the
   timeouts tripped circuit breakers, and the failure spread to dependent services. The second can be
   compared with other incidents; the first cannot. When several incidents share a mechanism despite
   different immediate causes, that pattern points at a systemic issue and is only visible if the shared
   words exist.
4. **Learning over reflex controls.** Adhorn: adding a control after every incident ends in controls over
   controls; learning means understanding the conditions that enabled the problem.

## 1.3 Interviewing the people involved
1. **Say the goal is understanding and improvement, not assigning blame** (adhorn).
2. **Ask what made the action reasonable then**: what they knew, what they did not know, what pressures
   existed (adhorn).
3. **Let people narrate** rather than answer a list of closed questions, and talk to several people to build
   a fuller picture (adhorn).
4. **Write down the context, not only the answers**: conditions, constraints and considerations behind a
   decision (adhorn).
5. **Question prompts, as one template's list**: how did this make sense to everyone at the time, what
   information would have helped but was not available, what constraints in time, resources or access
   shaped the choice (adhorn). Pick the ones that fit; none is required.
