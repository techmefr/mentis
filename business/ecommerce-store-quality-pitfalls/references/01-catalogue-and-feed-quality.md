# ecommerce-store-quality-pitfalls §1 — Catalogue and feed quality

> Part 1 of `business/ecommerce-store-quality-pitfalls`. Read it when products are created, imported or sent to a
> channel.

## 1.1 Identity and variants
1. **Give each sellable unit one stable identifier of its own.** Symptom: an order for the wrong size, or a stock
   count shared by every colour. Check: is each size and colour a separate unit with its own identifier, price
   and stock? Fix: parent product for the description, a variant for each purchasable combination; feeds carry a shared group
   identifier for the variants of one product, required for variants in several named countries and in free listings
   on the channel read, with the group kept unchanged across updates.
2. **Never reuse or recycle an identifier.** A reused code rewrites order history and corrupts reports. Retired
   products keep theirs. The feed specification read asks for a unique identifier per product, the SKU where possible,
   kept unchanged across updates and across countries and languages (Google Merchant Center product data spec).
3. **Use the manufacturer's global trade number where it exists**, and keep it as text (leading zeros:
   `business/spreadsheet-data-cleaning-pitfalls` §1). A wrong or invented number is rejected by channels and
   mismatches duplicate listings. The same spec says digits only, a valid checksum, no restricted or coupon prefixes, and
   to supply a number only when sure it is right, since a wrong one gets the product disapproved; it also warns against
   marking a product as having no identifier when it has one.
4. **Keep the variant axes few and named the way buyers name them.** Symptom: "L / Large / 12" as three sizes.
   Fix: one controlled value list per axis.

## 1.2 Words and attributes
1. **Write the title for the buyer, not the supplier.** Symptom: a supplier code string as the title, found by no
   search. Fix: what it is, its key attribute and brand, in the words buyers type; check with the site's own search
   log. The feed spec adds that the title matches the landing page, carries no promotional text or all capitals, and
   includes the distinguishing colour or size for variants.
2. **Fill the attributes a buyer filters on**: size, colour, material, compatibility. Empty attributes drop the
   product from filters, so it is never found. Check: count products with each filter attribute empty.
3. **Describe what is true and testable.** Claims about a product need support (`business/marketing-claim-substantiation-pitfalls`).
4. **Keep units explicit and consistent**: millimetres or inches, and per-unit price where the market expects it.
5. **Do not copy the supplier text verbatim.** Many shops with identical text compete on price alone, and a
   supplier's copy may carry a licence. Write the description from the facts.

## 1.3 Stock, price and the feed
1. **Stock has a state the page can show**: available, low, back-order with a date, out. The feed spec lists in stock,
   out of stock, preorder and backorder, requires a date for the last two, and requires the state to match the landing
   page, checkout and structured data. Symptom: the buyer pays
   and the shop emails a cancellation. Fix: reserve on the cart or the order by a stated rule, and show the state.
2. **One source of truth for price, stock and availability, and the feed is generated from it.** The feed spec requires
   price and availability to match the landing page and checkout, with the price as a number plus a currency code, and a
   sale price submitted next to the regular one with its dates. Symptom: an
   advertisement shows a price that the page contradicts. A feed built by hand is wrong by afternoon.
3. **Refresh the feed as often as stock and price change, and send a stock-out immediately.** Check: change a price
   and time how long each channel takes to agree.
4. **Treat feed errors and warnings as a defect list.** Read the channel's diagnostics each week; a disapproved
   product earns nothing. Rules differ by channel and change, so read the channel's current documentation. On the channel read, a listing that
   violates policy is disapproved and does not serve, repeat or serious cases risk impression caps or suspension, and a
   fix or an appeal is possible (Google Merchant Center policy page).
5. **Reconcile the feed with the page on a sample.** Pick products at random, compare title, price, availability,
   image and link, and keep the count of mismatches over time.

## 1.4 Images and pages
1. **Every product has a clear first image on a plain background and images of detail and scale.** Symptom: a
   thumbnail that cannot be read. Check on a phone.
2. **Give images alternatives** (`business/image-alt-text-writing-pitfalls`) and sensible file sizes; a slow
   category page loses buyers before they see a product (`skills/cwv-diagnosis-pitfalls`).
3. **One product, one address; handle variants without duplicate pages**, and send a retired product to its
   successor or a clear explanation, not a 404 (`skills/seo`).
