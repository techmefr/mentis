# ad-creative-testing-and-policy-pitfalls §2 — An ad result is not proof about the page

A common move is to screen headlines in ads because impressions are cheap and fast, then to rewrite the landing
page around the winner. The screen is useful; the leap is not.

## 2.1 Why the ad result does not transfer
1. **Impressions are not independent users.** The same person can see the same ad several times, so a large
   count of impressions is a smaller count of distinct people.
2. **A click is not the outcome you want.** A headline can attract clicks from people who never buy; the
   click rate rising while qualified conversions fall is a known way to be wrong.
3. **Optimised delivery shows variants to different people.** When a platform steers each variant to the
   audience it expects to respond, two ads are no longer compared on like-for-like viewers. Ordinary ad
   variants under optimised delivery are exploratory. Whether and how a platform offers a randomised ad
   comparison is a point to read on its current help page (`re-read before relying`). One platform's developer
   documentation, read raw 2026-10-20, describes a split test that divides the audience into mutually exclusive
   groups, advises one variable per test, wants KPIs and the confidence level fixed before the test, asks for
   comparable group sizes, and for creative tests returns confidence values per ad; such a test is the
   comparison to ask for, not the default delivery.
4. **Many variants raise the chance of a lucky winner.** Screening a large set and taking the best one picks
   noise as often as signal; account for the number of comparisons when reading it
   (`skills/experiment-design-pitfalls`).

## 2.2 What to do with the winner
1. **Treat it as a candidate.** Write it down as a promising promise to try on the page, with the click and the
   qualified-outcome figures and the sample sizes beside it, not the click rate alone.
2. **Make a truthful page variant that mirrors the candidate's promise.** The page must be able to deliver
   what the ad says; a message the page cannot honour is a claim problem before it is a test problem
   (`business/marketing-claim-substantiation-pitfalls`).
3. **Confirm with a fresh randomised test on the page**, against the unchanged page, with the incoming ads and
   the traffic split kept the same across the two page versions. Fix the primary outcome, the guardrails, the
   sample and the stopping rule before starting (`skills/experiment-design-pitfalls`; not restated here).
4. **Report the observed effect and its uncertainty, and keep the original page when the evidence does not
   justify replacing it.** There is no guaranteed lift from matching the ad's wording. Message continuity is a
   reasonable hypothesis, and an ad result does not establish it.
5. **Do not reuse the screening result as the proof.** The visitors in the confirmation test are new visitors;
   the screening numbers stay in the notes as the reason the test was run.
