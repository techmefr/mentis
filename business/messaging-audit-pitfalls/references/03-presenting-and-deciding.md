# messaging-audit-pitfalls §3 — Presenting findings and deciding

An audit that ends as a list of nitpicks changes nothing. What leadership needs is the structure of the
finding, the risks first, and the two or three decisions that gate the rewrite.

## 3.1 How to present
Structure the report in this order (chrisrodde audit mode):
1. **The inventory with dates**, so vintage is visible.
2. **The core finding in a sentence**: usually one structural problem.
3. **The inconsistencies**, evidenced, in tables, with the surface named.
4. **Risk items first in priority**: anything legally or factually exposed, called out separately.
5. **What is working**: the strongest existing artefact and why. There is usually one better than the
   rest; naming it gives the rewrite a template and the team a win.
6. **The decisions that must be made**: the two or three forks that determine everything downstream.

The pmalliance consistency skill's report adds a consistency table (message element, what the reference
says, where it diverges, surface, severity), a short list of priority fixes with the specific edit for
each, and a watchlist of lower-stakes divergences for later.

## 3.2 Tone of the finding
1. **Do not soften the structural finding.** A team that asked for an audit wants the diagnosis; a hedged
   one wastes the engagement.
2. **Do not moralise about how it happened.** Drift is normal and usually comes from a company moving
   fast (chrisrodde).
3. **Deliver it plainly, with the evidence attached.**

## 3.3 Patch or rebuild
1. **Rebuild when** there are several heroes or several categories, core differentiators became table
   stakes, the target customer has changed or is about to, a strategic decision postdates the framework,
   or the framework was built narrative-first (chrisrodde).
2. **Patch when** the decision is sound and only its expression is weak, only specific claims are stale or
   legally exposed, or the problem is distribution and adoption rather than content.
3. **Say which you recommend and why.**
4. **If a strategic decision already taken contradicts the framework** (a new category, a new segment, a
   decision about what the product is called), surface it immediately and prominently. The source calls it
   almost always the real finding, with everything else downstream.

## 3.4 After the decisions
1. **Rewrite only after the decisions of §3.1 are taken.** Own guidance: the audit's output is an input
   to `business/product-marketing` §1, not a replacement for it.
2. **Send the claims you found to the claim check** (`business/marketing-claim-substantiation-pitfalls` §1),
   so a stale claim is not carried into the new copy.
3. **Re-run the checks that produced risk items** after the fix, on the same surfaces, and record the date.
   Own guidance.
