---
name: deprecation-migration
description: Use quand il faut retirer/remplacer un système, une API, une colonne DB ou une dépendance encore utilisée, cadre la décision (dépréciation avisée vs imposée) puis choisit le pattern de migration progressive (Strangler, Adapter, Feature Flag, Expand/Contract), plutôt qu'un remplacement brutal en un seul déploiement.
---

# deprecation-migration

Étape transverse, avant `plan` (4) sur une tâche de migration/dépréciation
spécifiquement : distinct de `archi` (décisions d'architecture neuve) et de
`plan` (découpage d'un travail déjà cadré).

## Quand
Dès qu'une tâche consiste à retirer, remplacer ou faire évoluer de façon
incompatible un système déjà utilisé (API, colonne DB, dépendance, module) : 
jamais pour une feature neuve sans rien à déprécier.

## Étapes

### 1. Cinq questions avant de décider
1. Ce système a-t-il encore une **valeur unique** que rien d'autre ne couvre ?
2. Combien de **consommateurs réels** en dépendent (grep effectif, pas
   estimation) ?
3. Un **remplaçant existe-t-il déjà** et est-il prêt (pas seulement prévu) ?
4. Quel est le **coût de migration par consommateur** (un script mécanique
   vs une réécriture manuelle) ?
5. Quel est le **coût de maintenir** le système tel quel vs le coût de la
   migration : si maintenir coûte moins cher que migrer, ne pas migrer par
   principe.

### 2. Dépréciation avisée vs imposée
1. **Avisée** (advisory) : le consommateur choisit son rythme, un avertissement
   existe (log, doc, warning) mais rien ne casse tant qu'il n'a pas migré.
2. **Imposée** (compulsory) : une date/version fixe où l'ancien cesse de
   fonctionner : réservée aux cas où le maintien du legacy devient un risque
   réel (sécurité, dette bloquante), jamais choisie par défaut.

### 3. Choisir le pattern de migration
1. **Strangler** : le nouveau système absorbe progressivement les
   responsabilités de l'ancien, route par route/fonctionnalité par
   fonctionnalité, les deux coexistent le temps de la bascule.
2. **Adapter** : une couche de traduction fait parler l'ancien et le nouveau
   sans toucher aux consommateurs : utile quand la migration interne doit
   rester invisible du dehors.
3. **Feature Flag** : bascule contrôlée, réversible instantanément si un
   problème apparaît : préféré dès que la réversibilité immédiate compte plus
   que la simplicité du code.
4. **Expand/Contract** (schéma DB) : ajouter la nouvelle colonne/table →
   double-écriture (ancien + nouveau) → backfill de l'historique → bascule
   des lectures vers le nouveau → suppression de l'ancien, **en déploiements
   séparés**, jamais en un seul déploiement qui fait tout d'un coup.

## Sortie / checkpoint
Décision documentée (avisée/imposée + pattern choisi) avant que `plan` (4)
découpe le travail en étapes : jamais un remplacement en un seul commit/
déploiement pour un système avec des consommateurs réels identifiés.

## Garde-fous
- Jamais de suppression brutale d'un système ayant des consommateurs actifs
  non migrés, même en dépréciation imposée (une fenêtre de transition existe
  toujours).
- Expand/Contract : chaque étape est un déploiement séparé et observable, pas
  une transaction unique : sinon le rollback redevient aussi risqué que le
  problème qu'on évitait.
- Ne pas migrer par principe si l'étape 1.5 (coût de maintenir vs coût de
  migrer) penche vers le statu quo.

## Origine
Réécriture du skill `deprecation-and-migration` d'un catalogue de skills dev généralistes du marché, 
la checklist des 5 questions et les 4 patterns (Strangler/Adapter/Feature
Flag/Expand-Contract) sont repris tels quels, réécrits en français au gabarit
Xefi.
