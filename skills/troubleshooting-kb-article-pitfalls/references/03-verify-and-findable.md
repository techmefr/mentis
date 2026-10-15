# troubleshooting-kb-article-pitfalls §3 — Verify and make it findable

A confident, wrong fix costs more trust than an admitted gap. And readers paste the error string; nobody
browses a troubleshooting section for pleasure.

## 3.1 Verify before publishing
1. **Reproduce the failure, run the fix exactly as written from the reader's starting state, and capture the
   signal after the fix.**
2. **Check the oldest supported version and the current one.**
3. **Have someone who did not write the entry follow it cold.**
4. **An entry that could not be reproduced ships only with an explicit note**: reported under these
   conditions, not reproduced here.
5. **Then search your own docs for the error string as a reader would** and confirm the entry is the first
   result, with the string in its title.

## 3.2 Findable by the string
1. **Put the error string verbatim in the title, in the first heading and in the body.**
2. **Answer on the first screen**: message, cause and first fix, before any feature preamble.
3. **Repeat the string on every entry that shares it** instead of sending the reader to a common section. The
   match matters more than the duplication.
4. **Link the entry from where the failure happens**, and from the product when you can, for example a
   documentation address in the error output.

## 3.3 Stable anchors
1. **One addressable target per error**: its own page, or one stable anchor on a codes page.
2. **Never rename an identifier or its address.** Renaming invalidates every link and every saved answer
   pointing at it.

## 3.4 Examples carry no customer data
1. **Strip credentials and customer identifiers from every example.** A page that shows a whole token teaches
   readers to paste theirs into public issues.
2. **Keep the environment facts that decide whether the entry applies**, such as version and platform.
3. **Use documentation addresses and placeholders**: 192.0.2.10, `TOKEN_PLACEHOLDER`, `user@example.com` (our
   examples).

