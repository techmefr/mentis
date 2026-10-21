# computer-use-agent-pitfalls §2 — Tools and turns

> Part 2 of `skills/computer-use-agent-pitfalls`. Read it when the loop and the tool definitions are written.
> Sources: the macOS computer-use reference of anthropics/claude-quickstarts (MIT), its README section on explicit
> and hosted tools and its loop (read 2026-10-20); Anthropic's computer-use tool and vision pages and OpenAI's
> computer-use guide, re-read 2026-10-20 for the points that cite them (product documentation, facts only).
> Sentences marked "own guidance" are ours. Behaviour claims not tied to a vendor page are the repository's.

1. **Two ways to declare the screen tool.** Either you define the tool yourself, with its name, description and
   input schema in your own code, or you declare the vendor's built-in one. The reference defaults to its own
   definition so a reader can see exactly what the model sees, and says that is a teaching choice.
2. **The built-in declaration is what engages the vendor's computer-use safety checks.** The reference states that
   classifiers for this use, including detection of injected instructions in screenshots, run only when the
   request declares the vendor's tool; a self-defined schema is on the generic path, and you carry your own
   mitigations. Anthropic's page says that when you use its computer-use tools, classifiers scan what the tools return,
   screenshots included, and steer the model to check with you whether an instruction really came from you; it does not
   say what applies to a tool you define yourself. It also says this layer is not ideal for runs without a human in the
   loop and can be turned off through support, and that the other precautions stay necessary. Decision: if you need those checks, declare the built-in tool; either way, write down which path
   you are on, because it changes what the rest of the safety story must supply (§3).
3. **Execution stays yours in both cases.** Declaring the built-in tool changes the declaration only; your code
   still runs every action. The reference keeps its batch, browser and shell tools explicit while switching the
   screen tool's declaration.
4. **The hosted declaration may come as one entry with one member per action.** In the reference, calls arrive as
   ordinary tool-use blocks named after the action (click, zoom, and so on) carrying the name of their set and no
   `action` field. Anthropic's page tells you to dispatch on the pair (set name, tool name), because a custom tool in the
   same request can share a member's name. Own guidance: fold the name back into one action field internally, and
   let one implementation serve both declarations.
5. **A turn may carry several actions.** They run in block order. After the first failure, answer each remaining
   block as an error with a "not executed" text instead of running it, because every later action assumed the
   earlier one worked. Symptom of running on: typing into whatever window has focus after a click that missed.
   Anthropic's page specifies the answer: the failed action gets an error result with a description, every later block
   gets an error result with a fixed not-executed text, and a request that leaves any block unanswered is rejected
   with an invalid-request error, so a loop that reads only the first block breaks on its next call.
6. **Every call gets an answer.** Each tool-use block needs a matching result, including the ones you skipped and
   the ones you interrupted. The reference fills interrupted calls with an "interrupted by user" result when the
   operator presses cancel. Symptom of a missing answer: the next request is rejected for an unmatched call.
7. **Echo the set name on results of set members, and only those.** The reference stamps each member's result with
   the same set name as its call, and results for ordinary tools do not carry one; Anthropic's page says a member
   result that omits the name, or names another set, is rejected. It also says only screenshot and zoom results need an
   image, a short text acknowledgment is enough for the rest. Symptom: a request rejected
   for a mismatched result block after a loop that worked with the single-tool declaration.
8. **Batch predictable steps, and only those.** A batch tool lets the model chain actions it can plan with
   confidence (focus a field, type, press enter) in one turn, which cuts latency and cost. The reference nudges the
   model toward batching with a short reminder after a lone call. Own guidance: never batch across a point where
   the screen decides what happens next (a dialog that may or may not appear), and apply point 5 inside the batch.
   Where a person confirms consequential actions, Anthropic's page says to ask before each block runs, since one batch can
   complete a multistep action in a single turn.
9. **Return a screenshot after actions that change the screen.** The vendor page lets a result be a short text
   acknowledgment, so this is a design choice (own guidance): the model cannot see an effect it was not shown, and a
   click answered with text only forces an extra screenshot call or a blind next step. Anthropic's prompting advice
   says the model sometimes assumes an action worked without checking, and suggests telling it to take a screenshot
   after each step, say what it shows and move on only when the step succeeded; to end every batch with a screenshot,
   say so in the system prompt.
10. **Restrict the tool list to what the task needs.** The reference lets a run disable the desktop tools entirely and
    use only a headless browser. Own guidance: an agent that only reads web pages should not hold a mouse and a
    shell; every extra tool is a way for a screen's text to do something (§3.1). OpenAI's guide gives the same pattern: its
    browser driver exposes only the operations the task needs through a list of members, and its sample allows only
    screenshots and one click.
11. **Cap iterations and report a stuck screen.** OpenAI's sample bounds the run at a small fixed number of requests;
    the stuck-screen rule itself is own guidance: a loop of identical screenshots and identical
    actions is a failure; stop after a few repeats and hand back to a person with the last two images.
12. **Count images across the whole history.** Anthropic's vision page says that once a request holds more than twenty
    images, a stricter per-image size limit applies to every image in it, including earlier turns' screenshots inside
    tool results; an image over it is rejected. Symptom: a loop that works for dozens of turns and then fails with an
    error about many-image requests. Fix: size every screenshot under the stricter limit, or prune old ones. The tool
    page adds how to prune without losing the cache: drop screenshots in batches, not one per turn, since each removal
    changes the prefix (`llm-cost-latency-control-pitfalls` §1.2).
13. **Give the interface time to react.** Anthropic's best-practice notes show a short wait after each click so the next
    screenshot is not taken mid-update. Symptom: the model sees the old screen and repeats an action that had worked.
14. **Put the instruction before the screenshot** in a turn: Anthropic's prompting advice says a target description
    that precedes the image improves click accuracy.
