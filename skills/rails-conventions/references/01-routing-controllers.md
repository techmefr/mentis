# § 1 — Routing, controllers and views

> Section 1 of `skills/rails-conventions`. Read it when a route, a controller action, a parameter list, a
> redirect or a template is written or changed. Pinned to the Rails 7.1 to 8.x range as read on 2026-10-02;
> where a rule needs a minimum version the point says so. The other sections and the guardrails stay in
> `SKILL.md`.

1. **A route names a resource; an extra action is a decision.** Start from `resources`. When a verb really
   does not fit a resource (ask whether a new resource would: "unsubscribe" is a `subscription` going away),
   add it as a `member` or `collection` route inside the resource, in the block form when there are several.
   A free-standing `get 'subscriptions/:id/unsubscribe'` is a route the router cannot relate to its resource,
   and it will not get the helpers, the nesting or the namespacing of the resource around it.
2. **Never mount the legacy wildcard route** (`:controller/:action/:id`). It makes every public method of every
   controller reachable by GET, including the ones nobody meant as actions. Use `match` only to bind several
   verbs to one action, and then say which with `via`.
3. **Nest to express the relation, and stop at one level.** Parent-scoped collections nest
   (`posts/1/comments`); a member two levels down gets `shallow: true` so its URL and its route helper stay
   short (`comments/5/edit`, not `posts/1/comments/5/versions/7/edit`). Group a family of controllers under a
   `namespace` so the module, the path and the helper prefix move together.
4. **Keep controllers skinny.** An action fetches what the view needs, calls one method on the model or a
   plain object that holds the behaviour, and chooses the response. Beyond an initial `find` or `new`, one
   call; and few instance variables handed to the view, because each is a name the template depends on.
   Business rules in an action are unreachable from a job, a console or a test that does not make an HTTP
   request.
5. **Filters are scoped where the actions are.** A `before_action ..., only:` that names an action defined in a
   parent class is invisible when reading the child; the filter belongs in the class that defines the action.
   For a filter that enforces access, prefer `except:` over `only:`: a list of what the filter covers silently
   skips every action added later, a list of what it exempts fails closed (the permitted-list principle).
6. **Parameters go through strong parameters, and on Rails 8 through `expect`.** `params.expect(user:
   [:name, :email])` requires the root key, permits only the listed attributes, is strict about the type (a
   scalar where a hash is expected, or the reverse), and raises `ActionController::ParameterMissing`, which
   the framework turns into a 400 instead of a 500 or a nil dereference later in the action. Before Rails 8
   the pair is `require(...).permit(...)`. Never pass `params` itself, or a `to_unsafe_h`, to `new`, `update`
   or `assign_attributes`: an attribute that appears on the model later is writable from the request the day
   it is added, with no code change at the controller.
7. **`flash.now` when rendering, `flash` when redirecting.** A `flash` set before `render` stays for one more
   request and shows the message twice, on the page it was meant for and on the next one.
8. **Never redirect to a URL the request supplied.** `redirect_to(params.update(action: "main"))` lets a
   `host` key in the query string send the user to another site; the same holds for any `return_to` parameter.
   Redirect to a route helper, or validate the target against the application's own host or an allowlist, and
   use `redirect_back_or_to` (Rails 7.0+; the older `fallback_location:` form is soft-deprecated) rather than
   building the previous URL by hand. `request.referer` is a hint from the client, never an authority.
9. **Templates over inline rendering, symbols over numbers.** `render inline:` puts a template in a controller
   where nobody lints or reviews it as a view; `render plain:` replaces `render text:`; `status: :forbidden`
   reads as intended where `403` makes the next reader look it up.
10. **A view does not call the model layer, and a partial does not read instance variables.** Pass locals to
    `render`: a partial that reads `@course` raises nothing when it is rendered from an action that never set
    it, it just prints nothing, while an undefined local raises. Formatting that grows past a helper or two
    moves to a presenter, not into the model: methods that only format data for display belong in helpers
    unless they mean something in the business domain.
11. **Outgoing HTML is escaped by construction.** `html_safe`, `raw` and `safe_concat` do not escape, they
    assert; use `safe_join` and `concat` to assemble markup from parts, and treat each remaining `html_safe`
    as a line that needs a reason beside it in review. A `link_to` whose target comes from user data checks
    the scheme (an allowlist of `http` and `https`), because `javascript:` is a valid URL.
