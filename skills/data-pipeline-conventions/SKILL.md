---
name: data-pipeline-conventions
description: Use quand on écrit/revoit un pipeline de données (ETL/ELT), une modélisation de schéma analytique, ou une validation de qualité de données — conventions pour la fiabilité et la traçabilité des données, distinct du code applicatif transactionnel. Pas de vécu de production Xefi dédié à ce stade, sourcé sur les pratiques établies (dbt, data quality dimensions).
---

# data-pipeline-conventions

Étape 6 du pipeline (`WORKFLOW.md`), pour le code qui déplace/transforme de la
donnée entre systèmes (ETL/ELT, entrepôt analytique) — distinct du code
applicatif transactionnel (CRUD métier) couvert par les conventions
Laravel/NestJS.

## Quand
Dès qu'on écrit ou modifie un pipeline de données, une transformation
analytique, ou une définition de schéma de données destinée à l'analyse
(pas la base transactionnelle de l'app elle-même).

## Étapes

### 1. Idempotence et reproductibilité — la base non négociable
1. Un pipeline rejoué deux fois sur la même source produit le même résultat
   (idempotent) — jamais un `INSERT` qui duplique à chaque exécution sans
   déduplication ni `UPSERT`.
2. Chaque exécution est traçable : source, version du code de transformation,
   horodatage — pour pouvoir remonter à "quelle version du pipeline a produit
   cette ligne".
3. Transformations testées sur un échantillon avant un run complet sur la
   donnée de prod, surtout pour une transformation destructive (remplacement
   complet d'une table).

### 2. Qualité de données — vérifiée, pas supposée
1. Validation explicite des contraintes attendues (non-null sur les champs
   requis, unicité des clés, plages de valeurs plausibles) à l'entrée et à la
   sortie du pipeline — un échec de validation bloque le pipeline, il ne
   passe pas silencieusement en produisant une donnée fausse.
2. Les quatre dimensions de qualité vérifiées explicitement quand
   pertinentes : complétude (rien de manquant), exactitude (valeur correcte),
   cohérence (même fait, même valeur entre systèmes), fraîcheur (donnée à
   jour au moment de l'usage).
3. Une source externe (API tierce, fichier partenaire) est traitée comme
   non fiable par défaut : schéma vérifié à chaque ingestion, pas supposé
   stable dans le temps.

### 3. Modélisation de schéma analytique
1. Séparation claire entre couche brute (donnée telle que reçue, jamais
   modifiée) et couche transformée (donnée nettoyée/agrégée) — jamais de
   transformation qui écrase la donnée brute originale sans conservation.
2. Nommage de colonnes/tables cohérent et documenté (grain de la table
   explicite : une ligne = quoi exactement) — une table sans grain défini
   invite aux jointures fausses.
3. Historisation (SCD - slowly changing dimension) explicite quand une valeur
   change dans le temps et que l'historique compte pour l'analyse, plutôt
   qu'un simple `UPDATE` qui perd l'état précédent.

### 4. Performance et coût
1. Traitement incrémental (seulement les nouvelles/modifiées données) plutôt
   qu'un retraitement complet par défaut, sauf si le volume le permet
   vraiment sans coût significatif.
2. Partitionnement/clustering de table aligné sur les patterns de requête
   réels (filtre le plus fréquent), pas choisi arbitrairement.

## Sortie / checkpoint
Pipeline conforme aux quatre sections ci-dessus ; les validations de qualité
de données tournent et sont vertes avant que le résultat soit considéré
utilisable en aval.

## Garde-fous
Jamais d'exécution d'un pipeline destructif (remplacement complet d'une table
de prod) sans confirmation humaine explicite. Cette brique n'a pas encore de
vécu de production Xefi dédié — à confronter au premier vrai pipeline de
données réel, pas à traiter comme doctrine éprouvée.

## Origine
Sourcé sur les conventions établies dbt (couches staging/intermediate/marts,
tests de schéma), les dimensions de qualité de données du DAMA-DMBOK
(complétude/exactitude/cohérence/fraîcheur), et les patterns SCD classiques
en modélisation dimensionnelle (Kimball). Mécanismes réécrits, pas de texte
copié. Recherche de marché, pas de retour de production interne à ce stade.
