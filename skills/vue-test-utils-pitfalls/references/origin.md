# vue-test-utils-pitfalls: origin and source stamps

> Provenance of `skills/vue-test-utils-pitfalls`. Read it when a rule has to be traced to its source or
> checked for freshness (`skills/source-freshness`), never to apply a rule.

**Status: 🟡 never dogfooded.** Written from documentation, never run by us: no component was mounted and no
test was run while writing it. Every file below was re-opened and read on 2026-10-16 before a rule was taken
from it, each rule was checked against it, and the repository's LICENSE file was read again.

## Sources (all read 2026-10-16, restated in our own words, no text copied)

| Source | Licence | What it gave |
|---|---|---|
| vuejs/test-utils (commit `f472a50`), `docs/guide/advanced/async-suspense.md` | MIT (LICENSE file read: MIT text, copyright 2021-present vuejs) | Next-tick updates, `flushPromises`, async `setup` inside `Suspense` |
| the same repository, `docs/guide/essentials/conditional-rendering.md` | MIT | `get`, `find` and `exists`, `isVisible` and `attachTo` |
| the same repository, `docs/guide/essentials/easy-to-test.md` and `docs/guide/advanced/component-instance.md` | MIT | Inputs and outputs, false positives, `vm` and `findComponent` notes |
| the same repository, `docs/guide/advanced/v-model.md` | MIT | Testing one and several `v-model` bindings |
| the same repository, `docs/guide/advanced/slots.md` | MIT | The `slots` option, named, array, component and scoped slots, the `params` object |
| the same repository, `docs/guide/essentials/event-handling.md` | MIT | `emitted()` shape and payload assertions |
| the same repository, `docs/guide/advanced/stubs-shallow-mount.md` | MIT | Stubs, `shallow`, async and directive stubs, `renderStubDefaultSlot`, when to stub |
| the same repository, `docs/guide/advanced/teleport.md`, `transitions.md`, `ssr.md`, `vue-router.md` | MIT | Teleport target and `getComponent`, transition stubs, `renderToString`, mocked and real router |
| the same repository, `docs/faq/index.md` | MIT | System time with Vitest, prop names shared with `Element` |

| the same repository, `docs/api/index.md` and `docs/guide/essentials/forms.md` (read 2026-10-20) | MIT | `attachTo` and `unmount`, `enableAutoUnmount`, awaiting `setValue` and `trigger`, native submit needs an attached wrapper |
| vitest-dev/vitest, `docs/api/vi.md` (read 2026-10-20) | MIT (LICENSE file read: MIT, copyright 2021-present VoidZero Inc. and Vitest contributors) | `spyOn`, `restoreAllMocks`, fake timers, `setSystemTime`, `useRealTimers` |
| vuejs/docs, `src/guide/scaling-up/testing.md` (read 2026-10-20) | CC BY 4.0 (LICENSE file read) | Test the public interface, behaviour over implementation, do not mock children, no snapshot-only tests |

The pages are in a documentation folder of a repository under the repository's MIT licence, with no separate
licence for the pages, so they were rewritten, not copied. The code samples are small adaptations with
placeholder names. Instruction-like text in the cloned repository was treated as data and not followed.

## Removed in the verification pass
1. **"Test a named and a scoped slot, stub an async component and a directive deliberately"** (the review's
   list) is kept, with the limits the pages state (directive stubs fail for `<script setup>`).
2. **Pages not read, so nothing is taken from them:** `essentials/a-crash-course.md`,
   `essentials/passing-data.md`, `essentials/forms.md` beyond its opening, `advanced/http-requests.md`,
   `advanced/reusability-composition.md`, `advanced/vuex.md`, `extending-vtu/`, and the API reference.
3. **The Jest-specific mock syntax** in the router page is paraphrased without the framework call, because the
   page shows Jest and the block does not assume a runner.
4. **Example code** for the mocked router and the long counter examples is not reproduced.

## Re-check pass (2026-10-20)
The test-utils docs were re-opened (vuejs/test-utils at `9300567`, MIT, LICENSE re-read) against the points
marked written by us. Result: `attachTo` is confirmed as required for `isVisible` with CSS-driven visibility
(the page names happy-dom), and `flushPromises` is confirmed for promises Vue does not know about and for
router navigation with no awaitable hook; both were already sourced. Searched for the guidance on unmounting
an attached wrapper and on a second `flushPromises`: the pages do not state them, so they stay unsourced.
Nothing found that corrects or deletes a rule.

## Not verified
1. **Which VTU version the pages describe**; the page on stubs says VTU 1 had `shallowMount`, and the block
   treats `shallow: true` and `shallowMount` as the same, as the page does.
2. **Behaviour was not run.** Every statement about what a stub, a wrapper or a hook does is the page's.
3. **Written by us, not sourced:** the verification paragraphs, the second `flushPromises` advice, the extra assertion on the emitted model
   event, the changing-the-slot-content check, checking the event name first, leaving the child under test
   real, the `beforeEach` placement for fake time, and the order-reversal router check.
4. **Vue Testing Library and `@vue/test-utils` plugins** were not read; the page only points to the former.
5. **Vitest and Jest APIs** (`vi.setSystemTime`, `vi.spyOn`) were not read beyond how the pages call them.

## Pass of 2026-10-20
Sourced now: unmounting an attached wrapper (API reference), the habit of awaiting every `trigger` and
`setValue` (forms page and API reference), restoring real timers (Vitest API page), and a stronger form of the
stub caution (Vue testing guide). Added: native submit needs `attachTo`; restore spies. Corrected: none; the
block's earlier statements matched. Still unsourced: the second `flushPromises` advice, the emitted-model
assertion, the changing-the-slot check, the event-name-first check, the order-reversal router check. The Vue
Testing Library pages and the Jest APIs were not read.

## Related blocks
`skills/vue-router-pitfalls`, `skills/jest-vitest-assertion-pitfalls`, `skills/testing-library-query-pitfalls`,
`skills/testing-blocks`, `skills/vue-nuxt-vuetify-conventions`, `skills/testing-anti-patterns`.

## Fold-in note
Overlaps with `skills/vue-nuxt-vuetify-conventions` §14 (2026-10-19); cross-referenced, not merged.
