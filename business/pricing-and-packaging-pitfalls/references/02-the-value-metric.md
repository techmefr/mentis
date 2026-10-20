# pricing-and-packaging-pitfalls §2 — The value metric

The metric decides who feels the price grow and when. Pick it by testing it, not by copying the shape of a
well-known product.

## 2.1 The test
Ask four things about a candidate unit, and write the answers:
1. **Value:** when a customer uses more of this unit, do they get more value?
2. **Understandable:** can a buyer explain it to their own manager in a sentence?
3. **Predictable:** can the buyer estimate next month's bill from what they know today?
4. **Hard to game:** what is the cheapest way to use the product while paying for less of the unit, and do you
   mind it?

A "no" on the first is the serious one: the price then no longer follows value.

## 2.2 Seats
1. **Per seat fits a product whose value rises with the number of people using it** (shared work, review,
   coordination).
2. **Where value does not rise with headcount, seats punish adoption.** Teams share one login to avoid paying,
   the vendor sees fewer users than there are, and the signal about who really uses the product is lost.
3. **Check what happens at the edges:** a read-only viewer, an occasional user, a contractor. Decide whether
   each pays, in writing.

## 2.3 Usage
1. **A usage metric needs a meter the customer can see**, in the product, in near real time, in the same unit
   as the bill.
2. **Add alerts at thresholds and, where the buyer wants it, a cap.** The main buyer fear is a surprise
   invoice; the meter and the alert are what remove it.
3. **Keep overage visible.** Usage charges hidden inside a flat plan ("includes a quantity, then charged per
   unit") are two pricing models presented as one; say plainly that the plan has an included amount and a
   metered part, or pick one model.
4. **Decide the unit by what the customer controls.** A unit the customer cannot influence (an internal
   retry, a background job) makes the bill unpredictable even with a meter.

## 2.4 Feature, credit and outcome models
1. **Feature-based pricing** segments well but follows the gating rule in §3.2: gate what separates casual from
   serious use, never the core.
2. **Credits** suit products where each action has a different cost and use is bursty; the credit is a unit
   you must define, explain and keep stable (what one credit buys changing silently is a price change).
3. **Outcome-based pricing** needs an outcome that is measurable and clearly attributable to your product, and
   a definition both sides accept in advance (what counts, who counts it, what is disputed). The sources
   treat credit and outcome models mostly from marketing material: check them against independent
   practitioner or academic references before relying on them (`references/origin.md`).
5. **Mixed models** (a base fee plus a metered part) are common; add the second component only when a single
   model clearly misprices a real segment, and name that segment.

**Never** choose a metric because a successful product uses it. Run the test in §2.1 for your own product.
