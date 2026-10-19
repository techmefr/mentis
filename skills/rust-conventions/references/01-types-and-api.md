# rust-conventions §1 — Types and public API design

> Section 1 of `skills/rust-conventions`. Read it when a type, a constructor, a function signature, a trait, a
> name or a public re-export is written. Errors are §2, wrappers and statics in signatures are §4. The other
> sections and the guardrails stay in `SKILL.md`.

1. **A value that carries a meaning gets its own type.** A distance in miles and a distance in kilometres are
   both a float; a function that takes either will be called with the wrong one. A newtype makes the compiler
   tell them apart at no runtime cost. The same holds for identifiers (a user id is not an order id), for
   units, and for "a validated string".
2. **A newtype that exists for an invariant enforces it.** Wrapping a `u8` and calling it `Month` while
   leaving the field public and the constructor infallible only moves the check to every caller. The
   constructor that can fail returns a `Result`; a panicking convenience constructor may sit beside it, and
   should be `const` where possible. Once the type exists, the rest of the code may rely on the invariant and
   stop re-checking.
3. **An argument that is a bare `bool` or `Option` at a call site says nothing.** `render(true, false)` has
   to be looked up. Prefer an enum with named variants, or a small struct, so the call reads as the intent.
   A set of independent on/off flags is a bit-flag type, not an enum with hand-picked discriminants.
4. **Pick the strongest standard type for the job, as early as the API allows.** Anything that talks to the
   operating system about a location is a path type, not a string; a count that cannot be zero says so in its
   type. Plain numbers stay plain at a public boundary where the standard library itself uses them (a window
   size is a `usize`, not a wrapper), so do not wrap a number just to look careful.
5. **Fields of a public struct are private unless the struct is passive data.** A public field freezes the
   representation and forbids any invariant on it. Use accessors; keep public fields for plain record-like
   types whose whole point is to be filled in and read.
6. **Constructors are plain associated functions named `new`, or `with_<detail>` for a variant, or
   `from_<other>` for a conversion.** If the basic constructor can take no argument, offer both `new()` and
   `Default`: users look for `new` first. A type that needs four or more independent optional inputs gets a
   builder instead of a ladder of `with_*` constructors; setters on the builder never fail, and the final
   `build()` returns a `Result` so that checks between fields happen once, in one place.
7. **Conversions are named by cost and by ownership.** `as_` is free and borrows to a borrow, `to_` does work
   (a copy, an allocation, a check) and keeps the original, `into_` consumes the value. A wrapper around one
   value exposes it with `into_inner`. A conversion lives on the more specific of the two types. Implement the
   standard `From`, `TryFrom`, `AsRef` and `AsMut`; never implement `Into` or `TryInto` yourself, since they
   come for free from the first two.
8. **Getters have no `get_` prefix.** `first()` and `first_mut()`, not `get_first()`. `get` is kept for the
   single obvious "look it up" case of a container. A checked getter that returns an `Option` may be paired
   with an `unsafe` `_unchecked` variant.
9. **Iteration follows the standard names.** A collection offers `iter`, `iter_mut` and `into_iter`, and the
   iterator types are named after the method that returns them (`Iter`, `IterMut`, `IntoIter`).
   A collection implements `FromIterator` and `Extend` so that `collect`, `unzip` and `extend` work on it.
10. **Eagerly implement the common traits.** A downstream crate cannot add a trait to your type (the orphan
    rule), so leave out only what does not apply: `Debug` always, `Clone`, `Copy`, `PartialEq`, `Eq`,
    `PartialOrd`, `Ord`, `Hash`, `Default` where meaningful, `Display` for anything meant to be read. A type
    that plays the role of a data structure implements the serialisation traits behind a feature named exactly
    `serde`. Make types `Send` and `Sync` wherever the compiler allows, and pin that with a compile-time
    assertion for any type that holds a raw pointer.
11. **Naming.** Types, traits and variants in `UpperCamelCase`; functions, methods, modules and locals in
    `snake_case`; constants and statics in `SCREAMING_SNAKE_CASE`. In `UpperCamelCase` an acronym is one word
    (`Uuid`, not `UUID`). A crate name does not carry a `-rs` or `-rust` marker. Word order is consistent with
    the standard library (`ParseAddrError`, not `AddrParseError`). Keep identifiers short: no more than two
    short words, no crate or module name repeated as a prefix (`foo::Id`, not `foo::FooId`), accepted
    abbreviations over long forms.
12. **No weasel words in type names.** `Service`, `Manager` and `Factory` add nothing: all code manages
    something. Name what the type does (`Bookings`, `BookingDispatcher`). A factory is a builder; a function
    that needs repeatable construction takes an `impl Fn() -> Foo`, not a `FooBuilder`. Lifecycle is `Drop`'s
    job, not a manager's.
13. **Regular functions for what has no receiver.** An associated function is for creating an instance;
    a helper that merely sits next to a type is a free function. Essential behaviour is an inherent method,
    with trait impls forwarding to it, so that using the type does not require importing a trait to discover
    what it can do. A function with a clear receiver is a method.
14. **Accept the weakest input, borrow or own as the body needs.** A function that needs to own an argument
    takes it by value; one that only reads it takes a borrow. Take `impl AsRef<Path>` or `impl AsRef<str>`
    where a path or string of any flavour will do, `impl RangeBounds<_>` for ranges, and `impl Read`/`impl
    Write` for one-shot input and output so that a file, a socket and a byte slice all work (a function written
    that way can be tested without a disk). A generic reader taken by value can still be given `&mut reader`;
    say so in the docs.
15. **No out-parameters.** Return a tuple or a small struct. Compound return values are cheap and need no heap.
16. **Operators and `Deref` mean what they mean.** Implement `Mul` only for something that behaves like
    multiplication. Implement `Deref` and `DerefMut` only for smart pointers, never to fake inheritance.
17. **Keep the public surface deliberate.** Do not `pub use` a whole module with a glob; list the items. A
    glob is acceptable only to forward one platform-specific module as a whole. Do not define a `prelude`.
    Each public item is reachable through one path. Do not leak a third-party crate's type in a public
    signature unless it is behind a feature that names that crate or the interoperability is the point: the
    leaked type becomes part of your contract and your semver.
18. **Future-proof the type.** Seal a trait that only your crate may implement. Mark enums that may grow as
    `#[non_exhaustive]`. Do not repeat on a struct the trait bounds that `derive` already adds on the impl.
    Hide a returned iterator chain behind a newtype or `impl Iterator` instead of naming its concrete type.
19. **Names of features.** A Cargo feature is named for what it enables (`std`, `serde`), never `use-std` or
    `with-serde`, and never negatively (`no-std`): features are additive (§6.5).
