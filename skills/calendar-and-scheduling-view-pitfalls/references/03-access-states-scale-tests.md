# calendar-and-scheduling-view-pitfalls §3 — Accessibility, states, scale and tests

Sources: own craft, plus the W3C ARIA Authoring Practices date-picker dialog example (page read 2026-10-20, facts only, own words, credited) where marked; other grid points are public practice, recalled and not re-read.

## 3.1 Accessibility
1. **Symptom: a calendar nobody can use with a keyboard or a screen reader.** A grid of positioned boxes has no structure and no operations (`accessibility` §1, §2).
2. **Give the view real structure:** a heading with the visible range, previous, next and today as buttons with names ("Previous week"), a view switcher that exposes the selected view, and a table or grid for the days.
3. **Name each event** with title, date and time range, all-day status, zone when different, and recurrence ("Planning, Monday 3 March, 9:00 to 10:00, repeats weekly"), through its text or accessible name, not colour or position.
4. **Keyboard navigation in a date grid:** arrow keys move by day and week, Home and End to the row ends, Page Up and Page Down to the previous and next period, Enter opens the day or event. Roving focus, one tab stop for the grid. The W3C date-picker example (read 2026-10-20) confirms this shape and adds details: left and right move one day, up and down the same weekday in the adjacent week, Home and End the first and last day of the week, Page Up and Page Down the previous and next month on the same day number (the last day of the month when it does not exist), with Shift they move by year; Enter or Space selects and Escape closes, both returning focus to the opening button. Only one cell is in the tab sequence, the script moves it. The month heading is a polite live region so a month change is announced, and the grid is a table with the grid role named by that heading, with the full day name on abbreviated column headers. For an event grid Enter opens the event instead of selecting, which is our adaptation.
5. **A list alternative:** an agenda view of the same data is the most usable form for screen reader and magnifier users. Offer it as a peer view, not a hidden fallback.
6. **Every drag has a keyboard route:** an "Edit time" dialog or a move command with date and time fields, and the same server rules (`kanban-board-ui-pitfalls` §2.1 for the pattern). Announce the result in a polite live region.
7. **Do not rely on colour for category, busy or today;** pair it with text, an icon or a pattern, at sufficient contrast in light and dark themes (`accessibility` §3).
8. **A date picker is a separate widget** with its own rules: label the field, accept typed dates in the locale's format, and keep the grid as help, not the only input (`international-input-pitfalls` §3).
9. **Respect reduced motion:** period changes cut instead of sliding (`accessibility` §7).
10. **Zoom and small screens:** at narrow widths switch to an agenda or day view rather than shrinking a seven-column grid until it is unreadable.
11. **Colour-blind and low-vision checks cover the "now" line, selected cell and conflict marks.**

## 3.2 States
1. **Render each distinctly:** first load, empty range ("Nothing scheduled", with an add action), refreshing (events stay), failed load (error and retry), partial failure (one calendar source failed, others shown with a notice), failed save, conflict, busy slot, read-only, and offline.
2. **Symptom: an empty week shown while the request failed.** Same rule as tables (`data-table-ui-pitfalls` §2.1).
3. **Multiple calendars can be toggled;** the toggle state is saved per user and the legend says what is hidden.
4. **The "now" marker updates and does not steal focus;** it moves with time and respects the viewer's zone.
5. **A timeout for a held slot is visible as text** and announced when it ends (§2.5).

## 3.3 Load by range and scale
1. **Load events by the visible range plus a margin,** and cancel or ignore responses for a range the user left. Key the request by range and filters (`data-fetching-state-conventions`).
2. **Symptom: the month view is slow with hundreds of events per day.** Cause: every event is a mounted element. Show a count and a "+n more" control in dense cells (§2.4) and mount the detail only on open.
3. **Day grids render only the visible hours** when scrolled, with the working hours as the initial scroll position.
4. **Cache by range and invalidate on edit,** including the ranges a recurring edit touches.
5. **A week of events for many resources** (a room or staff timeline) needs the resource list paged or virtualized; keep the time axis fixed while resources scroll.
6. **Subscribe to changes for the visible range only** and patch events; do not refetch the whole range on every message.

## 3.4 Tests
1. **Fix the clock and the zone in tests.** Tests that read the machine's zone pass on one laptop and fail in CI; set the zone explicitly in the test setup.
2. **Zone matrix:** an event read in a zone ahead of UTC, behind UTC and with a half-hour offset; the displayed day and time are correct.
3. **Clock-change cases:** a series crossing the spring gap and the autumn repeat; a day with 23 and 25 hours; "plus one day" against "plus 24 hours".
4. **All-day tests:** an all-day event displays on one date in every zone; the exclusive end round-trips through the form.
5. **Recurrence tests:** weekly and monthly rules, "the 31st", an exception, an excluded date, "this and following", a hard cap.
6. **Drag tests:** snapping, resize, a drop across midnight, cancel with Escape, the keyboard equivalent giving the same result.
7. **Server conflict test:** two parallel bookings of one resource; back-to-back events allowed.
8. **Accessibility tests:** an automated check on the rendered grid, keyboard-only completion of create, move and delete, and a manual screen reader pass on the event names.
9. **Range query test:** an event spanning the range edge is returned.

## 3.5 Framework pointers
1. **Calendar components** for React, Vue and others (FullCalendar, Schedule-X, Toast UI Calendar and similar) cover grids, drag and recurrence expansion to different degrees; check how each stores time zones, whether all-day end dates are exclusive, and what keyboard support it ships. Read its documentation for the version in use; none was verified here.
2. **Date libraries and the platform:** prefer the platform's zone-aware date types where available and a maintained zone-aware library otherwise; plain `Date` objects carry only an instant and the machine zone.
3. **Recurrence libraries** that implement the iCalendar rule format exist for most stacks; use one on the server for expansion (§2.1) rather than writing rules by hand.
4. **Laravel and Carbon:** store UTC, keep the zone in its own column for wall-clock events, and expand series in a service (`laravel-date-via-localised-accessors`).
5. **Vuetify** offers a calendar component and a date picker; apply §1 and §3.1 on top, since neither answers zone semantics.

## Checks
- A keyboard-only user can create, move and delete an event and hear the result.
- Every state in §3.2 has a test or a fixture.
- The agenda view returns the same events as the grid for the same range.
