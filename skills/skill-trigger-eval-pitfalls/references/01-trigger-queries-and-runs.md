# skill-trigger-eval-pitfalls §1 — Trigger queries and runs

## 1.1 What is being measured
1. **Triggering is decided from the name and description alone.** The Agent Skills guide says agents load only
   those two fields of every available skill at startup and read the full `SKILL.md` when a task matches. The
   description therefore carries the whole burden of triggering.
2. **A skill may not be consulted for a simple task even with a perfect description.** The guide notes that
   agents typically consult skills only for tasks that need knowledge or capability beyond what they handle
   alone, and gives a one-step "read this PDF" as an example that may never trigger a PDF skill.
3. **A should-trigger query must therefore need the skill** (own guidance). A query the agent can finish with
   basic tools that never triggers under any wording is a bad query, not a bad description.
4. **Output quality is another measurement.** Whether the skill helps once loaded is in
   `llm-eval-regression-pitfalls` §1; this block measures activation only.

## 1.2 The query set
1. **Label each query with whether it should trigger.** The guide stores them in a small JSON file with a
   `query` text and a `should_trigger` flag:

   ```json
   [
     { "query": "my manager sent ~/Downloads/q4_numbers.xlsx, can you add a margin column and flag rows under the target", "should_trigger": true },
     { "query": "whats the quickest way to turn this json file into yaml", "should_trigger": false }
   ]
   ```

2. **Aim for about twenty, half and half.** The guide suggests 8 to 10 that should trigger and 8 to 10 that
   should not, as a starting size.
3. **Vary the should-trigger queries along four axes:** phrasing (formal, casual, typos), explicitness (names the
   domain or only describes the need), detail (terse or context-heavy) and complexity (single step or a step
   buried in a longer chain).
4. **The most useful positives are the ones where the connection is not obvious.** If the query asks for exactly
   what the skill does, any reasonable description triggers and the query separates nothing.
5. **The most useful negatives are near-misses:** queries that share keywords or concepts with the skill but need
   something else. The guide's weak examples are an unrelated function request and a weather question; its
   strong ones share the vocabulary (a spreadsheet formula edit against a data-analysis skill, a database load
   against a CSV-analysis skill).
6. **Write queries the way users type them.** The guide lists file paths, personal context, specific details
   such as column or company names, casual language, abbreviations and occasional typos.
7. **Include the neighbours' territory in the negatives** (own guidance). When other installed skills overlap in
   vocabulary, a near-miss that belongs to a neighbour is the case a broad description fails first.

## 1.3 Running the queries
1. **Make sure the skill is registered and discoverable before reading any result.** How that works varies by
   client (a skills directory, a configuration file, a flag). A skill the client never saw fails every
   should-trigger query and says nothing about the description.
2. **The skill triggered if the agent loaded its `SKILL.md`.** The guide points to execution logs, tool-call
   histories or verbose output, whichever the client offers; the detection logic is client-specific and has to be
   written per client.
3. **A query passes in one of two ways:** it should trigger and the skill was invoked, or it should not trigger
   and the skill was not invoked.
4. **Run each query several times.** Model behaviour is nondeterministic and the same query can trigger on one
   run and not on the next. The guide suggests three runs as a starting point and a trigger rate, the fraction
   of runs that invoked the skill.
5. **Apply a threshold to the rate.** A should-trigger query passes if its rate is above the threshold and a
   should-not-trigger query passes if it is below; the guide gives 0.5 as a reasonable default.
6. **Script it.** Twenty queries at three runs is sixty invocations. The guide's script counts invocations per
   query and prints the rate; its detection step is a placeholder for the client's own.
7. **Stop a run early when the client allows it.** The outcome is known as soon as the agent consults the skill or
   starts working without it, and the guide says this can cut time and cost considerably.
8. **Report the rate of each query, not only the pass count** (own guidance). A query at the threshold is
   unstable and tells you the description is on the edge for that phrasing. Record the client, its version and
   the model with the results, since the behaviour belongs to that combination.
