# Comment j'écris et je gouverne mes agents

Ce doc explique la méthode, pas juste le résultat : pourquoi ce framework a
cette forme, comment un agent naît chez moi, et les règles qui s'appliquent
à tous, sans exception. Écrit pour quelqu'un qui ne connaît aucun de mes
agents.

## 1. Le contexte

Ça fait à peu près un mois que je travaille là-dessus. Construit petit
bout par petit bout, pas en une fois : un agent à la fois, chacun testé sur
du travail réel avant que je le considère comme acquis. Certains ont déjà
un vécu de production réel (les reviewers Nuxt/Vue et PHP/Laravel, le gate
final, le juge à froid). D'autres sont écrits mais pas encore éprouvés sur
du réel, faute de projet sur ces stacks pour l'instant (les agents
Go/.NET). Le détail est dans la partie [Statut réel](#8-statut-réel-honnêteté-sur-la-maturité).

Ma méthode de base : j'assemble le pipeline complet d'abord, sur une vraie
tâche de bout en bout, avant de figer un découpage en projets séparés. Je
ne fige aucune frontière tant que le tour complet n'a pas tourné une fois.

## 2. Le problème que je résous

Un agent générique type "assistant de code" me pose trois problèmes
concrets.

Le premier : celui qui écrit le code ne peut pas être celui qui le juge,
dans la même session. Il a vu le code s'écrire, il connaît les compromis
pris en cours de route, il est complaisant avec lui-même, structurellement.

Le deuxième : "fais de ton mieux" n'est pas vérifiable. Sans critère
testable, un agent qui affirme "c'est fini, ça marche", je ne peux ni le
confirmer ni le contredire. Il me faut une preuve citée (fichier, ligne,
sortie de test), jamais une déclaration prise pour argent comptant.

Le troisième : je m'inspire du marché sans en dépendre. De bonnes idées
existent dans des repos publics, des conventions, des patrons d'agents, des
structures de frameworks. Mais les installer comme dépendance, c'est
s'exposer à ce qu'un tiers change son comportement du jour au lendemain et
casse mon pipeline sans prévenir.

Trois règles répondent à ces trois problèmes.

## 3. Les trois règles fondatrices

### Règle A — je teste l'approche complète d'abord
J'assemble le pipeline entier (brainstorm → ... → finish) et je le fais
tourner sur une vraie tâche avant de découper en projets séparés. Le
découpage vient après, une fois que l'approche a fait ses preuves sur le
terrain.

### Règle B — je réécris à ma sauce, jamais je ne dépends
Toute idée venue de l'extérieur (skill, agent, technique), je la réécris en
interne. Jamais branchée en dépendance runtime. Je lis la source, j'extrais
le mécanisme (pas la prose), je le réécris dans mon gabarit, et je crédite
l'origine honnêtement dans `CATALOG.md`. Ce que je garde, c'est l'idée,
jamais le paquet.

Pourquoi je procède comme ça : personne en amont ne peut casser mon
workflow. Je sais exactement ce que fait chaque brique, c'est mon code, mes
mots. Et tout est écrit de la même façon, donc n'importe qui connaît le
gabarit peut s'y retrouver.

### Règle C — le framework reste publiable
Je l'écris dès le départ pour pouvoir l'extraire un jour dans un repo
public : aucun secret, aucun nom de projet réel, aucune réalité d'infra
dans ce dossier. Une brique nomme un rôle ("le back Laravel"), jamais un
projet précis. Ma règle simple : si une phrase ne pourrait pas être lue par
quelqu'un d'extérieur, elle ne va pas ici.

## 4. Le gabarit unique — comment j'écris un agent

Tous mes agents suivent la même structure en 7 sections, jamais improvisée
au cas par cas.

```mermaid
flowchart TD
    R["1. RÔLE
    une seule responsabilité,
    ce que l'agent ne fait JAMAIS"]
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

RÔLE, c'est quelle est la seule responsabilité de cet agent, et ce qu'il ne
fait jamais. MÉMOIRE, c'est ce qui persiste entre deux invocations et où ça
vit. BOUCLE, c'est le cycle exact, action puis vérification puis décision,
et comment ça s'arrête. OUTILS & PÉRIMÈTRE liste ce qui est autorisé et ce
qui est interdit, en dur, pas juste à l'oral. GARDE-FOUS, c'est ce qui doit
arriver toujours, ce que je demande plutôt que deviner, ce que je
m'interdis. REVIEW CONTEXTE FRAIS explique comment je garantis que le
jugement n'est pas pollué par la session qui a produit le travail. TRACE,
enfin, c'est ce que l'agent restitue à la fin, pour que quelqu'un d'autre
puisse vérifier après coup.

Exemple concret, mon agent `arbitre` (le juge à froid). Son rôle : rendre
un verdict binaire PASS/NEEDS_WORK, rien d'autre, pas de correction, pas de
suggestion de code. Sa mémoire : rien ne persiste entre deux invocations,
l'entrée doit contenir explicitement le diff, les critères d'acceptation et
les preuves. Son garde-fou principal : preuve absente ou non concluante,
c'est `NEEDS_WORK` automatique, jamais de bénéfice du doute.

## 5. Les deux garanties transversales

### Contexte frais
Celui qui juge n'a jamais vu le code s'écrire.

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

Ce n'est pas une option que j'active de temps en temps, c'est structurel.
L'agent juge est invoqué comme un sous-agent à part, sans accès à
l'historique de la conversation qui a produit le travail.

### Défaut = échec
Une affirmation du genre "j'ai testé, ça marche" sans preuve citée, ce
n'est pas une preuve, je l'ignore. Si le périmètre donné est trop
incomplet pour évaluer quoi que ce soit, le verdict par défaut est
`NEEDS_WORK`, jamais `PASS` par optimisme. Cette règle, je ne l'ai trouvée
dans aucune des sources publiques que j'ai consultées sur la conception
d'agents. C'est la partie que j'ai dû inventer moi-même.

### Sortie courte par défaut
Une réponse d'agent ne se facture pas comme une réponse humaine, chaque mot
de sortie a un coût réel en tokens. Par défaut, un agent restitue le strict
nécessaire : un statut, un verdict, une liste de findings fichier + ligne +
une phrase. Jamais un pavé de justification ou de contexte redondant avec
ce que je peux déjà voir. Le détail (raisonnement complet, alternatives
explorées) reste disponible si je le redemande, il n'est pas donné par
défaut. J'avais exploré une piste dans le sourcing, un agent "Caveman" en
mode compression de sortie. Le style entièrement télégraphique, je l'ai
écarté, illisible à la relecture. Mais le principe, sortie courte par
défaut plutôt que verbeuse, je le garde comme garantie transversale, au
même titre que le contexte frais et le défaut-échec.

## 6. TOUJOURS / DEMANDER / JAMAIS

Le format de garde-fous le plus robuste que j'ai trouvé dans la recherche
externe (analyse de plus de 2500 fichiers de configuration d'agents
publics), c'est une règle en trois tiers plutôt qu'une liste plate
d'interdits : TOUJOURS pour ce qui doit arriver systématiquement, DEMANDER
pour les cas où l'agent doit s'arrêter et me demander plutôt que de choisir
à ma place, JAMAIS pour les lignes rouges absolues.

Exemple réel avec `elrond`, mon orchestrateur qui détecte le stack d'un
diff et route vers le bon reviewer. En cas d'ambiguïté de stack (monorepo,
signatures contradictoires), la règle n'est pas "fais de ton mieux" mais
explicitement DEMANDER. Jamais deviner, quitte à interrompre le flux.

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

Je n'adopte rien parce que c'est dans un repo populaire. Chaque ligne du
`CATALOG.md` porte une décision explicite de ma part, adoptée ou écartée,
avec sa raison notée. Une bonne partie du backlog, je l'écarte
volontairement, et c'est justement ce qui prouve que le tri est réel, pas
un simple empilement.

## 8. Statut réel, honnêteté sur la maturité

Pas de survente ici. Certains de mes agents ont un vécu de production réel,
d'autres sont écrits mais pas encore confrontés à un vrai projet. Le
tableau est tenu à jour dans `CATALOG.md`, la colonne maturité (✅ / 🟡 /
🔜) est la source de vérité, pas ce document.

## 9. Loop possible, mais pas sur tout

Mon pipeline peut tourner en boucle sans supervision jusqu'au gate :
brainstorm → spec → archi → plan → code → debug peuvent s'enchaîner sans
qu'un humain valide chaque étape. Deux points restent quand même des arrêts
humains volontaires, non négociables : le gate (`arbitre`) rend un
verdict mais ne merge rien, et le merge lui-même demande toujours 2
approbations humaines.

Ce n'est pas une limitation technique de ma part. L'autonomie bout-en-bout
façon des frameworks d'autonomie agentique totale du marché, je l'ai
explicitement écartée comme repoussoir dans le sourcing (`CATALOG.md`) : un
agent qui merge du code tout seul sans validation, c'est exactement le
contre-exemple que je ne veux pas devenir. La boucle accélère la
production, jamais la décision de merger.

## 10. La vision — que le système apprenne, pas juste qu'il tourne

Mon objectif, ce n'est pas d'avoir un set d'agents figé. C'est un système
qui devient plus intelligent avec l'usage, sans jamais toucher aux règles
fixes (contexte frais, défaut=échec). Ce qui s'améliore, c'est la
connaissance métier accumulée, pas la doctrine. J'ai déjà trois boucles de
retour en place, même si partiellement.

La calibration d'abord : chaque review réelle, findings retenus ou faux
positifs infirmés, est journalisée, pour que le tri futur reconnaisse plus
vite ce qui vaut la peine d'être remonté. Ensuite la mémoire persistante :
mes corrections et confirmations sur une approche deviennent des règles
durables, relues avant d'agir à nouveau, pas ré-expliquées à chaque fois.
Et `extract-conventions`, qui génère des conventions depuis le code réel
existant plutôt que depuis une doctrine abstraite, donc ça se met à jour
avec le code lui-même.

Ce qui me manque encore pour que ce soit systématique et pas juste au fil
de l'eau : une revue périodique qui relit ces trois sources et met à jour
`CATALOG.md` (maturité, garde-fous affinés). Pas encore automatisée, à
poser comme prochaine étape.

## 11. Pourquoi ça compte

La review ne complaît pas, parce que le reviewer n'est jamais celui qui a
écrit le code, dans une session séparée à froid. Rien n'est cru sur
parole, "c'est fini" n'est jamais suffisant, une preuve concrète l'est. Ça
s'enrichit sans dépendre : le marché évolue, je pioche dedans, mais rien
ne peut casser mon pipeline en changeant de l'extérieur. Et c'est adapté à
ma réalité, pas à une fiction de compétence uniforme : un agent formule
ses remarques en questions honnêtes sur un stack que je ne maîtrise pas
encore (PHP/Laravel), et en affirmations tranchées sur un stack où j'ai une
vraie expertise (JS/TS). Le style suit ma réalité, pas un ton générique.
