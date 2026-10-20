# rich-text-editor-pitfalls §1 — Format, sanitising and paste

Sources: Lexical documentation on serialisation (MIT, commit stamped in origin.md, read 2026-10-20) for the facts marked as such; the rest is own craft.

## 1.1 Choosing the storage format
1. **Three families, three trades.** Stored HTML is easy to render and index but mixes content with presentation and must be sanitised every time. A structured document tree (JSON) round-trips the editor exactly and can be validated against a schema, but needs the editor or a renderer to display. Markdown is human-diffable and portable, but cannot express everything an editor offers (colours, tables with merged cells, mentions) without extensions.
2. **Pick by what must survive.** Content shown in a browser by your own app and edited only by the same editor: the editor's tree. Content sent by mail, exported or consumed by other systems: HTML or Markdown as a derived output. Content edited by developers too: Markdown.
3. **The library documentation draws the same line**: its JSON records the whole node tree so a document restores exactly as it was, while its HTML and Markdown outputs are conversions that need a DOM or a transformer and can lose structure.
4. **Keep one stored source of truth and derive the rest.** Symptom: the HTML column and the JSON column disagree after an edit. Store the tree, generate HTML for mail and search on write or on demand, never edit the derived copy.
5. **Version the format.** Store a schema version next to the content and write a migration for each editor upgrade that changes node shapes. Symptom: old documents render blank after a library update.
6. **Unknown nodes must degrade, not crash.** When a node type is removed, render its text or a placeholder and keep the rest.
7. **Store a plain-text projection** for search, previews, notification text and length limits, generated from the tree rather than by stripping tags with a pattern (`search-index-sync-pitfalls`).

## 1.2 Where HTML is dangerous
1. **Stored markup is rendered to other people**, often privileged ones: an administrator opens a ticket another user wrote. A script, an event attribute or a `javascript:` link in it runs with the reader's rights.
2. **The editor's output is not a security boundary.** An attacker posts to the API directly and skips the editor entirely. Only the server, and the render point, can enforce.
3. **Markup arrives by other doors too**: imports, an email-to-ticket gateway, a webhook, a migration from another tool, an API client. Each must pass the same sanitiser.

## 1.3 Sanitise on write and on render
1. **Use an allow-list of tags, attributes and URL schemes**, small enough to read in one screen. Everything else is dropped, not escaped into view.
2. **Sanitise at render as well as at write.** The allow-list changes, libraries get fixed, and rows written years ago pass through the new rules at the render point. Cost: cache the sanitised output keyed by content hash and list version.
3. **Sanitise last, and ship what came out.** Do not concatenate, re-parse or post-process the sanitised string (`csp-and-sanitiser-pitfalls` §2).
4. **Server and client must apply the same list.** Symptom: preview looks fine, saved page strips the table. One shared configuration, or the client preview renders the server's result.
5. **Links: allow `http`, `https`, `mailto`, `tel` only**, add `rel` for external targets, and never allow script or data URLs. Open in a new tab only on purpose.
6. **Images: allow only URLs from your own storage or an allow-listed host**, require alternative text, and never let a stored URL make the reader's browser call an arbitrary host (tracking and mixed content). Upload handling is its own block.
7. **Styles: drop inline style attributes and classes** and map allowed formatting (bold, list, heading) to your own markup; colour and size belong to the design system, not the document.
8. **Embeds (video, frames) go through an explicit allow-list of providers** and a sandboxed frame, or are not offered.
9. **Add a content security policy as the second layer**, not the first (`csp-and-sanitiser-pitfalls` §1).
10. **Test with real hostile samples** (attribute handlers, nested tags, malformed markup, encoded schemes), from a maintained list, not invented once.

## 1.4 Output encoding is still needed
1. **A rich field is not an excuse for unescaped plain fields.** Titles, mentions' display names and link text from the same editor are escaped as text unless they pass through the sanitiser.
2. **Plain-text channels get the projection from §1.1**, not a tag strip: mail subject, push body, notification preview.
3. **Do not render stored HTML inside another sanitiser-free context** (a PDF generator, a mail template) without passing it through the allow-list again.

## 1.5 Paste
1. **Paste is an import**, and the common sources are word processors and web pages, which carry fonts, colours, nested spans, layout tables and hidden metadata. Symptom: a pasted paragraph shows a different font and cannot be restyled.
2. **Run pasted content through the editor's schema.** The library documentation describes its clipboard order: its own JSON when present, then HTML, then plain text. Anything the schema does not know is dropped or turned into text.
3. **Offer paste as plain text** (a shortcut and a menu entry) and make it the default in fields where formatting is not wanted (names, subjects).
4. **Convert, do not copy, structure that matters**: headings, lists, links, simple tables. Drop everything else including comments, hidden elements and tracking attributes.
5. **Pasted images** arrive as embedded data or temporary URLs. Upload them through your normal path with limits, or reject them with a message; never store a data URL in the document.
6. **Preserve line breaks and spaces on plain paste**, converting lines to paragraphs by a defined rule.
7. **Size-limit the paste** (characters and nodes) so a megabyte of markup does not freeze the editor, and report the truncation.
8. **Markdown shortcuts and autolinking are input, not paste**: decide whether typing `# ` makes a heading and whether a pasted URL becomes a link, and test the undo of each.

## 1.6 Limits
1. **Count characters on the plain-text projection**, not on markup, and say the unit. Symptom: "500 characters" rejects a short note full of formatting.
2. **Limit the stored size, node count and nesting depth** on the server. A deeply nested list is a cheap denial of service for the renderer.
3. **Show remaining characters accessibly** (§2.4) and keep the typed content on a validation failure.
4. **Empty is not equal to an empty string.** A document with one empty paragraph is empty; compare against the projection, not against the markup.

## 1.7 Links and anchors
1. **Check link targets when saving user-entered URLs** (scheme allow-list, whitespace, accidental `www.` without scheme) and show the destination in the editor's link control.
2. **Internal links store ids, not URLs**, like notification targets (`in-app-notifications-pitfalls` §1.5), so a rename or domain change does not break the content.
3. **Heading anchors are generated stably** or not at all; a regenerated slug breaks inbound links.
