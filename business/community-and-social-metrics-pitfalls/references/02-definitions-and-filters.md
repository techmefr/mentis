# community-and-social-metrics-pitfalls §2 — Definitions that need filters

A number without its filters is a different number each time someone reads it.

## 2.1 Time to first response
1. **Definition:** the time between the creation of an activity that needs attention (an issue, a change
   request, an email) and the first response (CHAOSS wg-common, `time-to-first-response`).
2. **Collect two timestamps**, creation and first response (same file, data collection).
3. **Exclude bots and automated replies**; count only real people (same file, data collection and filters).
4. **Filter by the role of the responder**, for example only maintainers (same file, filters).
5. **One filter per type of activity**: issues, emails, chat and change requests behave differently, so do
   not blend them (same file, filters).
6. **A response need not be an action** (opensource.guide, Maintainer activity). Decide whether an
   acknowledgement counts and write it down. Own guidance.

## 2.2 Occasional contributors
1. **Define the term before counting.** The working group lists a minimum number of contributions and a maximum
   gap between them as the filters that decide who is occasional (CHAOSS, `occasional-contributors`, filters).
2. **Report the share of all contributors** and the repeat occasional contributors too (same file).
3. **Do not treat them as a failure.** Their reasons include one bug fix, a time-boxed event, trying the
   community out, or a life event (same file, overview).

## 2.3 Bursts
1. **When activity spikes, ask what caused it before reading growth.** The working group's examples are
   releases, hackathons, mentorship programmes, conferences, media announcements, a critical bug, or people
   arriving from another project that depends on yours (CHAOSS, `burstiness`, overview).
2. **Look at the fluctuation against a norm**, using a time box or an outlier rule (same file, data
   collection). Own guidance: write the cause next to the spike in the report.
3. **Ask people why they contributed more in that period**, if you can; the file lists this as a
   qualitative route (same file).

## 2.4 Harm metrics
These come from a trust-and-safety teaching deck (TeachingTrustSafety, "Metrics and Measurement", CC0) and
are platform-scale; only the generic ideas are carried.
1. **A metric is useful when it can change**, either through people's behaviour or through a change you make
   (deck, "What is a metric?").
2. **Count of harmful items is not enough.** Pair prevalence (how common) with severity: a rare but severe
   issue matters more than a common mild one (deck, "Other Metrics Examples").
3. **Add enforcement delay**: the time between harmful content appearing and being handled, and how much it
   was seen meanwhile (same slide).
4. **Own guidance:** for a brand community, the same three questions apply to abusive comments and
   spam: how many, how bad, and how long they stayed up. Handling itself belongs to
   `business/community-moderation-ladder-pitfalls`.
