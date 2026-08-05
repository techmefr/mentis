---
name: writing-skills
description: Use quand il faut créer une nouvelle skill (ou réviser une skill existante) pour ce framework, applique le gabarit unique, vérifie qu'aucune brique existante ne couvre déjà le besoin, et crédite la source si l'idée vient d'ailleurs.
---

# writing-skills

Brique transverse (méta) : c'est la skill qui explique comment écrire les
autres skills. S'applique dès qu'un manque est identifié dans le pipeline ou
qu'une idée sourcée mérite d'être réécrite à notre sauce (Règle B).

## Quand
- Un manque est repéré dans le pipeline (ex : "il manque un routeur de
  modèle" → `choose-model`).
- Une idée vue ailleurs (repo marché, article, aitmpl.com, superpowers)
  semble utile mais n'existe pas encore chez nous.
- Une skill existante ne colle plus à l'usage réel et doit être révisée.

## Étapes
1. **Vérifier qu'aucune brique existante ne couvre déjà le besoin** : lire
   `CATALOG.md` et le tableau skills de `README.md` avant d'écrire quoi que ce
   soit. Un doublon coûte plus cher qu'un manque (Règle B, checklist
   d'adoption).
2. **Isoler le mécanisme réel**, pas l'emballage : si la skill est sourcée
   d'un repo externe, lire le concept jusqu'à pouvoir l'expliquer sans le
   fichier source sous les yeux.
3. **Écrire au gabarit unique** (`CONVENTIONS.md`) :
   - frontmatter `name` + `description` qui commence par "Use quand..."
   - `# nom`
   - `## Quand`
   - `## Étapes`
   - `## Sortie / checkpoint`
   - `## Garde-fous`
   - `## Origine` : jamais vide : soit une source externe créditée
     honnêtement, soit "pas de source externe, synthèse interne".
4. **Placer la skill dans le pipeline** si elle a une étape numérotée (voir le
   tableau `README.md`), ou la marquer "transverse" si elle s'applique partout
   sans être une étape séquentielle (ex `choose-model`, `dispatch-parallel`).
5. **Mettre à jour `CATALOG.md`** (registre + traçabilité de la source) et le
   tableau skills de `README.md` dans le même geste, une skill non
   référencée dans les deux devient invisible et se fait réécrire en double
   plus tard.
6. **Rester publiable** (Règle C) : pas de nom de projet réel, pas de secret,
   un rôle générique ("le back Laravel") jamais un nom de repo interne : sauf
   dans `xefi-mr-review` qui a un statut différent (preuve de prod, noms réels
   assumés).

## Sortie / checkpoint
Un fichier `skills/<nom>/SKILL.md` complet au gabarit, référencé dans
`CATALOG.md` et dans le tableau `README.md`, avec une section `Origine` non
vide.

## Garde-fous
- Jamais de skill sans `## Origine` : l'honnêteté sur la source (interne vs
  sourcée marché vs réécrite d'un repo précis) est structurelle, pas
  optionnelle.
- Jamais d'installation d'un repo externe comme dépendance : on lit, on
  réécrit, on crédite (Règle B) : jamais un `git submodule` ou un import
  runtime vers un repo tiers.
- Une skill qui duplique une brique existante est une régression, pas un
  ajout : vérifier l'étape 1 avant d'écrire, pas après.

## Origine
Réécriture de la skill `writing-skills` d'un framework de skills/agents du marché, chez eux elle
documente leur propre gabarit ; ici elle documente le nôtre (le gabarit unique
de `CONVENTIONS.md`), avec en plus la checklist d'adoption de la Règle B
(vérifier les doublons, créditer la source) qui n'existe pas telle quelle côté
superpowers.
