# computer-use-agent-pitfalls §2 — Tools and turns

> Part 2 of `skills/computer-use-agent-pitfalls`. Read it when the loop and the tool definitions are written.
> Source, read 2026-10-20: the macOS computer-use reference of anthropics/claude-quickstarts (MIT), its README
> section on explicit and hosted tools and its loop. Sentences marked "own guidance" are ours. Behaviour claims are
> the repository's; re-read the vendor documentation before relying on them.

1. **Two ways to declare the screen tool.** Either you define the tool yourself, with its name, description and
   input schema in your own code, or you declare the vendor's built-in one. The reference defaults to its own
   definition so a reader can see exactly what the model sees, and says that is a teaching choice.
2. **The built-in declaration is what engages the vendor's computer-use safety checks.** The reference states that
   classifiers for this use, including detection of injected instructions in screenshots, run only when the
   request declares the vendor's tool; a self-defined schema is on the generic path, and you carry your own
   mitigations. Decision: if you need those checks, declare the built-in tool; either way, write down which path
   you are on, because it changes what the rest of the safety story must supply (§3).
3. **Execution stays yours in both cases.** Declaring the built-in tool changes the declaration only; your code
   still runs every action. The reference keeps its batch, browser and shell tools explicit while switching the
   screen tool's declaration.
4. **The hosted declaration may come as one entry with one member per action.** In the reference, calls arrive as
   ordinary tool-use blocks named after the action (click, zoom, and so on) carrying the name of their set and no
   `action` field. Own guidance: route on the pair (set name, tool name), fold the name back into one action field
   internally, and let one implementation serve both declarations.
5. **A turn may carry several actions.** They run in block order. After the first failure, answer each remaining
   block as an error with a "not executed" text instead of running it, because every later action assumed the
   earlier one worked. Symptom of running on: typing into whatever window has focus after a click that missed.
6. **Every call gets an answer.** Each tool-use block needs a matching result, including the ones you skipped and
   the ones you interrupted. The reference fills interrupted calls with an "interrupted by user" result when the
   operator presses cancel. Symptom of a missing answer: the next request is rejected for an unmatched call.
7. **Echo the set name on results of set members, and only those.** The reference stamps each member's result with
   the same set name as its call, and results for ordinary tools do not carry one. Symptom: a request rejected
   for a mismatched result block after a loop that worked with the single-tool declaration.
8. **Batch predictable steps, and only those.** A batch tool lets the model chain actions it can plan with
   confidence (focus a field, type, press enter) in one turn, which cuts latency and cost. The reference nudges the
   model toward batching with a short reminder after a lone call. Own guidance: never batch across a point where
   the screen decides what happens next (a dialog that may or may not appear), and apply point 5 inside the batch.
9. **Return a screenshot after actions that change the screen.** Own guidance: the model cannot see an effect it
   was not shown; a click answered with text only forces an extra screenshot call or a blind next step.
10. **Restrict the tool list to what the task needs.** The reference lets a run disable the desktop tools entirely and
    use only a headless browser. Own guidance: an agent that only reads web pages should not hold a mouse and a
    shell; every extra tool is a way for a screen's text to do something (§3.1).
11. **Cap iterations and report a stuck screen.** Own guidance: a loop of identical screenshots and identical
    actions is a failure; stop after a few repeats and hand back to a person with the last two images.
