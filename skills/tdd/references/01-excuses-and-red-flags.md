# tdd §1 — Excuses and red flags

> Section 1 of `skills/tdd`. Read it when you notice yourself explaining why the test can come after the code,
> or why a red result can be made green by changing the test. **These excuses are predicted, not recorded**: written
> before a run exists. When `skills/testing-blocks` §1 yields the sentences a run without this block really
> produced, replace them here, verbatim, and drop this notice.

1. **The law of the block.** No production code without a failing test that demanded it. Code written before its
   test is not kept as a reference and adapted; it is set aside, and the test comes first. "Adapting" it is
   writing the test to fit the code, which is the order this step exists to prevent.

2. **The excuses**

   | The thought | What is actually true |
   |---|---|
   | "It is too small to test" | Small code is where a wrong boundary hides. The test is two lines. |
   | "I will write the tests after, the result is the same" | After, the tests describe what the code does. Before, they describe what it must do. |
   | "I already tested it by hand" | A manual run leaves nothing that runs tomorrow. |
   | "Deleting what I wrote would be a waste" | The time is spent. Keeping unproven code is the waste. |
   | "The test is hard to write, so the design must be right as it is" | A test that is hard to write is the design telling you it is hard to use. |
   | "I need to explore first" | Explore, then throw the exploration away and start from the test. |
   | "The test is wrong, I will change the assertion to match" | Decide which is wrong, the test or the code. If the code, the test stays. |
   | "It passed on the first run" | A test that never failed may test nothing. Break the code and watch it fail. |
   | "Mocking everything keeps it fast" | A test of mocks checks the mocks (`skills/testing-anti-patterns`). |

3. **Red flags that mean stop and go back to the failing test:**
   - production code exists and no test for it was seen to fail;
   - a test passes immediately and nobody broke the code to check it;
   - the explanation for a red result is "flaky" with no evidence;
   - an assertion was loosened, a case removed or a threshold lowered in the same change as the code;
   - tests are being added "later" and the list of what they will cover is not written;
   - the reason for skipping is a deadline, or "just this once".

4. **A red result is read before it is trusted** (`SKILL.md` step 4). A test that crashes on a broken import
   satisfies the contract and proves nothing; it turns green later for reasons unrelated to the behaviour.

5. **A test names the break it catches.** The name is the regression or the decision it guards ("rejects a
   negative quantity", "keeps the order of the lines when two share a date"). A test whose break you cannot
   name is a candidate for deletion: it fails for no reason you could explain, so it will also pass for none.

6. **A regression test is proven by reverting.** Write it, see it green with the fix, revert the fix, see it red,
   restore the fix, see it green. Only the red in the middle shows it tests the bug.
