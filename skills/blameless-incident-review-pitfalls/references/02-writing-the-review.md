# blameless-incident-review-pitfalls §2 — Writing the review

The facts section is where a review earns trust: each statement can be checked, and nothing in it argues
for a fix.

## 2.1 The timeline
1. **Make it an accurate representation of events** (PagerDuty), and **never change details or events so
   the story looks better**. PagerDuty's reason: the review is only effective if the team is honest, even
   with itself.
2. **Put in the changes of status or impact and the key actions of responders** (PagerDuty).
3. **One entry, one piece of evidence.** For each entry, name the metric, graph, log search, message or other
   page the data point came from (PagerDuty). Adhorn's entry shape, with the time zone stated:

   ```
   <time and zone> - <what happened> - <evidence>
   09:19 UTC - Connection pool exhausted, new requests failing - database metrics
   ```

4. **Post the commands and queries used** to look up the data, so others can see how the numbers were
   gathered and reproduce them (PagerDuty).
5. **List the responders**, from the chat history, and mark who led and who took notes if your process has
   those roles; link the recording of the incident call if there is one (PagerDuty).
6. **Note how it was detected** (monitoring or a customer) and the duration from start to full resolution
   (adhorn's incident details).

## 2.2 The description
1. **No "alternate reality" sentences.** PagerDuty's two examples: "if service X had rate limited the
   requests it would not have failed", and "there was insufficient monitoring to detect the elevated CPU".
   Both blend the real problem with a hypothetical fix. State what happened and keep every improvement in a
   separate section, so each can be discussed on its own.
2. **Separate "what happened" from "how to fix it"** (PagerDuty's review question).
3. **Define technical lingo and acronyms** that newcomers may not know (PagerDuty).
4. **Quantify the customer impact**: how many or what share of customers, which regions, which functions
   degraded or unavailable, and for how long (adhorn). PagerDuty's examples of impact are event submission,
   processing delay and slow notification delivery, which are that company's product, not a list to copy.
5. **Say what worked.** Adhorn asks for what kept the incident from being worse and the adaptations people
   made, so the next review does not only list failures.
6. **Say how the incident fits into the picture of the health and resiliency of the services affected**
   (PagerDuty).

## 2.3 Classification and patterns
1. **Tag each review** with searchable keywords (adhorn's examples: configuration, database, dependency,
   latent defect, capacity, deployment), an incident type (adhorn lists outage, degradation, near-miss and
   surprising behaviour) and the systems involved.
2. **Look across reviews.** Adhorn asks whether earlier incidents had similar characteristics and what
   patterns across incidents suggest a systemic issue rather than isolated failures. Tags and the
   precise vocabulary of §1.2 are what make that question answerable.
3. **Say which assumptions proved wrong.** Adhorn's surprise questions: what surprised the team, where the
   understanding of the system was wrong, which mental models need updating.
