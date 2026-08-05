---
name: qa-exploratory-testing
description: Use quand une feature est codée et gatée mais avant le merge — test manuel/exploratoire d'un vrai parcours utilisateur sur l'app qui tourne, distinct de tdd (tests automatisés écrits pendant le code) et de gate (preuve que les tests passent). Trouve ce qu'aucun test automatisé n'a pensé à couvrir.
---

# qa-exploratory-testing

Étape complémentaire à `review` (8), avant `ship` (10) — le regard QA, pas le
regard dev. `tdd` (5) écrit les tests qu'on savait devoir écrire ; cette
brique cherche ce qu'on n'a pas pensé à tester.

## Quand
Après `gate` (7, tests automatisés verts) et en parallèle de `review` (8),
sur toute feature qui touche un parcours utilisateur réel — pas sur un
refactor interne sans surface utilisateur.

## Étapes

### 1. Charter — cadrer l'exploration, pas improviser à l'aveugle
1. Définir le **charter** en une phrase : quelle zone/parcours explorer et
   pourquoi (ex "le formulaire de paiement, angle erreurs réseau") — sans
   charter, l'exploration part dans tous les sens et ne converge jamais.
2. Timeboxer la session (30-60 min) — l'exploratoire sans limite de temps ne
   finit jamais et dérive hors sujet.

### 2. Techniques — au-delà du chemin heureux déjà couvert par tdd
1. **Boundary testing** : valeurs limites (0, négatif, max, vide, très long)
   sur chaque champ/paramètre du parcours.
2. **État et navigation** : retour arrière navigateur, rafraîchissement en
   plein milieu d'un flux multi-étapes, double-clic sur un bouton de
   soumission, onglet dupliqué sur la même session.
3. **Erreurs externes simulées** : réseau coupé/lent, API tierce qui répond
   en erreur ou timeout — le parcours dégrade-t-il proprement ou casse-t-il ?
4. **Persona switching** : le même parcours rejoué avec un rôle/permission
   différent (utilisateur non connecté, permission manquante, agence
   différente) pour vérifier qu'aucun accès non prévu ne fuit.

### 3. Non-régression — ce qui touchait avant ne casse pas ailleurs
1. Vérifier les parcours adjacents (pas seulement celui modifié) quand le
   diff touche un composant/service partagé.
2. Comparer le comportement avant/après si un doute existe, plutôt que de se
   fier à la mémoire de "comment ça marchait avant".

## Sortie / checkpoint
Chaque bug trouvé est rapporté avec : parcours exact pour reproduire, résultat
observé vs attendu, sévérité (bloquant/majeur/mineur). Pas de bug rapporté
sans séquence de reproduction précise.

## Garde-fous
- Ne remplace jamais `tdd`/`gate` : c'est un complément humain-piloté sur ce
  que l'automatisé ne pense pas à tester, pas un filet de sécurité de premier
  niveau.
- Timeboxé : au-delà du temps alloué, on s'arrête et on rapporte l'état
  atteint, pas de session qui s'étire indéfiniment.
- Un bug trouvé ici et jugé mineur ne bloque pas `ship` par défaut — c'est à
  l'humain de trancher priorité vs délai, pas à l'agent de décider seul.

## Origine
Sourcé sur les techniques d'exploratory testing établies (James Bach/Michael
Bolton — session-based test management, charter, timeboxing) et le boundary
testing classique (ISTQB). Mécanismes réécrits, pas de texte copié. Recherche
de marché, pas de retour de production interne dédié QA à ce stade.
