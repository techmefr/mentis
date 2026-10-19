# prototype §3 — After the answer

> Section 3 of `skills/prototype`. Read it once the question of §1.1 has an answer.

## 3.1 Three outcomes, nothing merged as it is
1. **Record the answer first**: the verdict and the question it settled, in the ticket or the spec that asked
   (a decision with a reason goes in an ADR, `skills/spec` §5.16 on why it does not carry over by default).
2. **Lift what was validated into the real code, rewritten under the project's standards.** The prototype was
   written under prototype constraints (no tests, minimal error handling), so promoting it directly carries those
   constraints into production.
3. **Keep the prototype itself as a record, off the main line**: commit it to a throwaway branch and leave a
   pointer to that branch on the implementation ticket. The main branch keeps only the validated decision.
4. **Delete everything else from the main line.** Losing variants, the switcher and any throwaway route left in
   place rot quickly and mislead the next reader.

## 3.2 What lifts, per shape
| Shape | Lifts into the real code | Goes to the throwaway branch | Never reaches the main line |
|---|---|---|---|
| Logic demo | the pure module (reducer, machine, functions), after review and tests | the page around it, still runnable alone | the page itself |
| UI variants, hosted | the winning variant, folded into the existing page | the losing variants and the switcher | variants, switcher |
| UI variants, new page | the winning variant, promoted to a real route | the throwaway route and the others | the throwaway route, switcher |

## 3.3 Anti-patterns
1. **A prototype that needs tests has stopped being one.** Either it is now the feature, or the tests are waste.
2. **Wiring a logic demo to the real database** when the question was not about persistence.
3. **A pure module that touches the page**, which makes it impossible to lift.
4. **A framework or a server for the logic demo**, which defeats "open it by double-click".
5. **Leaving a prototype on the main line "for now"**, which is how its decisions are taken as production ones.
