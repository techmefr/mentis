---
name: python-conventions
description: Use quand on code ou revoit du Python, typage (type hints, mypy/pyright), gestion d'erreurs, patterns async, structure de projet. Pas de vécu de production interne Xefi sur ce langage (contrairement à vue-nuxt-vuetify-conventions), sourcé sur PEP officiels et l'outillage établi (ruff, mypy).
---

# python-conventions

Étape 6 du pipeline (`WORKFLOW.md`). Cadre l'écriture et la review de code
Python. **Statut particulier** : comme `go-conventions`/`dotnet-conventions`,
pas encore de vécu de production Xefi derrière cette brique : contenu venant
des PEP officiels et de l'outillage déterministe (ruff, mypy), pas de retours
de review réels.

## Quand
Dès qu'on écrit ou modifie du code Python, pendant `code` (6) ou `tdd` (5).

## Étapes

### 1. Typage : PEP 484 et suivants
1. Type hints sur toute signature de fonction publique (paramètres + retour)
, `mypy`/`pyright` en mode strict tourné sur le diff, pas seulement à
   l'installation initiale du projet.
2. `Optional[T]`/`T | None` explicite plutôt qu'une valeur par défaut `None`
   non typée qui laisse deviner le contrat réel.
3. `dataclass`/`pydantic` pour une structure de données avec validation,
   plutôt qu'un dict non typé passé de fonction en fonction.
4. `TypedDict` pour typer un dict existant (API externe, JSON) sans le
   convertir en classe : pas de `Dict[str, Any]` par réflexe.

### 2. Error handling
1. Exception spécifique levée (classe dédiée héritant d'`Exception`), jamais
   `except Exception:` nu qui avale tout sans distinction.
2. Un `except` sans relance ni log masque un vrai bug : jamais silencieux,
   même en dernier recours.
3. Context manager (`with`) pour toute ressource qui doit être fermée
   (fichier, connexion, lock) : jamais de fermeture manuelle qui peut être
   sautée par une exception intermédiaire.

### 3. Async
1. `asyncio.gather` pour des opérations indépendantes, jamais un `await` en
   série dans une boucle par réflexe.
2. Ne jamais mélanger code bloquant (I/O synchrone, calcul CPU lourd) dans une
   fonction `async` sans l'isoler (`run_in_executor`) : bloque toute la boucle
   d'événements, pas seulement l'appelant.
3. Une coroutine créée mais jamais awaitée ni stockée est un bug silencieux
   (`RuntimeWarning: coroutine was never awaited`), toujours vérifié.

### 4. Structure et style
1. Immutabilité par défaut : argument par défaut mutable (`def f(x=[])`)
   proscrit : partagé entre tous les appels, piège classique.
2. `pathlib.Path` plutôt que manipulation de chaînes pour les chemins de
   fichiers.
3. Compréhensions (list/dict/set) plutôt que boucle + `append` quand la
   lisibilité y gagne, jamais imbriquées au point de nuire à la lecture.

## Sortie / checkpoint
Code conforme aux quatre sections ci-dessus, et `ruff check`/`mypy` (ou
`pyright`) sans nouveau finding introduit par le diff. Vérifié par `gate` (7)
et `review` (8).

## Garde-fous
Pas de commentaires dans le code produit. Cette brique n'a pas encore été
confrontée à un vrai projet Python de production chez Xefi : en cas d'écart
entre une règle ici et un besoin réel observé, corriger cette brique plutôt
que de la traiter comme acquise.

## Origine
Idées reprises de : PEP 484/526/604 (type hints), PEP 8 (style), ruff
(règles par défaut, remplace flake8/isort/pyupgrade), mypy/pyright (typage
strict). Mécanismes réécrits, pas de texte copié. Recherche de marché, pas de
retour de production interne à ce stade : même statut que `go-conventions`.
