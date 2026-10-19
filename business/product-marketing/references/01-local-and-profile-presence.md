# § 1 - Business details, local presence and profiles

> Section 1 of `business/product-marketing`. Read it when the product or the company has a physical
> location, a service area, public business listings or social profiles, or when a page prints contact
> and address details. The technical markup side is `skills/seo`; consumer-protection and data questions
> go to the legal blocks named below.

A business's details (name, address, phone number, hours, categories, links to its profiles) are claims
like any other in `SKILL.md` §2: they are checkable, they go stale, and the reader acts on them. The
mechanism is to keep them in one place and let every surface read from it.

1. **One source of truth for business details.** Legal name, trading name, address, phone, e-mail, hours
   (including exceptions such as holidays), categories and profile links live in one record. The site,
   the structured data, the footer, the listings and the e-mail signatures take their values from it. The
   usual defect is the same shop with three phone numbers on five surfaces.
2. **Write the details the same way everywhere.** Name, street abbreviations, suite numbers and phone format
   identical across the site and the listings you control. Consistency is what lets a person and a
   crawler decide that two entries are the same business.
3. **Markup reads from that record.** Where the business is local, publish the organisation or local-business
   structured data (schema.org types, as documented by the search provider) from the same record, not typed
   by hand; validate it with the provider's tool. Markup must match what is visible on the page, never
   claim more (`skills/seo`).
4. **Only publish an address people can visit.** A business that serves customers at their location, with no
   public premises, is a service-area business: describe the area served, not a private or invented
   address, and follow the listing provider's own rules on hiding the address. A virtual or shared
   address presented as a shop is a false claim (§2 here).
5. **Claim and verify your listings, and keep them current.** Verification tells the platform you may
   represent the business. Complete and accurate details are what the platforms say they use to show a
   business for local queries. Review the listings when anything changes: move, new hours, new category,
   a closure.
6. **Reviews are customers' words.** Reply to them, including negative ones, in the tone of
   `business/community-management`. Never write, buy or trade reviews, never ask only satisfied customers
   to review (review gating), never offer a reward for a positive review: it is against the platforms' rules
   and, in many places, against consumer-protection law (`business/legal-documents`, ask a lawyer).
   Showing a rating you computed yourself needs a method and a source (`SKILL.md` §2.2).
7. **Photos and descriptions are claims.** An image of the shop, the team or a product must show the real
   thing; a description does not promise a service the business does not offer.
8. **Name, address and phone are personal data when they are a person's.** A sole trader's home address on a
   public page, a team photo, a named contact: decide deliberately with `business/data-protection`.
9. **Profiles point at the site, and the site points back.** Each social or directory profile uses the
   same name and the same description, links to the canonical site, and the site lists the profiles that
   are really maintained (structured data has a property for this). An unmaintained profile is worse than
   none: it shows old hours and unanswered messages.
10. **Share buttons are optional and cost something.** Third-party share widgets often load trackers and
    scripts before consent; a plain link that opens the share dialog of the platform, or none, is the
    default (`business/data-protection`). The reader who wants to share has a browser.
11. **Review the record on a schedule.** A quarterly look at the record against the listings and the site,
    and again at each event that changes a detail, is cheaper than a customer arriving at a closed door.
