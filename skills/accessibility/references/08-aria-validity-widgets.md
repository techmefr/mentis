# § 8 — ARIA validity and component recipes

> Section 8 of `skills/accessibility`. Read it after §2 has decided that ARIA is needed: first to make
> the markup valid, then when building one of the recipes below. §2 says when ARIA is allowed; this section
> says what a valid use looks like and how the common composite widgets are assembled. Role and attribute
> tables are not copied here: they live in the standards and they change.

## Validity

1. **The standards are the source of truth.** Which roles exist, which states and properties each role
   supports, and what each requires is in WAI-ARIA (the version the project targets) and, for which role an
   HTML element may take, in ARIA in HTML. A checker that implements those tables is the efficient
   reader; reading the tables from this block would be reading a copy that can fall behind
   (`skills/source-freshness`).
2. **A role is one the element may take.** An invented value, an abstract role, or a role that the HTML
   mapping forbids on that element (`role="button"` on a heading, `role="presentation"` on a focusable
   element) is wrong ARIA and worse than none (§2.1). Redundant roles on elements that already have them
   are noise; the exception is the list case in §6.8.
3. **Required context and children are present.** Some roles only make sense inside or around others: a
   `tab` inside a `tablist`, a `menuitem` inside a `menu` or `menubar`, a `treeitem` inside a `tree` or
   `group`, a `listitem` inside a `list`, rows and cells inside a `grid` or `table`, an `option` inside a
   `listbox`. The role without its owner, or the owner empty, breaks navigation in assistive technology.
4. **Attributes are supported, required, and valid.** An `aria-*` attribute is used only on roles that
   support it; roles with required properties carry them (a custom checkbox exposes `aria-checked`, a
   slider its value and range, a heading given a role its level); values are of the right type (a
   boolean, a token from the allowed set, a number); and every ID reference (`aria-labelledby`,
   `aria-describedby`, `aria-controls`, `aria-owns`, `aria-activedescendant`) points at an element that
   exists in the same tree (§6.9). A state that is not kept in sync with the interface is a lie (§2.5).
5. **Deprecated and unsupported roles are replaced.** When the standard marks a role or attribute
   deprecated, or an engine or reader ignores it, use the native element or the current form. The status
   is read from the standard at the time of writing.
6. **Some roles must be named.** A `dialog`, `alertdialog`, `meter`, `progressbar`, `tooltip` or `tree`
   (and the items of one) has an accessible name from the author, by a visible heading
   (`aria-labelledby`) or by `aria-label` (§2.2); command and toggle controls and input fields need names
   as in §2.2 and §4.1.
7. **`aria-hidden` is never on the `body`**, nor on an ancestor of anything focusable (§2.7). Hiding a
   page to reveal a layer is done with the native modal dialog or with the `inert` attribute on the
   background (§1.4), not with `aria-hidden` on the root.

## Recipes

Each recipe is a floor, not a design. In every case the native element comes first (§2.9), the
keyboard map is part of the component (§2.8), and the state is exposed (§4.10).

8. **Tabs.** A `tablist` holding `tab` buttons, each controlling a `tabpanel` (`aria-controls`), with
   `aria-selected` on the active one and the panel labelled by its tab. One tab stop for the list (roving
   `tabindex`); arrow keys move between tabs, `Home` and `End` jump; activation follows focus when the
   panels render instantly and waits for `Enter` or `Space` when they do not. A panel with no focusable
   content is itself focusable. If the pieces are plain links to separate pages, it is navigation, not
   tabs.
9. **Accordion.** A heading (the right level for its place in the outline, §1.9) containing a native
   `button` whose `aria-expanded` mirrors the open state, with `aria-controls` pointing at the panel.
   `details` and `summary` do this natively and are the default; a custom accordion is justified only by
   a requirement the native one cannot meet. Avoid giving every panel a `region` role in a long list.
10. **Tooltip.** A short, non-interactive description tied to its trigger with `aria-describedby`, shown
    on focus as well as hover, dismissible without moving the pointer (`Escape`), persistent while the
    pointer is over it, and never the only place an essential instruction lives (WCAG 1.4.13;
    §1.12). A control that needs a name gets a name, not a tooltip (§2.10).
11. **Carousel.** A region labelled as a carousel, with a pause control as the first control and
    previous and next buttons that are real buttons, each slide labelled with its position. Automatic
    rotation is off by default or stops on focus and hover, the live region announces politely only when
    the visitor drives the change, and the content never moves faster than it can be read (§7.7).
12. **Breadcrumb.** A `nav` labelled "Breadcrumb", an ordered list of links, with the current page last and
    `aria-current="page"` on it. The structured-data twin of this trail is `skills/seo` §6; the visible
    one and the data say the same thing.
13. **Pagination.** A `nav` labelled for what it paginates, a list of links, `aria-current="page"` on the
    present page, previous and next with names that say what they do, and an unavailable direction
    rendered as disabled text rather than a dead link. The page position is announced; infinite scroll
    is not the only way to reach content (§1.14).
14. **Search.** A search landmark (the `search` element or `role="search"`) around a field with a visible
    label, `type="search"`, and a submit button; results state their count through a polite live region
    (§2.3). Several `nav` or `search` landmarks on one page each get a distinct label so a landmark list
    tells them apart.
15. **File upload.** The native `input type="file"` with a visible label, whatever the custom styling; the
    chosen file names appear as text; progress, success and error go through a live region and the error
    sits next to the field (§4.8, §4.13). Drag-and-drop is an addition to the button, never a replacement
    (§1.7).
16. **Custom element.** A web component exposes the semantics a native element would: role and states set
    through the element's internals, focus delegated to the interior control, form participation
    through the form-associated mechanism rather than a copy of the value. Shadow boundaries break ID
    references, so labels and descriptions are inside the same root or passed as properties. Prefer
    extending nothing and styling a native element first.

## Mechanical checks

```
grep -rnE '<body[^>]*aria-hidden' src
grep -rnP 'role="(dialog|alertdialog)"(?![^>]*aria-(label|labelledby))' src
grep -rnE 'role="(tab|tabpanel|treeitem|menuitem|option)"' src
grep -rnE '<nav\b' src
grep -rnE 'type="file"' src
```

- For each `tab`, `treeitem`, `menuitem` and `option` hit, confirm the owning role exists in the same
  file.
- When several `nav` appear, each has a distinct label.
- The validity rules of points 2 to 6 are implemented by an accessibility engine run over the rendered
  page (axe-core's `aria-*` rules, for example); filter its report by rule identifier, read the nodes,
  and treat a clean report as the floor, not a verdict (§2.12).
- Keyboard maps and live announcements are checked by hand, with a keyboard and a screen reader.
