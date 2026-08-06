# Social platforms: publishing reality

> Reference doc for `business/social-publishing`. Holds the **volatile** facts that block keeps out of
> itself: who gates programmatic posting, what it costs, and which platforms are worth the effort.
>
> **Verified 2026-08-06. Treat anything here as unverified after six months** — this is the fastest-moving
> table in the repo (X changed its pricing model twice during 2026 alone). See `skills/source-freshness`:
> past its window a fact is unverified, not wrong, and gets re-read against the platform's own developer
> documentation — never against a vendor blog.

## Why this file exists

The recurring mistake is planning an automation around an API you turn out not to be allowed to use. On
most platforms, publishing programmatically to an account you don't personally own requires an app review
or a partner status, and several now bill per post. **Check access before designing the workflow**, and
before promising anyone a cadence.

Everything below is *access reality*, not editorial advice. Tone, length and format belong in the platform's
own current documentation, which is exactly the thing that goes stale in a written table.

## Publishing access, by platform

| Platform | Programmatic posting | Practical gate |
|---|---|---|
| **X** | yes, paid | Free tier discontinued; pay-per-use is the default for new developers, billed per post created (more when the post contains a link) and per read. Several engagement endpoints moved to enterprise-only during 2026. |
| **LinkedIn** | organisation pages via the Community Management API | Marketing Developer Platform **partner approval**, in practice reserved for enterprise partners. This is the hardest gate of the set for anyone posting on behalf of accounts they don't own. |
| **Instagram** | yes | Professional/Business account + linked Facebook Page + Meta app + an approved content-publishing permission (review measured in business days). Two-step publish (container, then publish), with per-account hourly call limits and a daily published-post cap. |
| **Facebook Pages** | yes | Meta app and page permissions; same review machinery as Instagram. |
| **TikTok** | yes | Content Posting API, app audit required. Two modes: direct post, or **upload to the creator's inbox/drafts** so a human publishes — that second mode is the one that fits our approval rule by construction. |
| **YouTube** | yes | Data API with a quota that an upload consumes a large share of; plan around the quota, not around the request. |
| **Threads, Bluesky, Mastodon** | yes | Threads through Meta's API; Bluesky and Mastodon are open and by far the least gated. |
| **Pinterest, Reddit** | yes | Own app registration and content rules; Reddit's rules are subreddit-level and unforgiving of anything reading as promotion. |
| **Viadeo** | **no realistic route** | ~4M French accounts, mostly inactive, down from a 2017 peak; acquired by the Le Figaro group and repositioned toward company reviews and employer brand, with company pages moved to the group's jobs brand and job posting removed. No evidence of a usable third-party publishing API. **Verdict: not a publishing channel.** If it matters at all it's an employer-brand surface, handled by hand by whoever owns recruitment. |

## Format mechanics (for `business/content-creation`)

**Read this section with more suspicion than the one above.** Platform access is documented by the
platforms; format mechanics are *community-observed heuristics* — measured by people with different
audiences, on algorithms that change without announcement, and repeated between blog posts until they
sound like rules. Treat every line here as "reported", verify against a platform's own current guidance
where one exists, and above all **check it against what has actually worked on our own accounts**, which
is the only measurement that concerns us.

| Platform | Reported mechanics |
|---|---|
| **LinkedIn** | the fold is short — the first line or two is the whole preview; medium-length posts (roughly 900–1300 characters) are commonly reported as the sweet spot; outbound links are widely believed to reduce reach, hence the convention of putting the link in the first comment; first-person writing outperforms company-voice |
| **X** | 280 characters per post; threads of ~6–10 posts to carry one argument; the first post is the whole decision to read or not; links reduce reach, and now also cost more per post via the API |
| **Instagram** | image and short video first, caption second; carousels for step-by-step; hashtags far less load-bearing than they were |
| **TikTok / Shorts / Reels** | vertical 9:16, the first seconds decide everything, captions burned in because most viewing is silent |
| **YouTube** | title and thumbnail are the click decision and are worth more effort than the edit; the first 30 seconds decide retention; chapters help long technical content |
| **Threads / Bluesky / Mastodon** | conversational, short, links tolerated — the least penalised place to send someone elsewhere |
| **Reddit** | subreddit rules override everything, and anything reading as promotion is removed; only useful with a real answer to a real question |
| **Newsletter** | one idea per issue, and the subject line is the whole open decision |

## Aggregators

Multi-platform MCP servers exist (a dedicated posting server, plus MCP connectors shipped by the
mainstream scheduling vendors during 2026). They solve the access problem by holding the partner status
themselves.

**Our position:** usable by a human who has chosen and paid for that vendor, never a dependency of a
mentis block (rule B — no consumer of this framework should have to buy a subscription to run a block).
And an aggregator does not relax the approval rule: it makes posting easier, which is precisely why the
human gate matters more, not less.

## Rules that don't change with the table

- **A human approves the exact content before it leaves.** No exceptions, no maturity path toward
  autonomous posting.
- **Tokens are per-platform, scoped, revocable by the account owner, never in a repo or a log.**
- **Prefer a draft/inbox mode** where the platform offers one, so the final action stays manual.
- **Per-post cost and rate limits are design constraints**, and a common reason an automation gets
  switched off a month later.
