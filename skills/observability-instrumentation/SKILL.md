---
name: observability-instrumentation
description: Use quand on ajoute des logs, métriques, traces ou alertes dans du code applicatif, définit d'abord les questions que l'on-call se posera, avant d'instrumenter quoi que ce soit, pour éviter de collecter des données inutiles. Complète devops-conventions (qui couvre le pipeline/l'infra) au niveau du code lui-même.
---

# observability-instrumentation

Étape 6 du pipeline (`WORKFLOW.md`), en complément de `devops-conventions`
(qui couvre CI/CD/infra/monitoring au niveau plateforme) : ici l'instrumentation
au niveau du code applicatif : où logger, quelle métrique, quel label.

## Quand
Dès qu'on ajoute ou modifie du logging, une métrique, une trace ou une alerte
dans du code applicatif : jamais en ajoutant de l'instrumentation "au cas où"
sans question précise derrière.

## Étapes

### 1. Définir les questions avant d'instrumenter
1. Formuler 2 à 4 questions concrètes que l'on-call se posera en incident
   ("pourquoi cette requête est-elle lente ?", "combien d'utilisateurs sont
   affectés ?"), **avant** d'écrire le premier log ou la première métrique.
2. Chaque donnée collectée doit répondre à au moins une de ces questions : 
   une métrique/log qui ne répond à aucune question posée est du bruit à ne
   pas ajouter.

### 2. Logs structurés
1. Format structuré (JSON), jamais du texte libre pour un événement qui doit
   être requêtable en incident.
2. Correlation ID obligatoire sur toute chaîne d'appels traversant plusieurs
   services/couches : sans lui, impossible de relier les logs d'une même
   requête.
3. Redaction des données personnelles/sensibles (PII) avant écriture : jamais
   un email, un mot de passe ou une donnée client en clair dans un log.

### 3. Métriques : anti-cardinalité
1. Métriques RED (Rate/Errors/Duration) pour les services, USE
   (Utilization/Saturation/Errors) pour les ressources : grille de départ,
   pas la seule possible, mais un défaut sain.
2. Labels de métriques **bornés** : jamais un user ID, une URL brute ou tout
   autre identifiant à cardinalité illimitée en label : explosion de
   cardinalité qui rend le système de métriques inutilisable ou hors de prix.
3. Traces distribuées (OpenTelemetry ou équivalent déjà en place) posées aux
   frontières de service, pas à chaque fonction interne.

### 4. Alerting : symptom-based
1. Une alerte se déclenche sur un **symptôme observable par l'utilisateur**
   (latence, taux d'erreur), jamais directement sur une cause infra
   (CPU haut) sauf si ce lien est déjà prouvé causal.
2. Vérification finale obligatoire : forcer volontairement la condition
   d'alerte (ou la simuler) pour confirmer qu'elle se déclenche réellement : 
   une alerte jamais testée est une alerte dont on ne sait pas si elle marche.

## Sortie / checkpoint
Instrumentation ajoutée répond explicitement à une des questions on-call
formulées en étape 1 ; aucun label à cardinalité non bornée introduit ;
alerte testée en conditions simulées avant d'être considérée fiable.

## Garde-fous
Ne jamais instrumenter par réflexe ("on ne sait jamais") sans question
on-call identifiée derrière : le coût de collecte/stockage n'est pas gratuit
et le bruit noie le signal utile en incident réel. Jamais de PII en clair
dans un log, même en environnement de test.

## Origine
Réécriture du skill `observability-and-instrumentation` d'un catalogue de skills dev généralistes du marché, 
la règle "définir les questions avant d'instrumenter", les métriques RED/USE,
la règle anti-cardinalité et l'alerting symptom-based sont repris tels quels,
réécrits en français au gabarit Xefi.
