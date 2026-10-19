# cpp-build-and-lifetime-pitfalls §1 — Static storage duration and thread_local

Sources: the C++ working draft ([basic.start.dynamic], [dcl.constinit], read 2026-10-08), and the Google C++
style guide section on static and global variables and `thread_local` (CC BY 3.0, credit: Google). The guide's
rules are one company's project policy; where a rule below is the guide's, it says so, and the language facts
come from the draft.

## 1.1 What the language guarantees
1. **Dynamic initialisation of a namespace-scope variable is ordered only within one translation unit** (and
   across translation units linked by a module interface dependency), by the order of its definition.
   Otherwise the draft calls the initialisations indeterminately sequenced, so one global's constructor reading
   another global from a different file can run first.
2. **Whether dynamic initialisation happens before `main` or is deferred is implementation-defined.** The
   draft's own example shows a global in one file whose constructor uses a global from another file, with the
   outcome depending on that choice.
3. **An exception escaping the initialiser of a non-block variable with static or thread storage calls
   `std::terminate`.** There is no handler to put around a global's constructor.
4. **Destruction runs in reverse order of initialisation at program exit**, and (the guide's observation) that
   happens before unjoined threads are terminated, so a thread still running can touch an object whose
   destructor has already run.
5. **Dynamic initialisation of a `thread_local` variable is also implementation-defined in timing**: it may be
   deferred until the first use on each thread.

## 1.2 Default rule: only trivially destructible, constant-initialised globals
The guide's rule, adopted here as the default (own decision to adopt):
1. **No object with static storage duration unless it is trivially destructible.** Informally, its destructor
   does nothing, bases and members included; fundamental types, pointers, arrays of them and `constexpr`
   variables qualify. A namespace-scope `std::string`, `std::map` or smart pointer does not, and neither does a
   function-local `static std::map`.
2. **Constant initialisation is always allowed**: the initialiser is a constant expression and any constructor
   it calls is `constexpr`. Mark such variables `constexpr` or `constinit`, and treat any other non-local static
   as dynamically initialised and review it very carefully.
3. **`constinit` makes the compiler enforce it.** The draft says a `constinit` variable that has dynamic
   initialisation makes the program ill-formed even if the implementation would have initialised it
   statically; it applies only to static or thread storage duration variables (C++20).
4. **Dynamic initialisation of function-local statics is fine and common**, initialised the first time control
   passes through the declaration. Dynamic initialisation of namespace-scope variables is discouraged and
   allowed only when nothing depends on its order relative to others (the guide's example is a process id
   nobody else reads during start-up).

## 1.3 What to write instead
From the guide's patterns:
1. **A global string constant** is a `constexpr` `std::string_view`, a character array or a `const char*`
   pointing at a literal; literals already have static storage duration.
2. **A fixed lookup table** is an array of trivial elements or of pairs; for small sizes a linear search is
   enough, and a sorted array with binary search covers larger ones. Do not use a standard dynamic container as
   a global.
3. **A static of your own type** gets a trivial destructor and a `constexpr` constructor.
4. **If a dynamic container or object is truly needed, make it a function-local pointer or reference that is
   never deleted**, as in `static const auto& impl = *new T(args...);`. References are not objects, so the
   destructibility rule does not apply, and the object is never destroyed, which is the point.
5. **Smart pointers as statics are excluded by the guide** because they run cleanup in their destructors; use
   the pattern above.

## 1.4 thread_local
The guide's rules, with the draft facts above:
1. **A `thread_local` outside a function must be initialised with a true compile-time constant, enforced with
   `constinit`.** Inside a function it is safe, because it is initialised on first use.
2. **Destruction order at thread exit is the reverse of initialisation**, and if one `thread_local` destructor
   uses another that has already been destroyed on that thread the result is a use after free that is hard to
   diagnose. So a `thread_local` object should have a trivial destructor or one that touches nothing else.
3. **Accessing one can run an unpredictable amount of other code at thread start or first use**, and the memory
   used scales with the number of threads, which in the worst case is large.
4. **It cannot be an ordinary data member**, only a static one.
5. **The guide still prefers `thread_local` over other ways of defining thread-local data**, since it is the
   only standard-supported way.

## 1.5 Reviewing a global
A global in a diff gets three questions: is it constant-initialised, is its destructor trivial, and which
thread can still touch it after `main` returns. If any answer is no, convert it to a function-local never
destroyed object, or remove it (own guidance, a checklist built from the points above).
