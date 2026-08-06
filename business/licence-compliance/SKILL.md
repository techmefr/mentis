---
name: licence-compliance
description: Use before adding a dependency, vendoring code, or shipping a product that bundles third-party code, check what the licence obliges us to do while the choice is still cheap. Also covers code produced from copied snippets. Structured checklist, not legal advice.
---

# licence-compliance

Business layer (`business/README.md`), applied at step 6 of the dev pipeline. A dependency is a legal
commitment that arrives through a package manager, which is why it gets made by whoever is closest to
the keyboard and reviewed by nobody.

The cost profile is what makes this worth a block: checking before installing takes a minute, and
unwinding a licence problem after shipping means replacing working code under time pressure.

**Not legal advice.** It exists to catch the obvious cases and route the rest to someone qualified.

## When
Before adding a dependency, before vendoring or copying third-party code into the repo, before shipping
anything that bundles someone else's code, and when a dependency changes its licence in a major
version.

## Steps

### 1. Know what you're taking on
1. **Read the licence of the thing you're adding**, not the README's summary of it, and note it.
2. **Sort it into the category that matters**:
   - **Permissive** (MIT, BSD, Apache-2.0): generally fine to use in a product, but almost all of them
     still require **attribution** — keeping the copyright notice and licence text with what you ship.
     Skipping that is the most common violation and the easiest to avoid.
   - **Weak copyleft** (LGPL, MPL): usually workable, with conditions attached to how you link or
     modify it. Modifying the library itself is where obligations appear.
   - **Strong copyleft** (GPL, AGPL): obligations that can extend to **your** code. **AGPL in
     particular reaches software offered over a network**, which is exactly what a web product is. This
     is the one to escalate, not to reason about alone.
   - **No licence at all**: no permission. "It's on GitHub" is not a licence, and a repo with no
     licence file is the most restrictive case, not the least.
   - **Source-available / custom terms** (BSL, SSPL, "free for companies under N employees"): read the
     actual terms, and check whether our situation crosses their threshold.
3. **Check the transitive dependencies**, not just the one you typed. The lock file is the real
   inventory, and a permissive package can pull a copyleft one.

### 2. Escalate rather than interpret
Take to legal, don't decide alone: anything strong-copyleft in a shipped product, any custom or
source-available licence, any dual-licensed package where the free tier's conditions are unclear, and
any licence change in a version you're upgrading to. Frame the question with what you found (the
package, the licence, how we'd use it), which is what makes the answer fast.

### 3. Meet the obligations you accepted
1. **Attribution, mechanically.** Generate the notices from the lock file rather than maintaining a
   list by hand, and ship them where the product can show them.
2. **Keep licence headers** in any file you copied or vendored. Stripping them to tidy up converts a
   compliant copy into an infringing one.
3. **Record the decision** when a non-obvious licence was accepted, and why — an ADR is the right home
   (`skills/documentation-adr`). The next person will ask.

### 4. Copied code and generated code
1. **A snippet copied from a blog, an answer site or another repo carries that source's licence.** It
   doesn't become ours by being pasted. For anything beyond a trivial line, either write it or check.
2. **Code an assistant produced from a copyrighted body of work is a real question**, and not one this
   block can settle. Treat a suspiciously complete or recognisable chunk as needing the same check as
   a copied one.
3. **Our own code leaving the company** — a snippet in a public issue, an example in a talk, a block
   shared outside — is the same question in reverse: what's ours to publish is a decision, not a
   reflex. That's rule C's boundary in the dev framework, and it's the same instinct.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: the licence of what's being added, its
category, the obligations accepted, and either the notices generated or the question sent to legal.

## Guardrails
- **Never add a dependency whose licence you haven't looked at**, however small the package.
- **Never strip a licence header or a notice file.**
- **Never decide alone that a copyleft licence is acceptable for a shipped product.**
- No licence file means no permission: don't use it while assuming someone will grant it later.
- An automated scan is a starting point, not an answer: tools mislabel licences, and they can't tell
  how we're using the code.

## Origin
Assembled from public sources: the licence texts themselves and the widely published distinctions
between permissive, weak- and strong-copyleft terms. Written **without internal legal expertise**,
shaped as "recognise the category, then escalate" rather than as interpretations. The engineering
angles are ours: the lock file as the real inventory, generating notices instead of maintaining them,
copied snippets carrying their source's licence, and the symmetry with rule C for our own code leaving
the company.
