# § 2 — Models, Active Record and queries

> Section 2 of `skills/rails-conventions`. Read it when a model, an association, a validation, a callback or a
> query is written. The schema side (columns, indexes, constraints) is §3, so that a uniqueness validation and
> its index are read together. Pinned to Rails 7.1 to 8.x as read on 2026-10-02.

## Models

1. **Keep Active Record's defaults.** Table name, primary key and timestamps columns are what every Rails tool
   assumes; override them only for a database you do not own. When columns are retired in a rolling deploy,
   *append* to `ignored_columns` (`+=`), because an assignment silently drops what an earlier line or an
   engine already put there.
2. **Domain objects that are not tables are plain objects**, with `ActiveModel::Model` (and
   `ActiveModel::Attributes` for typed attributes) when they need validations or form integration. Introduce
   them freely: a model class does not have to be a table, and a fat model is often a table plus three objects
   that never had their own name.
3. **A model subclasses the application base class, not `ActiveRecord::Base`**, and so do jobs and mailers
   (`ApplicationRecord`, `ApplicationJob`, `ApplicationMailer`): the day behaviour is shared, there is one
   place to put it. Migrations that define a throwaway model are the exception, to stay independent of
   application code (§3.9).
4. **Enums use the hash form with explicit values.** An array form stores the position, so inserting or
   reordering a value in the middle changes the meaning of every stored row.
5. **Prefer `has_many :through` to `has_and_belongs_to_many`.** The join table grows attributes and rules the
   day someone asks when a membership started, and a join without a model cannot hold them.
6. **Give `has_many` and `has_one` an explicit `dependent:`** (destroy, delete_all, nullify, restrict) so that
   deleting a parent is a decision written down. Where Active Record cannot work out the inverse of an
   association because of a scope or an option, state `inverse_of:` yourself or set it to `false`; otherwise
   `blog.posts.first.blog` loads the blog a second time.
7. **Group the macros at the top in one order** (constants, attribute macros, enums, associations, validations,
   callbacks) so that the shape of a model can be read without scrolling. Order callback declarations in the
   order they run.
8. **Validations: the current syntax, one attribute per line, one concern per validator.** `validates :email,
   presence: true, length: { maximum: 100 }`, not `validates_presence_of`. A validation that lists several
   attributes is read as one rule and edited as five. A custom validation method is named for the rule it
   states (`expiration_date_cannot_be_in_the_past`), not as a predicate. A validator reused more than once, or
   a pattern, becomes an `EachValidator` under `app/validators`.
9. **A validation does not replace a constraint.** A uniqueness validation needs a unique index (§3.7): the
   validation is a `SELECT` and a later `INSERT`, two requests pass the first before either performs the
   second. Presence of a foreign key needs the foreign key. Application checks are for good error messages;
   the database is for invariants.
10. **Anchors in a format regex are `\A` and `\z`, never `^` and `$`.** In Ruby the latter match line boundaries,
    so a value with a harmless line followed by a payload passes a URL or an email check.
11. **A bang method, or a checked return.** `save!`, `create!`, `update!`, `destroy!` raise on failure; the
    plain forms return `false` and a caller that ignores it carries on with a record that was never saved.
    This includes `first_or_create` and `find_or_create_by`.
12. **Know which methods skip validations and callbacks:** `update_attribute`, `update_column(s)`,
    `update_all`, `touch`, `toggle`, `increment!`/`decrement!` and the counter-cache class methods. They have
    uses (a counter, a heartbeat column); each use is a deliberate exception, never the default way to write a
    value.
13. **Callbacks are for the record's own consistency, not for orchestration.** Do not override `save` or
    `destroy` to run side effects; use callbacks, and keep cross-object workflows in an object that the
    controller or job calls. One `after_commit` per callback name per model (a second declaration with the
    same method name replaces the first, silently). A `before_destroy` that can veto must be declared with
    `prepend: true`, because `dependent: :destroy` callbacks are created at the association and would
    otherwise run first and delete the children of a record that then refuses to be deleted. Anything that
    must happen only if the transaction commits belongs in `after_commit` (§4.8).
14. **A transaction is left by an exception or by falling off the end.** In Rails 7 and later, `return`,
    `break` and `throw` inside a `transaction` block roll it back; use `next` to commit and raise to roll back,
    so the intent is in the code.
15. **Scopes and `default_scope`.** Named scopes are cheap and chain; when a scope with parameters gets
    complicated, write a class method that returns a relation. Avoid `default_scope`: it changes every query
    on the model, including the ones that expected to see all the rows, and cannot be seen at the call site.

## Queries

16. **Never interpolate into SQL.** Pass values as placeholders (`where("orders_count = ?", n)`), as named
   placeholders when there are several, or as a hash (`where(orders_count: n)`). For `order`, pass symbols or hashes
   (`order(created_at: :desc)`); a string column name without its table breaks as soon as a join introduces
   a second column of that name.
17. **Choose the finder by what absence means.** `find(id)` raises `RecordNotFound` (the framework answers 404);
   `find_by(...)` returns `nil` and means "maybe". Do not use `where(...).take`, dynamic `find_by_name`
   finders or `find_by!(id:)`. Do not memoize a `find_by` with `||=`: a `nil` is recomputed on every call.
18. **Order chronologically by a timestamp, not by `id`.** Id order is usually chronological by accident, not
   by contract.
19. **Ask for what you need.** `pluck` for values from many rows (`ids` for the primary key), `pick` for one value
   of one record, `exists?` for a boolean, `where.missing(:association)` (Rails 6.1+) for rows with no related
   row; not `map(&:name)` over instantiated objects, and not `pluck` inside a `where` (use a subquery:
   `select`, to let the database do it in one statement). `size` picks `count` or `length` according to whether
   the collection is loaded; `count` always queries, `length` always loads.
20. **Ranges for comparisons.** `where(created_at: 30.days.ago..7.days.ago)`, endless and beginless ranges for
   one-sided bounds, rather than SQL fragments with two placeholders.
21. **`where.not` takes one condition.** With several attributes its meaning changed in Rails 6.1 (it now excludes
   rows matching either), so a query written before and after the upgrade disagree; write the negation out.
22. **No `all` as a receiver** (`User.all.order(...)`): it adds nothing. The exception is an association
   receiver, where `delete`, `destroy` and their `_all` forms behave differently with and without it: read the
   documentation before removing it there.
23. **Batches for big sets.** `find_each` (or `in_batches`) for any loop over more than a screenful of rows;
   `all.each` instantiates the whole table. Deleting or updating in bulk goes through batches with a pause, not
   a single statement that locks the table (§3.10).
24. **Raw SQL in a squished heredoc** (`<<~SQL.squish`), parameterised, so the log shows one readable line and
   the editor highlights it.

## N+1

25. **A relation read inside a loop is a query per row.** Ten books and their authors is eleven queries. Load
   the association first: `preload` (one query per association, no conditions on it), `eager_load` (one query
   with a `LEFT OUTER JOIN`, needed when the filter is on the association), or `includes` which picks one of
   the two. Declare it where the loop's data is loaded, not in a global scope that forces the load on every
   query of the model (`laravel-no-queries-in-loops` states the same rule for another framework).
26. **Make lazy loading fail where it should not happen.** `strict_loading` on a relation (or
   `strict_loading_by_default` for the application, with `:log` as the action while an existing codebase is
   cleaned up) raises `StrictLoadingViolationError` on any lazy load; run the test suite with it on, and the N+1
   becomes a failing test instead of a slow page.
27. **Count and exist in the database.** `size`, `exists?`, `sum` and `group` with counts run as SQL;
   `records.select { ... }.count` loads everything first.
