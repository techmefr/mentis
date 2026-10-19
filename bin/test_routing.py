#!/usr/bin/env python3
"""Routing check: does a plain-language request find the block meant for it? Stdlib only, no network:

    python3 bin/test_routing.py              run the cases
    python3 bin/test_routing.py "a query"    print the top 5 blocks for a query

A block is reached through its `description` (the "Use when..." line), because that is the text a
runtime shows the model when it chooses. This builds a TF-IDF index over `name` + `description` of every
block, ranks blocks by cosine similarity to a query, and asserts that for each case the expected block
is among the top RANK results. It is a proxy for the model's choice, not the choice itself: a case that
fails means the description does not carry the words a person would use, which is the defect to fix.

Add a case when a block is created or its description is rewritten.
"""
import math
import os
import re
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(REPO, "skills")
RANK = 3
STOP = set("a an and are as at be by for from in is it of on or that the this to use used using when with within "
           "into not no than then their there these those you your any all can may must should whether which "
           "while who what how".split())
FRONT = re.compile(r"\A---\n(.*?)\n---", re.S)
DESC = re.compile(r'^description:\s*(.+?)\s*$', re.M)
NAME = re.compile(r'^name:\s*(.+?)\s*$', re.M)


def tokens(text):
    out = []
    for word in re.findall(r"[a-z0-9][a-z0-9+#.]*", text.lower()):
        word = word.strip(".")
        if len(word) < 2 or word in STOP:
            continue
        out.append(word)
        if "-" in word:
            out.extend(part for part in word.split("-") if part not in STOP and len(part) > 1)
    return out


def load():
    docs = {}
    for name in sorted(os.listdir(SKILLS)):
        path = os.path.join(SKILLS, name, "SKILL.md")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as handle:
            front = FRONT.match(handle.read())
        if not front:
            continue
        desc = DESC.search(front.group(1))
        if not desc:
            continue
        text = desc.group(1).strip().strip('"').strip("'")
        docs[name] = tokens(name.replace("-", " ") + " " + name.replace("-", " ") + " " + text)
    return docs


def build(docs):
    count = len(docs)
    frequency = Counter()
    for words in docs.values():
        frequency.update(set(words))
    idf = {w: math.log((1 + count) / (1 + n)) + 1 for w, n in frequency.items()}
    vectors = {}
    for name, words in docs.items():
        tf = Counter(words)
        vec = {w: (1 + math.log(c)) * idf[w] for w, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1
        vectors[name] = {w: v / norm for w, v in vec.items()}
    return vectors, idf


def rank(query, vectors, idf):
    tf = Counter(w for w in tokens(query) if w in idf)
    vec = {w: (1 + math.log(c)) * idf[w] for w, c in tf.items()}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1
    scored = []
    for name, doc in vectors.items():
        score = sum(v / norm * doc.get(w, 0) for w, v in vec.items())
        scored.append((score, name))
    scored.sort(key=lambda pair: (-pair[0], pair[1]))
    return scored


CASES = [
    ("review this Angular component that uses signals and OnPush", "angular-conventions"),
    ("write a Svelte 5 component with runes and a SvelteKit load function", "svelte-conventions"),
    ("my Tailwind classes are built dynamically and the styles disappear in production", "tailwind-conventions"),
    ("VITE_ environment variable exposed to the browser and the dev server host option", "vite-bundler-conventions"),
    ("where should server data live: query cache or a client store, invalidation after mutation", "data-fetching-state-conventions"),
    ("a Vue composable and a Pinia store with Vuetify components", "vue-nuxt-vuetify-conventions"),
    ("a React server component and a Next.js server action", "react-nextjs-conventions"),
    ("Playwright end to end test with locators by role and no fixed waits", "frontend-testing"),
    ("a NestJS module with guards, pipes and a Prisma transaction", "nestjs-node-conventions"),
    ("a freshness lock for the pinned versions a block depends on", "source-freshness"),
    ("an accessibility review of a form: labels, focus order and contrast", "accessibility"),
    ("write a Go service with context and error wrapping", "go-conventions"),
]


def main():
    docs = load()
    vectors, idf = build(docs)
    if len(sys.argv) > 1:
        for score, name in rank(" ".join(sys.argv[1:]), vectors, idf)[:5]:
            print(f"{score:.3f}  {name}")
        return 0
    ok = fail = 0
    for query, expected in CASES:
        if expected not in docs:
            print(f"SKIP  {expected} is not a block of this checkout")
            continue
        top = [name for _, name in rank(query, vectors, idf)[:RANK]]
        if expected in top:
            ok += 1
            print(f"PASS  routes to {expected}: {query[:60]}")
        else:
            fail += 1
            print(f"FAIL  {expected} not in top {RANK} {top}: {query[:60]}")
    same = {}
    for name, words in docs.items():
        same.setdefault(tuple(sorted(set(words))), []).append(name)
    twins = [names for names in same.values() if len(names) > 1]
    if twins:
        fail += 1
        print(f"FAIL  blocks with an identical description vocabulary: {twins}")
    else:
        ok += 1
        print("PASS  no two blocks share an identical description vocabulary")
    print(f"\n{ok} passed, {fail} failed")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
