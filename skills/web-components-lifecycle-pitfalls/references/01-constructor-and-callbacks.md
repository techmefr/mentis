# web-components-lifecycle-pitfalls §1 — Constructor and lifecycle callbacks

An element can be created in several ways: by the parser as it reads the document, by `createElement`, by an
upgrade of an element already in the page once its class is registered, or by cloning. In some of them the
element has no attributes or children yet at construction; in others it has both. The rules below hold for all
of them.

## 1.1 The constructor
1. **Call `super()` first, take no parameters, and do not return.** The platform and the parser construct the
   element without arguments. A `return` is allowed only as a simple early return.
2. **Do not inspect the host's attributes or children.** In the non-upgrade case none are present, so reading
   gives nothing or a wrong default.
3. **Do not add attributes or children to the host.** It violates what consumers expect of an element they
   created. This includes a `setAttribute` call in the constructor.
4. **The shadow root is the exception: attach it in the constructor.** The shadow tree is not part of the
   consumer's tree. Attaching in the constructor means no later method has to check whether something already
   altered the host or already attached a root.
5. **Put everything else in `connectedCallback`** or later: listeners, reads of the host's state, anything that
   needs the element to be in a document.

## 1.2 attributeChangedCallback
1. **Declare `static observedAttributes`.** Only the attributes it lists trigger the callback; a typo in the
   getter or in the callback name means it silently never runs.
2. **It can run before `connectedCallback`, and before the element has a parent.** When the element is created
   from HTML, or from script by setting attributes before appending, the callback fires first, for each
   observed attribute present. At that moment `isConnected` is false and the document-level lookups return
   nothing.
3. **Initialise state from the attribute value; do not walk the DOM.** Querying children or the owner document
   here can find nothing. Record the value, and apply it when the element connects.
4. **For an upgrade, the callback runs once per observed attribute already on the element,** in attribute order,
   so the first call is not a "change".

## 1.3 connectedCallback and disconnectedCallback
1. **`connectedCallback` runs every time the element is inserted,** not once. Moving the element, or removing
   and re-adding it, runs it again. Make the setup idempotent: do not add a second listener, and do not
   rebuild state that already exists.
2. **It can run before the children have been parsed.** An element written in HTML can be connected while its
   children are still arriving, so `querySelector` in the callback can miss them, and a one-time traversal never
   sees children added later.
3. **React to children with an event listener or a `MutationObserver`** instead of a single traversal in the
   callback, or read them lazily when needed.
4. **Tear down in `disconnectedCallback`.** A listener added in `connectedCallback` and not removed is a memory
   leak once the element leaves the page, and a re-add then registers it a second time.

## 1.4 Subclasses
1. **Guard calls to a parent's lifecycle hook** when extending an element you do not own: the parent may not
   define it, and `super.connectedCallback()` then throws.
2. **Spell the hooks exactly.** `connectedCallback`, `disconnectedCallback`, `adoptedCallback`,
   `attributeChangedCallback` and `observedAttributes`: a misspelt hook is an ordinary method that the platform
   never calls, with no error.

## Verification
- Create the element by each of the three routes in the checkpoint and compare the resulting state (§1).
- Remove and re-append it, and count listeners before and after (§1).
- Define the class after the markup is in the page, so the element is upgraded rather than constructed (§1).
