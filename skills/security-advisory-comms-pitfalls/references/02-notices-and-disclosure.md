# security-advisory-comms-pitfalls §2 — Notices and disclosure

The failure this section prevents is an advisory that cannot be acted on: no versions, no fix, no date, or one
that reaches the people who must patch on a Friday evening.

## 2.1 The patch itself
1. **Make it easy to adopt.** The guide says a fix should not force users onto a different API or remove
   functionality unless that is unavoidable; if it must, look for a mitigation that does not require the
   change, because many users cannot install such a change quickly.
2. **Work out affected versions during assessment** and note backward compatibility and upgrade needs (for
   example: version A is affected and the fix is only available from a later version, so users must upgrade).
   The announcement needs this.
3. **Develop privately.** A patch tested in public can be read by an attacker before it ships. If the flaw is
   already widely known, the guide says there is no advantage to secrecy and public development is better.

## 2.2 Prepare the release, do not cut it
1. **Prepare the release and hold it** until the embargoed notice (if you use one) has gone out. Otherwise the
   people you meant to warn learn about it from the public release.
2. **Decide who is on the embargo list and why.** The guide says an embargo list is about giving those who run
   other people's systems time to prepare, not about avoiding embarrassment or favouring large customers, and
   that it is probably unnecessary without a significant provider ecosystem.
3. **An embargo list has costs**: more people know early, it adds time before the fix is public, and the guide
   quotes another team's observation of leaks and slower releases. Weigh severity, how hard the patch is to roll
   out and how long the list is.

## 2.3 Choose the day
1. **Avoid the days before weekends and widely observed holidays**, so people can update in working time. The
   guide suggests early in the working week when the flaw is not being exploited.
2. **Allow providers real time**, and account for holidays and busy periods of the businesses on your list.

## 2.4 The embargoed notice
1. **Contents**: the identifier, a short description, the reporter's credit, affected versions, how and when the
   patch will be delivered, and the public disclosure date.
2. **Say plainly that it is confidential and must not be forwarded**, and that nobody may publish, notify users
   or release patches before the date.
3. **Promise to tell the list at once if the date is at risk or changes**, and have someone watch for replies.

## 2.5 The public advisory
1. **A summary** short enough for a vendor to assess quickly, then the identifier, the affected versions and
   the reporter.
2. **Severity with a reason and an attack scenario.** If you give a CVSS score, include the vector string.
3. **Reproduction steps** so others can verify the fix.
4. **Remediation and mitigation**, naming the fixed versions.
5. **Exploitation in the wild**, if known.
6. **A timeline**: reported, fixed, disclosed.
7. **Do not hold exploit details back beyond a few days.** The guide says withholding only helps when the attack
   is not obvious, which is rare, and that attackers can read the patch to work it out.
8. **Publish where users look**: release notes or security bulletins, plus the community's announcement lists.
   A machine-readable record of affected versions helps users match their own.
