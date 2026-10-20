# game-engine-loop-and-lifecycle-pitfalls §1 — Time and update steps

Source: own craft knowledge; engine facts are stated generally and are to be re-read for the version in use.

## 1.1 Frame-rate independence
1. **Symptom: the game runs at a different speed on a fast display, a laptop on battery or after a hitch.** Cause: a value is added once per frame. Fix: multiply every per-frame change (speed, rotation, fade, cooldown) by the step the engine passes to the callback; a timer subtracts the step, it does not count frames.
2. **Check:** cap the frame rate low, then high, and compare the distance covered in one second of real time. They must match within the tolerance the game accepts.
3. **A long frame produces one huge step** (after a breakpoint, a window drag, a loading hitch). Clamp the step used by gameplay code to a maximum, or the player falls through the floor and every timer fires at once.
4. **Do not rely on vertical sync as a speed limiter.** It is a user setting and a driver decision; a build that is correct only with it on is wrong.

## 1.2 Fixed step versus variable step
1. **Two callbacks exist on most engines: a variable one per rendered frame, and a fixed one at a set rate for physics.** Put physics, forces, movement of physics bodies and anything that must be reproducible in the fixed one; put visuals, camera, UI and animation in the variable one.
2. **Symptom: a character jitters when the camera follows it.** Cause: the body moves in the fixed callback and the camera in the variable one, at different rates. Fix: follow from the same callback, or interpolate the visual between the last two physics states.
3. **Setting a body's position directly teleports it and bypasses collision.** Move it with the engine's motion or force API, and keep teleports for respawns.
4. **A slow fixed step feeds on itself.** The engine runs more steps next frame to catch up and falls further behind; engines cap the catch-up, so the simulation slows down instead of freezing. Measure the cost of one fixed step, not only the frame.
5. **Check:** log the number of fixed steps per frame during a hitch. A value that keeps growing means the physics code is too heavy for its rate.

## 1.3 Input
1. **Read held state for continuous actions and events for one-shot actions.** Polling a button each frame to detect a press fires it for as many frames as the button is down; use the engine's "just pressed" form or the event.
2. **Name actions, not keys, in the input map.** Code that checks a key code cannot be rebound, and a controller needs a second code path.
3. **Mouse and touch positions are in different coordinate spaces from world positions** (window, viewport, canvas, world). Convert once at the boundary with the engine's helper, not by hand in gameplay code.

## 1.4 Determinism and randomness
1. **Floating-point results can differ between CPUs, compilers and operation order.** Lockstep multiplayer, replays and rewind need a deterministic design (fixed step, integer or fixed-point state, a seeded generator owned by the simulation); do not assume two machines agree.
2. **Use one seeded generator per concern** (loot, level generation, effects) so a visual effect that draws a random number does not change the loot a seed produces.
3. **Never iterate an unordered collection to apply gameplay effects** when order matters; sort by a stable id first.

## Checks
- The movement test at two frame rates (§1.1) passes.
- Physics code lives in the fixed callback; the camera does not jitter (§1.2).
- Continuous and one-shot input use the right form; actions are named (§1.3).
