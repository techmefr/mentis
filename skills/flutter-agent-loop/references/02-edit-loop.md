# flutter-agent-loop §2 — The loop after an edit

Applies to the server and rule text read on 2026-10-08 (see §1 for versions).

## 2.1 Reload or restart after an edit under `lib/`
1. **After editing a `.dart` file under `lib/` while an app is running, connect and reload.** The Flutter
   agent-plugins hot-reload rule is explicit: discover running apps (§1), then reload.
2. **Hot reload** for widget code, including the `build` method of a stateful widget, and for simple
   methods.
3. **Hot restart** when the edit touched `main()`, state initialization such as `initState`, or global or
   static state. The server describes a restart as applying the latest code, including changes to global
   `const` values, while resetting the application state; a reload does not reset it. So if a change to
   initialization code seems to have no effect after a reload, restart before suspecting the code.
4. **Skip both** for an edit that only changes comments, docstrings or whitespace, and for any file outside
   `lib/` (tests, `integration_test`, `benchmark`, `test_driver`, `example`).
5. **Hot restart does not apply to a non-Flutter Dart program** (the tool's own description says so).
6. The server describes connecting and reloading as a safe operation to do without waiting to be asked.
   That is the vendor's claim about its own tool; in this repo it holds only while the app is a debug or
   profile build the user started for development.

## 2.2 Order of one iteration
Our own ordering, not a claim of the sources: analyze, then run the tests for the changed code, then
reload or restart, then read the runtime errors, then look at the widget tree if the screen is the point of
the change. A step that reports a problem ends the iteration there; the next one starts from that report.

## 2.3 Layout errors
1. **Capture the exact exception from the running app,** with the app in debug mode. The agent-plugins
   layout skill lists the usual signatures: a scrollable given unbounded height inside a column, a text
   field given unbounded width inside a row, a flex child overflowing, a parent-data widget outside the
   ancestor it needs, and the "not laid out" error.
2. **Fix the primary error, not the cascade.** The skill calls the "RenderBox was not laid out" message a
   side-effect and says to look further up the trace for the unbounded-constraint error that caused it.
3. **Reload and look again;** a layout fix that has not been seen in the running app is not verified. The
   layout rules themselves are in `flutter-conventions` §3, which governs where the skill's suggested wraps
   differ.

## 2.4 Fixes the tools can apply
Mechanical lint fixes go through the fix tool (dry run, review, apply, format, analyze; §1). A fix that
changes behavior is an edit like any other and takes the loop from §2.
