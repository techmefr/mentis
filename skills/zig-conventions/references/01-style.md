# zig-conventions §1 — Names, layout, doc comments

> Section 1 of `skills/zig-conventions`. Read it when a declaration is named, a file is created or a doc
> comment is written. The guardrails stay in `SKILL.md`.

1. **Do not put words that apply to every type in a type name:** value, data, context, manager, or utility
   buckets and people's initials. Everything is a value and every type is data, so the word says nothing; a
   utility bucket is a failure to categorise, and its members belong at the root of the module that needs
   them.
2. **Choose a name from its fully qualified namespace.** The file and the enclosing struct are already part of
   the path, so do not repeat a segment (a JSON value in a `json` namespace is just `Value`). The exception is
   a name that has been reduced to its core and cannot be more specific without being wrong.
3. **Layout:** four spaces of indentation; opening brace on the same line unless wrapping; a list of more
   than two items goes one per line with a trailing comma; line length around 100, with common sense. The
   formatter implements these.
4. **Case by what the thing is.**
   - A struct with no fields never instantiated (a namespace): snake case.
   - A type or a type alias: title case.
   - A callable that returns a type: title case.
   - Any other callable: camel case.
   - Everything else (variables, constants, fields, parameters): snake case.
5. **Words with written-English capitalisation rules follow the naming rules like any other word,** even
   two-letter acronyms: `xml_document`, `XmlParser`, `readU32Be`.
6. **File names:** a file with top-level fields is a struct and is named like one in title case; otherwise
   snake case. Directories are snake case.
7. **Established conventions win** over these rules (a constant name copied from the system, for example).
8. **Doc comments:** omit what the name already says; repeating information on several similar functions is
   encouraged, since tools show one function's help at a time; use the word "assume" for an invariant whose
   violation is unchecked illegal behaviour, and "assert" for one whose violation is checked by the safety
   mechanism.
9. **Source encoding:** UTF-8, LF line endings (a CR before it is discouraged), no hard tabs, and a final
   newline; control characters and the non-ASCII line separators are rejected.
