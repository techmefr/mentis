# deprecation-notice-pitfalls §2 — Notice and clients

The failure this section prevents is a notice that exists but is read by the wrong person, or one that omits
the change that silently breaks callers.

## 2.1 A warning meant for a human debugging
1. **Azure's guideline defines a response header for a human reading logs or responses**: a semicolon-separated
   list in which each item says what is deprecated, when it stops working and a link to more information.
2. **Send it only when the operation will stop working and the client must act.** The guideline says it does
   not want to scare customers.
3. **The text is informational and not part of the contract.** Clients are not expected to parse it, and it can
   be improved at any time without a breaking change. Machine consumers should use the standard headers
   (§1.5).
4. **Use a fully qualified link** to a page where the replacement is explained.

## 2.2 Reach the right reader
1. **The contact on a cloud subscription is often not the developer** writing against your API, because of how
   organisations are structured. The Azure design guidance says an email to that address is the usual route and
   that the header exists to reach the developer.
2. **Carry the notice in the response and in the documentation.** The guidance asks that the documentation
   mention the header and encourage logging and alerting on it.
3. **Ask clients to alert on the deprecation headers**, so the notice shows up as an event in their own
   monitoring (Zalando's client rule).

## 2.3 The removed-APIs page
1. **Per release, list what is no longer served**, as the Kubernetes migration guide does, one entry per
   resource.
2. **Each entry names the replacement and the version in which the replacement exists**, so a reader knows
   whether it is available to them.
3. **State whether existing stored objects remain reachable** through the new version.
4. **List the notable behaviour differences, especially changed defaults.** The Kubernetes guide records, for
   one removed version, a default that changed for an unspecified field and an explicit zero that is no longer
   overwritten. These are the changes that break callers silently.
5. **Say "no notable changes" when that is true**, so absence of information is not read as absence of
   differences.
6. **A "removed" line in a changelog is not enough.**

## 2.4 If you are the client
1. **Do not start using anything already deprecated.** The Zalando client rule is a requirement.
2. **Read the response headers of your dependencies**, alert on them and treat a sunset date as a deadline you
   own, not as a notice for someone else.
3. **Check the removed-APIs page of each release before upgrading**, looking at changed defaults first.
