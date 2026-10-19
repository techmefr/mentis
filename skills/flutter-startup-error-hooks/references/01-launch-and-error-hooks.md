# flutter-startup-error-hooks §1 — Launch order and error hooks

Documentation read on 2026-10-08: the Flutter page on handling errors and the Flutter API reference for
`PlatformDispatcher.onError`, `SchedulerBinding.addPostFrameCallback` and `AppLifecycleState`. Where the rule
comes from an agent-skill repository instead, the point says so and a second source is named when one was
read.

## 1.1 Order
1. **Initialise the binding, then install both error hooks, then do anything that can throw.** The step most
   likely to throw on a cold start is opening storage; a hook installed after it is blind to its failure.
   (The ordering comes from a startup skill in an MIT-licensed repository; the two hooks and their scopes are
   from the Flutter error-handling page.)
2. **The framework hook and the platform-dispatcher hook cover different errors.** The framework hook receives
   every error Flutter catches during callbacks such as build, layout and paint. The platform-dispatcher hook
   receives errors raised with no Flutter callback on the stack, such as in async code or plugin calls
   (Flutter error-handling page). One of them alone leaves a class of errors with only the default handling.

## 1.2 What each hook does and returns
1. **The framework hook should still call the framework's presentation function,** so the error stays visible
   in the console while it is also recorded (the Flutter page recommends this).
2. **The platform-dispatcher hook returns `true` when it has handled the error.** The API reference states
   the callback must return `true` if it handled the error and `false` otherwise, and that `false` makes the
   engine fall back to another mechanism such as printing to the standard error stream. Our inference, not a
   documented sentence: an error that was recorded and then reported as unhandled is reported twice, once by
   you and once by the fallback, so a hook that has recorded the error returns `true`. The same page notes the callback is not
   invoked for failures that end the VM or process before it can run.

## 1.3 A hook never throws
An error thrown inside either hook is an error in the machinery meant to report errors. Keep the hook's
body to recording the error (a synchronous, size-bounded write that cannot itself fail is the goal) and
guard the recording call so a failure inside it cannot escape. This rule is from the startup skill
mentioned in 1.1; the Flutter documentation does not state it, so it is also listed in `origin.md` as own
guidance.

## 1.4 Zones
With both hooks installed, no zone wrapper is needed to catch the errors the hooks already cover; the Flutter
error-handling page does not mention zones at all in its current text. Two agent-skill repositories disagree
about crash SDKs: one says never to add a zone, the other wraps its run function in one when initialising a
specific crash reporter. Follow the **current setup guide of the crash SDK actually used**, which was not
read here, and add a zone only when that guide asks for one.

## 1.5 The first frame and warm-up
1. **Read what the first frame needs before running the app,** such as the theme, locale and text-scale
   policy, so the first frame is already right; a theme that flips after the first frame is visible. The read
   must be small enough to await.
2. **The only awaited work on the launch path is what the first frame cannot be drawn without.** Everything
   else is deferred.
3. **Run plugin and engine warm-up after the first frame, not awaited in `main`.** A post-frame callback
   registered with the scheduler runs once, just after a frame, cannot be unregistered, and does not itself
   request a frame (API reference). Register it from the root widget and do not wait for its result.
4. **A failed warm-up and the real operation it warms have opposite failure policies:** the warm-up may fail
   quietly and cost latency on first use, the real operation fails loudly. Do not merge the two.

## 1.6 Flushing on the way to the background
1. **Register one lifecycle observer at the root and flush durable state when the app becomes inactive or
   paused,** and re-read time-sensitive state on resume. Add and remove it as `flutter-conventions` §1
   requires (`initState` and `dispose`).
2. **The flush is a best effort, never the only write.** The `AppLifecycleState` reference says the app
   should not count on receiving every notification: when the OS ends the process abruptly no notification is
   sent and some states are skipped. Anything that must survive is written when it changes; the flush only
   narrows the window.
3. **Features expose a flush on their own repository or notifier,** and the root observer calls it, rather
   than each widget implementing the lifecycle callback (own guidance, from the same startup skill).

## 1.7 Logging the cause
A state library that rethrows a failed provider's error wrapped in another exception type produces reports
that all read as the wrapper (Riverpod documents `ProviderException` as the type a dependent provider throws
when the provider it watches failed). Unwrap to the underlying cause before recording it.
