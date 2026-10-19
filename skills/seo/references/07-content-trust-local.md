# § 7 — Content trust signals and local presence

> Section 7 of `skills/seo`. Read it when a public site publishes articles or advice, when a page is about
> health, money or the law, or when the business has a physical location or serves a geographic area. The
> first six sections are what a developer controls on a page; this one is what a developer or a product
> owner has to provide so that the page can be trusted by a visitor and by an engine. It states
> requirements and checks for presence; the prose itself is `business/content-creation` and
> `business/ai-prose-tells`. Engine statements here are paraphrases of its published guidance on helpful,
> people-first content and on its spam policies, read at the time of writing and expected to move.

## Trust signals a site must carry

1. **Say who wrote it and who stands behind the site.** An article has a byline that links to a page about
   the author; the site has an about page and a way to make contact, both reachable from every page
   (footer or main navigation). These are product requirements, and a page missing from the router is a
   build defect, not an editorial one.
2. **Say when, and what changed.** A publication date, a modification date when the content was
   substantively revised (§6.6), and for evolving topics a short change note. A date nobody maintains is
   worse than none.
3. **Show sources.** Claims that a reader could check link to the primary source, in the text where the
   claim sits, and the links are checked for rot (§5.2). Outbound links to credible sources are normal and
   are not a ranking leak.
4. **Policies are reachable.** Privacy, terms and, for a publisher, an editorial or corrections policy are
   linked from the footer; their content is `business/legal-documents`. Transport security and an
   accurate contact address are part of the same signal.
5. **Subjects that can harm get a named reviewer.** Pages on health, money, safety or the law are held to
   a higher bar by the engines and by readers: a qualified named author or reviewer, dated sources, and a
   disclaimer where the advice is general. This is a process decision recorded in the project, not
   something markup can add after the fact.

## What does not need chasing

6. **No density targets.** A keyword percentage, a minimum word count, a reading-grade score, a slug
   stuffed with search terms or a list of stop words to avoid are not ranking requirements; the engine's
   own guidance says content is written for people, in the length the topic needs. Repeating a phrase to
   be found is spam under the engine's policies, and it reads as such to people.
7. **Origin of the text is not the test; value is.** Text produced with tools is judged like any other. What
   the policies target is content mass-produced to manipulate rankings, with no added value, whoever or
   whatever wrote it. A page generated per keyword variant with the same body is the pattern to avoid.
8. **Conventions with no documented effect are not adopted.** A geographic meta tag, a keywords meta tag
   and a machine-oriented summary file that no engine documents as read add maintenance and no
   documented benefit; if one becomes documented, it is added here with its source.
9. **Share buttons and social profile counts are not signals.** They are a product choice; if present they
   follow `skills/webperf` §4.5 as third-party code.

## Local presence

10. **One source for the business facts.** Name, address, telephone number and opening hours live in one
    place (a configuration file or a data record) and render everywhere from it: footer, contact page,
    structured data and any map. Two spellings of the same address are two entities to an engine and
    two answers to a customer.
11. **Local structured data matches the visible block.** A `LocalBusiness` (or the more specific
    subtype) with name, address, telephone, opening hours and, where relevant, coordinates, on the
    page that shows them (§6.1). Opening hours that change (holidays) change in the data in the same
    commit.
12. **A page per location, with its own content.** Each location page has its own address, hours, local
    information and a way to reach that site; a set of pages that differ only by the town name is the
    doorway pattern the policies list as spam. A service area is described on the business page rather than
    multiplied into pages with nothing to say.
13. **Third-party listings are product-owned.** The business profile with a search or map provider, and
    directory entries, are maintained by whoever owns marketing; the site's job is to publish the same
    facts, from the same source, and to link to the listing. Review requests and reply policy belong to
    `business/community-management`.
14. **A map is an embed with a cost.** It is a third-party frame (name it, `skills/accessibility` §6.10),
    loads on interaction or below the first screen (`skills/webperf` §4.5, §4.6), and the address is
    also given as text.

## Mechanical checks

```
grep -rniE 'href="[^"]*(about|contact|privacy|terms)' src
grep -rnE '\+?[0-9][0-9 .()-]{8,}[0-9]' src public
grep -rnE '"@type"\s*:\s*"(LocalBusiness|Organization|Person)"' src
```

- From the crawl (§5), confirm the about, contact and policy pages are linked from every template.
- The telephone and address variants found by the second command are compared with the single source; more
  than one spelling is a finding.
- The address, telephone and hours in the structured data are compared with those in the rendered text.
- A count of location pages that share the same body text (a hash of the main content) above a project
  threshold is a finding for a person to judge.
