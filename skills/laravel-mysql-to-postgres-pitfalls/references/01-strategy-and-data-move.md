# laravel-mysql-to-postgres-pitfalls §1 — Strategy and the data move

> Part 1 of `skills/laravel-mysql-to-postgres-pitfalls`. Read it when a move is planned, rehearsed or
> executed. Sourced from `skills/laravel-mysql-to-postgres/SKILL.md` in `majdghithan/agent-skills` (commit
> `538264f`), read 2026-10-16. Sentences marked "own guidance" are ours; every other claim is the source's and
> was not run by us.

1. **Run the migrations on an empty PostgreSQL database first.** Point the environment at a fresh, empty
   PostgreSQL database and run the full migration, with `migrate:fresh`. The source's reasoning: if every
   migration runs clean the schema is database-agnostic, and if one fails you have found a MySQL-only
   assumption before touching real data, and it says this one test surfaces about half the problems. Own
   guidance: put this run in CI as a separate job for the length of the project, so a MySQL-only migration is
   rejected when it is written.
2. **Keep MySQL running after the switch.** The source says not to delete MySQL the day you switch, and to keep
   it running for days or weeks until you are sure, because cutovers get reverted. Own guidance: keep the
   application able to read from it and write the rollback steps (which connection the application uses, who
   changes it) before the cutover, not during it.
3. **Pick the data-move tool by what it does with the schema.** The source gives two options. A loader tool
   built for this move (it names pgloader) reads MySQL and writes PostgreSQL in one command, converts types as it
   goes (a one-byte integer used as a boolean becomes a real boolean, auto-increment becomes a sequence) and
   usually resets sequences for you. The other is Laravel's query builder: read from the old connection,
   write to the new, transform rows in PHP; more control and more code, useful when the schema has corners
   the loader trips on, and it does not reset sequences. Own guidance: whichever is chosen, rehearse it against
   a copy of production and compare row counts per table afterwards.
4. **Reset every imported table's id sequence, and test it.** After a bulk import the table's sequence does not
   advance: with ids up to 40,000 in the data the sequence still starts again at 1, so the first insert after
   go-live collides on a duplicate key, in production and perhaps at checkout. The source says this passes
   tests and explodes in production, and gives the remedy as a SQL call that sets each sequence to at least the
   table's maximum id, using the function that finds a serial column's sequence by table and column name. The
   loader tool usually handles it; a query-builder import does not. Own guidance: after the import, create one
   record in each critical table through the application and confirm no duplicate-key error; and generate the
   reset statements from the catalogue so a table is not forgotten.
5. **Treat the move as an audit of the application.** The source's framing: MySQL is forgiving and PostgreSQL is
   strict, so every place you relied on the leniency is a defect waiting on the other side. Own guidance: list
   the places before the rehearsal: every use of a raw query call (point 3 in part 2), every user-typed search,
   every aggregate report.
