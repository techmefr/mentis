# marketing-claim-substantiation-pitfalls §2 — Statistics and sources

A number in a deck is the claim type that fails most expensively. These checks come from the ContentForge
fact-checker agent. Every threshold in it is that tool's own configuration; it is quoted here as an
example of a threshold to write down, never as a standard.

## 2.1 The number is in the source, in the same context
1. **Find the exact number in the cited source and check the context matches**: the population, the
   subject and the metric. A number found with a different context is flagged, not accepted
   (ContentForge fact-checker, statistic step).
2. **Not found means unverified.** If the number cannot be located in the source, the statistic is not
   verified, however plausible and whatever the source's reputation.
3. **Two numbers that differ much between sources go to a human**, not to the writer's preference. The
   fact-checker marks conflicting data for human review.
4. **Quotes follow the same test**: the words match, the attribution is right and the meaning is not
   changed by the way it is used (an altered "might, if" turned into "will" is a misquote, in its
   example).

## 2.2 Access and source type
1. **A paywalled source is not verified on faith.** The fact-checker cannot read behind a paywall, so it
   needs a free corroborating source that confirms the data points before marking it verified.
2. **A source whose type does not match what was cited is flagged**: a blog cited as an academic journal
   is its example.
3. **A dead link means replace the source**, not keep the number: it is flagged for removal until a
   replacement is found.
4. **A rate-limited source is retried once and stays unverified if still blocked; one that times out is
   marked as a timeout** (same agent). Do not promote "could not check" to "checked".

## 2.3 One source is not enough for a key claim
1. **A key claim resting on one source is not verified.** In ContentForge, a statistic in the title, the
   thesis or the core argument of a section counts as key, and a single-sourced one blocks its gate until
   a second independent source is found or the number is removed.
2. **The count is a policy choice.** That tool configures two corroborating sources and a narrow exception
   for a non-key supporting statistic from a primary source publishing its own data, attributed in the
   text and hedged in scope. Write down your own count and your own exception. Own guidance: say which
   claims count as key before checking, not after.
3. **A source count is a threshold too.** The same tool asks for 10 of its 12 to 15 sources to be
   reachable; that is its configuration, not a rule.

## 2.4 What the number means
1. **Sample size and population**: is it stated, and is it the population your sentence implies (one
   country versus global)?
2. **The definition of the metric**: its example is "use AI" meaning at least once versus regularly.
3. **The time period**: a stated quarter or year, not "recent data".
4. **Mark the quality.** In the fact-checker a vague methodology or unclear definition means use with
   caution, and an unreliable methodology or no source transparency means replace the figure. Own
   guidance: write the sentence of your claim only after reading these three facts.

## 2.5 Recency
1. **Write age limits down, per field.** The fact-checker's configuration uses 2 years by default and 1
   year for two fast-moving fields, 5 for another; those are its settings. Choose yours per subject and
   keep them in the claim table.
2. **An evergreen exception must name why** the topic is evergreen and state that no newer figure exists.
3. **Measure age against today's date**, not against the date the draft was started (same agent).
