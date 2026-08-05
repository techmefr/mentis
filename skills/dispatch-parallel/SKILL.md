---
name: dispatch-parallel
description: Use quand une tâche se découpe en sous-parties indépendantes (plusieurs stacks à reviewer, plusieurs fichiers à migrer, plusieurs pistes à explorer) — lance des sous-agents en parallèle sur des périmètres disjoints plutôt qu'un seul agent séquentiel.
---

# dispatch-parallel

Brique transverse (pas une étape numérotée du pipeline) : s'applique dès qu'un
travail se décompose naturellement en sous-tâches qui ne se marchent pas dessus.

## Quand
- Plusieurs stacks/repos à traiter dans la même passe (ex `elrond` qui délègue
  à `aragorn`/`gimli`/`legolas` en parallèle sur des MR disjointes).
- Plusieurs fichiers/modules indépendants à migrer, auditer ou documenter.
- Plusieurs pistes de recherche à explorer avant de trancher (panel de juges,
  plusieurs implémentations candidates).
- Ne s'applique **pas** si les sous-tâches partagent un état mutable commun
  (même fichier édité par deux agents à la fois) — dans ce cas, séquentiel.

## Étapes
1. **Découper en périmètres disjoints** : chaque sous-agent reçoit un scope
   clair qui ne recouvre aucun autre (fichiers différents, ou même fichier en
   lecture seule pour tous sauf un).
2. **Isoler par worktree** si les sous-agents écrivent du code (voir
   `merge-worktree`) — jamais deux agents qui écrivent dans le même
   répertoire de travail en même temps.
3. **Lancer en un seul message** tous les agents indépendants (plusieurs
   appels d'outil dans le même tour) plutôt qu'en série — le gain n'existe
   que si l'attente est réellement concurrente.
4. **Agréger** les résultats une fois tous revenus : ne pas commencer à
   synthétiser avant d'avoir tout, sauf si le pipeline est construit en
   pipeline continu (un résultat avance à l'étape suivante dès qu'il est prêt,
   sans attendre les autres).
5. Chaque sous-agent produit sa propre trace (voir gabarit unique, pilier 7) :
   pas de rapport fusionné qui masque quel agent a dit quoi.

## Sortie / checkpoint
Tous les sous-agents dispatchés sont revenus (ou explicitement abandonnés
avec la raison notée), et l'agrégation cite quel résultat vient de quel
agent — jamais une synthèse anonyme.

## Garde-fous
- Jamais deux agents avec Write/Edit sur le même fichier en simultané.
- Un agent qui échoue n'annule pas les autres : on isole l'échec, on ne relance
  pas tout le lot.
- Ne pas dispatcher pour dispatcher : une seule sous-tâche ne justifie pas ce
  mécanisme, il ne vaut que si le parallélisme fait gagner du temps réel.

## Origine
Réécriture des deux idées `dispatching-parallel-agents` et
`subagent-driven-development` d'un framework de skills/agents du marché,
fusionnées ici parce que dans notre usage elles se recouvrent : dispatcher en
parallèle et déléguer à des sous-agents spécialisés sont la même décision
chez nous (`elrond` → `aragorn`/`gimli`/`legolas`/`boromir`/`theoden`/`frodo`
en est l'exemple vécu de production).
