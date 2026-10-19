# security-advisory-comms-pitfalls §1 — Intake and embargo

The failure this section prevents is the reporter who goes public out of frustration because nothing came
back, or because a deadline was never discussed.

## 1.1 Acknowledge before you assess
1. **Say you received it, quickly.** The guide says within one to two days, and notes that at this point you
   have probably not assessed anything; you are only saying you are on it. Set your own interval and publish it
   in the security policy; the guide's own example policy states a response time too.
2. **To assess, you need two things**: the steps the reporter took, and the systems, versions or packages
   involved. If the report is too thin, ask what lines, how the flaw creates a risk, what an attacker could
   ultimately do, how to reproduce it and what a fix would look like. The guide adds that you should still
   validate any contributed patch yourself.
3. **Use one intake path** and help a report that arrived by the wrong route into it, kindly.

## 1.2 Assess into four outcomes, and say why
1. **Four outcomes**: working as intended, a bug, a feature request, a vulnerability.
2. **A vulnerability is a compromise of confidentiality, integrity or availability**, for example unintended
   access, elevated permissions or remote code execution. A suggestion to harden something, or an intentional
   design that is not optimal for security, is not a vulnerability by this definition.
3. **For every outcome except a vulnerability, tell the reporter why**, in case you misread the report. For a
   bug, ask them to refile it as one; for a feature request, invite one; then close the security item.
4. **For a vulnerability, confirm it to the reporter and continue the process.**

## 1.3 Agree the embargo
1. **The embargo is the period the report stays private** while you respond, fix and disclose. Ask the
   reporter what they will accept before you propose yours.
2. **Published timeframes differ between groups and are a starting point for negotiation**, not a hard
   deadline; the guide quotes a coordination body for that stance. Do not copy a number from this block; look
   up the policy of the body whose norm you intend to follow.
3. **Agree it with the reporter and keep talking.** Reporters are usually willing to give more time when they
   see continued effort, steady communication and a reason. If you think the time is too short, make the case
   now and give the reasons.
4. **No deadline reads as opposition.** Many reporters conclude that a project with no date does not want to
   fix the flaw.
5. **Each day of embargo is a day attackers may find it, and a day users stay unaware.** The guide presents
   this as a trade-off, not as a reason to run the clock down.

## 1.4 Involvement and credit
1. **Ask whether the reporter wants to help with the patch**, and whether they want to help write the CVE
   entry and how they want to be credited.
2. **Omitting credit is inappropriate unless the reporter does not want it.** Record what they chose.
3. **A reporter may ask to publish their own technical advisory on your release day**; the guide calls
   co-issuing common. Decide who sends what before the day.
4. **No payment is owed for unsolicited details**, and a reporter who asks for money in exchange for them is
   outside this process; the guide says so. Treat a bounty programme as a separate arrangement.
