# game-engine-loop-and-lifecycle-pitfalls §2 — Lifecycle, cost and persistence

Source: own craft knowledge, with the points marked "Godot docs" checked on 2026-10-20 against the Godot Engine documentation (CC BY 3.0, rewritten in our words, nothing copied). Engine facts are to be re-read for the version in use.

## 2.1 Per-frame cost
1. **Symptom: a stutter every few seconds that the profiler shows as a collection or allocation spike.** Cause: a callback that runs each frame creates objects (vectors in a managed language, strings, arrays, closures, temporary nodes). Fix: reuse a field, pool the objects, or preallocate the array and clear it.
2. **Never look nodes or entities up by name or path inside a per-frame callback.** Resolve the reference once when the object enters the scene and keep it; a path lookup walks the tree by string and returns nothing after a rename.
3. **Building a label string every frame is a hidden allocation.** Update the text only when the value changes.
4. **Turn off per-frame processing on objects that are idle, off-screen or paused,** instead of returning early at the top of a callback that still runs.
5. **Check:** profile one minute of a busy scene and look at allocations per frame, not only the frame time. The target is zero in steady state.

## 2.2 Scene, node and entity lifecycle
1. **Freeing an object while one of its callbacks or a signal handler is running crashes or reads freed memory.** Use the engine's deferred free (queue the free for the end of the frame), never an immediate delete inside a handler (own guidance: the Godot pages read confirm only that freeing a node frees its children, not the timing of the deferred form).
2. **A reference to a freed object is not null in every language.** Test validity with the engine's check, not with a null test, before using a reference you stored.
3. **Order of readiness is not order of creation.** A parent is ready after its children; a child that reads a sibling or parent in its constructor sees nothing. (Godot docs: the ready callback of a node runs once all its children have run theirs, bottom-up, after the tree is complete; the construction callback runs before entering the tree; a scene instantiated but not added to the tree gets only the construction callback.) Do initialisation that needs the tree in the ready callback, and cross-object wiring in the code that builds both.
4. **Changing scene frees the old one at a point the engine chooses, and the current scene must not be deleted while its own code is still running** (defer the change; Godot docs, autoload page, read 2026-10-20). Autoloaded singletons survive every scene change, and so does everything they reference; a singleton holding the player or an enemy keeps it alive into the next scene. Never free an autoload at run time: the docs say the engine crashes.
5. **Symptom: memory grows with every level change.** Cause: an object removed from the tree but never freed (removal is not deletion: Godot docs, removing a child leaves the tree and runs the exit callback, it does not free the node), or a connection that references it. Fix: free it, and compare the live object count before and after ten level changes.

## 2.3 Signals and events
1. **Every connection has an owner that must disconnect it, or the emitter keeps the receiver alive** where the emitter holds a callable. Disconnect in the exit-tree callback, or connect with the engine's one-shot form.
2. **A connection made twice runs twice.** Guard with the engine's "is connected" check when a node can enter the tree more than once.
3. **Do not emit an event from inside its own handler on the same object without a guard.** The recursion shows up as a stack overflow or a doubled effect.
4. **Prefer a signal up and a method call down:** a child announces what happened, a parent tells a child what to do. A child that reaches into the parent's methods cannot be reused in another scene.

## 2.4 Loading, content and save data
1. **Loading a resource on the main thread in the middle of play is a visible hitch.** Preload what is certain, load in the background what is probable, show a loading state, and poll the load status instead of blocking. (Godot docs: the plain load call blocks the thread; the threaded request queues a load, a status call reports progress, and fetching the result before it is done blocks like a plain load.)
2. **Instantiating a large scene at once can also hitch.** Spread the creation over frames or pool it.
3. **A resource loaded twice from the same path is shared, not copied.** Changing it at run time changes it for every user (a material colour, a stats resource). Duplicate it when each instance needs its own. (Godot docs, resource class page read 2026-10-20: loaded resources are cached by path, later loads return the same object, and the cache entry goes away only when all references are released. A duplicate is shallow by default, so nested resources, arrays and dictionaries stay shared unless you ask for a deep copy; a per-scene flag, off by default, makes every scene instance get its own copy.)
4. **Save plain data (numbers, strings, arrays, dictionaries) with a version field, never live engine objects or scripts.** A save format that can embed objects can run code from a file the player downloaded, and a renamed class breaks old saves. Migrate by version on load. (Godot docs: the text format has a limited type set and needs your own encoding for custom classes, the binary form handles most types with less custom code and smaller files; neither page read warns about code execution or discusses versioning: own guidance.)
5. **Write the save to a temporary file and rename it,** so a crash during the write does not destroy the previous save.
6. **Desktop and web exports differ in storage, threads and memory.** Test the web export before promising it.

## Checks
- No allocation or name lookup in per-frame callbacks (§2.1).
- Deferred free, validity checks and ready-order assumptions reviewed (§2.2).
- Connections have a matching disconnect; object count is stable across ten reloads (§2.2, §2.3).
- Saves hold plain versioned data and are written atomically (§2.4).
