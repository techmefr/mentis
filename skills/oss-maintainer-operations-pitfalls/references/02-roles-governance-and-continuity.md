# oss-maintainer-operations-pitfalls §2 — Roles, governance and continuity

> Part 2 of `skills/oss-maintainer-operations-pitfalls`. Read it when someone asks for access, or the project
> depends on one person. Source, read 2026-10-20: Open Source Guides, "Leadership and Governance" and the
> security chapter (CC BY 4.0). Sentences marked "own guidance" are ours and rest on no source read.

1. **Roles mean what you define.** The guide notes that "maintainer", "contributor" and "committer" mean
   different things in different projects: sometimes the holders of commit access, sometimes a list in the
   README. Define each in one sentence in your own project. A maintainer need not write code; it can be the
   person who owns the documentation or the community.
2. **Make roles public and attainable.** Listing leaders in a file or on a page tells people whom to ask and
   gives them ownership. Document how someone becomes a maintainer or joins a sub-team, in a governance file,
   so that it does not look like a closed circle. Let people volunteer for the areas they like rather than
   assigning them.
3. **Decide commit access by a stated rule.** The guide describes two camps: access for everyone who contributes,
   or access only for people who have shown commitment, and says neither is wrong. Own guidance: pick one,
   write it down, and back it with branch protection so that access to push is not the same as access to
   release.
4. **Name a second person for every critical power.** The guide advises moving a project from a personal account
   to an organisation and adding at least one backup administrator. Own guidance: list the powers that stop the
   project if one person vanishes (merge, release, package registry, domain, signing, security contact) and give
   each a second holder. Symptom: a release waits for one person's holiday. When no second person exists and none is realistic, point 12 gives the one-person variant instead of a finding nobody can fix.
5. **Choose, and write, how decisions are made.** The guide names three common shapes: one person with the final
   say, formal voting among active contributors, and consensus-seeking weighted by current work. Each has
   trade-offs; the guide notes the second's name carries negative associations for some communities. Own
   guidance: say who breaks a tie and how a disagreement is escalated, even if the answer is "the founder".
6. **Governance can wait, expectations cannot.** The guide says there is no right moment to write governance, and
   that it is easier once community dynamics have appeared, but conduct and the contribution process should be
   written at launch. A company launching a project should settle internally how it will take part, then say
   publicly what is particular about its involvement.
7. **Treat paid contributors like everyone else.** The guide says commercial activity is normal and a paid
   developer gets no special treatment: contributions are judged on merit, and people may state their use cases.
   Keep the discussion on the change, not on who pays for it.
8. **A legal entity only when money is involved.** The guide says a project needs none until it handles funds;
   donations are not automatically tax-deductible, and a fiscal sponsor is an alternative to forming a non-profit.
   This is background, not legal or tax advice.
9. **Limit privileges and secure them.** The security chapter asks that everyone with elevated rights uses
   multi-factor authentication, that write and admin access go only to those who need it and are reviewed
   regularly, and that protected branches stop unreviewed changes to the main branch.
10. **Spread the security duties too.** The same chapter says to assign who handles vulnerability reports, who
    reviews dependency updates and who approves patches, and to engage with upstream and downstream projects when
    something affects them.
11. **Write the hand-over path.** Own guidance: a short file saying who takes over when a maintainer steps down,
    how an abandoned module is marked, and what is archived rather than left to rot. A project whose last active
    maintainer leaves silently is worse off than one that is archived with a note.
12. **A one-person project: what to do when no second holder exists.** Own guidance. Symptom: every critical power
    (merge, release, registry, domain, security contact, conduct contact) sits with one account, the repository's
    owners file names only that account, and the contact page is that person's profile. A second administrator may
    not be available, and demanding one only produces a finding that stays open. Fix, in order of cost: write the
    hand-over file of point 11 (who may be asked to take over, and where the owner records the credentials and the
    domain, never in the repository); keep the contact channels separate from the personal account where the
    forge allows it; turn on multi-factor authentication and note it; decide in writing what happens to the project
    if the owner stops (archive with a note, §3.9); and invite a second holder only when someone has shown the
    commitment of point 3. Report the single holder as a known risk with its mitigations, not as an unmet check.
13. **A setting you cannot read is unverified, and the report says how to verify it.** Own guidance. Symptom: a
    page states that the main branch is protected, that every administrator uses multi-factor authentication, or
    that the issue queue is small, and nothing in the repository proves it; an audit from the files alone either
    believes it or guesses. Check: for each such claim, name the settings page or the forge query that settles it
    and who can run it (usually the owner), and record the result with its date. Fix: report "unverifiable from
    the repository: verify at <page or query>", and never record the claim as met or unmet. Indirect evidence (pull
    request numbers in the history suggest review through the forge) is stated as indirect.

## Checks (own guidance)
1. Each critical power has two named holders, and a list says who they are.
2. The governance file says how to gain a role and who decides a tie.
3. Every account with write or admin rights has multi-factor authentication on, and the list of such accounts
   was reviewed within the last cycle.
