---
name: wayfinder
description: Use quand un travail dépasse une session/plusieurs semaines et reste incertain (migration large, refonte progressive), découpe le travail en une carte de tickets Jira (un parent + des enfants typés Research/Prototype/Grilling/Task) liés par dépendances, plutôt qu'un seul gros ticket ou un plan figé d'avance. Distinct de breakdown (qui découpe une story déjà cadrée en 1pt=1h).
---

# wayfinder

Étape transverse, avant/à côté de `plan` (4) : pour l'incertitude qui dépasse
le cadre d'une story déjà chiffrable. `breakdown` (skill existante) découpe
une story cadrée en tâches d'1h ; `wayfinder` gère un chantier dont la forme
finale n'est pas encore connue.

## Quand
Dès qu'un travail est trop gros/incertain pour une session, et que son
découpage complet ne peut pas être connu à l'avance (migration progressive,
refonte qui s'affine au fil de l'avancement) : jamais pour une story déjà
cadrée (ça, c'est `breakdown`).

## Étapes

### 1. Ticket parent : la destination, pas le chemin détaillé
1. **Destination** : où on veut arriver, en une phrase, même si le chemin
   exact n'est pas encore connu.
2. **Notes** : contexte libre qui s'accumule au fil de l'avancement.
3. **Décisions déjà prises** : ce qui est tranché et ne se rediscute plus.
4. **Pas encore spécifié** : les zones grises identifiées mais non résolues, 
   explicitement listées, jamais implicites.
5. **Hors scope** : ce qu'on a choisi de ne pas faire, pour éviter qu'un
   ticket enfant dérive dessus plus tard.

### 2. Tickets enfants typés
1. **Research** : lever une inconnue avant de pouvoir avancer (pas de
   livrable code).
2. **Prototype** : vérifier qu'une approche fonctionne, jetable si besoin.
3. **Grilling** : cadrer précisément une zone encore floue (proche de
   `spec`).
4. **Task** : travail concret, cadré, prêt à exécuter.
5. Chaque enfant est lié au parent par une dépendance native du tracker (pas
   un simple lien texte) pour que l'outil visualise ce qui est "frontière"
   (débloqué, prenable maintenant) vs bloqué en attente d'un autre ticket.

### 3. Une session = un ticket résolu
1. On ne travaille jamais sur plusieurs tickets enfants en même temps dans la
   même session : cohérent avec `worktree-one-task-close-after-merge`.
2. À la fin d'une session, le ticket parent est mis à jour (notes, décisions,
   ce qui est passé de "pas encore spécifié" à "décidé").

## Sortie / checkpoint
Un ticket parent Jira avec les cinq sections remplies, des tickets enfants
typés créés au fur et à mesure (pas tous d'un coup au départ : seulement ce
qui est identifié), liés par dépendances bloquantes natives.

## Garde-fous
Ne pas essayer de découper tout le chantier d'un coup en début de projet : 
`wayfinder` accepte explicitement que le découpage complet n'est pas connu à
l'avance, contrairement à `plan`/`breakdown`. Ne pas laisser le ticket parent
devenir un fourre-tout non maintenu : chaque session le met à jour.

## Origine
Réécriture du skill `wayfinder` d'un auteur de skills reconnu du marché : 
la structure du ticket parent (5 sections) et les 4 types de ticket enfant
sont repris tels quels, adaptés à un usage Jira (au lieu du tracker
générique d'origine) et distingués explicitement de `breakdown` déjà existant.
