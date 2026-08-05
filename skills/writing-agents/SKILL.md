---
name: writing-agents
description: Use quand il faut créer un nouvel agent (ou réviser un agent existant) pour ce framework, applique le gabarit unique en 7 piliers (RÔLE, MÉMOIRE, BOUCLE, OUTILS & PÉRIMÈTRE, GARDE-FOUS, REVIEW CONTEXTE FRAIS, TRACE), vérifie qu'aucun agent existant ne couvre déjà le rôle, et choisit le bon modèle.
---

# writing-agents

Brique transverse (méta), pendant de `writing-skills` mais pour les agents :
un agent a un rôle exécutable persistant (revoit, construit, audite,
tranche), une skill est une procédure appliquée à l'intérieur du pipeline.

## Quand
- Un manque est repéré dans le roster d'agents (ex : "il manque un audit
  SEO dédié" → `seo-auditor`).
- Une idée sourcée (repo marché, catalogue d'agents) mérite d'être réécrite
  en agent Xefi.
- Un agent existant a un rôle qui a dérivé de sa description d'origine et
  doit être clarifié ou scindé.

## Étapes
1. **Vérifier qu'aucun agent existant ne couvre déjà le rôle** : lire
   `CATALOG.md` et le tableau agents de `README.md` avant d'écrire quoi que
   ce soit. Un agent qui fait presque la même chose qu'un autre finit par
   créer de la confusion sur lequel invoquer.
2. **Distinguer rôle d'agent vs étape de skill** : si la brique est une
   procédure appliquée pendant une étape du pipeline (ex vérifier une
   convention avant de commit), c'est une skill (`writing-skills`) ; si c'est
   un rôle qui reçoit une tâche, agit avec ses propres outils et rend un
   verdict/livrable autonome, c'est un agent.
3. **Écrire au gabarit unique en 7 piliers** (voir
   `doc/COMMENT-ON-ECRIT-NOS-AGENTS.md` §4) :
   - **1. RÔLE** : une seule responsabilité, énoncée avec ce que l'agent
     n'est *pas* (les confusions à éviter avec les agents voisins).
   - **2. MÉMOIRE** : ce qui persiste entre deux invocations (conventions
     dans MEMORY.md) et ce qui ne persiste jamais (aucun état de session à
     session, chaque tâche relit le réel).
   - **3. BOUCLE** : les étapes concrètes, avec une **condition de sortie
     explicite et bornée** (jamais "je continue tant que ce n'est pas
     parfait" : un nombre d'itérations maximum ou un critère binaire).
   - **4. OUTILS & PÉRIMÈTRE** : ce qui est autorisé et interdit, en clair.
   - **5. GARDE-FOUS** : ce qui checkpoint un humain avant une action difficile
     à annuler (migration destructive, merge, push en Ready).
   - **6. REVIEW CONTEXTE FRAIS** : qui relit ce travail, avec un contexte
     neuf : un agent ne se certifie jamais lui-même "prêt".
   - **7. TRACE** : ce que la sortie de fin de tâche contient toujours
     (fichiers touchés, preuve de test, statut).
4. **Choisir le modèle** via `choose-model` (Haiku/Sonnet/Opus), documenté
   dans le frontmatter `model:`.
5. **Mettre à jour `CATALOG.md`** (registre + traçabilité) et le tableau
   agents de `README.md` dans le même geste.

## Sortie / checkpoint
Un fichier `agents/<nom>.md` complet avec les 7 piliers, référencé dans
`CATALOG.md` et le tableau `README.md`, `model:` renseigné et justifié.

## Garde-fous
- Jamais d'agent sans pilier 6 (REVIEW CONTEXTE FRAIS) explicite : même un
  agent d'audit en lecture seule doit dire clairement comment ses résultats
  repassent par le pipeline normal.
- Jamais de Write/Edit accordé à un agent de review/audit (`aragorn`,
  `gimli`, `seo-auditor`, `security-auditor`, etc.), son scope est de
  rapporter, jamais de corriger lui-même.
- Un agent qui duplique un rôle existant est une régression, pas un ajout :
  vérifier l'étape 1 avant d'écrire.

## Origine
Synthèse interne : formalisation du gabarit 7 piliers déjà en usage sur tous
les agents de ce framework (`doc/COMMENT-ON-ECRIT-NOS-AGENTS.md` §4), packagé
en skill invocable pour symétrie avec `writing-skills`.
