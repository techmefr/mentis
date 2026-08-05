---
name: api-design
description: Use quand on conçoit une nouvelle API/interface (REST, tRPC, GraphQL) avant de l'implémenter, contract-first, loi de Hyrum (tout comportement observable finit par être dépendu), extension plutôt que rupture, checklist de vérification courte avant de livrer le contrat.
---

# api-design

Étape 3 du pipeline (`WORKFLOW.md`, entre `archi` et `plan`), quand la tâche
consiste à concevoir une interface consommée par d'autres (front, service
tiers, autre équipe) : pas pour une fonction interne sans contrat public.

## Quand
Avant d'implémenter un nouvel endpoint/route/procédure : jamais après coup en
"documentant ce qui existe déjà" (ça, c'est trop tard pour orienter le design).

## Étapes

### 1. Contract-first
1. Le schéma typé (DTO, type tRPC, schéma OpenAPI/GraphQL) est écrit **avant**
   l'implémentation, pas déduit du code après coup.
2. Validation posée **uniquement aux frontières** (entrée de l'API) : le code
   interne fait confiance au type déjà validé, pas de revalidation en
   profondeur qui duplique la logique.
3. Un seul format d'erreur système-wide (même structure pour toute erreur
   renvoyée), jamais un format différent par endpoint.

### 2. Loi de Hyrum : ce qui est observable sera dépendu
1. Tout comportement observable (ordre des champs, valeur par défaut, format
   d'une erreur) finira, tôt ou tard, dépendu par un consommateur même non
   documenté : traiter ce risque dès la conception, pas le découvrir en
   cassant un consommateur plus tard.
2. Champs internes/techniques jamais exposés "parce que c'est pratique" : 
   seul ce qui est un vrai contrat public l'est.

### 3. Extension plutôt que rupture : "One-Version Rule"
1. Étendre le contrat existant par des **champs optionnels** plutôt que de
   forker une nouvelle version pour un changement mineur.
2. Un changement réellement incompatible (retrait de champ, changement de
   type) passe par `deprecation-migration` (Expand/Contract ou versioning
   explicite), jamais par une modification silencieuse du contrat existant.
3. Pagination, tri, filtrage : conventions cohérentes sur toute l'API, pas
   réinventées endpoint par endpoint.

## Sortie / checkpoint
Checklist de vérification finale passée avant de livrer le contrat :
pagination cohérente avec le reste de l'API, compatibilité ascendante
vérifiée (aucun champ existant retiré/retypé), format d'erreur conforme au
standard système-wide, aucun champ interne exposé sans raison.

## Garde-fous
Pas de sur-ingénierie du contrat pour un besoin hypothétique non demandé : 
le contrat couvre le besoin réel, extensible plus tard si besoin, pas
pré-généralisé. Un changement incompatible ne se glisse jamais discrètement
dans une évolution "mineure" : passer explicitement par `deprecation-migration`.

## Origine
Réécriture du skill `api-and-interface-design` d'un catalogue de skills dev généralistes du marché, 
la loi de Hyrum, la "One-Version Rule" et la checklist de vérification finale
sont reprises telles quelles, réécrites en français au gabarit Xefi.
