# ad-measurement-pitfalls §3 — Why platform numbers differ

An ad platform, a web analytics product and a CRM will not agree, and most of the time none of them is broken.
`skills/metric-movement-diagnosis-pitfalls` §3 covers the generic causes (definition, filters, grain, time
zone, refresh); this section adds the causes specific to advertising and an order for checking them.

## 3.1 Structural reasons for a gap
1. **Date basis.** An ad platform books a conversion to the day of the click; an analytics product books it to
   the day it happened. For a long cycle this alone makes the recent window differ, and recent ranges grow
   afterwards.
2. **Credit rule.** A platform credits its own clicks; an analytics product with a cross-channel model splits
   credit across all channels, so it usually gives a paid channel less.
3. **Who counts as having seen the ad.** Platforms may count a conversion after a view with no click, and
   across devices for people they can recognise when signed in. Analytics cannot see either.
4. **Counting rule.** One conversion per click against every conversion, first against all, per event against
   per session.
5. **Attribution window.** A conversion on day ten after the click exists for a platform with a thirty-day
   window and is invisible to one with a seven-day window. Windows differ by platform and change; read the
   one in use (`re-read before relying`).
6. **Modelled conversions.** Where consent signals reduce what can be observed, platforms and analytics each
   fill the gap with their own estimate, by their own method. Two estimates are two opinions.
7. **Processing lag.** Reports fill in over hours or days, and imports from one system to another add more.
   The newest days are incomplete in every source.
8. **Time zone and currency.** Different day boundaries and conversions of value move rows across days.
9. **Two senders of the same action.** A native tag plus an import, or browser plus server without a shared
   identifier, inflate one side (§2.4). This is a defect, not a structural gap, and it is the first thing to
   rule out when one platform is far above the others.
10. **Environmental loss.** Blockers, privacy settings in browsers, banners that stop tags before consent, a
    cookie that expires, a click identifier stripped on the way (§1.3). These lower every browser-side number.
    How large they are depends on audience and on setup; measure the account's own gap between the CRM and the
    platform and do not quote a figure from elsewhere.

## 3.2 What to line up before comparing
1. **Line up five things first**: the conversion action, the date basis, the time zone, the window, and the
   campaign scope. Plenty of healthy accounts show a large gap for definitional reasons alone.
2. **Expect a gap, and do not quote a "normal" band.** Practitioner material in the sources states a normal
   percentage between ad platform and analytics and a higher one to investigate. Neither number has a primary
   source and both depend on audience, so none is carried. Investigate instead when the gap changes suddenly
   against its own history, when its direction flips, when one source reads zero, or when one platform is far
   above all the others.
3. **A threshold is a trigger to look, not a verdict.** Write down your own trigger for this account from its
   own past gaps, with the owner of the report (`skills/metric-movement-diagnosis-pitfalls` §3.1).
4. **Never judge the last few days** of any source (`business/paid-media-decision-pitfalls` §2.3).

## 3.3 Never turn a gap into a multiplier
A platform that claims twice what analytics shows does not mean "halve the platform". Check windows, view
credit and double counts first; if the question still matters, test it with a holdout (§4.3). A fixed ratio
carried from one account or one quarter to the next hides the cause and breaks the first time anything
changes.

## 3.4 Conversions with no leads, and leads with no conversions
1. **Conversions but no real leads**: bots, test entries, duplicate counting, a form tool that failed to
   deliver (check the form tool's own entries before blaming tracking), and soft signals counted as
   conversions (§2.3).
2. **Leads but no conversions**: a visitor who refused or could not be tracked, a confirmation page that never
   loads (an embedded form, a script-driven page), a click identifier stripped on the way (§1.3), a lead who
   arrived by a path the tag cannot see (phone, a reply by email, chat), a window that expired, or a different
   action than the one reported.
3. **Absence of a tag in the page is not absence of tracking.** A server integration, an import job and a
   native connector leave nothing in the markup. Ask what already sends conversions before concluding
   anything is missing.
