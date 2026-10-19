# dsar-handling-pitfalls §2 — Package, delivery and the DPO line

> Part 2 of `skills/dsar-handling-pitfalls`. Read it when the answer to a request is assembled or sent, or the
> process is tested. Lifecycle shape (manifest, token-gated delivery, appeals, audit): the inthhq `dsar`
> request-lifecycle guide, an alpha project. The statements about Article 12 are from Regulation (EU)
> 2016/679 as published in the Official Journal, read 2026-10-16 (source in part 1). Everything else is own
> guidance and says so.

1. **Assemble the package from a manifest of systems searched.** The lifecycle guide has a fulfilment stage
   built around a manifest that can be read and validated before the package goes out. Own guidance: the
   manifest lists every system that may hold data about the person: the main database, but also logs, search
   indexes, caches, backups, analytics and product telemetry, mail and ticket systems, files, and the systems
   of processors. Get the list from the processing inventory in `business/data-protection`, and add a system
   when a case finds data in a place not on the list.
2. **Write a result per system, including nothing.** Own guidance: each manifest line ends with "found,
   included", "found, held back for the DPO's decision" or "searched, nothing found", with the query used and
   the date. A blank line is not a result. A deletion that skipped the search index and an export that skipped
   the analytics store are the same failure.
3. **Delivery of personal data is a disclosure.** Own guidance: the person is who they say they are before the
   package is sent. Use an authenticated or token-gated download with an expiry, not an attachment to an
   address taken from the request itself, and log each download. The lifecycle guide describes prepared
   delivery, address verification, a step-up challenge for access and a delivery log; the pattern is worth
   copying, the project is not a dependency. Article 12(3) asks for electronic delivery where the request was
   electronic and where possible; an authenticated download is one way to deliver electronically (own guidance).
4. **Verify the recipient, not only the request.** Own guidance: the wrong-address export is the common
   incident. Check the destination against what was verified, not against what the message says, and have a
   second person confirm the destination for a first delivery to a new address.
5. **Complaints and appeals are cases too.** The lifecycle guide includes an appeals stage after delivery.
   Article 12(4) says that a person who is refused is told of the possibility of a complaint to a supervisory
   authority and of a judicial remedy. Own guidance: a complaint or appeal opens a linked case with its own
   events and keeps the original package and notices unchanged.
6. **What is not an engineer's call.** Whether the person is entitled to a given right in a given case (access,
   erasure, portability, objection), whether an exemption applies, what may be held back because it concerns
   other people, whether a request is unfounded or excessive and what that allows, how identity doubts may be
   handled, and the effect of any pause on the clock. The text read for this block is Article 12(3) and (4)
   only; the articles that define each right were not read, so none of those questions is answered here. Put
   each in the case as a named question to the DPO, with the quoted request and the facts found.
7. **Deletion has its own check.** Own guidance: after a deletion decided by the DPO, run the manifest again
   and record that each system returns nothing, and note what remains by decision (backups waiting for
   rotation, records held for another duty) with the reason and the date it is expected to go.
8. **Test it end to end on a dummy person.** Own guidance: create a person with data in every system on the
   manifest, send a request through each channel, run intake to closure including an extension, a refusal and
   an appeal, and check every notice, the delivery link expiry and the audit trail. Do it before launch and
   after each change of system list, and record the date.
