# price-change-and-billing-pitfalls §1 — A price change is a rollout

The common failure is to treat a price change as a switch: the number is decided, every account moves on the same
day, and the first signal is the support queue. This section turns it into a sequence with a read at each step.

## 1.1 Order of exposure
1. **New customers first.** A new buyer has no old price to compare with and no relationship at stake, so their
   behaviour is the cleanest read on whether the market accepts the number. Read conversion and the mix of plans
   chosen before touching an existing account.
2. **Then a small slice of existing accounts**, picked so that it is not the easy ones (not only the happiest, not
   only the smallest). Write the selection rule down; a hand-picked slice proves nothing.
3. **Then waves.** Each wave is larger than the last only if the previous read was acceptable. The size of the
   first slice and of each wave is a decision with a reason, not a figure taken from an article.

## 1.2 What is read each cycle
Name, before the first wave, what will be read and when: cancellations and downgrades in the cohort, support
volume and its topics, failed or disputed payments, plan changes made to dodge the increase. Compare with a
cohort that did not change in the same period. A cohort read after one billing cycle says little about a yearly
plan: say which plans cannot be read yet.

## 1.3 The off-ramp
Write, before the first wave, what stops the rollout and who decides: which signal, over which window, and what
happens to the accounts already moved (stay, go back, get a credit). An off-ramp invented after the signal
appears is a negotiation with the loudest voice.

## 1.4 Churn is expected, not a surprise
Some accounts will leave over a justified increase. State beforehand which loss is acceptable, so that a cycle's
read is compared with a decision and not with a feeling. Do not claim that the accounts that leave are the least
valuable: that is a hypothesis to check against the cohort's revenue and support cost.

## 1.5 Link to the metrics
After the change, revenue and churn figures must be defined the same way before and after
(`skills/saas-metric-definition-pitfalls`), or the read compares two different things.
