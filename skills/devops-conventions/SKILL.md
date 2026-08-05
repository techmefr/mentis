---
name: devops-conventions
description: Use quand on écrit/revoit un pipeline CI/CD, de l'infra as code (Docker, Terraform, Ansible) ou du monitoring/alerting, conventions pour la fiabilité et la reproductibilité, pas pour le code applicatif. Pas de vécu de production Xefi dédié à ce stade, sourcé sur les pratiques établies (12-factor, DORA metrics).
---

# devops-conventions

Étape 6 du pipeline (`WORKFLOW.md`) côté infra/CI, en complément de
`portless-ready` (qui rend une stack portless) : ici la fiabilité et la
reproductibilité du pipeline de livraison lui-même.

## Quand
Dès qu'on écrit ou modifie un fichier de CI/CD (`.gitlab-ci.yml`,
`Dockerfile`, `docker-compose.yml`), de l'infra as code (Terraform, Ansible),
ou une config de monitoring/alerting.

## Étapes

### 1. CI/CD : reproductible et rapide à diagnostiquer
1. Pipeline idempotent : rejouer le même job sur le même commit produit le
   même résultat, jamais dépendant d'un état externe muable non versionné.
2. Chaque étape échoue vite et clairement (fail-fast) : pas de step qui
   continue silencieusement après une erreur (`continue-on-error` seulement
   si explicitement voulu, jamais par défaut).
3. Secrets jamais en dur dans le pipeline ni loggés en clair : variables
   protégées/masquées côté CI, jamais un `echo $SECRET` de debug oublié.
4. Cache de dépendances explicite et versionné (clé de cache liée au
   lockfile), jamais un cache qui masque une dépendance cassée.

### 2. Infra as code
1. État versionné et déclaratif (Terraform state, Ansible inventory) : jamais
   de modification manuelle d'une ressource gérée par l'IaC (drift silencieux
   au prochain apply).
2. `plan`/`dry-run` toujours lu avant un `apply`/exécution réelle sur un
   environnement partagé : jamais d'apply direct sans revue du diff d'infra.
3. Secrets d'infra (clés, tokens) dans un vault/secret manager, jamais commit
   en clair même dans un repo privé.

### 3. Monitoring et alerting
1. Une alerte qui se déclenche doit être actionnable : sinon c'est du bruit
   qui désensibilise l'équipe (alert fatigue), à retirer ou reformuler.
2. Logs structurés (JSON ou format parsable), jamais uniquement du texte libre
   sur les événements qui doivent être requêtables en incident.
3. Healthcheck distinct du monitoring métier : un service "up" (process
   vivant) n'est pas la même chose qu'un service "sain" (répond correctement
   aux requêtes réelles).

### 4. Incident response
1. Rollback toujours possible et testé avant qu'il soit nécessaire en urgence
, un rollback qu'on découvre cassé pendant l'incident aggrave la panne.
2. Post-mortem sans blâme individuel, focalisé sur la cause systémique (ce
   qui a permis l'incident), pas sur qui a appuyé sur quoi.

## Sortie / checkpoint
Pipeline/infra conforme aux sections ci-dessus, `plan`/`dry-run` lu et cité
avant tout `apply` réel sur un environnement partagé.

## Garde-fous
- Jamais d'`apply`/déploiement automatique sur un environnement partagé sans
  confirmation humaine explicite (cohérent avec la doctrine générale du
  framework : les actions difficiles à annuler restent un point de passage
  humain).
- Cette brique n'a pas encore de vécu de production Xefi dédié : à confronter
  au premier vrai audit infra/CI réel, pas à traiter comme doctrine éprouvée.

## Origine
Sourcé sur les 12-factor app (config par variables d'environnement, logs
comme flux d'événements), DORA metrics (Accelerate : Forsgren/Humble/Kim :
fréquence de déploiement, lead time, MTTR, taux d'échec des changements) et
les pratiques établies GitOps/IaC. Mécanismes réécrits, pas de texte copié.
Recherche de marché, pas de retour de production interne à ce stade.
