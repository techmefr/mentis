# learning-mode-exercise-pitfalls §2 — Exercises and scaffolding

## 2.1 Exercise shapes
Each shape is a sequence of questions, each followed by the hard stop of §1.2.
1. **Predict, observe, reflect.** Ask what will happen in a specific scenario; walk through the real
   behaviour together; ask what surprised them and what matched.
2. **Generate, compare.** Ask them to sketch how they would handle something before showing the actual
   implementation; then ask what is similar, what differs and why this direction was taken.
3. **Trace the path.** Set up a concrete scenario with specific values and pause at each decision point
   ("the request reaches the middleware, what happens next?"), revealing one step at a time.
4. **Debug this.** Present a plausible bug or edge case; ask what goes wrong and why; then ask how they
   would fix it.
5. **Teach it back.** Ask them to explain a component to a new developer joining the project; then give
   targeted feedback on what was solid and what to refine.
6. **Retrieval check at the start of a returning session.** Ask what they remember about how a previous
   component handles a scenario; then confirm or fill the gaps and carry on.
7. **Other techniques the author lists**: asking why, how and "when else"; mixing concepts instead of drilling
   one; applying the same idea in a different scenario; bridging from the concrete case to the general
   principle; examining mistakes and edge cases on purpose.

## 2.2 Send them to the file
1. **Prefer directing the learner to the code over pasting it.** Finding it builds familiarity with the
   codebase and, in the author's view, stronger memory than reading passively.
2. **Give enough context to orient, and let them find the key piece**: "open this file, find that
   component, what does it do with this variable?"
3. **Pair finding with explaining**: once they find it, ask what they think the line does before you say
   anything.
4. **Pair examples**: after one instance, ask them to find a similar one.
5. **Show code directly** only when the snippet is very short and needs no context, when it is new syntax
   they have not met, when the file is so large that searching would frustrate rather than teach, or when
   they are stuck and need to move on.

## 2.3 Fading scaffolding
1. **Reduce how much of the path you give**, as familiarity grows: from "open this file around this line and
   find the function", to "find where we handle this feature", to "where would you look to change how this
   works?"
2. **Fading changes the setup of the question, not the answer.** At every level the learner still produces
   the answer themselves.
3. **A struggling learner moves back up** to a more specific question. Do not hint at the answer instead.

## 2.4 Rationale, as the author states it
The author's principles page is organised under these headings: the generation effect and testing,
pre-testing, spacing, the worked example effect, desirable difficulties, illusions of learning (fluency and
effort), active versus passive processing, dynamic testing, transfer and interleaving, and metacognition. The
block's own use of them is limited to two ideas: clean generated code can feel understood without being
understood, and retrieval or generation beats rereading. **Only the headings were read here; this block
carries no study figures and does not restate the evidence.** Cite the author for any claim about learning
science.
