---
name: php-patterns
description: Use quand on code ou revoit du PHP pur, indépendamment du framework (pas Laravel/Eloquent, ça c'est gimli/laravel-builder), typage, gestion d'erreurs, patterns OOP. Pas de vécu de production interne profond sur ce langage seul (g.compigni débute en PHP), contenu sourcé sur PHP-FIG (PSR) et les standards établis du marché.
---

# php-patterns

Étape 6 du pipeline (`WORKFLOW.md`), en amont de la couche Laravel, le
langage lui-même, avant les conventions Eloquent/Laravel qui s'ajoutent
par-dessus (voir `gimli`, `laravel-builder`).

## Quand
Dès qu'on écrit ou revoit du PHP, sur n'importe quel framework : cette brique
est le socle commun, les conventions Laravel s'appliquent en plus, pas à la
place.

## Étapes

### 1. Typage : PHP moderne (8.x) n'est plus du PHP non typé
1. Signatures de fonction/méthode typées (paramètres + retour), y compris
   `void`/`?type` explicite, un paramètre non typé est une régression, pas
   un style neutre en PHP 8+.
2. `readonly` sur les propriétés qui ne changent jamais après construction
   (value objects, DTO) : évite une mutation accidentelle en profondeur.
3. Types union (`int|string`) plutôt que `mixed` par réflexe : `mixed`
   n'exprime aucune intention, un union type explicite documente le contrat
   réel.
4. Enums natifs PHP 8.1+ (`enum ... : string`) plutôt que des constantes de
   classe éparpillées pour représenter un ensemble fermé de valeurs.

### 2. Error handling
1. Exception spécifique levée (classe dédiée, pas `\Exception` générique) dès
   que l'appelant doit pouvoir distinguer le cas d'erreur pour réagir
   différemment.
2. Un `catch` qui avale l'exception sans la relancer ni la logger masque un
   vrai bug : jamais un `catch` silencieux, même en dernier recours.
3. `null` de retour ambigu (échec vs absence légitime) : préférer une
   exception pour un échec réel, `null`/option seulement pour une absence
   attendue et documentée.

### 3. OOP et structure
1. Composition plutôt qu'héritage profond (>2 niveaux) : un héritage profond
   couple des comportements qui devraient rester indépendants.
2. Interface définie au bord (contrat public d'un service) même à un seul
   côté implémenté : facilite le remplacement/mock sans casser l'appelant.
3. Propriété statique mutable = état global caché : à éviter sauf cas
   explicitement assumé (config immuable, pas un compteur qui change).
4. `match` (PHP 8+) plutôt que `switch` pour une comparaison de valeur simple
, pas de fallthrough implicite, retourne une valeur directement.

## Sortie / checkpoint
Code conforme aux trois sections ci-dessus, vérifié en plus des conventions
Laravel applicables via `gate` (7) et `review` (8, `gimli`).

## Garde-fous
Pas de commentaires dans le code produit (règle d'équipe Xefi, tous repos).
Cette brique n'a pas de vécu de production interne profond derrière (g.compigni
débute en PHP, comme noté sur `gimli`) : en cas d'écart entre une règle ici et
un besoin réel observé sur le terrain, corriger cette brique plutôt que la
traiter comme acquise.

## Origine
Sourcé sur PHP-FIG (PSR-12 style, PSR de base), la documentation officielle
PHP (types, enums, `readonly`, `match`) et les pratiques établies du marché
PHP moderne. Mécanismes réécrits, pas de texte copié. Recherche de marché, pas
de retour de production interne profond à ce stade : même statut
d'incertitude que `gimli`.
