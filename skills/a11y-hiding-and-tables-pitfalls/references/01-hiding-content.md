# a11y-hiding-and-tables-pitfalls §1 — Hiding content

> Section 1 of `skills/a11y-hiding-and-tables-pitfalls`. Read it when something is hidden or a hidden-text class
> is used. Restated from the A11y Project post `src/posts/how-to-hide-content.md` (repository commit `27de226`,
> Apache-2.0 repository licence, no separate content licence stated), read 2026-10-16. Browser support notes in
> the post (old Internet Explorer versions) are dropped. Sentences marked "own guidance" are ours.

1. **Do not use `display: none` for content a screen reader user is meant to find.** The post says the common
   habit is problematic for screen reader users, above all when the hidden content was meant for them to
   discover. A search field whose label is replaced by a magnifying-glass icon is its example of text that should
   be hidden visually only.
2. **Hide visually with the clip pattern.** The post's class sets a zero clip rectangle, an inset clip path of
   50 percent, a height and width of 1 pixel, hidden overflow, absolute positioning and no wrapping of the
   text. It says that, unlike positioning off-screen or a negative text indent, this works on right-to-left pages,
   and it links an article on squashed off-screen text for the reason one added line is in the snippet. Own
   guidance: keep one shared class for the whole code base and give it a name that says what it does.
3. **A hidden element that can take focus must appear when it does.** If the class is on a link, button or input
   or another natively focusable element, a sighted keyboard user would otherwise have no visible focus and
   cannot see where they are. The post's selector applies the hiding declarations only when the element is not
   focused and not active, so that focus undoes the hiding. Own guidance: this is the pattern behind a skip
   link that appears on the first Tab press; the check is to press Tab and look.
4. **Frameworks ship the class under another name.** The post notes that popular CSS frameworks provide a
   visually hidden or screen-reader-only class, the second abbreviating screen reader. Own guidance: use the
   framework's before writing one, and read whether it also reveals on focus, because the post's rule in
   point 1.3 is about the class, not the name.
5. **`aria-hidden="true"` is the opposite: hidden from assistive technology, still visible.** The post's use is
   decorative icons that sit beside a text label and need no announcement. Nothing about it hides the element
   from sighted users. `skills/accessibility` carries the rule against putting it on anything focusable.
6. **To hide from everyone, use the `hidden` attribute, or `display: none` keyed on `aria-hidden`.** The post
   says the HTML `hidden` attribute hides content both visually and from assistive technology, and suggests a
   global rule that makes the attribute set `display: none` as important so a component's own display value
   cannot override it. It also shows a selector that adds `display: none` to a component whose `aria-hidden` is
   true, instead of toggling a second class.
7. **Choose by audience.**

   | Who should still get the content | Mechanism |
   |---|---|
   | Screen reader users, not sighted users | the visually hidden class (reveal on focus if focusable) |
   | Sighted users, not assistive technology | `aria-hidden="true"` |
   | Nobody | the `hidden` attribute, or `display: none` |

   Own guidance: write the audience in the review comment, because the three look the same in a screenshot of
   the code and different in a screen reader.
