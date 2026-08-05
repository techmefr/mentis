# Comment j'écris et je gouverne mes agents

> Ce doc explique la méthode, pas juste le résultat : pourquoi ce framework
> a cette forme, comment un agent naît chez moi, et les règles qui
> s'appliquent à tous, sans exception. Écrit pour quelqu'un qui ne connaît
> aucun de mes agents.

## 1. Le contexte

Ça fait à peu près un mois que je bosse là-dessus, petit bout par petit
bout. Pas de big-bang, un agent à la fois, chacun testé sur du vrai travail
avant que je le considère comme acquis. Y'en a qui ont un vécu de
production réel (les reviewers Nuxt/Vue et PHP/Laravel, le gate final, le
juge à froid), d'autres sont écrits mais pas encore éprouvés sur du réel
(les agents Go/.NET, faute de projet sur ces stacks pour l'instant) — voir
[Statut réel](#8-statut-réel-honnêteté-sur-la-maturité).

Ma méthode : j'assemble le pipeline complet d'abord, sur une vraie tâche de
bout en bout, avant de figer un découpage en projets séparés. Je fige rien
tant que le tour complet n'a pas tourné une fois.

## 2. Le problème que je résous

Un agent générique type "assistant de code", ça me pose trois problèmes
concrets :

1. **Celui qui écrit le code peut pas être celui qui le juge**, dans la
   même session — il a vu le code s'écrire, il connaît les compromis pris
   en cours de route, il est complaisant avec lui-même, structurellement.
2. **"Fais de ton mieux" c'est pas vérifiable.** Sans critère testable, un
   agent qui dit "c'est fini, ça marche", je peux ni le confirmer ni le
   contredire. Il me faut une preuve citée (fichier, ligne, sortie de
   test), jamais une déclaration prise pour argent comptant.
3. **Je m'inspire du marché sans en dépendre.** Y'a de bonnes idées dans
   des repos publics — conventions, patrons d'agents, structures de
   frameworks. Mais les installer comme dépendance, ça veut dire qu'un
   tiers peut changer son comportement du jour au lendemain et péter mon
   pipeline sans prévenir.

Trois règles répondent à ces trois problèmes.

## 3. Les trois règles fondatrices

### Règle A — je teste l'approche complète d'abord
J'assemble le pipeline entier (brainstorm → ... → finish) et je le fais
tourner sur une vraie tâche avant de découper en projets séparés. Le
découpage vient après, une fois que l'approche a fait ses preuves sur le
terrain.

### Règle B — je réécris à ma sauce, jamais je dépends
Toute idée qui vient de dehors (skill, agent, technique), je la réécris en
interne, jamais branchée en dépendance runtime. Je lis la source,
j'extrais le mécanisme (pas la prose), je le réécris dans mon gabarit, et
je crédite l'origine honnêtement dans `CATALOG.md`. Ce que je garde, c'est
l'idée — jamais le paquet.

Pourquoi je fais ça comme ça : personne en amont peut me casser mon
workflow ; je sais exactement ce que fait chaque brique, c'est mon code,
mes mots ; et tout est écrit pareil, du coup n'importe qui connaît le
gabarit s'y retrouve.

### Règle C — le framework reste publiable
Je l'écris dès le départ pour pouvoir l'extraire un jour dans un repo
public : aucun secret, aucun nom de projet réel, aucune réalité d'infra là
dedans. Une brique nomme un rôle ("le back Laravel"), jamais un projet
précis. Ma règle simple : si une phrase peut pas être lue par quelqu'un
d'extérieur, elle va pas dans ce dossier.

## 4. Le gabarit unique — comment j'écris un agent

Tous mes agents suivent la même structure en 7 sections, jamais improvisée
au cas par cas :

```mermaid
flowchart TD
    R["1. RÔLE
    une seule responsabilité,
    ce que l'agent fait JAMAIS"]
    M["2. MÉMOIRE
    ce qui persiste, où,
    ce qui est relu à chaque appel"]
    B["3. BOUCLE
    action → vérification → décision,
    condition de sortie explicite"]
    O["4. OUTILS & PÉRIMÈTRE
    autorisés / interdits, en dur"]
    G["5. GARDE-FOUS
    TOUJOURS / DEMANDER / JAMAIS"]
    C["6. REVIEW CONTEXTE FRAIS
    comment la fraîcheur de jugement
    est garantie par construction"]
    T["7. TRACE
    ce qui est restitué,
    lisible et vérifiable après coup"]
    R --> M --> B --> O --> G --> C --> T
```

Chaque section répond à une question précise :

| Section | Question à laquelle elle répond |
|---|---|
| RÔLE | C'est quoi la seule responsabilité de cet agent, et qu'est-ce qu'il fait jamais ? |
| MÉMOIRE | Qu'est-ce qui persiste entre deux invocations, et ça vit où ? |
| BOUCLE | C'est quoi le cycle exact (action/vérification/décision), et comment ça s'arrête ? |
| OUTILS & PÉRIMÈTRE | Quels outils sont autorisés, lesquels sont interdits — en dur, pas juste à l'oral |
| GARDE-FOUS | Ce qui doit arriver toujours, ce que je demande plutôt que deviner, ce que je m'interdis |
| REVIEW CONTEXTE FRAIS | Comment je garantis que le jugement est pas pollué par la session qui a produit le travail |
| TRACE | Ce que l'agent restitue à la fin, pour que quelqu'un d'autre puisse vérifier après coup |

**Exemple concret** — mon agent `arbitre` (le juge à froid) :
- RÔLE : rendre un verdict binaire PASS/NEEDS_WORK, rien d'autre. Pas de
  correction, pas de suggestion de code.
- MÉMOIRE : rien persiste entre deux invocations ; l'entrée doit contenir
  le diff, les critères d'acceptation, et les preuves, en dur.
- GARDE-FOUS (TOUJOURS) : preuve absente ou pas concluante → `NEEDS_WORK`
  automatique, jamais de bénéfice du doute.

## 5. Les deux garanties transversales

### Contexte frais
Celui qui juge a jamais vu le code s'écrire :

```mermaid
sequenceDiagram
    participant Dev as Session de production
    participant Code as Code produit
    participant Judge as Agent juge (contexte neuf)
    Dev->>Code: écrit le code, connaît les compromis pris
    Note over Judge: invoqué séparément,<br/>aucune mémoire de la session Dev
    Code->>Judge: diff + preuves citées uniquement
    Judge-->>Dev: verdict PASS / NEEDS_WORK, jamais négocié dans la même session
```

Cette séparation, c'est pas une option que j'active parfois, elle est
structurelle. L'agent juge est invoqué comme un sous-agent à part, sans
accès à l'historique de la conversation qui a produit le travail.

### Défaut = échec
Une affirmation ("j'ai testé, ça marche") sans preuve citée, c'est pas une
preuve, je l'ignore. Si le périmètre donné est trop incomplet pour évaluer
quoi que ce soit, le verdict par défaut c'est `NEEDS_WORK`, jamais `PASS`
par optimisme. Cette règle-là, aucune des sources publiques que j'ai
regardées sur la conception d'agents la couvre — c'est la partie que j'ai
dû inventer moi-même plutôt que reprendre du marché.

### Sortie courte par défaut
Une réponse d'agent, ça se facture pas comme une réponse humaine : chaque
mot de sortie coûte des tokens, pour de vrai. Par défaut, un agent
restitue le strict nécessaire — un statut, un verdict, une liste de
findings fichier + ligne + une phrase, jamais un pavé de justification ou
de contexte redondant avec ce que je vois déjà. Le détail (raisonnement
complet, alternatives explorées), je le garde dispo si je le redemande,
je le donne pas par défaut. J'ai regardé une piste dans le sourcing (agent
"Caveman", compression de sortie) : le style entièrement télégraphique, je
l'ai écarté, illisible à la relecture — mais le principe, sortie courte
par défaut plutôt que verbeuse, je le garde comme garantie transversale,
au même titre que le contexte frais et le défaut-échec.

## 6. TOUJOURS / DEMANDER / JAMAIS

Le format de garde-fous le plus solide que j'ai trouvé en cherchant dehors
(analyse de plus de 2500 fichiers de config d'agents publics) : une règle
en trois tiers plutôt qu'une liste plate d'interdits.

- **TOUJOURS** : ce qui doit arriver à chaque fois, sans exception.
- **DEMANDER** (jamais deviner) : les cas où l'agent doit s'arrêter et me
  demander plutôt que choisir à ma place.
- **JAMAIS** : les lignes rouges absolues.

Exemple réel (mon agent `elrond`, l'orchestrateur qui détecte le stack d'un
diff et route vers le bon reviewer) : en cas d'ambiguïté de stack (monorepo,
signatures contradictoires), la règle c'est pas "fais de ton mieux" mais
explicitement DEMANDER — jamais deviner, quitte à couper le flux.

## 7. Comment un agent naît chez moi — le cycle de sourcing

```mermaid
flowchart LR
    V[Veille — un repo/idée<br/>repéré au fil de l'eau] --> T[Tri dans CATALOG.md<br/>statut 🔎 à miner]
    T --> D{Une brique interne<br/>couvre déjà l'idée ?}
    D -->|oui| X[Écarté — statut ✕<br/>raison notée honnêtement]
    D -->|non| E[Extraction du mécanisme<br/>jamais de la prose copiée]
    E --> W[Réécriture dans<br/>le gabarit unique, en français]
    W --> O[Origine créditée<br/>dans CATALOG.md]
    O --> DF[Dogfood sur du travail réel]
    DF --> S[Statut mis à jour<br/>🟡 écrit → ✅ éprouvé]
```

J'adopte rien "parce que c'est dans un repo populaire". Chaque ligne du
`CATALOG.md` c'est une décision explicite de ma part (adoptée ou écartée)
avec sa raison. Une bonne partie du backlog, je l'écarte volontairement —
ça prouve que le tri est réel, pas un empilement.

## 8. Statut réel, honnêteté sur la maturité

Pas de survente : certains de mes agents ont un vécu de production réel,
d'autres sont écrits mais pas encore confrontés à un vrai projet. Ce
tableau est tenu à jour dans `CATALOG.md` — la colonne maturité (✅ / 🟡 /
🔜) c'est la source de vérité, pas ce document.

## 9. Loop possible, mais pas sur tout

Mon pipeline peut tourner en boucle sans supervision jusqu'au gate :
brainstorm → spec → archi → plan → code → debug peuvent s'enchaîner sans
qu'un humain valide chaque étape. Par contre deux points restent des
arrêts humains volontaires, non négociables :

- **Le gate** (`arbitre`) rend un verdict, mais merge rien.
- **Le merge lui-même** : 2 approbations humaines avant merge, toujours.

C'est pas une limitation technique — l'autonomie bout-en-bout façon des
frameworks d'autonomie agentique totale du marché, je l'ai explicitement
écartée comme repoussoir dans le sourcing (`CATALOG.md`) : un agent qui
merge du code tout seul sans validation, c'est exactement le
contre-exemple que je veux pas devenir. La boucle accélère la production,
jamais la décision de merger.

## 10. La vision — que le système apprenne, pas juste qu'il tourne

Mon objectif, c'est pas un set d'agents figé : c'est un système qui devient
plus intelligent avec l'usage, sans jamais toucher aux règles fixes
(contexte frais, défaut=échec). Ce qui s'améliore, c'est la connaissance
métier accumulée, pas la doctrine. J'ai déjà trois boucles de retour,
partiellement en place :

- **Calibration** : chaque review réelle (findings retenus, faux positifs
  infirmés) est journalisée, pour que le tri futur reconnaisse plus vite ce
  qui vaut la peine d'être remonté.
- **Mémoire persistante** : mes corrections et confirmations sur une
  approche deviennent des règles durables, relues avant d'agir à nouveau —
  pas ré-expliquées à chaque fois.
- **`extract-conventions`** : génère des conventions depuis le code réel
  existant plutôt que depuis une doctrine abstraite, du coup ça se met à
  jour avec le code lui-même.

Ce qui me manque encore pour que ce soit systématique et pas juste au fil
de l'eau : une revue périodique qui relit ces trois sources et met à jour
`CATALOG.md` (maturité, garde-fous affinés) — pas encore automatisée, à
poser comme prochaine étape.

## 11. Pourquoi ça compte

- **La review complaît pas** : parce que le reviewer est jamais celui qui a
  écrit le code, dans une session séparée à froid.
- **Rien n'est cru sur parole** : "c'est fini" c'est jamais suffisant, une
  preuve concrète oui.
- **Ça s'enrichit sans dépendre** : le marché avance, je pioche dedans,
  mais rien peut casser mon pipeline en changeant de l'extérieur.
- **Adapté à ma réalité, pas à une fiction de compétence uniforme** : un
  agent formule ses remarques en questions honnêtes sur un stack que je
  maîtrise pas encore (PHP/Laravel), et en affirmations tranchées sur un
  stack où j'ai une vraie expertise (JS/TS) — le style suit ma réalité, pas
  un ton générique.
