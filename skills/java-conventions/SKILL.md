---
name: java-conventions
description: Use quand on code ou revoit du Java — typage/immutabilité (records, Optional), gestion d'erreurs (checked vs unchecked), concurrence, patterns Spring courants. Pas de vécu de production interne Xefi sur ce langage, sourcé sur les conventions établies du marché (Effective Java, Spring) et l'outillage (SpotBugs/Error Prone).
---

# java-conventions

Étape 6 du pipeline (`WORKFLOW.md`). Cadre l'écriture et la review de code
Java. **Statut particulier** : comme `go-conventions`/`python-conventions`,
pas encore de vécu de production Xefi derrière cette brique — contenu venant
des conventions établies (Effective Java) et de l'outillage déterministe
(SpotBugs, Error Prone), pas de retours de review réels.

## Quand
Dès qu'on écrit ou modifie du code Java, pendant `code` (6) ou `tdd` (5).

## Étapes

### 1. Immutabilité et typage
1. `record` (Java 16+) pour toute donnée immuable simple (DTO, value object)
   plutôt qu'une classe avec getters/setters manuels.
2. Champs `final` par défaut, mutabilité seulement si réellement nécessaire.
3. `Optional<T>` en type de retour pour une absence légitime, jamais en
   paramètre de méthode ni en champ de classe (source de complexité inutile,
   consensus Effective Java).
4. Éviter `null` en retour d'une méthode publique quand `Optional` ou une
   exception exprime mieux l'intention réelle.

### 2. Error handling — checked vs unchecked
1. Exception *unchecked* (`RuntimeException`) pour une erreur de programmation
   (précondition violée), *checked* pour une erreur récupérable que
   l'appelant doit gérer explicitement — ne pas transformer toute exception
   en unchecked par confort.
2. Un `catch` qui avale l'exception sans la relancer ni la logger masque un
   vrai bug — jamais silencieux.
3. `try-with-resources` pour toute ressource `AutoCloseable` (fichier,
   connexion) — jamais de fermeture manuelle dans un `finally` écrit à la
   main quand `try-with-resources` couvre le cas.

### 3. Concurrence
1. Collection partagée entre threads : `java.util.concurrent`
   (`ConcurrentHashMap`, etc.) plutôt qu'une collection standard synchronisée
   manuellement au coup par coup.
2. `synchronized` sur un bloc le plus court possible, jamais sur une méthode
   entière par réflexe quand seule une section critique le nécessite.
3. `ExecutorService` avec un pool dimensionné et fermé explicitement
   (`shutdown()`), jamais de `Thread` brut créé à la volée sans gestion de
   cycle de vie.

### 4. Patterns Spring courants (si applicable)
1. Injection par constructeur, jamais par champ (`@Autowired` sur un champ) —
   rend les dépendances explicites et testables sans réflexion.
2. DTO distinct de l'entité JPA exposé en API — jamais l'entité persistée
   directement au bord de l'API (couplage schéma DB / contrat public).
3. Transactions (`@Transactional`) posées au niveau du service, jamais du
   contrôleur — le contrôleur ne doit pas connaître la frontière
   transactionnelle.

## Sortie / checkpoint
Code conforme aux quatre sections ci-dessus (section 4 seulement si Spring),
et SpotBugs/Error Prone sans nouveau finding introduit par le diff. Vérifié
par `gate` (7) et `review` (8).

## Garde-fous
Pas de commentaires dans le code produit. Cette brique n'a pas encore été
confrontée à un vrai projet Java de production chez Xefi — en cas d'écart
entre une règle ici et un besoin réel observé, corriger cette brique plutôt
que de la traiter comme acquise.

## Origine
Idées reprises de : Effective Java (Joshua Bloch — immutabilité, `Optional`,
checked vs unchecked), SpotBugs/Error Prone (règles statiques par défaut),
conventions Spring établies (injection par constructeur, DTO vs entité).
Mécanismes réécrits, pas de texte copié. Recherche de marché, pas de retour de
production interne à ce stade — même statut que `go-conventions`.
