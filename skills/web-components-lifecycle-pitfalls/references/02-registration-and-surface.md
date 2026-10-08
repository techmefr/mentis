# web-components-lifecycle-pitfalls §2 — Registration and public surface

Registration is global and happens once per name. The public surface of an element is shared with every
consumer and with the platform's own conventions.

## 2.1 Registering
1. **A second `define` for the same name throws.** The platform raises `NotSupportedError`, and the same error
   when the same constructor is registered under two names. A script loaded twice, or two bundles that both
   include the element, crashes the second load. Guard with `if (!customElements.get('my-tag'))`.
2. **Define after the class declaration.** A `define` placed above a `class` declaration hits the temporary
   dead zone. Passing a class expression straight into `define` also leaves nothing to export or assign.
3. **Expose the class under its own global name,** the way built-ins expose `HTMLDivElement`, so other code can
   refer to the constructor.
4. **One element per file, and export only the element.** Extra exports and several classes in one file make
   imports confusing and are a sign the file is doing too much. Keep the file name, class name and tag name
   visibly related.
5. **Never take constructor arguments.** The parser and `createElement` supply none.

## 2.2 Names
1. **A tag name must contain a hyphen and start with an ASCII lowercase letter.** The hyphen keeps names
   forward-compatible with new built-in tags, and the lowercase start lets the parser treat it as a tag.
   Names such as `app`, `1-app`, `-app`, `my-App` or `my--app` are invalid or reserved.

## 2.3 What to extend
1. **Extend `HTMLElement` for an autonomous element.** A customized built-in element (the `extends` option and a
   subclass of, say, a paragraph class) must extend that element's constructor and match the `extends` value.
2. **Avoid customized built-ins.** Safari does not support them and has said it does not plan to, and new
   features added to the built-in element must be adopted by every subclass.

## 2.4 Shadow root and host
1. **Use open shadow roots.** A closed root hinders inspection and interaction and is rarely needed.
2. **Do not set classes on the host from inside the element.** The host belongs to its consumer, and the
   element changing `classList`, `className` or the `class` attribute can clobber classes the consumer set. Use
   attributes and `:host` styling, or the shadow tree.
3. **Do not name methods `on<something>`.** The platform's event-handler properties (`onclick`, `ontoggle`) are
   assignable and fire with their event; a method with such a name breaks that contract or collides with a
   property the platform adds later. Use verbs such as `handleX`.

## Verification
- Load the module twice in one page and confirm no error (§2).
- Check each registered tag name: it contains a hyphen and starts with a lowercase letter (§2).
- Read the element's public methods and confirm none starts with `on` (§2).
