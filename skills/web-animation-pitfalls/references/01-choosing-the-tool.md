# web-animation-pitfalls §1 — Choosing the tool

> Part 1 of `skills/web-animation-pitfalls`. Read it when a tool is chosen or a library is proposed.
> Sources, read 2026-10-20 (WebFetch digests, not verbatim): Motion documentation (performance), MDN animation
> performance and Web Animations API pages, the GSAP licence page, Rive and Lottie documentation. Sentences
> marked "own guidance" are ours.

1. **Climb the ladder only as far as the job needs.** Own guidance, in order of cost to maintain and to ship:
   - a state change on one element (hover, open, selected) is a CSS transition on the named properties;
   - a keyframed sequence with no logic is a CSS animation, or the Web Animations API when the sequence has to
     start, pause, reverse or be cancelled from script (it is the platform's script interface to the same
     engine, and `element.animate()` returns an object that carries those controls);
   - gestures, springs that react to input, layout and exit animations, or one timeline across many elements
     justify a library;
   - an animation a designer authored in a motion tool is a Lottie, dotLottie or Rive file, played by that
     format's runtime (point 4);
   - a short non-interactive loop is a video, not a script (`skills/webperf` §5).
2. **The ladder is about maintenance and ceiling, not raw speed.** Script-driven animation runs on the main thread
   and stutters when other script is busy, while CSS and the Web Animations API can be handed to the compositor
   (Motion documentation). MDN's own comparison in Firefox found CSS and script close, so "CSS is faster" is
   not a reason by itself. Choose the rung for what the code has to express and who has to maintain it.
3. **A second tool needs a reason the first cannot meet.** Two animation systems on one page fight over the same
   element: a CSS transition left on an element a library also drives produces stutter or no animation, and a
   library's own documentation tells readers to remove the conflicting transition classes (own guidance, one
   of the sources' known issues; verify on the page's own library before relying). Name which system owns each
   property of each element.
4. **An authored asset is a runtime, not an image.** Lottie plays a timeline. Rive adds state machines and runtime
   inputs, and its documentation warns that without naming the state machine an instance may only play the
   first linear animation it finds. dotLottie is a packaged delivery format for Lottie animations; its
   container, themes and player API were not read (`references/origin.md`, "Not verified"). Own guidance:
   ask for the asset's player to expose pause and a reduced-motion path before accepting it, and treat an
   asset that autoplays and loops as moving content that needs a stop control (`skills/accessibility` §7.7).
   Re-read the runtime documentation before wiring one; this block gives no API.
5. **Name the licence in one sentence when recommending a library, and re-read it.** The GSAP standard licence
   page, read 2026-10-20: a proprietary no-charge licence effective 30 April 2025, held by Webflow, free for
   commercial use on websites, web apps and digital interfaces, with prohibited uses (notably tools that let
   users build visual animations without code where GSAP materially assists a product competing with Webflow's
   animation builder) and a clause that Webflow may amend it. It is not open source. Re-read the page before
   building an animation product, because "competing" is a legal judgement this block cannot make. The Lottie
   and Rive runtimes are published as MIT by their projects (licence files read as one-line digests); Motion's
   own licence was not checked here.
6. **Say what leaves the page with the library.** Own guidance: a library adds download weight and a second
   lifecycle (§3). The weight is a measured number of the build, not a figure from a vendor page; read it from the
   project's own bundle report rather than quoting one.
