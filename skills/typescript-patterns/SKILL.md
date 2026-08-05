---
name: typescript-patterns
description: Use quand on code ou revoit du TypeScript/JavaScript pur, indépendamment du framework (pas Nuxt, pas React, pas NestJS, ça c'est vue-nuxt-vuetify-conventions/react-nextjs-conventions/nestjs-node-conventions), types avancés, patterns async, closures, immutabilité. Vécu de production réel côté g.compigni sur ce langage.
---

# typescript-patterns

Étape 6 du pipeline (`WORKFLOW.md`), en amont des briques framework, le
langage lui-même, avant la couche Nuxt/React/NestJS qui s'ajoute par-dessus.

## Quand
Dès qu'on écrit ou revoit du TS/JS, sur n'importe quelle stack : cette brique
est le socle commun, les conventions framework s'appliquent en plus, pas à la
place.

## Étapes

### 1. Typage : éviter le faux-typé
1. `any` jamais utilisé pour éviter de réfléchir au type réel : `unknown` +
   narrowing si le type est vraiment inconnu à ce point du code.
2. Assertion de type (`as`) seulement quand TypeScript ne peut structurellement
   pas inférer (ex. résultat de `JSON.parse`), jamais pour faire taire une
   erreur de type légitime.
3. Types dérivés (`ReturnType`, `Parameters`, `Pick`/`Omit`, mapped types)
   plutôt que dupliquer une forme de données déjà déclarée ailleurs : un type
   dupliqué diverge silencieusement du premier au premier refactor.
4. `interface` pour une forme extensible (objet, contrat public), `type` pour
   une union/intersection/alias : pas de règle qui les oppose par dogme, mais
   pas de choix au hasard non plus.
5. Discriminated unions (`{ type: 'a', ... } | { type: 'b', ... }`) plutôt
   qu'un objet à champs optionnels tous nullable pour représenter des états
   mutuellement exclusifs.

### 2. Async : la source n°1 de bugs silencieux
1. `Promise` jamais laissée en l'air sans `await` ni `.catch` explicite, une
   promesse rejetée non gérée est un crash silencieux ou un unhandled
   rejection.
2. `Promise.all` pour des opérations indépendantes, jamais un `await` en
   série dans une boucle par réflexe quand le parallélisme est possible et
   sûr (pas de dépendance entre elles).
3. `async` sur une fonction qui ne fait rien d'asynchrone est un signal
   d'aspiration à retirer, pas un style neutre.
4. Race condition classique : deux `await` qui modifient le même état partagé
   sans verrou logique (ex. deux appels qui lisent puis écrivent la même
   variable) : vérifier l'ordre réel d'exécution, pas l'ordre apparent dans
   le code.

### 3. Immutabilité et closures
1. `const` par défaut, `let` seulement si la réassignation est réellement
   nécessaire : jamais `var`.
2. Une closure dans une boucle capture la référence, pas la valeur au moment
   de la création : piège classique avec `var`, moins avec `let`/`const` mais
   à vérifier si un tableau de callbacks est construit dynamiquement.
3. Mutation d'un objet/tableau reçu en paramètre = effet de bord invisible
   pour l'appelant : retourner une copie (spread, `structuredClone`) si le
   contrat n'est pas explicitement "je mute en place".
4. Enum natif TS (`enum`) évité au profit d'un objet `as const` + type dérivé
   (`typeof X[keyof typeof X]`) : l'enum natif génère du JS runtime superflu
   et se comporte différemment en `isolatedModules`.

## Sortie / checkpoint
Code conforme aux trois sections ci-dessus, vérifié en plus des conventions
framework applicables (`vue-nuxt-vuetify-conventions`/`react-nextjs-conventions`/
`nestjs-node-conventions`) via `gate` (7) et `review` (8).

## Garde-fous
Pas de commentaires dans le code produit. Ne pas imposer un style de typage
plus strict que ce que `tsconfig.json` du projet exige déjà (`strict`,
`noImplicitAny`) : s'aligner sur la config réelle, pas sur un idéal théorique
non appliqué au repo.

## Origine
Synthèse interne à partir du vécu de production réel de g.compigni (JS/TS de
longue date, cf `frodo`/`legolas`) et des recommandations établies TypeScript
(handbook officiel sur les discriminated unions, `as const`). Pas de repo
externe unique retenu : brique de langage, pas de framework, donc pas de
source "expert X" à créditer comme pour les conventions framework sourcées
marché.
