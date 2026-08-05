# xefi-superpowers

**Notre version de [superpowers](https://github.com/obra/superpowers), en gardant la main.**
Un framework d'agents et de skills Claude Code pour tout le cycle de dev — pas
seulement la review — construit en réécrivant les meilleures idées du marché
à notre voix, jamais en dépendant d'un repo tiers.

> Repo de test de la méthode de travail de g.compigni avec Claude Code.
> `xefi-mr-review` (repo séparé) est l'implémentation spécialisée de la seule
> étape review/gate de ce framework, câblée en CI GitLab — ce repo-ci couvre
> tout le reste : brainstorm, spec, plan, TDD, code, debug, gate, ship.

## Sommaire

- [Comment on écrit et on gouverne nos agents](./doc/COMMENT-ON-ECRIT-NOS-AGENTS.md) — le document à lire pour tout comprendre, avec schémas
- [Pourquoi une version à nous](#pourquoi-une-version-à-nous)
- [Positionnement](#positionnement)
- [Le pipeline](#le-pipeline)
- [Ce qu'il y a dedans](#ce-quil-y-a-dedans)
- [La règle qui garantit qu'on maîtrise](#la-règle-qui-garantit-quon-maîtrise)
- [Quickstart](#quickstart)
- [Statut](#statut)
- [Licence](#licence)

## Pourquoi une version à nous

[obra/superpowers](https://github.com/obra/superpowers) encode une bonne
discipline générique (brainstorming, TDD, debugging systématique, review à
contexte frais). Mais une méthode générique ne porte pas nos conventions
Xefi, nos stacks réelles (Nuxt/Vuetify, Laravel, React), ni notre exigence
propre : **défaut = échec** — un travail déclaré "fini" n'est jamais cru sur
parole, il doit être prouvé (voir `arbitre`, l'agent qui incarne cette règle
et qui n'est couvert par aucune des sources marché consultées).

Plutôt que d'installer superpowers tel quel, on a réécrit chaque idée utile
dans notre gabarit, avec notre voix, nos exemples, notre stack — et on ne
dépend jamais d'un repo externe pour que notre pipeline continue de tourner.

## Positionnement

- **Ce repo** = la **méthode** : *comment* le travail coule (skills) et *qui*
  l'exécute (agents).
- **`xefi-mr-review`** ([repo séparé](https://github.com/techmefr/xefi-mr-review)) = une
  implémentation spécialisée : uniquement l'étape review/gate, câblée en CI
  GitLab, un dossier par stack.
- **Agents métier** (`vue-nuxt-builder`, `laravel-builder`, `sql-es-tuner`,
  les reviewers par stack, `gandalf`, `arbitre`) = la couche qui exécute
  réellement le travail, branchée dans les slots du pipeline ci-dessous.

## Le pipeline

```mermaid
flowchart LR
    A[brainstorm] --> B[spec]
    B --> C[archi]
    C --> D[plan]
    D --> E[tdd]
    E --> F[code]
    F --> G[debug]
    G --> H[gate — arbitre]
    H --> I[review — reviewers par stack]
    I --> J[ship — gandalf]
    J --> K[finish]
```

Deux garanties tiennent tout le pipeline : **contexte frais** (celui qui
juge/review n'a jamais "vu" le code s'écrire — `arbitre`, les reviewers,
`gandalf`) et **défaut = échec** (rien n'est cru sans preuve citée).

## Ce qu'il y a dedans

### Skills — le pipeline

| Skill | Étape | Ce qu'il fait |
|---|---|---|
| `using-construct` | 0 | Discipline d'utilisation du framework, point d'entrée |
| `start-feature` | 0 | Démarre une feature (worktree) |
| `brainstorm` | 1 | Explore intention/besoin avant tout code |
| `spec` | 2 | Cadre le besoin en critères vérifiables |
| `archi` | 3 | Décisions d'architecture, avant le plan |
| `plan` | 4 | Découpe le travail en étapes vérifiables |
| `tdd` | 5 | Test-driven development, doctrine test-casebook |
| `code` | 6 | Implémentation |
| `typescript-patterns` | 6 | Patterns TS/JS purs (typage, async, closures) — vécu de production réel |
| `php-patterns` | 6 | Patterns PHP purs (typage, OOP, erreurs) — sourcé PSR/marché |
| `vue-nuxt-vuetify-conventions` | 6 | Conventions Nuxt/Vue/Vuetify — vécu de production réel |
| `react-nextjs-conventions` | 6 | Conventions React/Next.js — sourcé marché |
| `nestjs-node-conventions` | 6 | Conventions NestJS/Node — DI, DTO, Zod, Prisma |
| `go-conventions` | 6 | Conventions Go — concurrence, erreurs, contexte (sourcé marché) |
| `dotnet-conventions` | 6 | Conventions C#/.NET — async, IDisposable, DI, EF Core (sourcé marché) |
| `python-conventions` | 6 | Conventions Python — typage, erreurs, async (sourcé marché) |
| `java-conventions` | 6 | Conventions Java — immutabilité, erreurs, concurrence, Spring (sourcé marché) |
| `seo` | 6 | Checklist SEO technique pour pages publiques (sourcé Google/web.dev) |
| `debug` | support | Debugging systématique |
| `gate` | 7 | Vérification à froid avant merge — voir agent `arbitre` |
| `review` | 8 | Review de diff — voir agents reviewers par stack |
| `over-engineering-review` | 9 | Angle suppression exclusif : code mort, sur-abstraction, yagni |
| `simplify` | 9 | Applique les simplifications identifiées |
| `ship` | 10 | Merge + notification, voir agent `gandalf` |
| `finish` | 11 | Nettoie la worktree, met à jour la branche de base |
| `merge-worktree` | 11 | Mécanique de merge multi-worktree |
| `extract-conventions` | maintenance | Génère des conventions depuis le code réel existant |
| `choose-model` | transverse | Décide Haiku/Sonnet/Opus pour un nouvel agent ou une tâche ponctuelle |
| `dispatch-parallel` | transverse | Découpe une tâche en sous-agents parallèles sur des périmètres disjoints |
| `writing-skills` | transverse (méta) | Comment écrire/réviser une skill de ce framework |
| `portless-ready` | infra | Rend une stack portless (alias HTTPS, hygiène des ports) |

### Agents

| Agent | Rôle | Statut |
|---|---|---|
| `arbitre` | GATE à contexte frais — verdict PASS/NEEDS_WORK, jamais d'édition, jamais de bénéfice du doute | Vécu de production réel |
| `gandalf` | Gate final de MR — gate de tests + délègue la review + `/code-review` + `/security-review` | Vécu de production réel |
| `elrond` | Orchestrateur — détecte le stack et délègue au bon reviewer, ne review jamais lui-même | Vécu de production réel |
| `aragorn` | Reviewer Nuxt/Vue/Vuetify | Vécu de production réel |
| `gimli` | Reviewer PHP/Laravel — incertitude en questions (g.compigni débute sur ce stack) | Vécu de production réel |
| `legolas` | Reviewer React | Sourcé via test-casebook |
| `boromir` | Reviewer Go — incertitude en questions | Sourcé marché |
| `theoden` | Reviewer C#/.NET — incertitude en questions | Sourcé marché |
| `frodo` | Reviewer JS/TS backend générique (NestJS/Node) — vraie expertise, style assertif | Vraie expertise |
| `vue-nuxt-builder` | Implémente du code Vue3/Nuxt3 (jamais reviewer de son propre code) | Écrit, pas encore dogfoodé |
| `laravel-builder` | Implémente du code Laravel/Eloquent (jamais reviewer de son propre code) | Écrit, pas encore dogfoodé |
| `sql-es-tuner` | Tuning SQL (MySQL/SQL Server) et mapping/indexation Elasticsearch-Scout | Écrit, pas encore dogfoodé |
| `seo-auditor` | Audit SEO technique d'une page/site déjà en ligne, jamais d'édition | Écrit, pas encore dogfoodé |

Détail complet : [`CATALOG.md`](./CATALOG.md) (registre + backlog de sourcing,
avec chaque idée créditée à sa source réelle) et [`CONVENTIONS.md`](./CONVENTIONS.md)
(le gabarit unique et les règles A/B/C).

## La règle qui garantit qu'on maîtrise

On ne branche jamais un repo externe en dépendance. On lit → on extrait le
mécanisme → on **réécrit** dans notre gabarit unique → on crédite la source
dans `CATALOG.md`. Ça garantit deux choses : personne en amont ne peut casser
notre pipeline en changeant son repo, et tout est écrit pareil (donc
maintenable). Détail dans [`CONVENTIONS.md`](./CONVENTIONS.md).

## Quickstart

Chaque skill/agent est un fichier markdown autonome (frontmatter + corps),
au format natif Claude Code :

1. Copier le(s) fichier(s) voulu(s) dans `.claude/agents/` ou `.claude/skills/`
   du repo cible.
2. Les skills du pipeline s'invoquent en séquence (`brainstorm` → `spec` →
   ... → `finish`) ou à la carte selon le besoin.
3. Les agents s'invoquent via l'outil `Agent` / `Task` de Claude Code,
   directement par nom (ex `elrond` pour une review multi-stack, ou
   directement `aragorn`/`gimli`/... si le stack est déjà connu).

## Statut

Démonstrateur actif : la doctrine (gabarit, règles A/B/C, défaut=échec,
contexte frais) est stable et appliquée, certains agents ont un vécu de
production réel (`aragorn`, `gimli`, `gandalf`, `arbitre`, `elrond`), d'autres
sont écrits mais pas encore dogfoodés (`vue-nuxt-builder`, `laravel-builder`,
`sql-es-tuner`) ou sourcés marché sans vécu interne encore (`boromir`,
`theoden`, `go-conventions`, `dotnet-conventions`). Le détail exact par ligne
est dans `CATALOG.md`.

## Licence

Pas encore de licence choisie — repo interne Xefi à ce stade (références à
des repos/outils internes), pas destiné à être public tel quel.
