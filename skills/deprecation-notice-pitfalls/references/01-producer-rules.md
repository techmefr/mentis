# deprecation-notice-pitfalls §1 — Producer rules

The failure this section prevents is a sunset by surprise: a date the producer chose alone, announced in a
place nobody was watching.

## 1.1 Record it in the specification
1. **The deprecation is part of the API specification.** Mark the affected element (an operation, a
   parameter, a data object, or a single attribute) as deprecated and explain it in its description.
2. **If a shutdown is planned, state the sunset date**, what to use instead and how to migrate.
3. **Microsoft Graph's annotation adds fields worth copying in spirit**: the date it was marked, a category for
   the changelog, a human description, and the earliest date the element can be removed.

## 1.2 Shutting down needs consent
1. **While clients still use it, a shutdown is a breaking change.** The Zalando rule is that all clients must
   have consented to a sunset date before the producer shuts anything down.
2. **Help them migrate**: a migration guide, the timeline for the replacement and for the sunset.
3. **Once every client has migrated, the producer may shut it down.**
4. **External partners agree the minimum time between deprecation and first possible sunset before they start
   using the API.** The owner defines a reasonable span first, and each partner states consent to it.
5. **A header alone is not consent.** The same guideline says adding the headers below is not sufficient to
   gain a client's agreement to a shutdown.

## 1.3 Two philosophies, and your choice
1. **Zalando's model is consent per client**: no fixed number, the date is agreed.
2. **Microsoft Graph's model is a fixed schedule**: its documentation has the gateway add a sunset date a set
   interval after the deprecation date. Another Microsoft source states a breaking-change policy with
   approvals; none of its windows was read here.
3. **Choose one for your product and write it down.** If you have external partners and no contracts yet,
   consent per client is the safer default. Do not copy either source's number.

## 1.4 Monitor usage
1. **Measure who still calls anything scheduled for sunset**, so migration progress is visible and a shutdown
   does not break a caller you did not know about.
2. **Name who reads that monitor.** Usage nobody reviews is not monitoring.

## 1.5 The two headers
1. **Send a Deprecation header, and a Sunset header if a sunset is planned, on every response affected by a
   deprecated element.** Zalando classifies this as a recommendation, not a requirement.
2. **The Deprecation value is either "true" when a feature is retired or a timestamp** at which a replacement is
   or was available and consumers must not start using the old one. The Sunset value is the date by which
   consumers must have stopped. Leave a real interval between the two.
3. **The two headers use different time formats**, for historical reasons. Copy the format from the
   specification you cite, not from memory.
4. **With several deprecated elements in one response, send the earliest dates**, which show the shortest
   interval consumers have to act in.
5. **Link relation variants add little**: Zalando discourages them because the specification already carries
   the information. Microsoft Graph's gateway sends them anyway; pick one approach.
6. **A header does not reach people who are not looking at responses.** Pair it with the specification, the
   documentation and a direct notice (§2.2).
