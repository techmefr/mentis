---
name: choose-model
description: Use quand on écrit un nouvel agent, ou qu'on lance une tâche ponctuelle, et qu'il faut décider quel modèle Claude assigner, Haiku pour les tâches mécaniques/répétitives à faible enjeu, Sonnet par défaut pour le build et la review, Opus pour un gate ou un juge dont le verdict est difficile à revenir en arrière (bloque un merge, une décision).
---

# choose-model

Brique transverse (pas une étape numérotée du pipeline) : s'applique à
chaque fois qu'un agent est créé ou qu'une tâche ponctuelle est lancée sans
modèle déjà imposé.

## Quand
- En écrivant un nouvel agent (frontmatter `model:` à renseigner).
- En lançant une tâche ponctuelle où le modèle n'est pas déjà fixé par un
  agent existant.
- En doutant si un agent existant est sur le bon modèle (sur- ou
  sous-dimensionné).

## Étapes

1. **Caractériser la tâche**, pas le rôle de l'agent :
   - Est-ce mécanique/répétitif (extraction, formatage, résumé court,
     classification simple) ? → **Haiku**.
   - Est-ce un travail de construction ou de lecture normale (écrire du
     code, reviewer un diff, appliquer des conventions documentées) ?
     → **Sonnet**, le défaut.
   - Le verdict est-il difficile à revenir en arrière une fois pris (bloque
     un merge, tranche entre deux architectures, juge à contexte frais sans
     seconde chance immédiate) ? → **Opus**.
2. **Vérifier le coût de l'erreur**, pas seulement la complexité apparente :
   une tâche qui a l'air simple mais dont une erreur est coûteuse à
   rattraper (ex. un gate qui laisse passer un bug en prod) monte d'un cran
   plutôt que de rester au niveau "complexité perçue".
3. **Ne jamais sur-dimensionner par réflexe.** Opus partout coûte cher et
   n'améliore rien sur une tâche mécanique : le sur-dimensionnement est aussi
   une erreur de choix, pas seulement le sous-dimensionnement.
4. **Documenter le choix** dans le frontmatter de l'agent (`model: sonnet`
   par exemple) : jamais laissé implicite, pour qu'une relecture ultérieure
   puisse contester le choix sur des critères explicites.

## Sortie / checkpoint
Le champ `model:` du frontmatter de l'agent est renseigné, avec un choix
justifiable en une phrase selon la grille ci-dessus. Pour une tâche
ponctuelle sans agent dédié, le modèle est choisi avant de lancer, pas
changé en cours de route sauf signal fort (timeout, échec répété).

## Garde-fous
- Pas de règle rigide par nom d'agent : un agent déjà "connu" peut changer
  de palier si la nature réelle de son travail a changé.
- En cas de doute entre deux paliers, prendre le palier du dessous et
  remonter seulement si un échec concret le justifie : pas l'inverse.

## Origine
Grille de décision interne : caractérisation par nature de tâche
(mécanique/construction/verdict-difficile-à-défaire) et par coût de
l'erreur, pas par complexité perçue. Pas de source externe spécifique
retenue : plusieurs frameworks de routing de modèle du marché existent,
mais aucun n'a été jugé assez proche de notre réalité de stack/agents pour
être réécrit tel quel ; la grille ci-dessus est une synthèse propre.
