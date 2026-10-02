# flutter-conventions §14 — App variants, forced update and web input

> Section 14 of `skills/flutter-conventions`. Read it when a dev, staging or production variant is added or
> audited, when a minimum-version gate is built or triggered, or when a tappable element ships to the web or
> desktop. Store release mechanics (bundle, signing, tracks) are in `skills/mobile-release`.

1. **A variant is one application id, one display name and one remote configuration, declared once and
   derived everywhere.** Production keeps the bare identifier; the others get a suffix. The list of variants
   in the project file, the native build configurations (Android product flavours, iOS configuration files
   and schemes) and the entry points must agree; an audit compares those lists and any mismatch is a
   finding. Install side by side must work, so identifiers and display names differ per variant.
2. **Never run a generator that rewrites the main entry file or the native projects wholesale.** It destroys
   start-up logic silently. Apply targeted changes, keep the working tree clean before generating so the
   diff is reviewable, and never run a tool that prompts in a non-interactive shell without its force flag.
   Verify current tool versions before pinning (`skills/source-freshness`).
3. **Variants have separate remote projects.** The push, analytics and crash configuration of one variant is
   never shared with another; resolving the variant name falls back safely on the web, where there are no
   native flavours.
4. **A forced-update gate exists from the first release.** An app shipped without one cannot be forced to
   update later: there is no code in the field to read the threshold. It compares the installed version
   with a floor that is read remotely.
5. **The order of operations is the rule.** Publish the new version to the stores; wait until it is actually
   available (propagation across regions is not instant, the source course suggests about an hour); only then
   raise the remote floor. Raising it earlier locks users out with nothing to update to, which is worse than
   no gate. If the new version needs new backend behaviour, deploy the backend first, backward compatible.
6. **The floor is a minimum, not a window.** A single floor cannot express "below X blocked, at or above
   always fine, but the newest not yet required". If a version range is a real requirement, say so; do not
   approximate it with a floor.
7. **The remote source is chosen with the project.** A hosted file, the remote-config service already in
   use, or an endpoint of the project's backend: pick by what is already there and by rate limits. The
   in-code fallback value is never the value used in production, and a backend source needs the floor set per
   environment. A build distributed outside the stores needs an update destination other than the store
   page; do not point it at a listing that does not exist.
8. **Watch adoption before retiring anything.** After raising the floor, read the active-version breakdown
   from analytics or the crash reporter's release tags before removing the endpoint the old versions use;
   store download counts lag real usage.
9. **On web and desktop, a tappable element answers to pointer and keyboard.** A bare gesture detector gives
   no pointer cursor and no focus: wrap it in a mouse region for the click cursor, and make it focusable with
   a keyboard activation (Enter and Space) so it is operable without a mouse. Built-in buttons and tooltips
   already do this; the rule is for custom tappables.
