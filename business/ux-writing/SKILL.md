---
name: ux-writing
description: Use when writing any text a user reads in the product — labels, buttons, errors, empty states, confirmations, emails — the words are part of the interface and they're usually written last by whoever is closest to the code. Complements accessibility (which covers how the text is exposed) and i18n conventions (how it's stored).
---

# ux-writing

Business layer (`business/README.md`), applied at step 6 of the dev pipeline. Interface text gets
written in the last ten minutes by a developer with a component to finish, and then it's what every
user reads for the next three years.

This block isn't about tone of voice, which belongs to whoever owns the brand. It's about the specific
places where wording causes a support ticket, a wrong click, or a user stuck with no route forward.

**Boundary with an org design catalogue.** Where one exists, its UX-writing skill covers the same subject
**at design time**, inside a mockup, and carries the organisation's own rules — form of address, one word
per action, explicit button labels. Where that plugin is installed, **it is the authority on the wording
rules and this block defers to it**; what remains here is the code-time pass, on text that reaches a diff
without ever passing through a mockup: validation messages, error states, transactional emails,
concatenated strings. A dedup audit on 2026-08-06 confirmed the overlap is real; this is the resolution,
and the two must not diverge on a shared rule.

## When
As soon as a diff adds or changes text a user sees: a field label, a button, a validation message, an
error, an empty state, a confirmation dialog, a notification, a transactional email.

## Steps

### 1. Errors: say what happened, and what to do now
1. **Name what went wrong in the user's terms**, not the system's. "Request failed with status 422" is
   a log line, not a message.
2. **Every error gives a next action.** If there's nothing the user can do, say who can, or that it's
   been reported. A dead end with no route forward is what turns an error into a support call.
3. **Never blame the user.** "Invalid input" for a date typed in a format you didn't accept is our
   parser's problem stated as the user's failing.
4. **Be specific about which field and why.** "Some fields are invalid" makes the user hunt.
5. **Don't leak internals**: stack traces, table names, internal ids. That's a security habit as much
   as a writing one (`skills/security-hardening`).

### 2. Labels and buttons: describe the outcome
1. **A button says what it does**, not where it goes. "Save changes" beats "OK"; "Delete account" beats
   "Confirm". The user who reads only the button — which is most of them — should still be right about
   what happens.
2. **Confirmation dialogs state the consequence and its reversibility.** "Are you sure?" carries no
   information. "Delete 12 invoices? This can't be undone." lets someone decide.
3. **The dangerous option is never the default**, and it isn't the one styled to be clicked.
4. **Match the words to the destination**: a link labelled "Settings" leading to a page titled
   "Preferences" makes the user wonder whether they arrived.

### 3. Empty states: the screen someone sees first
1. **An empty list is the new user's first impression**, and "No data" wastes it. Say what belongs here
   and how to add the first one.
2. **Distinguish "nothing yet" from "nothing matches"**: a filter returning nothing needs a way to
   clear the filter, not an invitation to create something.
3. **Distinguish both from "failed to load"** — showing an empty state when a request errored teaches
   the user their data is gone.

### 4. One product, one voice
1. **One form of address, applied everywhere** — every message, error, label and confirmation. Which one is a
   product decision, and in several languages it is a grammatical fork with no neutral option; mixing them
   inside one product is what reads as unfinished.
2. **One word per action, across the whole product.** If deleting an item is "Delete", it is never "Remove" or
   "Clear" three screens later. Two words for one action make a user wonder whether they do the same thing,
   and they make consistent translation impossible.
3. This is also why the wording lives in one place rather than wherever it was first typed
   (`vue-nuxt-vuetify-conventions` section 6, `laravel-conventions` section 5).

### 5. Mechanics that keep it consistent
1. **One term per concept, everywhere.** If it's a "customer" in one screen and a "client" in the next,
   users assume they're different things. Pick one and use it in the code too
   (`skills/domain-modeling` §1).
2. **Sentence case, no shouting, no exclamation marks** in system messages.
3. **Translation keys are for a translator**, so keep the source sentence readable and never build a
   sentence by concatenating fragments: word order differs between languages and the result is
   unreadable in half of them.
4. **Numbers, dates and currency are localised**, not formatted by hand.
5. **Text a screen reader will announce** has its own requirements — see `skills/accessibility`.

## Output / checkpoint
No pipeline checkpoint (business layer). What it owes: every new user-facing string has a next action
where it's an error, a consequence where it's destructive, and a term consistent with the rest of the
product. Where the wording carries brand or legal weight, it goes to whoever owns that.

## Guardrails
- **Never ship a placeholder.** "Lorem ipsum", "TODO", "test" and a bare "Error" all reach production
  eventually.
- **Never invent a legal or commercial commitment in interface text** — a guarantee, a deadline, a
  price, a promise about data. That's someone else's decision to make.
- Never let humour into an error path: the person reading it is already having a problem.
- This block doesn't own tone of voice or brand vocabulary. Where it conflicts with them, they win.

## Origin
Assembled from public sources: established interface-writing guidance (errors stating cause and next
action, buttons naming the outcome, useful empty states) as published in the major design systems'
content guidelines. Written **without internal UX-writing expertise** and without access to a company
tone-of-voice reference, so it deliberately stops at the mechanical cases where wording causes a
measurable failure and leaves voice to whoever owns it. The consistency link to `domain-modeling`, the
concatenation rule and the "empty vs no-match vs failed-to-load" distinction are ours.
