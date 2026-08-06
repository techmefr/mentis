---
name: data-protection
description: Use when a feature collects, stores, exports or shares personal data, or when a new third-party service will receive it, the questions to settle before writing the code rather than during an audit. Structured checklist, not legal advice: it exists to make the question reach a lawyer or DPO earlier.
---

# data-protection

Business layer (`business/README.md`), touching step 3 and step 6 of the dev pipeline. GDPR is where
an engineering decision quietly becomes a legal exposure, usually at the moment someone adds a field
"we might need later" or wires in a convenient third-party API.

**This is not legal advice.** It's the set of questions that, unasked, turn into a problem nobody can
fix cheaply afterwards. Where a question has a legal answer, the answer comes from a lawyer or the DPO,
not from here.

## When
As soon as a feature: adds a field holding personal data, exports or displays it in a new place, sends
it to a third party, or changes how long it's kept. Also when a new dependency or SaaS will process
it.

## Steps

### 1. Name the data and why you have it
1. **List the personal data this feature touches**, field by field. "Personal data" is wider than most
   engineers assume: a name, an email, an IP address, a device id, a photo, free-text notes that
   mention someone, and anything that identifies a person once combined with something else.
2. **Flag the special categories separately** — health, biometrics, union membership, religion, sexual
   orientation, criminal records. These carry much stricter obligations, and a "just a comment field"
   that ends up holding health information is the standard way of acquiring them by accident.
3. **State why each field exists**, in one sentence tied to the feature. A field nobody can justify is
   a field to remove: that's not a legal nicety, it's the cheapest way to shrink the problem.
4. **Collect the minimum.** "We might need it later" is not a purpose. Later, with a purpose, is when
   to add it.

### 2. Settle the questions an engineer can't answer alone
Take these to the DPO/legal rather than guessing:
- **On what basis are we allowed to hold this?** (consent, contract, legal obligation, legitimate
  interest — they are not interchangeable and they have different consequences in the code)
- **If it's consent**: it has to be freely given and withdrawable. Withdrawable means there's a code
  path for withdrawal, which is a feature someone has to build.
- **How long do we keep it, and what happens at the end?** Deletion or anonymisation, and a mechanism
  that actually runs. A retention rule with no job behind it is a sentence in a document.
- **Does this need a formal impact assessment?** Large-scale, sensitive or systematic-monitoring
  processing may. That call isn't ours.

### 3. What the code has to provide
1. **Access and portability**: a person can ask what you hold about them. If satisfying that request
   means a developer writing a bespoke query each time, it will be slow and eventually wrong.
2. **Deletion**: an actual mechanism, and know what it does about backups, logs, analytics and search
   indexes. Deleting the row while the record survives in a search index and three log lines is the
   normal outcome of not asking.
3. **Correction**: editable, or a route to get it corrected.
4. **Never personal data in logs or URLs.** Same reasoning as credentials
   (`skills/auth-session-conventions` §2.1 and §2.4): logs have wider read access and longer retention
   than the system that produced them, and URLs travel into history, `Referer` and every proxy.
5. **Non-production environments.** A production dump in a dev database is a real disclosure with real
   consequences. Anonymise or generate; if you must copy, that's a decision someone senior takes
   knowingly.
6. **Access is scoped**: the same discipline as any authorisation
   (`skills/security-hardening` §3), applied to the data most likely to be requested.

### 4. Third parties
1. **A new service that receives personal data is a decision, not a dependency choice.** It needs a
   data processing agreement, and where the data is hosted matters. Both are legal questions.
2. **Analytics, error reporting and session replay are the common unnoticed cases**: an exception
   reporter that serialises request bodies is exporting personal data to a third party, whatever the
   feature intended.
3. **Write down what leaves the system, to whom, and why** — you will be asked, and reconstructing it
   later from the code is much harder than noting it now.

## Output / checkpoint
No pipeline checkpoint (business layer, see `business/README.md`). What it owes: the field list with a
purpose each, the questions routed to the DPO/legal with their answers when they come back, the
retention mechanism named, and the list of third parties receiving data. If the answers aren't in yet,
that's a blocker to state, not a reason to guess.

## Guardrails
- **Never decide a lawful basis or a retention period yourself.** Wrong here is expensive and
  invisible for a long time.
- **Never widen collection because it's convenient.** Every extra field is an obligation you now carry.
- Never copy production personal data to a local or shared dev environment on your own initiative.
- **When in doubt about whether something is personal data, treat it as if it is** and ask. The cost of
  asking is a message; the cost of being wrong is a notification obligation.

## Origin
Assembled from public sources: the GDPR text itself (lawful bases, data-subject rights, special
categories, impact assessments) and published regulator guidance. Written **without internal legal
expertise**, deliberately shaped as "which questions must reach a lawyer" rather than as answers. The
engineering consequences — logs and URLs, search indexes and backups surviving a deletion, exception
reporters exporting data unnoticed, non-production copies — are ours, and are the part this block adds
that a legal summary wouldn't.
