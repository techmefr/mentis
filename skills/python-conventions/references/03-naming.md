# python-conventions §3 — Naming

> Section 3 of `skills/python-conventions`. Read it when a symbol, a domain value or a constant has to be named. The other sections and the guardrails stay in `SKILL.md`.

1. A name reveals **intent** — what the value represents or what it's for. `tmp`, `data`, `result`, `arr`,
   `item`, `value`, `x` push the meaning into the reader's head; `column_value`, `user_to_import`,
   `pending_applications` state it.
2. **Placeholders survive because the first draft only has one thing in scope.** `data` is fine until a
   second `data` is unpacked next to it, or a comprehension nests inside another, and then the body is a
   puzzle about which one is meant. That is also why renaming at the point of unpacking is worth doing when
   a library hands back a generic name.
3. **A name describes the value, not its type or where it came from.** `user_list`, `config_dict` and
   `name_str` restate what the annotation already says and go stale when it changes; `users_from_api` and
   `cached_rows` name an implementation detail, so moving the fetch or dropping the cache leaves a name that
   actively misleads.
4. **Singular for one, plural for many.** `user = fetch_users()` is among the cheapest mistakes to make and
   the easiest to read past, because it looks correct locally and only breaks where the value is consumed.
5. **A function name starts with a verb; a variable does not.** `amount()` reads as a value at the call site
   and `format_amount()` reads as work; a predicate reads as a question (`is_expired`, `has_access`,
   `can_publish`), and phrased positively, since `is_not_ready` and `disable_save` are always read inside a
   negation.
6. **A leading underscore is a contract, not decoration.** It says the name is not part of this module's
   surface, which is what makes §8.8's rule enforceable: a test reaching for an underscore-prefixed path has
   crossed a line the author drew, and it breaks on any refactor while proving nothing.
7. **No magic strings or numbers with domain meaning.** A domain value (status, type, kind, mode) becomes an
   `Enum`/`StrEnum` and is typed as that enum on the model; a threshold or limit becomes a named constant.
   A literal `"pending"` compared in three files is three chances to typo it — and a typo there is not an
   error, it is a comparison that quietly returns false, so the row is simply never picked up.
8. **An enum crossing a boundary publishes its values.** Stored in a column, sent in a payload or put on a
   queue, the member's *value* is the contract, so renaming it is a migration of existing rows and in-flight
   messages rather than a refactor. Worth knowing while choosing the name, which is the only moment it is
   free.
9. **`StrEnum` is a convenience with a cost**: its members compare equal to plain strings, so it accepts the
   magic string this rule exists to remove and a typo passes the comparison again. Where the point is to
   make the wrong value impossible, the plain `Enum` is the one that does it.
10. **A status field whose values move through named transitions is a state machine, not a column.** Two
    signals together are enough — more than one function branching on the status, and at least one
    transition that must be refused — and the answer is `skills/design-patterns` §4 plus
    `skills/domain-modeling`, read before the first transition function exists. Named here because the task
    never arrives in pattern vocabulary: it arrives as "add a publish action" or "it should go back to
    draft".
11. **Two enums that share four values today are still two enums.** Order statuses and invoice statuses look
    alike until one grows `refunded` and the other `returned`; then the shared type admits states each
    consumer must defensively ignore, and adding a value re-tests every consumer of the other domain
    (`code-baseline` §5).
12. **A generic name shared across domains cannot be read locally.** A module-level `Status`, `Type`, `Kind`
    or `State` forces the reader to know which domain they are in before the name means anything, and the
    import list is where they have to go to find out.
13. **A module name is part of every import that uses it.** A name that shadows a standard-library or
    third-party module — `types.py`, `logging.py`, `json.py` next to code that imports the real one —
    produces an import that resolves to the wrong file depending on how the process was started, which is a
    long way from where it will be diagnosed.
14. **A constant is only constant by convention.** Upper case says "do not reassign" and nothing enforces
    it, so a mutable value declared as a constant — a list, a dict, a set of defaults — is shared state that
    every importer can edit. Make it immutable (a tuple, a frozen mapping) rather than trusting the case.
15. **The name and the docstring say different things or one of them is wrong.** Where a function needs a
    docstring to explain what its name should have said, the rename is the fix — the same reasoning as
    `code-baseline` §1.4, arriving through the one comment form this repo does allow.
