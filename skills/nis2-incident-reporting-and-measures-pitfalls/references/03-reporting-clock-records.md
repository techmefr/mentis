# nis2-incident-reporting-and-measures-pitfalls §3 — The reporting clock and its records

> Part 3 of `skills/nis2-incident-reporting-and-measures-pitfalls`. Read it when an incident process, an on-call
> rota or a reporting template is built, or an incident is live. Source: Directive (EU) 2022/2555, Article 23(1) to
> (4), read 2026-10-19 (see part 1 for the edition). National transposition may differ in detail and was not read
> (part 1, point 6). Periods are restated from the text read; verify them in the national law before use. Own
> words; "own guidance" marks ours.

1. **What is reported (Article 23(1) and (3)).** Entities notify the CSIRT or, where applicable, the competent
   authority, without undue delay, of an incident with a significant impact on the provision of their services. An
   incident is significant if it has caused or can cause severe operational disruption or financial loss for the
   entity, or has affected or can affect others by considerable material or non-material damage. Own guidance: the
   words "is capable of" matter; do not wait for the damage to have occurred. Whether a given incident qualifies is
   counsel's call; the Commission could specify cases by implementing act for some entity types (not read).
2. **Stages as read (Article 23(4)).** An early warning without undue delay and within 24 hours of becoming aware,
   saying where applicable whether unlawful or malicious acts are suspected or a cross-border impact is possible. An
   incident notification within 72 hours of awareness, updating that and giving an initial assessment with severity,
   impact and, where available, indicators of compromise. An intermediate report on request. A final report no later
   than one month after the incident notification, with a detailed description, the likely threat or root cause,
   mitigation applied and ongoing, and any cross-border impact; if the incident is still ongoing, a progress report
   then and a final report within one month of handling. A trust service provider has a 24-hour period in place of
   the 72-hour one for incidents affecting its trust services.
3. **Other communications (Article 23(1) and (2)).** Where appropriate, recipients of the services likely to be
   adversely affected are told of significant incidents without undue delay, and recipients potentially affected by a
   significant cyber threat are told of measures they can take. Notification does not in itself increase liability.
   Own guidance: prepare who decides these communications; see `skills/incident-comms-pitfalls` part 1.
4. **Owners, named in advance (own guidance).** One role, with a deputy, that declares "we are aware of a possibly
   significant incident"; one filer, with a deputy, for each stage. The 24-hour period does not pause for a weekend.
5. **Record the time of awareness when it is known (own guidance).** One case field, set by the person who declares
   awareness, with the source of the information; later periods are computed from it, as in
   `skills/cra-exploited-vulnerability-clock` part 2, point 3. Keep the original messages with the case. When
   awareness starts, in a doubtful case, is a question for counsel before the day.
6. **Prepare the channel and templates before the day (own guidance).** Find out from counsel which authority or CSIRT
   receives the notification in each state, how (form, portal, mail), and in which language. Create and test the
   accounts, with credentials in the secret store and a named owner. Draft blank templates for the early warning,
   the incident notification and the final report using the fields in point 2; a named reviewer signs before filing.
7. **Evidence an incident can feed (own guidance).** Time-stamped logs, the timeline, indicators of compromise,
   decisions and who made them, and the mitigation steps; a blameless review follows
   (`skills/blameless-incident-review-pitfalls`).
8. **Escalate immediately (own guidance).** A suspected significant incident, doubt about awareness time, a cross-border
   effect, a suspected criminal act, or a request from an authority goes to the security owner and to counsel the same
   day. A dry run, from a test incident to drafted stage documents with times recorded, is the evidence that the
   process works.
