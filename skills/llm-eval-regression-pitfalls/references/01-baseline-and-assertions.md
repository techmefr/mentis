# llm-eval-regression-pitfalls §1 — Cases, baseline and assertions

## 1.1 Test cases
1. **A case is a realistic prompt, a description of success and any input files.** The Agent Skills guide
   stores them in a file next to the skill and says to write them as a user would type them, with paths and
   context, not as "process this data".
2. **Start small and vary them.** The guide suggests a few cases first, different phrasings and levels of
   detail, and at least one edge case. Grow the set after the first results show what matters.
3. **Add assertions after a first run,** not before. You often do not know what good looks like until the
   output exists.

## 1.2 The baseline
1. **Run every case twice: with the change and without it.** The comparison is the result; a with-skill score
   alone does not say what the skill added.
2. **When improving an existing version, the baseline is the previous version.** Snapshot it before editing
   and run the same cases against the snapshot.
3. **Each run starts in a clean context,** with no leftovers from the authoring session, so the output reflects
   what the written instructions say. Use a fresh subagent or session per run.
4. **Record cost next to quality:** tokens and time per run, and the difference between arms. A gain that
   triples cost is a different decision from one that is cheaper too.
5. **Repeat runs when results vary.** The guide notes that spread is meaningful only with several runs per
   case; with one run each, look at raw pass counts and the difference.

## 1.3 Assertions
1. **A good assertion is checkable from the output:** a valid file, a countable item, an observable property.
   "The output is good" cannot be graded, and an exact-phrase match fails correct output worded differently.
2. **Use code for what code can check** (valid format, row count, a file exists) and a model or person for
   the rest. Scripts are more reliable than a model for mechanical checks and are reusable.
3. **A pass needs evidence.** Grade with a quoted piece of the output; a section titled "Summary" holding one
   vague sentence fails an assertion that asks for a summary.
4. **Review the assertions as well as the results.** One that always passes is too easy, one that always fails
   is broken or too hard, and one that cannot be checked from the output should be rewritten.
5. **Not everything needs an assertion.** Style and feel are for human review.

## 1.4 Reading the results
1. **Remove assertions that pass in both arms,** since they inflate the with-change rate without showing any
   value of the change.
2. **Investigate assertions that fail in both arms** before changing the change: the case may be too hard or
   the assertion wrong.
3. **Study those that pass only with the change.** That is where it adds value; find which instruction did it.
4. **Read the transcripts of outliers** in time or tokens.
5. **Have a person read outputs next to the grades** and write specific feedback per case; "the axes have no
   labels" is usable, "looks bad" is not. Stop when feedback is empty or iterations stop improving.
6. **Prefer lean changes.** When the pass rate plateaus after adding rules, try removing instructions and
   see if results hold; explain the reason for an instruction rather than shouting it.
