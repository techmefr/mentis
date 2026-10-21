# design-contract-and-finish-gate-pitfalls §2 — The HOLD or PASS gate

Source: the design-ui-finish-gate-reviewer agent of msitarzewski/agency-agents (MIT), read 2026-10-21.

## 2.1 Evidence before opinion
1. **Symptom:** "this feels generic" with nothing behind it. **Fix:** name the interchangeable pattern and the
   product-specific replacement, or say nothing. "This screen could belong to any product" is allowed only with
   both.
2. Review the implemented screen at the widest and the narrowest supported size, not the brief or the component
   list.

## 2.2 Audit order
1. **Product legibility:** can a new user identify the product's object and primary workflow in the first view?
2. **Hierarchy:** does visual weight follow the user's decisions or the component library's defaults?
3. **Pattern fit:** does each layout choice earn its place for this workflow?
4. **States:** loading, empty, error, selection, focus and disabled are intentional and useful, not left for
   later.
5. **Responsive behaviour:** the narrow layout keeps the job, instead of stacking desktop cards and burying the
   column the user scans for.
6. **Implementation fidelity:** tokens, components, content and assets match the surrounding product.

## 2.3 Reject the interchangeable, not the simple
1. **Symptom:** a plain screen is marked down for being plain. **Check:** does it hide the user's real work, or
   are its choices interchangeable? **Fix:** plain and specific passes; decorated and generic holds.
2. Do not add gradients, glass, large rounded cards or animation to make an interface feel designed.

## 2.4 The decision
1. **PASS** only when the screen communicates its product and primary workflow without generic filler or
   unexplained visual decisions, and the contract's first-read object and primary action are visible.
2. **HOLD** when a critical finding remains. A hold is a decision, not a list of nice-to-haves.
3. **Each HOLD finding carries the observable change and the check:** what changes on screen, and in which state
   or at which size it is verified.
4. **Separate required changes from optional refinements** in the report, and keep a short list of choices that
   already serve the product so a rewrite does not undo them.
5. **PASS criteria are written in the report:** first-read object and primary action visible, no forbidden
   default without a product reason, the named states and sizes verified.

## 2.5 After a hold
1. A fix is verified against the same state or size that failed, with fresh evidence from this turn (`skills/gate`,
   claims and proof), then the gate is run again. A fixed screen is not a passed screen until it is re-read.
2. A fresh-context reviewer, with no write access, is the better seat for the second read (`agents/galadriel`).

## Checks
1. Every HOLD item has an observable change and a verification condition.
2. The report names the first-read object and the primary action.
3. No finding relies on "modern" or on a trend alone.
4. Both sizes and the empty and error states received an explicit PASS or HOLD.
