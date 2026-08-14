---
name: community-management
description: Use when running the ongoing conversation on an account or a community: replying, moderating, handling criticism, routing what arrives, and what a community manager must never answer alone.
---

# community-management

Business layer (`business/README.md`), communication. `business/content-creation` decides what's worth
saying and `business/social-publishing` gets it out. Neither covers the part that takes the actual time:
**what happens in the replies, every day, including the days something is broken.**

The job's real difficulty isn't writing replies, it's that a community manager is asked, in public and
under time pressure, questions that belong to engineering, sales, security and legal. Most damage here
comes from a helpful person answering something that wasn't theirs to answer.

## When
As soon as an account, a Discord/Slack community, a forum, a subreddit or a comment section is open to
the public — from the first day, not once volume justifies it.

## Steps

### 1. Write the rules before you need them
1. **A short published policy**: what isn't allowed, what happens when it is, and who decides. Three
   lines beat three pages nobody reads.
2. **Consistency matters more than severity.** The same behaviour treated differently twice is how a
   moderation decision becomes the story.
3. **What you tolerate early becomes the culture.** The tone of the first hundred members is the tone of
   every member after, and it's far cheaper to set than to correct.
4. **Name the escalation path in advance** — who to reach for a legal threat, a security claim,
   harassment, or a customer about to churn. Finding this out during the incident is the failure.
5. **State the response expectation you can actually hold** (business hours, next working day). A promise
   of speed you miss costs more than a modest promise kept.

### 2. Sort what arrives, then answer
Four kinds of incoming, and they route differently:
1. **A question** → answer it, or say who will and by when. "I don't know, I'll find out" is a complete
   reply.
2. **A bug** → `skills/bug-triage`. Get the version, the account and what they did; never diagnose in
   public.
3. **A complaint** → acknowledge the concrete part, say what happens next, move to a private channel only
   if personal data is needed. Never leave it visible with no reply.
4. **Criticism** → the most valuable of the four and the one handled worst. If it's fair, say so.

Rules that apply to all four:
- **Never promise a fix, a date or a feature in a comment.** That's an engineering commitment made by
  whoever happened to be at the keyboard (`business/sales-support` §2).
- **Never speculate about a cause** — same reason as during an incident.
- **Answer the reader, not the tone.** Extract the factual question and answer that.
- **Short and factual.** A long defensive reply is read as a defence, and it's the part screenshotted.

### 3. Criticism, trolls and pile-ons are three different things
1. **Criticism**: engage, concede what's true, correct what's wrong once, with a fact. Then stop.
2. **A troll**: no engagement. The policy applies, quietly and consistently.
3. **A coordinated pile-on**: stop replying individually. One clear public statement, then let it pass —
   replying fifty times feeds it and exhausts the person doing it.
4. **Never delete criticism.** Deleting is noticed, gets screenshotted, and converts a product complaint
   into a story about hiding things. Moderate what breaks the policy, never what stings.
5. **A single correction, then let the record stand.** Arguing to win in public loses even when you're
   right (`business/internal-communication` §4).
6. **When it's about an outage**, it's `business/incident-communication`: no cause speculation, the
   announced cadence, and never before affected customers have been told.

### 4. What is never answered alone
Route these out, the same day, without a public reply beyond "thanks, we're looking at it":
1. **A security report or a vulnerability claim** — never discussed publicly, whatever the reporter does.
   It goes to whoever owns security, privately.
2. **A legal threat, a takedown, a defamation or trademark claim** → legal, untouched.
3. **Harassment, threats, or content targeting a person** → the platform's mechanisms plus the internal
   owner. A community manager does not carry this alone, and the account owner needs to know.
4. **Illegal or hateful content** — removal duties and their deadlines are jurisdiction-specific legal
   questions (`business/regulatory-watch`), not a judgement call in a comment thread.
5. **A contractual question** — SLA, certification, data location, pricing → its owner
   (`business/sales-support` §4.3).

### 5. Listening, and routing it back
1. **Watch mentions, not just replies.** The most useful feedback is written somewhere you're not tagged.
2. **Route it where it's actionable**: bugs to `bug-triage`, feature demand to whoever owns the product,
   confusion about wording to `business/ux-writing`, recurring questions to the documentation.
3. **Recurring questions are a product signal**, not a support cost. The third identical question is a
   design or a documentation problem.
4. **Report honestly upward**, including what people dislike. A summary that only carries praise makes
   the whole channel worthless as a signal.

### 6. Personal data, in the details
1. **DMs, tickets and screenshots contain personal data** (`business/data-protection`). Don't copy them
   into an internal channel wholesale, and don't paste a screenshot showing someone's account.
2. **Never ask for a password, a token or full payment details.** Ever, in any channel — and say so
   openly, because impersonation of support accounts is common.
3. **Never republish someone's message or image** without their agreement, including a flattering one.

### 7. Measure what means something, and keep it sustainable
1. **Useful signals**: replies between members rather than only to us, questions answered without our
   involvement, recurring themes, time to first reply. **Follower count is not one of them.**
2. **A metric that rewards volume produces volume.** If engagement is the target, engagement bait is the
   result (`business/content-creation` §3.5).
3. **Nobody carries an account alone.** Cover for absences, and a named backup — otherwise the quiet
   outcome is that replies stop and nobody notices for a week.
4. **Hostility is aimed at the account, not the person answering.** That's a structural rule, not
   encouragement: anything abusive gets escalated and the person gets backup, not resilience advice.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: a published policy with an owner, a stated response
expectation being met, the escalation paths named before they're needed, incoming routed rather than
answered out of scope, and an honest periodic summary including the criticism.

## Guardrails
- **Never delete criticism**, and never moderate for tone what the policy doesn't cover.
- **Never answer a security report, a legal threat or a harassment case publicly or alone.**
- **Never promise a fix, a date or a feature in a comment.**
- **Never argue publicly with a customer**, and never reply more than once to the same point.
- **Never ask for or accept credentials**, and never reuse personal data from a DM elsewhere.
- **An agent never posts a reply on its own.** It can draft; a human sends
  (`business/social-publishing` §1.2). A wrong reply in a public thread cannot be recalled.
- Where a company has a communications owner or an existing policy, they decide; this is the fallback.

## Origin
Reviewed for this: a community-management skill from a Claude skills marketplace (platform selection,
moderation policy templates, an engagement ladder, and metrics — DAU/MAU, member-to-member replies,
support deflection) and a B2B SaaS social-media-manager skill covering community engagement and crisis
response. Two things taken and rewritten: **member-to-member replies and deflection as the meaningful
metrics** rather than follower count, and its central observation that what's tolerated among the first
members becomes the culture for everyone after.

Written **without internal community-management expertise**. What's ours: §4 in full — the list of things
a community manager must never answer alone is the failure mode we actually expect, and it exists because
a helpful reply to a security report or a legal threat is worse than a slow one; the four-way sort in §2
with its routing into `bug-triage`; separating criticism from trolls from pile-ons; and §7.3–7.4, because
an account carried by one unbacked person fails silently. Verified 2026-08-06.
