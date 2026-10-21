# documentation-craft-pitfalls §2 — Writing for scanning and following

> Part 2 of `skills/documentation-craft-pitfalls`. Read it when a page is written or edited.
> Source, read 2026-10-20: Microsoft Writing Style Guide, "Top 10 tips", "Headings", "Lists", "Writing
> step-by-step instructions" and "Code examples" (CC BY 4.0). Sentences marked "own guidance" are ours.

1. **Lead with what matters and cut the rest.** The guide's first tips are fewer words, a plain spoken voice and
   getting to the point fast, with the most important idea first so a scanner finds it. Symptom: the answer sits
   in the fourth paragraph. Fix: move it to the first sentence and delete what no longer has a job.
2. **Treat headings as an outline that carries the story.** The guide says readers who skip the headings will
   probably skip the text. Check: read only the headings and the first sentence under each; they should tell the
   page's story without gaps or repeats (the guide's own final-review trick).
3. **Make headings specific, short and parallel.** The guide asks for the key idea first, words the reader would
   use, the same grammatical form at one level, no two headings in a row without text, and a second level only
   when there are at least two distinct topics. Symptom: "Overview", "Details", "Misc". Fix: name what the
   section lets the reader do or know. For tasks, one consistent form (an infinitive or an imperative) beats a
   mix.
4. **Use a list when the content is a list.** The guide sets a bulleted list for items with no order, a numbered
   list for a sequence or a ranking, parallel items, and an introduction that makes the purpose clear. It
   suggests at least two and, if possible, no more than seven short items (confirmed on the live lists page, read 2026-10-20). Symptom: a
   comma-separated paragraph of eight options, or a numbered list whose order does not matter. The range is for
   prose a person reads through; a generated catalogue of dozens of entries is a lookup page, so group it under
   named headings and keep each group short (own guidance).
5. **Write one action per numbered step, in the imperative, as complete sentences.** From the guide's procedure
   rules: consistent structure, a step that includes the action that finalises it, the same shape for the
   "where" prefix, and a heading that says what the procedure achieves. Combine two short actions only when they
   happen in the same place. Symptom: "Configure the service" as one step hiding six decisions.
6. **Keep procedures short, and split long ones.** The guide's step-by-step page (read 2026-10-20) gives no number of steps: it says not to overwhelm readers with too many steps and to try to fit them on one screen (the earlier figure of seven was not found there and is dropped; it does not apply to a table of commands, which is a
   lookup). Own guidance: a longer task is two
   procedures with a named checkpoint between them, and the checkpoint says what the reader should see.
7. **Say what the reader should see after the risky step.** Own guidance: a step that changes state ends with an
   observable result or a command that prints one, so a wrong turn is caught at the step and not three steps
   later.
8. **Put prerequisites before step one.** Own guidance: versions, access, data and time needed belong above the
   procedure. The guide asks code examples for the same thing: list the requirements and dependencies, and
   introduce the scenario the code addresses.
9. **Pick examples from real tasks, start small, show the output.** The guide asks for concise examples of key
   tasks, simple first and complex later, a way to copy and run them, and the expected output beside the code.
   Symptom: an example that exists to show a feature and solves nothing.
10. **Examples teach by what they do, so they must be safe.** The guide asks for secure code in examples: validate
    input, no hard-coded passwords, and exception handling only where it is intrinsic to the example. Own
    guidance: a placeholder secret in a snippet is copied into a real file within a week; use an obvious
    placeholder and say where the real value comes from.
11. **Comment examples sparingly.** The guide says to explain details without stating the obvious. Own guidance:
    the explanation belongs in the sentence around the snippet, and the snippet stays free of comment noise,
    which also matches a house rule of no comments in code.
12. **Use the reader's words and the same word for the same thing.** Own guidance, consistent with the guide's
    plain-voice tips: a page that says "workspace", "project" and "environment" for one object sends the reader
    searching for three. Pick the term the product uses and keep it.
