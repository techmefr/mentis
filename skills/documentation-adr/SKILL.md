---
name: documentation-adr
description: Use quand une décision d'architecture significative et difficile à revenir en arrière est prise, sépare ADR (décision, avec contexte/alternatives/conséquences) de la doc inline (uniquement le pourquoi non évident) et de la doc API, avec un template ADR précis et une règle jamais-supprimer-toujours-superseder.
---

# documentation-adr

Étape 3 du pipeline (`WORKFLOW.md`, après `archi`), pour toute décision
significative et coûteuse à annuler : pas pour documenter chaque choix
mineur.

## Quand
Après `archi` (3), dès qu'une décision structurante est prise (choix d'une
techno, d'un pattern de migration, d'une frontière entre modules) : jamais
pour un choix local facilement réversible.

## Étapes

### 1. Distinguer les trois types de documentation
1. **ADR** (Architecture Decision Record) : une décision significative,
   difficile à revenir en arrière : un fichier dédié, jamais mélangé au code.
2. **Doc inline** (commentaire dans le code) : uniquement le **pourquoi** non
   évident (contrainte cachée, workaround, comportement surprenant) : jamais
   ce que le code fait déjà (règle existante `no-comments-in-blade` :
   pas de commentaire si le code bien nommé suffit).
3. **Doc API** : le contrat consommé par d'autres (voir `api-design`), pas
   le même document qu'un ADR.

### 2. Template ADR : cinq champs, toujours les mêmes
1. **Status** : proposé / accepté / superseded (jamais "en cours" indéfini).
2. **Date** : date de la décision, pour situer le contexte dans le temps.
3. **Context** : la situation qui a rendu la décision nécessaire, ce qui ne
   sera plus évident dans six mois.
4. **Decision** : ce qui a été décidé, en une formulation nette.
5. **Alternatives considérées** : chaque option écartée, avec son pour/contre
, sans ça, un lecteur futur ne sait pas si l'alternative a été pensée ou
   oubliée.
6. **Consequences** : ce que la décision implique, y compris les compromis
   assumés.

### 3. Jamais supprimer, toujours superseder
1. Un ADR n'est **jamais supprimé** même si la décision devient obsolète : 
   un nouvel ADR le remplace explicitement (`Status: superseded by ADR-0042`).
2. L'historique des décisions reste lisible dans le temps : comprendre
   pourquoi on a changé d'avis compte autant que la décision actuelle.

## Sortie / checkpoint
Un fichier ADR créé pour toute décision significative de l'étape `archi`,
avec les six champs remplis : jamais un champ laissé vide "pour aller plus
vite".

## Garde-fous
Ne pas écrire d'ADR pour un choix trivial/réversible : réservé aux décisions
qui coûtent cher à défaire. Rester publiable (Règle C) : un ADR ne contient
pas de secret ni de nom de client, seulement la décision technique.

## Origine
Réécriture du skill `documentation-and-adrs` d'un catalogue de skills dev généralistes du marché, 
le template ADR (5-6 champs) et la règle "jamais supprimer, toujours
superseder" sont repris tels quels, réécrits en français au gabarit Xefi.
