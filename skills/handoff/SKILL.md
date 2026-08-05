---
name: handoff
description: Use quand une tâche déborde d'une session et qu'il faut transmettre le contexte à une session/agent frais proprement — compacte l'état en un document de passation qui référence les artefacts déjà écrits (plan, ADR, ticket, commit, diff) par chemin/URL plutôt que de dupliquer leur contenu.
---

# handoff

Étape transverse, à la frontière entre deux sessions sur la même tâche —
complète `worktree-one-task-close-after-merge` : le worktree reste ouvert,
mais le contexte de la session qui se termine doit survivre proprement à la
suivante.

## Quand
Dès qu'une session touche à sa fin (limite de contexte, fin de journée,
changement de qui reprend) sans que la tâche soit terminée — jamais en
remplacement d'un simple résumé de fin de tâche complète.

## Étapes

1. **Écrire un document de passation** (fichier temporaire dédié, pas mêlé au
   code) qui contient : où on en est, ce qui reste à faire, ce qui a été
   décidé et pourquoi, ce qui bloque s'il y a un blocage.
2. **Référencer, ne jamais dupliquer** : renvoyer vers les artefacts déjà
   écrits par leur chemin/URL exact (plan, ADR, ticket Jira, commit, diff en
   cours) plutôt que de recopier leur contenu dans le document de passation —
   un handoff qui duplique gonfle le contexte de la session suivante pour
   rien.
3. **Suggérer les skills pertinentes** pour la suite (ex "reprendre à `tdd`,
   le `plan` est déjà fait et référencé ici") — la session suivante sait par
   où recommencer sans devoir redécouvrir l'état seule.
4. La session suivante lit le document de passation en premier, avant tout
   autre exploration — il fait gagner le temps de re-contextualisation.

## Sortie / checkpoint
Un document de passation existe, cite chaque artefact par chemin/URL exact
(pas de contenu dupliqué), et nomme explicitement la prochaine étape/skill à
reprendre.

## Garde-fous
Jamais de duplication de contenu déjà écrit ailleurs — le principe entier de
cette brique est la référence, pas la copie. Un handoff qui devient plus long
que les artefacts qu'il référence a raté son objectif.

## Origine
Réécriture du skill `handoff` d'un auteur de skills reconnu du marché —
la règle "ne jamais dupliquer, référencer par chemin" est reprise telle
quelle, réécrite en français au gabarit Xefi et reliée explicitement à
`worktree-one-task-close-after-merge` déjà en place côté Xefi.
