# troubleshooting-kb-article-pitfalls §4 — Capture, catalog and maintenance

Pages decay unless the practice around them is set up: how the raw material is captured, where the catalog
comes from, when a page is retired and what is measured.

## 4.1 Capture during resolution
1. **The person resolving the case writes the raw material while the exact error text and environment are in
   front of them.** Entries reconstructed from memory are the ones that turn out wrong.
2. **Add four fields to the ticket**: error text, environment, cause, resolution. The source takes these from a
   published support-knowledge framework that was not read here.
3. **Genericise before publishing**: strip customer identifiers, keep the environment facts that decide
   whether the entry applies.
4. **A weekly pass that promotes repeat resolutions into entries** keeps the queue from rebuilding. Whether
   a repeat is worth a page goes through §1.4.

## 4.2 One source for the catalog
1. **Where possible, generate the documented error catalog and the code constants from one machine-readable
   source** such as an enum or a table, so the code and the documentation cannot disagree.
2. **That is an engineering task and not a documentation one.** Say what it buys: the constant and the entry
   can never differ again.
3. **Hand-synchronised catalogs drift.** The source states this as a default, and cites published examples of
   generated catalogs that were not checked here.

## 4.3 Stamps and retirement
1. **Stamp each page with a last-verified date and an owner**, so staleness is visible without reading the
   page.
2. **A release that changes an error's text or cause updates the entry in the same release.**
3. **A shipped fix retires the known-issues entry**, with a version note.
4. **Re-run the clustering after publishing.** The same clusters reappearing unchanged mean the entries are
   not found, which is a findability problem and not a volume problem.
5. **Check one retired and one live entry**: the retired one links to the shipped fix, the live one has a
   verified date inside the last release cycle and a named owner.

## 4.4 Measure
1. **Measure the share of problems resolved without a ticket**, not the raw deflection rate. A deflection
   number looks good while readers fail repeatedly and come back.
2. **Per-error volume on fixed windows is measurable; a site-wide deflection rate is not.** Also useful:
   zero-result searches for covered strings and the share of entries touched since the last release.
3. **Do not quote cost-per-ticket or deflection figures without a method behind them.** Use your own ticket
   costs or say the number is unknown.

## 4.5 The escape hatch
1. **"Contact support" must point at a channel someone watches**, and say what to attach.
2. **A dead channel is fixed everywhere it appears**, not in one page.
3. **Feedback signals**: a "was this helpful" widget is cheap but low resolution, because a bare thumbs-down
   cannot tell "the page is wrong" from "this problem could not be solved by reading"; add an optional free-text
   field. The source calls zero-result and unanswered searches the strongest low-effort signal of a missing
   page.
