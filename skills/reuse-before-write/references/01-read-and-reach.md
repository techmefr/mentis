# reuse-before-write §1 — Read first, list the reach

> Section 1 of `skills/reuse-before-write`. Read it before the ladder. The ladder and the guards stay in §2 and §3.

1. **Read the task, then the code it touches.** Not the whole repository: the file you will edit, the
   functions it calls, and whoever calls it.
2. **List every place the change must reach before choosing how to write it.** Callers, tests, fixtures,
   seeds, config, exports, routes, translation files, generated types. The list is the scope. A change that
   renames a field in a Laravel model and misses the factory, the API resource and the seeder is not a small
   change, it is an unfinished one.
3. **Ask what the change could break for people who never see the diff.** Data it would destroy or expose, a
   caller that stops working, a payload a consumer still reads in the old shape. These are part of scope too.
4. **Extra features are not scope; completing the change is.** The two are easy to confuse once the list
   exists: a new option nobody asked for is out, the fixture your change breaks is in.
5. **Why this comes first.** The ladder asks "is it already here?". That question is only answerable by
   someone who has looked. Skipping the reading makes every later rung a guess, and a guess that lands on the
   shortest answer feels like skill.

## Worked failure

A ticket reads "add a date field to the booking form" in a Nuxt app. The author never opens the form
components folder and writes a calendar popup with month navigation, keyboard handling and a locale table.
The folder already held a `BaseInput` that forwards `type` to the native input, and every browser draws a date
picker for `type="date"`. Reading first turns the change into a few lines that use the house component the way
the neighbouring forms do; not reading it turned the change into a component nobody will maintain.
