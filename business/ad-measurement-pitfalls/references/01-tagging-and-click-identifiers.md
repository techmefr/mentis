# ad-measurement-pitfalls §1 — Tagging and click identifiers

Every attribution number rests on a link that carried the right labels to the right page. When it did not, the
traffic still arrives, only under the wrong name or no name. Points 1.1, 1.3 and the auto-tagging fact were
checked against two Google help pages on 2026-10-20 (read through a fetch tool that returns a digest, not the
raw page); the rest is method.

## 1.1 Campaign link hygiene (checked against Google's UTM page)
1. **Always set source, medium and campaign.** The page names more parameters (an identifier, the originating
   platform, term, content, and two newer ones about creative format and marketing tactic, which it says are
   not currently reported), and recommends the three first. Optional extras are optional.
2. **Values are case sensitive.** `google` and `Google` are two different values, and so are two spellings of
   a campaign name that differ by case or by an underscore. The page recommends a strict naming convention with
   lowercase as the standard; write the convention down once, in one place, and build every link from it.
3. **A missing parameter shows as "(not set)" in reports.** That is a gap in the link, not a quirk of the
   report. Count the "(not set)" share as a tagging defect to fix at the source.
4. **One link per placement.** If two ads or two emails share one link, their clicks cannot be told apart
   afterwards. Give each placement its own content value rather than splitting the traffic in the report.
5. **Optional own guidance: name by the kind of deal and who sent it.** For partner and affiliate traffic, let
   the medium name the kind of arrangement and the source name who sent it. It is a convention that keeps
   reports sortable, not a platform requirement.
6. **Where a platform fills parameters automatically** (dynamic values), check the result on a real click
   rather than trusting the template; a template that works in a link builder can be rewritten on its way to
   the page.

## 1.2 No personal data in a link (own guidance)
Google's page does not discuss personal data in link parameters; this point is ours. A link parameter is
copied into analytics reports, server logs, the referrer sent to other sites and anything that stores the
address. Put campaign labels in it, never an email, a name, a phone number or an identifier that maps to a
person. If a personal identifier must travel for a lawful purpose, that is a data-protection decision
(`business/data-protection` §4) and not a link-building choice.

## 1.3 The click identifier and redirects
1. **Auto-tagging appends a click identifier to the landing address when someone clicks.** Per Google's page,
   it supports conversion tracking across browsers, importing conversions from analytics or a CRM, importing
   cost and campaign data into analytics, and offline conversions, and it is on by default for new accounts
   (`re-read before relying`). If analytics has a tag on the site, the identifier is stored in a cookie on the
   site's domain.
2. **The identifier has to reach the final landing page.** When the site redirects (to https, to another
   hostname, through a vanity or shortened address, by country), the identifier must survive each hop. A hop
   that drops the query string loses attribution for everything on that path, and the loss is silent.
3. **In the analytics product named, auto-tagging takes priority over manual tags and cannot be overridden**,
   so a manual label on an auto-tagged click is ignored there (Google's page; `re-read before relying`). If
   you want manual labels to win, that is a decision to take with the account settings, not by adding more
   parameters.
4. **Some sites reject unknown parameters and show an error page.** Google's page says to click an ad and check
   that the page loads, and if it does not, to have the site accept arbitrary parameters before turning
   auto-tagging back on.
5. **Where paid traffic shows up as another channel in analytics**, suspect first that auto-tagging is off or
   that a hop or a script removed the identifier, before blaming the platform.

## 1.4 Test the final address
1. **Follow the whole chain with a test address** carrying a fake identifier, hop by hop, and check what
   arrives at the end and what is stored. A fake identifier proves transport only; it matches no real click, so
   a passing test never proves attribution works.
2. **Retest after anything that changes addresses**: a migration, a new redirect rule, a new shortener, a
   router change in a single-page site that rewrites the query string on first load.
3. **Test from the real source.** A click on an actual ad is the only test that exercises the full path; a
   direct visit never appears as an ad conversion.
