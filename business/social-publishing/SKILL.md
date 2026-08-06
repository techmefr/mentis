---
name: social-publishing
description: Use when something is going out on a public social platform — a launch post, a recruitment post, a technical thread, a company page update, a video — covering who approves it, how one message adapts per platform without becoming four different truths, and what must never be automated.
---

# social-publishing

Business layer (`business/README.md`), communication. Two facts shape everything here, and both are
usually discovered late.

**A post is published, not sent.** It gets screenshotted, indexed and quoted, and deleting it removes
nothing that already travelled. Every claim in it is as binding as one on the website
(`business/product-marketing` §2).

**Programmatic posting is gated, per platform, and the gates move.** The writing is the easy part; the
access is the project. Anyone planning an automation before checking the platform's current terms is
planning around an API they may not be allowed to use — see `references/social-platforms.md`, which holds
the dated per-platform reality this block deliberately doesn't repeat.

## When
Before publishing on X, LinkedIn, Facebook, Instagram, TikTok, YouTube, Threads, Bluesky, Mastodon,
Reddit, Pinterest, a Discord or Slack community, a company blog, or any other public account — whether
posted by hand or by a tool.

## Steps

### 1. Establish the owner before writing anything
1. **Every account has one owner** who decides what goes out. If nobody can name them for a given
   account, that's the finding, and it blocks publication.
2. **An agent never publishes.** It drafts; a human approves and presses the button. This is not a
   maturity issue to be fixed later: an autonomous poster on a company account is an unbounded
   reputational exposure with no undo.
3. **Route the claims** — anything about the product goes through `business/product-marketing`, anything
   about an incident through `business/incident-communication` (and never before the customers affected
   have been told), anything legal or contractual to legal.
4. **Recruitment and employer-brand posts have their own owner**, usually not the same one. Say something
   about hiring conditions and it can be held against the company.

### 2. One message, adapted — not four messages
1. **Write the substance once**: what it is, who it's for, what changes. That's the part that must be
   identical everywhere, because people follow you in more than one place.
2. **Then adapt the form per platform**: length, tone, whether links are penalised, whether the first
   line is the whole preview, media format and aspect ratio. The constraints are per-platform data and
   they change — read them from the reference file, don't memorise them.
3. **Never let the adaptation change the claim.** A number that grows on the platform where it fits is
   the failure this rule exists for.
4. **Write for someone who sees only this post.** No internal project names, no "as we said last week".
5. **Don't cross-post mechanically.** A message reformatted by a tool but not re-read is the most common
   way an internal codename or a broken link ships.

### 3. What every post owes before it goes out
1. **Alt text on every image**, captions or subtitles on every video. This is the same obligation as
   `skills/accessibility` applied outside the product, and it's the one most often skipped.
2. **Nothing personal that isn't cleared.** A screenshot with a real customer name, a photo of someone
   who didn't agree, an email address in a demo — each is a disclosure
   (`business/data-protection`). Employee photos need their agreement, and it is revocable.
3. **No customer name, logo or quote without their written agreement.** Theirs to give, not ours.
4. **Sponsored or paid content is disclosed as such**, per the platform's rules and the local
   advertising rules. Undisclosed paid promotion is a regulatory problem, not a style choice.
5. **Third-party media is licensed** — image, music, font, clip (`business/licence-compliance`). Music on
   a short video is the recurring trap.
6. **Check the links from a logged-out session.** A link that works for you because you're authenticated
   is the classic broken launch post.
7. **Read it once as a hostile reader.** Not to soften it, to find the sentence that will be quoted back.

### 4. If it's automated, automate the drafting only
1. **Draft-and-schedule with a human gate is fine. Post-without-review is not**, whatever the tooling
   makes easy.
2. **Prefer the platform's draft or inbox mode** where one exists, so the last step stays manual.
3. **Credentials are per-platform tokens with real scope** — never in a repo, never in a log
   (`skills/auth-session-conventions` §2.4), and revocable by the account owner without a developer.
4. **Rate limits and per-post costs are real** and are one of the reasons an automation gets switched off
   again; know them before designing around them.
5. **A scheduled post is a commitment made in the past.** Anything that could be overtaken by events —
   an incident, a delay, bad news — gets re-read before it fires, or isn't scheduled.

### 5. Afterwards
1. **Someone watches the replies.** Publishing with nobody reading the responses is worse than not
   publishing, because a question in public that goes unanswered is visible.
2. **Escalate, don't improvise**: a support issue goes to support, a security claim to whoever owns
   security, a legal threat to legal. Never debate a customer complaint publicly.
3. **Correcting is better than deleting.** A silent deletion is noticed and reads as hiding; a correction
   with the reason doesn't.
4. **Measure what you said you'd measure**, and don't publish an engagement number as a product number
   (`business/product-marketing` §2.2).

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a named owner and approver, the substance written
once with per-platform adaptations that don't alter it, alt text and captions present, media and personal
data cleared, disclosures where required, links checked logged-out, and someone assigned to the replies.

## Guardrails
- **Never publish, schedule or reply on a company account without a human approving that exact content.**
- **Never make the adaptation change the claim**, and never publish a number nobody measured.
- **Never publish personal data, a customer name or a logo without written agreement.**
- **Never post about an incident before the affected customers have been informed.**
- **Never hide a paid relationship.**
- Never store or log a platform token, and never let posting credentials outlive the person who owned
  the account.
- Where a company already has a communications or brand owner, they decide; this block is the fallback.

## Origin
Reviewed for this: a community Claude skill suite for social media (`social-ai-team`, ten skills — brand
onboarding, calendar, one writer per platform, publisher, performance review) and the MCP publishing
servers now available (a multi-platform posting server, plus MCP shipped by the mainstream scheduling
vendors during 2026). Two things taken: its **pause-and-approve gate at every handoff**, which matches our
doctrine exactly, and the observation that its per-platform writers differ only by form constraints.

Rejected, deliberately: **one skill per platform.** Eight near-identical blocks would drift into eight
different versions of the same claim, which is the fragmentation `when-stuck` was written against. One
block holds the discipline; the volatile per-platform facts live in `references/social-platforms.md` under
`skills/source-freshness`. Also rejected: any dependency on a paid generation or scheduling service, which
would make every consumer of this framework buy a subscription (rule B).

Written **without internal communications or social-media expertise**. What's ours: the owner-before-
writing rule, "one message adapted, never four messages", the accessibility and licensing obligations
applied outside the product, and §4.5 — a scheduled post is a commitment made in the past, which is how a
cheerful launch post fires during an outage. Verified 2026-08-06.
