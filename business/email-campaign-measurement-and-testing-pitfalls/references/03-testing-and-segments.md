# email-campaign-measurement-and-testing-pitfalls §3 — Testing and segments

The general discipline of a test is `skills/experiment-design-pitfalls`: one hypothesis, one primary metric fixed
before the send, a sample size from a formula, one look at the result. This section adds only what email
changes. Read that block first when planning.

## 3.1 Pick the metric first, and let it survive
1. **The primary metric is chosen before the test and must be one a person produced.** A subject-line test
   judged on opens is invalid for the reasons in §1: the winner may be the variant more readers' relays fetched.
2. **A test judged on a click followed by a session, a reply, or a downstream conversion is valid**, subject to
   the sample the programme can supply. If the audience is too small to see a difference on that metric, the
   honest result is "cannot test this here", not a switch to opens.
3. **Vendor guides still teach opens as the main test result**, with a bot filter and a 24 to 48 hour wait.
   Those figures (and a 1,000-per-variant rule) were not taken; the sample comes from a formula.

## 3.2 The unit is the recipient
1. **Randomise recipients, not sends or days.** Two campaigns on two days are not a test: the day is
   confounded with the variant.
2. **One recipient sees one variant**, in every message of the test, if the test spans several.
3. **A segment built from opens contaminates a test.** If the audience was selected by who opened before, the
   result describes the relay mix as much as the copy.
4. **Check the split** (recipients per arm against the plan) before reading, as in the general block.

## 3.3 The winner is a second decision
1. **Sending the winning variant to the rest of the list is a different decision from the test.** The test
   answered "which was better among those who got it". The follow-up sends to people who were not in it, at a
   different time.
2. **A tool that picks a winner automatically after a wait** has chosen the metric and the wait for you.
   Check which metric it uses and set it to the one in §3.1 or do not use the automatic choice.
3. **Results do not transfer** between segments or programmes by default. A winning subject for new customers
   says nothing certain about long-time ones.

## 3.4 Send time
1. **A time-zone and weekday claim is an untested hypothesis** until run on this audience, with the same rules
   as any test: recipient as the unit, a metric from §3.1, a sample that can show a difference.
2. **The sources' "best days and hours" are folklore.** They differ by guide, none is sourced to a method we
   could read, and none is carried.
3. **Recipient time zone matters for a different reason**: a message arriving in the middle of the night is a
   service problem, not a test result.

## 3.5 Segments built on engagement
1. **State which signal defined the segment and over what window**: "no click and no session in 90 days", not
   "inactive".
2. **Dormancy defined by opens is the common defect** (§1.2). It labels readers behind a relay as active and
   readers with images off as gone.
3. **Segment membership changes over time.** A test on "active" recipients selected on the send date is not the
   same population as the segment next month.
4. **A re-engagement attempt precedes removal**, and what counts as a response is a human signal
   (`business/email-deliverability-and-sender-requirements-pitfalls` §3.3).
5. **Removing contacts also changes the audience's data footprint**: how long inactive contacts' data is kept
   is for `business/data-protection`.

## 3.6 Failure patterns
- **Subject test won on opens.**
- **Two days, two variants.**
- **Automatic winner on a metric nobody chose.**
- **Winner assumed to hold in another segment.**
- **"Best send time" from a blog post.**
- **"Inactive" with no definition.**
