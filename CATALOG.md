# construct : catalogue des briques & backlog de sourcing

> **construct = superpowers, version Xefi, qu'on maîtrise.** Un framework *à nous*, enrichi en
> continu en **réécrivant** (règle B, `CONVENTIONS.md`) les meilleures idées/agents d'autres
> repos du marché, jamais en dépendant d'eux. Ce fichier tient : **1)** ce qu'on a, **2)** ce qu'on peut
> réécrire pour compléter/améliorer. Vivant : on l'étend au fil de l'eau.
> Statuts : ✅ réécrit chez nous / 🟡 écrit, pas encore dogfoodé / 🔜 à câbler / 🔎 à miner / ✕ écarté.

## 1. Registre des briques

### Skills : le pipeline (`WORKFLOW.md` §2)
| Brique | Étape / couche | Origine (idée réécrite) | Maturité |
|---|---|---|---|
| start-feature | 0 (worktree) | interne starfleet + un skill marché de gestion de worktrees | 🟡 |
| brainstorm | 1 | natif `brainstorming` | 🟡 |
| spec | 2 | un catalogue de skills du marché (grill-with-docs) + interne | 🟡 |
| archi | 3 | interne graphify (+ dédup à construire) | 🔜 |
| plan | 4 | un catalogue de skills du marché (planning-and-task-breakdown) | 🟡 |
| tdd | 5 | Xefi `test-casebook` + des patterns d'agents long-running du marché (default-FAIL contract) | 🟡 |
| code | 6 | natif + interne | 🟡 |
| vue-nuxt-vuetify-conventions | 6 | plusieurs catalogues de skills Vue/Nuxt/Vuetify du marché (patterns Vue, Nuxt4, composables Nuxt, Vuetify) + un linter Nuxt/Vue du marché (correctness/sécurité) + un projet open source TypeScript du marché (a11y/bundle) + retours de review internes Xefi dénominalisés (patterns récurrents) | 🟡 |
| react-nextjs-conventions | 6 | un catalogue de skills React du marché (best practices) + un catalogue de skills React/Node du marché (redux-toolkit) + un catalogue de skills shadcn du marché + un linter React du marché (section correctness/sécurité) + un projet open source TypeScript du marché (a11y/bundle) | 🟡 (écrit, pas encore dogfoodé) |
| over-engineering-review | 9 | un outil de review orienté suppression du marché (angle suppression, tags, score net de lignes) | 🟡 |
| nestjs-node-conventions | 6 | un catalogue de skills NestJS du marché + une skill TypeScript avancée du marché + un catalogue de skills React/Node du marché (prisma/trpc/zod) | 🟡 (écrit, pas encore dogfoodé ; première brique construct back Node) |
| typescript-patterns | 6 | synthèse interne (vécu de production réel g.compigni sur TS/JS pur) | 🟢 |
| php-patterns | 6 | PHP-FIG (PSR-12) + doc officielle PHP | 🟡 (sourcé marché, même statut d'incertitude que gimli (g.compigni débute en PHP)) |
| python-conventions | 6 | PEP 484/526/604/8 + ruff + mypy/pyright | 🟡 (sourcé marché, pas de vécu de production interne, même statut que go-conventions) |
| java-conventions | 6 | Effective Java (Bloch) + SpotBugs/Error Prone + conventions Spring établies | 🟡 (sourcé marché, pas de vécu de production interne, même statut que go-conventions) |
| seo | 6 | Google Search Central + web.dev (Core Web Vitals, structured data) | 🟡 (sourcé marché, pas de vécu de production Xefi dédié SEO) |
| accessibility | 6 | WCAG 2.2 (AA) + MDN + W3C ARIA APG | 🟡 (sourcé marché, pas de vécu de production Xefi dédié a11y) |
| qa-exploratory-testing | 8 (complément) | littérature établie du testing exploratoire (session-based testing) + ISTQB (boundary testing) | 🟡 (sourcé marché, pas de vécu de production Xefi dédié QA) |
| devops-conventions | 6 (infra/CI) | 12-factor app + DORA metrics (Accelerate) + pratiques GitOps/IaC établies | 🟡 (sourcé marché, pas de vécu de production Xefi dédié) |
| data-pipeline-conventions | 6 (data) | conventions dbt + DAMA-DMBOK (dimensions qualité) + modélisation dimensionnelle Kimball | 🟡 (sourcé marché, pas de vécu de production Xefi dédié) |
| deprecation-migration | transverse | un catalogue de skills dev généralistes du marché (5 questions + 4 patterns) | 🟢 (réécriture directe, mécanisme repris tel quel) |
| api-design | 3 | un catalogue de skills dev généralistes du marché (loi de Hyrum, One-Version Rule) | 🟢 (réécriture directe) |
| observability-instrumentation | 6 | un catalogue de skills dev généralistes du marché (questions on-call, RED/USE, anti-cardinalité) | 🟢 (réécriture directe) |
| documentation-adr | 3 | un catalogue de skills dev généralistes du marché (template ADR 5-6 champs) | 🟢 (réécriture directe) |
| wayfinder | transverse | un auteur de skills reconnu du marché (ticket parent 5 sections + enfants typés) | 🟢 (réécriture directe, adapté Jira) |
| handoff | transverse | un auteur de skills reconnu du marché (référencer par chemin, jamais dupliquer) | 🟢 (réécriture directe) |
| debug | support 6 | natif `systematic-debugging` | 🟡 |
| extract-conventions | setup/maintenance | graphify + auteurs de skills reconnus du marché | 🟡 (génère les références depuis le code réel) |
| choose-model | transverse | synthèse interne (aucune source externe reprise telle quelle) | 🟡 (grille écrite, pas encore appliquée rétroactivement à tous les agents existants) |
| dispatch-parallel | transverse | un framework de skills/agents du marché (dispatching-parallel-agents + subagent-driven-development, fusionnées) | 🟡 (écrit, vécu partiel via elrond→aragorn/gimli/legolas) |
| writing-skills | transverse (méta) | un framework de skills/agents du marché | 🟡 (écrit, applique le gabarit unique + checklist Règle B) |
| writing-agents | transverse (méta) | synthèse interne (formalisation du gabarit 7 piliers déjà en usage) | 🟢 |
| portless-ready | setup/infra | un outil portless du marché (câblage à nous) | 🟡 (rend une stack portless : alias HTTPS + hygiène ports) |
| **gate** | 7 | des patterns d'agents long-running du marché (`default-FAIL hook` + `fresh-context evaluator`) | 🟡 (agent `arbitre` écrit ; hook default-FAIL par repo reste à poser) |
| review | 8 | un auteur de skills reconnu du marché (code-review 2 axes) + agents Xefi + natif | 🟡 |
| simplify | 9 | natif `simplify` | 🟡 |
| ship | 10 | interne (`/SHIP`, gandalf) | 🟡 |
| finish | 11 | interne (`finish_task`) | 🟡 |
| merge-worktree | 11 | un kit d'ingénierie de contexte du marché (`git-worktrees`) | 🟡 |

### Agents métier (invoqués par les étapes 8/10)
| Agent | Rôle | Maturité |
|---|---|---|
| aragorn / gimli / legolas | review MR voix Xefi (Nuxt/Vue · React) | ✅ |
| valerianus | tri/reformulation des reviews (anti-débat) | ✅ |
| gandalf | gate final MR (`/code-review` + `/security-review`) | ✅ |
| tuteur-laravel | pédagogie (hors pipeline) | ✅ |
| **arbitre** (GATE, ex-« évaluateur ») | juge à contexte propre, **sans Write/Edit**, rend PASS/NEEDS_WORK avec preuve citée | ✅ (écrit ; hook default-FAIL par repo pas encore posé, pas encore dogfoodé) |
| vue-nuxt-builder | implémentation Vue3/Nuxt3 (Composition API, réactivité, perf) sur functional/ | ✅ (pas encore dogfoodé) |
| sql-es-tuner | tuning SQL (MySQL/SQL Server) et mapping/indexation Elasticsearch-Scout | ✅ (pas encore dogfoodé) |
| laravel-builder | implémentation Laravel/Eloquent (API, queues, perf), distinct de tuteur-laravel | ✅ (pas encore dogfoodé) |
| seo-auditor | audit SEO technique d'une page/site déjà en ligne, jamais d'édition | ✅ (pas encore dogfoodé) |
| accessibility-auditor | audit a11y technique d'une page/site déjà en ligne, jamais d'édition | ✅ (pas encore dogfoodé) |
| qa-tester | test manuel/exploratoire d'un parcours sur une app qui tourne, jamais d'édition | ✅ (pas encore dogfoodé) |
| security-auditor | audit sécurité statique dédié (OWASP, secrets, dépendances), lecture seule, jamais d'exploitation active | ✅ (pas encore dogfoodé) |
| architecture-debt-auditor | audit périodique de dette d'architecture (hot-spots git, test de suppression, rapport priorisé) | ✅ (pas encore dogfoodé) |

## 2. Backlog de sourcing : idées/agents à réécrire pour compléter/améliorer

Veille de marché menée en continu (dernière passe 2026-08). Chaque ligne = une
idée à **réécrire chez nous**, pas à installer, sources anonymisées par catégorie (catalogues
d'agents/skills Claude Code, linters de stack, frameworks d'orchestration, etc. du marché).

| Catégorie de source | Idée / agent à reprendre | Enrichit | Statut |
|---|---|---|---|
| patterns d'agents long-running du marché | `evaluator.md` (patron évaluateur contexte frais) → agent `arbitre` | gate | ✅ (agent écrit) |
| patterns d'agents long-running du marché | `verify-gate.sh` (hook PreToolUse default-FAIL sur preuve lue) | gate | 🟡 (mécanisme identifié, câblage par repo restant) |
| auteur de skills reconnu du marché | grill-with-docs → CONTEXT.md+ADR | spec | ✅ |
| auteur de skills reconnu du marché | code-review 2 axes non-polluants | review | ✅ |
| auteur de skills reconnu du marché | `wayfinder` → skill `wayfinder`, `handoff` → skill `handoff`, `improve-codebase-architecture` → agent `architecture-debt-auditor` | plan / reprise de session / audit archi | ✅ |
| auteur de skills reconnu du marché | `domain-modeling` | archi | 🔎 (recoupe partiellement documentation-adr, pas encore isolé en brique dédiée) |
| catalogue de skills dev généralistes du marché | `observability-and-instrumentation` → skill `observability-instrumentation`, `api-and-interface-design` → skill `api-design`, `documentation-and-adrs` → skill `documentation-adr`, `deprecation-and-migration` → skill `deprecation-migration` | code/api/doc/migration | ✅ |
| catalogue de skills dev généralistes du marché | `security-and-hardening`, `webperf`, `context-engineering` | nouvelles briques | 🔎 (context-engineering = méta sur l'écriture de prompts/CLAUDE.md, pas un skill dev (pertinent pour améliorer ce repo lui-même, pas un usage quotidien)) |
| catalogue de skills dev généralistes du marché | `browser-testing-with-devtools` | gate (recoupe déjà `qa-tester`/`verify-flow`) | ✕ (redondant) |
| framework de skills/agents du marché | `dispatching-parallel-agents`, `subagent-driven-development`, `writing-plans` | plan / orchestration | 🔎 (déjà en skills natifs → à *posséder*) |
| catalogues d'agents Claude Code du marché (plusieurs) | `git-advanced-workflows` (worktrees avancés) | start-feature / finish | 🔎 (réf citée, à vérifier) |
| outil d'état live du marché | état live depuis le réel + socket-API | FLEET | 🔎 (après dogfood) |
| outil de replay/audit du marché | replay/audit post-hoc | FLEET / graphify | 🔎 (nice-to-have) |
| outil de compression de tokens du marché | compression + mesure tokens par appel | Taskling | 🔎 (réécrire vs consommer natif (à trancher)) |
| pipeline voix→vault du marché | pipeline voix→vault | Lumia | 🔎 (réf, réécrire avec classifieur read-only) |
| framework d'orchestration multi-agents du marché | org-chart coordinateur+agents | dispatch multi-agents | 🔎 (réf archi seulement) |
| catalogue de skills Vue du marché | `skills/vue/` (script-setup-macros, core-new-apis, advanced-patterns) | vue-nuxt-vuetify-conventions | ✅ |
| catalogue de skills Nuxt du marché | `skills/nuxt4-patterns/SKILL.md` | vue-nuxt-vuetify-conventions | ✅ |
| catalogue de skills Nuxt du marché (autre) | `skills/nuxt/references/nuxt-composables.md` (discipline useState/useCookie/useRequestFetch, extrait limité) | vue-nuxt-vuetify-conventions | ✅ |
| catalogue de skills Vuetify du marché | `.deprecated/vuetify-4/SKILL.md` + `references/patterns/` | vue-nuxt-vuetify-conventions | ✅ |
| kit d'ingénierie de contexte du marché | `plugins/git/skills/git-worktrees/SKILL.md` (section "How to Merge Worktree") | merge-worktree | ✅ |
| catalogue d'agents Claude Code du marché | `vue-expert` (frameworks) → agent `vue-nuxt-builder` | agents métier (build front) | ✅ |
| catalogue d'agents Claude Code du marché (large collection) | absence confirmée d'agent Vue/Nuxt (grep sur 203 agents) → confirme le manque comblé par `vue-nuxt-builder` | agents métier (build front) | ✅ (référence croisée) |
| catalogue d'agents Claude Code du marché (autre) | `sql-pro` (02-language-specialists) → agent `sql-es-tuner` | agents métier (data) | ✅ |
| catalogue d'agents Claude Code du marché (large collection) | `sql-pro`, `database-optimizer` → agent `sql-es-tuner` | agents métier (data) | ✅ |
| catalogue d'agents Claude Code du marché | `elasticsearch-expert` → agent `sql-es-tuner` | agents métier (data) | ✅ |
| catalogue d'agents Claude Code du marché (autre) | `laravel-specialist` (02-language-specialists) → agent `laravel-builder` | agents métier (build back) | ✅ |
| catalogue d'agents Claude Code du marché (large collection) | `php-pro` (web-scripting), pas de spécialisation Laravel → confirme le manque comblé par `laravel-builder` | agents métier (build back) | ✅ (référence croisée) |
| patterns d'agents long-running du marché | kill-switch / steer (hooks opérateur) | / | ✕ (humain présent) |
| style de compression de sortie du marché | compression de sortie | / | 🟡 réévalué : le style télégraphique intégral reste écarté (illisible), mais le principe "sortie courte par défaut, pour limiter la dépense en tokens de sortie" est retenu comme garantie transversale (voir `doc/COMMENT-ON-ECRIT-NOS-AGENTS.md` §5) |
| des frameworks d'autonomie agentique totale du marché | autonomie 24/7 / bout-en-bout | / | ✕ (repoussoir : no-auto-merge) |
| catalogue de skills Vue du marché (autre) | `skills/vue/` (usage lib tierce de rendu JSON→Vue) | vue-nuxt-vuetify-conventions | ✕ (pas une convention Vue générique, hors besoin Xefi) |
| catalogue de skills Nuxt du marché (autre) | `skills/nuxt-modules/` (auteuring de module Nuxt publié/npm) | vue-nuxt-vuetify-conventions | ✕ (hors périmètre : g.compigni fait du code d'app, pas de module) |
| catalogue de skills Nuxt du marché (autre) | `skills/nuxt/SKILL.md` (dispatcher) | vue-nuxt-vuetify-conventions | ✕ (redondant avec le principe de progressive-disclosure déjà acquis dans using-construct) |
| catalogue de skills du marché (autre) | `using-git-worktrees` | merge-worktree | ✕ (redistribution telle quelle d'un skill déjà repris nativement et dans start-feature) |
| lib headless Vuetify du marché | lib headless (`@vuetify/v0`) | vue-nuxt-vuetify-conventions | ✕ (différente du Vuetify stylé Material utilisé sur le front Nuxt/Vue) |
| repo de skills Vue du marché (deux variantes, même contenu) | `vuetify-skilld` | vue-nuxt-vuetify-conventions | ✕ (dossier absent de l'arbre git actuel, contenu introuvable (même constat sur les deux forks)) |
| catalogue de skills du marché (autre) | `web-ui-vuetify` | vue-nuxt-vuetify-conventions | ✕ (fichier introuvable dans l'arbre actuel ; déjà couvert par les reviewers par stack en review) |
| corpus de référence Vuetify du marché | corpus de référence exhaustif (450 fichiers) | vue-nuxt-vuetify-conventions | ✕ (trop volumineux pour une brique condensée) |
| catalogue de skills du marché (autre) | `material-design-3-guide` | vue-nuxt-vuetify-conventions | ✕ (guide MD3 générique multi-framework, hors sujet) |
| handbook front-end du marché | `frontend-best-practices` | vue-nuxt-vuetify-conventions | ✕ (contenu générique déjà connu, mieux couvert par design:*, inaccessible en réalité 403) |
| catalogue de skills du marché (autre) | `frontend-design` | vue-nuxt-vuetify-conventions | ✕ (repo disparu 404, recoupe déjà le skill natif frontend-design) |
| catalogue de skills du marché (autre) | `ln-114-frontend-docs-creator` | vue-nuxt-vuetify-conventions | ✕ (fichier absent, dépend d'un pipeline propriétaire non transposable) |
| outil de mémoire pour Claude Code du marché | `mem-search` | / | ✕ (sous-système complet, redondant avec le système de mémoire déjà en place) |
| outil de mémoire pour Claude Code du marché (même éditeur) | `version-bump` (ex claude-code-plugin-release) | / | ✕ (script d'exploitation spécifique à cet outil, pas une méthode généralisable) |
| skill graphify tiers du marché | `graphify` | / | ✕ (doublon confirmé du skill natif graphify déjà installé) |
| catalogue d'agents Claude Code du marché (large collection) | mcp-developer | futur projet Node/NestJS (MCP) | ✕ (prématuré, pas de chantier MCP actif ; à ressortir en phase concrète de portage) |
| catalogues d'agents Claude Code du marché (plusieurs) | api-documenter | / | ✕ (aucun signal de douleur doc API dans la mémoire) |
| catalogue d'agents Claude Code du marché (large collection) | readme-generator | / | ✕ (recoupe déjà le changelog manuel test-casebook) |
| catalogue d'agents Claude Code du marché (large collection) | dependency-manager | / | ✕ (aucun signal CVE/conflit de versions) |
| catalogues d'agents Claude Code du marché (plusieurs) | error-detective | / | ✕ (aucun incident concret au-delà des ports Docker, déjà traité) |
| catalogue d'agents Claude Code du marché (large collection) | git-workflow-manager | / | ✕ (conventions déjà actées et stables : squash+delete, MR Draft, GCI naming) |
| catalogue d'agents Claude Code du marché (large collection) | code-reviewer/security-auditor/penetration-tester/debugger/test-automator/qa-expert/accessibility-tester/refactoring-specialist | / | ✕ (déjà couverts par les reviewers par stack/gandalf/kobold + skills systematic-debugging/testing-doctrine-casebook/design:accessibility/simplify) |
| catalogue d'agents Claude Code du marché (large collection) | legacy-modernizer | / | ✕ (aucune migration de framework en cours) |
| catalogue d'agents Claude Code du marché (large collection) | typescript-pro | / | ✕ (signal générique et faible, aucune douleur TS documentée) |
| catalogue d'agents Claude Code du marché (large collection) | database-architect | / | ✕ (pas de conception schéma from scratch ; couvert par `sql-es-tuner`) |
| catalogue d'agents Claude Code du marché (large collection) | frontend-security-coder / backend-security-coder | / | ✕ (gandalf fait déjà tourner /security-review + délègue au reviewer de stack) |
| catalogue d'agents Claude Code du marché (large collection) | devops-troubleshooter | / | ✕ (docker-proxy zombies déjà traité par fix documenté, pas un besoin d'agent) |
| catalogue d'agents Claude Code du marché (large collection) | context-manager/team-lead/team-reviewer/team-implementer/team-debugger | / | dispatch multi-agents | ✕ (implémentation type org-chart, archi à évaluer, pas un agent à écrire maintenant) |
| catalogue d'agents Claude Code du marché (large collection) | plugin git-pr-workflows (code-reviewer) | / | ✕ (recoupe les reviewers par stack/gandalf) |
| catalogue d'agents Claude Code du marché (large collection) | skill git-advanced-workflows | start-feature/finish | ✕ (cours de référence, pas un agent orchestré) |
| catalogue d'agents Claude Code du marché | nestjs-expert / typescript-expert | futur projet Node/NestJS | ✕ (prématuré, à ressortir en phase active NestJS+TS sur le futur projet Node) |
| catalogue d'agents Claude Code du marché | react-expert | / | ✕ (utile pour lire le code des collègues React seulement, pas un besoin de prod g.compigni) |
| catalogue d'agents Claude Code du marché | accessibility-expert / playwright-expert | / | ✕ (chevauchement design:accessibility + verify-flow) |
| catalogue d'agents Claude Code du marché | architecture-documenter / contract-testing-expert / runbook-generator | / | ✕ (confiance faible, usage ponctuel, aucun signal récurrent) |
| catalogue d'agents Claude Code du marché | core/code-reviewer, core/debugger, core/refactorer, core/architect, security-auditor, devsecops-engineer, ux-designer, ui-components-expert, code-documenter, orchestrators/*, postgresql-expert, redis-expert, graphql-expert, cypress-expert, jest-expert, e2e-testing-expert, operational/*, industry/* | / | ✕ (redondants avec le roster existant ou hors stack confirmée) |
| framework d'orchestration multi-agents du marché | org-chart généraliste (qui parle à qui) | dispatch multi-agents | ✕ (aucun contexte frais forcé ni mécanisme de preuve/verdict ; hors sujet pour le manque GATE, reste piste archi 🔎 séparée) |
| catalogue de skills React du marché | `react-best-practices` (AGENTS.md) (patterns perf/rendering/waterfalls avec code avant/après) | react-nextjs-conventions | ✅ |
| catalogue de skills React/Node du marché | `redux-toolkit/SKILL.md` (createSlice typé, hooks typés, createAsyncThunk, sélecteurs mémoïsés) | react-nextjs-conventions | ✅ |
| catalogue de skills shadcn du marché | `skills/shadcn/SKILL.md` (composition par wrapper, cn(), structure de dossiers) | react-nextjs-conventions | ✅ |
| linter React du marché | `oxlint-plugin-react-doctor`, ~780 règles déterministes (state/effects, perf, sécurité, a11y), sous-ensemble sévérité `error` hors frameworks niches repris en section 4 | react-nextjs-conventions | ✅ (contenu réécrit ; l'outil lui-même reste un candidat 🔎 séparé pour un futur gate CI React, pas installé, aucun repo React à g.compigni) |
| linter Nuxt/Vue du marché | `oxlint-plugin-vue-doctor`/`oxlint-plugin-nuxt-doctor` (verrouillé Vue 3 + Nuxt 4, explicitement inspiré de son équivalent React ; règles réactivité/composition, hydratation SSR, sécurité, server routes h3 reprises en section 4) | vue-nuxt-vuetify-conventions | ✅ (contenu réécrit ; candidat 🔎 séparé pour un futur gate CI le front Nuxt/Vue, pas installé) |
| alternative de linter Vue du marché | alternative Vue-only trouvée en sourcing | vue-nuxt-vuetify-conventions | ✕ (pas de couverture Nuxt, le linter retenu plus complet et plus proche de la stack réelle) |
| alternative de linter Vue du marché (autre) | alternative Vue trouvée en sourcing | vue-nuxt-vuetify-conventions | ✕ (moins mature/moins de règles que le linter retenu à l'inspection) |
| outil de review orienté suppression du marché | `ponytail-review`/`ponytail-audit` (angle suppression exclusif (dead code, stdlib réinventée, sur-abstraction, yagni), tags par catégorie, score net de lignes) | over-engineering-review | ✅ (mécanisme et tags réécrits, nouvelle brique dédiée) |
| catalogue de skills dev généralistes du marché | `code-review-and-quality` (nombreuses installations, taxonomie de sévérité Critical/Required/Nit/FYI, seuil de taille de diff, checklist dépendances) | gandalf | ✅ (taxonomie + seuils intégrés en étape 1/5/7 de l'agent, pas une brique séparée) |
| projet open source TypeScript du marché | `typescript-review` (blind-spots a11y (aria-label, focus modal) et poids bundle (import par défaut, module lourd en route)) | react-nextjs-conventions + vue-nuxt-vuetify-conventions | ✅ (2 items ajoutés à chaque brique) |
| catalogue d'instructions Copilot du marché | `review-and-refactor`, lit `.github/instructions/*.md`, refactore aux conventions du projet |, | ✕ (déjà couvert par les briques `*-conventions` + gandalf, rien de distinct) |
| projet open source TypeScript du marché (même éditeur) | `clojure-review` | / | ✕ (langage hors périmètre Xefi) |
| plugin de review d'un éditeur d'IDE du marché | `thermo-nuclear-code-quality-review` |, | ✕ (même angle qu'over-engineering-review, moins actionnable, pas de tags/score) |
| catalogue de skills internes d'un autre éditeur | `code-quality` | / | ✕ (spécifique à leur stack propriétaire par contexte, reste déjà couvert par les reviewers par stack+conventions) |
| outil de review d'architecture du marché | `architecture-review` | / | ✕ (chemin SKILL.md exact non confirmé ; contenu recoupe déjà gandalf/arbitre/over-engineering-review, pas assez différenciant) |
| catalogue de skills NestJS du marché | `skills/nestjs-expert/SKILL.md` (module/controller/service, DI constructeur, DTO+class-validator, exceptions HTTP, tests) | nestjs-node-conventions | ✅ |
| skill TypeScript avancée du marché | contrats Zod+z.infer, unions discriminées, mapped types/type guards sur modèles Prisma | nestjs-node-conventions | ✅ |
| catalogue de skills React/Node du marché | `prisma-development/SKILL.md` + `trpc/SKILL.md` + `zod-schema-validation/SKILL.md` | nestjs-node-conventions | ✅ |
| catalogue de skills Next.js du marché | `next-best-practices` | react-nextjs-conventions | ✕ (repo archivé, absorbé par Next.js lui-même (next dev 16.3+, rien de portable)) |
| catalogue de skills React/Node du marché (même source) | `nextjs-react-typescript` | react-nextjs-conventions | ✕ (converti de règles génériques d'un éditeur d'IDE, redondant et moins précis que la source retenue) |
| catalogue de skills React/Node du marché (même source) | `nextjs-react-redux-typescript` (variante convertie de règles d'un éditeur d'IDE) | react-nextjs-conventions | ✕ (doublon quasi total de react + redux-toolkit réunis) |
| catalogue de skills React/Node du marché (même source) | `react` (générique) | react-nextjs-conventions | ✕ (conseils génériques senior dev, recoupe la source retenue en moins riche) |
| catalogue de skills React/Node du marché (même source) | `express-typescript` | nestjs-node-conventions | ✕ (hors-cible : vision du futur projet Node/NestJS est NestJS pas Express, recouvrement partiel sans plus-value) |
| catalogue de skills React/Node du marché (même source) | `nodejs-development` | nestjs-node-conventions | ✕ (fourre-tout incohérent (CMS, Vue.js, générique)) |
| catalogue de skills React/Node du marché (même source) | `typescript` (générique) | nestjs-node-conventions | ✕ (trop générique, déjà répété par les briques nestjs/trpc/zod) |
| repo shadcn-ui du marché | shadcn-ui | react-nextjs-conventions | ✕ (repo introuvable/mort, seul un résumé tiers récupéré, pas la source elle-même) |
| outil d'audit shadcn du marché | audit/discovery de composants shadcn existants | react-nextjs-conventions | ✕ (mécanisme différent, rôle reviewer plutôt que conventions de code ; piste séparée à garder) |

## 3. La règle qui fait qu'on « maîtrise » (rappel)

On ne branche jamais un repo en dépendance. On lit → on extrait le mécanisme → on **réécrit**
dans le gabarit unique → on crédite `Origine`. Voir la checklist d'adoption dans
`CONVENTIONS.md`. C'est ce qui garantit : personne en amont ne casse notre workflow, et tout
est écrit pareil (maintenable). Le backlog ci-dessus est notre file d'enrichissement, on y
pioche quand une étape a un vrai manque, pas pour empiler.
