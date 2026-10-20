# web-animation-pitfalls §3 — Lifecycle and presence

> Part 3 of `skills/web-animation-pitfalls`. Read it when animation code lives inside a component, a list or a
> route. Sources, read 2026-10-20 (digests): GSAP documentation for `gsap.context()` and the React guide; Motion
> documentation for `AnimatePresence` and layout animations; Rive web runtime documentation. Sentences marked
> "own guidance" are ours.

1. **What a component starts, the component stops.** An animation, scroll trigger, listener or runtime
   instance created in a component that is not torn down with it keeps running after the element is gone, and
   when the component mounts again there are two. Own guidance: for each animation in a review, ask where it
   ends. If the answer is "when the page unloads", it is a leak.
2. **Collect, then revert in one place.** GSAP's `gsap.context()` gathers every animation and scroll trigger
   created inside it and reverts them together, restoring the elements; the documentation recommends its
   framework hook in React so the cleanup is not written by hand. Revert is the cleanup; the page does not
   describe how kill differs, so read before using it. Own guidance: whatever the library, one collection
   per component, one revert on teardown.
3. **Things created after the hook ran are outside the collection.** The React guide names click handlers and
   delayed callbacks as animations that are not cleaned up unless wrapped for the context, and says manually
   added event listeners stay until the cleanup function you return removes them. Selector text in those
   callbacks is also not scoped to the component without the wrapper. Own guidance: grep a component for
   animations inside event handlers and timers; each one is a place to check.
4. **Development double-runs expose teardown bugs.** React's development mode runs effects twice, and GSAP's guide
   says that without a revert this creates duplicate animations or breaks tweens that start from a given
   state. A duplicate in development is the test that the teardown is missing; do not suppress the double
   run to hide it.
5. **A dependency list does not mean "revert on change".** In GSAP's hook, dependency changes do not revert
   until unmount unless the option for it is set (the documentation says the default is off). An animation that
   should restart on a new value needs that option or an explicit revert. Own guidance: state which of the two
   the code relies on.
6. **An exit animation needs the node to stay mounted.** Motion's `AnimatePresence` detects an exit when a direct
   child leaves the tree, so the wrapper itself must stay mounted (put the condition inside it, not around
   it), and each direct child needs a stable unique key, not an index; an index key or a remounting wrapper is the
   usual reason an exit "does nothing". Nested exits are blocked by default unless the inner wrapper is told to
   propagate. Props of a removed component cannot update, so data an exit needs is passed through the
   documented channel, not read from state. Verify the names against the library's page for the version in use.
7. **Choose the exit mode on purpose.** Entering and leaving at the same time, one after the other, or taking the
   leaving node out of flow so siblings reflow at once are different designs; the default coordinates no layout,
   and group layout then needs its own wrapper (Motion documentation). Out-of-flow exits need a positioned
   parent. Pick the mode that matches the sentence a designer would use ("the new one waits", "the list closes
   the gap").
8. **A layout animation is transforms with side effects.** Motion measures before and after and animates with
   translate and scale, which is cheap, and scale can stretch children, borders and corner radii; the
   documentation lists the corrections (counter-scaling children, setting radius and shadow through style
   props, a padded parent in place of a border) and the cases that go wrong (scroll containers and fixed
   containers need telling, inline elements receive no transforms, a scrollbar appearing triggers an unwanted
   animation, SVG is not supported). Own guidance: before adopting layout animation for a component, list which
   of these it has.
9. **A runtime instance of an authored asset is released explicitly.** Rive's web documentation says to call its
   cleanup when an instance is no longer needed, which frees native-side objects to prevent memory leaks; the
   same teardown thinking applies to any player. Play, pause and input methods of Rive and dotLottie were not
   in the pages read: re-read the player documentation before relying on any (`references/origin.md`).
10. **Frame-driven timelines stay seekable only if nothing reads the DOM at tween time.** Own guidance, from the
    ideas of one source's video-rendering rules: compute sizes once at setup and animate from and to values
    that were fixed beforehand. The same discipline avoids layout thrash on a live page.
