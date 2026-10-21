# ad-measurement-pitfalls §4 — Attribution models and consent

An attribution model decides which touch gets the credit. That decision is a choice of story, and the data
cannot make it for you. This section is how to use models without being used by them, and how to treat a
visitor who declined tracking. Model definitions are standard; platform availability of each model changes
and is marked `re-read before relying`.

## 4.1 Every model is an opinion
1. **First-touch gives everything to the first known touch, last-touch to the closing one; each is wrong in
   the opposite direction.** Choosing a model is choosing whose story to believe, so say so when you present
   one.
2. **On a long cycle, show first-touch and last-touch side by side.** A made-up example: a ten thousand deal
   with four touches (a paid social ad, an organic article, a retargeting ad, a branded search). First-touch
   gives 10,000 to the paid social ad and 0 to the rest; last-touch gives 10,000 to the branded search and 0
   to the rest; linear gives 2,500 to each (10,000 / 4, checked). The gap between the first two rows is the
   finding: it says the paid social ad creates demand that later shows up as branded search, and no single
   number says that.
3. **The closing touch is often demand someone else created.** Branded search and "direct" are where people
   arrive after something else made them look; crediting them alone leads to defunding the thing that worked.
   Investigate what is in "direct" before calling it either real direct traffic or lost tracking.
4. **Do not turn a platform-to-analytics ratio into a multiplier** (§3.3). A documented override of credit is
   acceptable only when a holdout or a survey supports it, bounded to the channel and the window the evidence
   covers, with the raw table kept (own wording of one source's rule).

## 4.2 Credit from data needs volume
1. **A model that assigns credit from the paths of many people (data-driven) needs enough conversions to be
   stable.** With few, it tends to fall back towards last-click and its apparent precision is noise. Google
   Ads' own page says every conversion action is eligible regardless of volume and that performance improves
   with more data, and it states a recommended minimum of conversions and interactions. The figure changes, so
   read the current one on the page (`re-read before relying`) and do not carry a number.
2. **It can only weigh touches it was shown.** Offline events, private sharing and touches lost to cookies are
   invisible to it, so a business with a lot of word of mouth gets a confident model that is blind to it.
3. **Credit is modelled correlation, not proof of cause.** It reflects what co-occurs with conversion. The
   test that says what would have happened anyway is a holdout (§4.3).
4. **Availability changes.** Google Ads' help page says first click, linear, time decay and position-based
   models are no longer supported (actions that used them were moved to data-driven; last click and data-driven
   remain), and the GA4 help page says the same four are no longer available as of November 2023 and lists
   three models in its attribution reports (data-driven, paid and organic last click, Google paid channels last
   click). Symptom: a saved report or a vendor guide teaches a model the product no longer offers
   (`re-read before relying`); the rule-based ones remain useful as ways to score your own data from the CRM or
   a warehouse.

## 4.3 Keep one model and check it from outside
1. **Pick one model, keep it, and pair it with a check that does not depend on it.** Switching models to make
   a channel look better is the quickest way to lose trust in the whole programme.
2. **Self-reported answers** ("how did you first hear about us?", asked at the moment of conversion) catch
   what tracking cannot. A pick-list of known channels plus free text is easier to count and a free-text field
   catches the rest. People credit the memorable touch, not the first, so use the answers as evidence of
   awareness, not as a share of credit to convert directly into an allocation.
3. **A holdout or a geographic test** answers whether a channel caused conversions that would not have
   happened anyway. Design and reading belong to `skills/experiment-design-pitfalls` §1 and §2. An incremental
   cost per result divides spend by the conversions the test says were caused, not by all conversions the
   platform claimed, which is why it is usually worse than the platform's figure.
4. **A test can look flat because it leaked**: people in the control group were reached anyway through other
   devices or neighbouring regions. A "no effect" result needs the contamination question asked before it
   closes a channel.
5. **Match the effort to the decision.** For a small budget and a short cycle, careful link tagging, one
   simple model and an occasional survey beat a complicated one. Bigger and less reversible budget decisions
   justify a controlled test.

## 4.4 Consent
1. **A refusal of tracking is a decision by the visitor, not a loss to recover.** Do not design a measurement
   that counts or follows people who declined. Server-side delivery changes how data travels to the platform,
   not whether it may be collected, and firing for someone who refused is the same breach from a different
   place.
2. **Say what the gap is made of.** Visitors who declined, visitors blocked by their browser, and visitors
   whose identifier was lost are three different groups; only the second and third are measurement problems
   with technical answers.
3. **Whether and on what basis personal data (including hashed email or phone sent with a conversion) may be
   used for advertising is a legal question.** Hand it to `business/data-protection` §2 and §4, with the
   sentence "we want to send these fields to this ad platform for this purpose". This block names no statute
   and no authority and is not legal advice.
4. **Consent banners and consent signals are part of the measurement system.** A banner that blocks tags
   before consent hides everyone who ignored it; a banner that never sends the signals the platforms expect
   can make conversions fall sharply while clicks and spend continue. After any banner change, compare
   conversions against the CRM for the weeks around it.
