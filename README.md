# xefi-superpowers

Ma version d'un framework équivalent vu sur le marché open source, en
gardant la main dessus. Un framework d'agents et de skills Claude Code pour
tout le cycle de dev, pas seulement la review, construit en réécrivant les
meilleures idées du marché à ma voix, sans jamais dépendre d'un repo tiers.

> Repo de test de ma méthode de travail avec Claude Code (g.compigni).
> `xefi-mr-review` (repo séparé) est l'implémentation spécialisée de la seule
> étape review/gate de ce framework, câblée en CI GitLab. Ce repo-ci couvre
> tout le reste : brainstorm, spec, plan, TDD, code, debug, gate, ship.

## Sommaire

- [Comment j'écris et je gouverne mes agents](./doc/COMMENT-ON-ECRIT-NOS-AGENTS.md) — le doc à lire pour tout comprendre, avec schémas
- [Pourquoi ma propre version](#pourquoi-ma-propre-version)
- [Positionnement](#positionnement)
- [Le pipeline](#le-pipeline)
- [Ce qu'il y a dedans](#ce-quil-y-a-dedans)
- [La règle qui garantit que je maîtrise](#la-règle-qui-garantit-que-je-maîtrise)
- [Quickstart](#quickstart)
- [Statut](#statut)
- [Licence](#licence)

## Pourquoi ma propre version

Un framework équivalent du marché open source encode déjà une bonne
discipline générique : brainstorming, TDD, debugging systématique, review à
contexte frais. Mais une méthode générique ne porte pas mes conventions
Xefi, mes stacks réelles (Nuxt/Vuetify, Laravel, React), ni mon exigence
propre, le défaut = échec : un travail déclaré "fini" n'est jamais cru sur
parole, il doit être prouvé. C'est le rôle de `arbitre`, l'agent qui
incarne cette règle et qu'aucune des sources marché consultées ne couvre.

Plutôt que d'installer un tel framework tel quel, j'ai réécrit chaque idée
utile dans mon gabarit, avec ma voix, mes exemples, ma stack. Je ne dépends
jamais d'un repo externe pour que mon pipeline continue de tourner.

## Positionnement

- **Ce repo** = la **méthode** : *comment* le travail coule (skills) et *qui*
  l'exécute (agents).
- **`xefi-mr-review`** (repo séparé) = une
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

Deux garanties tiennent tout le pipeline. Le contexte frais : celui qui
juge ou review n'a jamais vu le code s'écrire (`arbitre`, les reviewers,
`gandalf`). Le défaut = échec : je ne crois rien sans preuve citée.

## Ce qu'il y a dedans

### Skills — le pipeline

| Skill | Étape | Ce qu'il fait |
|---|---|---|
| `using-construct` | 0 | Discipline d'utilisation du framework, point d'entrée |
| `start-feature` | 0 | Démarre une feature (worktree) |
| `brainstorm` | 1 | Explore intention/besoin avant tout code |
| `spec` | 2 | Cadre le besoin en critères vérifiables |
| `archi` | 3 | Décisions d'architecture, avant le plan |
| `api-design` | 3 | Design d'API contract-first (loi de Hyrum, extension vs rupture) |
| `documentation-adr` | 3 | Documente une décision significative (template ADR, jamais supprimé) |
| `deprecation-migration` | transverse | Cadre une dépréciation/migration (Strangler, Adapter, Feature Flag, Expand/Contract) |
| `wayfinder` | transverse | Découpe un chantier incertain en carte de tickets Jira (parent + enfants typés) |
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
| `accessibility` | 6 | Checklist a11y technique (sémantique, clavier, contraste, ARIA) — sourcé WCAG 2.2 |
| `qa-exploratory-testing` | 8 (complément) | Test manuel/exploratoire d'un parcours, distinct de tdd — sourcé ISTQB/session-based testing |
| `devops-conventions` | 6 (infra/CI) | Conventions CI/CD, IaC, monitoring/alerting, incident response — sourcé 12-factor/DORA |
| `data-pipeline-conventions` | 6 (data) | Conventions ETL/ELT, qualité de données, modélisation analytique — sourcé dbt/DAMA-DMBOK |
| `observability-instrumentation` | 6 | Où logger/quelle métrique/quel label — complète devops-conventions au niveau code |
| `handoff` | transverse | Document de passation entre deux sessions sur la même tâche, sans dupliquer |
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
| `writing-agents` | transverse (méta) | Comment écrire/réviser un agent de ce framework (gabarit 7 piliers) |
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
| `accessibility-auditor` | Audit a11y technique d'une page/site déjà en ligne, jamais d'édition | Écrit, pas encore dogfoodé |
| `qa-tester` | Test manuel/exploratoire d'un parcours sur une app qui tourne, jamais d'édition | Écrit, pas encore dogfoodé |
| `security-auditor` | Audit sécurité statique dédié (code/config/dépendances), lecture seule, complète `/security-review` natif | Écrit, pas encore dogfoodé |
| `architecture-debt-auditor` | Audit périodique de dette d'architecture (hot-spots git, test de suppression), jamais d'édition | Écrit, pas encore dogfoodé |

Détail complet : [`CATALOG.md`](./CATALOG.md) (registre + backlog de sourcing,
avec chaque idée créditée à sa source réelle) et [`CONVENTIONS.md`](./CONVENTIONS.md)
(le gabarit unique et les règles A/B/C).

## La règle qui garantit que je maîtrise

Je ne branche jamais un repo externe en dépendance. Je lis → j'extrais le
mécanisme → je réécris dans mon gabarit unique → je crédite la source dans
`CATALOG.md`. Ça garantit deux choses : personne en amont ne peut casser
mon pipeline en changeant son repo, et tout est écrit de la même façon
(donc maintenable). Détail dans [`CONVENTIONS.md`](./CONVENTIONS.md).

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

Démonstrateur actif : ma doctrine (gabarit, règles A/B/C, défaut=échec,
contexte frais) est stable et appliquée, certains agents ont un vécu de
production réel (`aragorn`, `gimli`, `gandalf`, `arbitre`, `elrond`),
d'autres sont écrits mais pas encore dogfoodés (`vue-nuxt-builder`,
`laravel-builder`, `sql-es-tuner`) ou sourcés marché sans vécu interne
encore (`boromir`, `theoden`, `go-conventions`, `dotnet-conventions`). Le
détail exact ligne par ligne est dans `CATALOG.md`.

## Licence

Pas encore de licence choisie — repo interne pour l'instant, pas destiné à
être public tel quel.
