---
name: accessibility
description: Use quand on code ou revoit une page/app front (Nuxt/React), checklist accessibilité technique : sémantique HTML, focus/clavier, contraste, ARIA, formulaires. Pas de vécu de production Xefi dédié a11y à ce stade, sourcé sur les WCAG 2.2 (niveau AA) et les guidelines établies (MDN, W3C).
---

# accessibility

Étape 6 du pipeline (`WORKFLOW.md`), en complément de `vue-nuxt-vuetify-conventions`/
`react-nextjs-conventions` : s'applique à toute page/composant destiné à des
utilisateurs réels (pas aux scripts internes, outillage dev-only).

## Quand
Dès qu'on écrit ou modifie un composant/page front, pendant `code` (6) ou en
review (`review`, 8) si le diff touche de l'UI.

## Étapes

### 1. Sémantique et navigation clavier : la base non négociable
1. Tout élément interactif (`button`, `a`, `input`) est une vraie balise
   native, jamais un `div`/`span` avec `onClick` simulant un bouton : sinon
   perdu au clavier et pour les lecteurs d'écran.
2. Ordre de tabulation (`tab`) suit l'ordre visuel logique : jamais de
   `tabindex` positif qui casse l'ordre naturel du DOM ; `tabindex="-1"`
   seulement pour retirer un élément du flux volontairement.
3. Focus visible (`:focus-visible`) jamais supprimé par un `outline: none`
   sans remplacement : un utilisateur clavier doit toujours voir où il est.
4. Piège à focus (modale, dropdown) : le focus reste dans le composant ouvert
   tant qu'il est actif, et revient à l'élément déclencheur à la fermeture.
5. Raccourcis clavier standards respectés : `Échap` ferme une modale/dropdown,
   `Entrée`/`Espace` active un bouton focus.

### 2. ARIA : seulement quand le HTML natif ne suffit pas
1. Règle d'or : pas d'ARIA plutôt qu'un ARIA faux, un `role` ou `aria-*`
   incorrect est pire que son absence (contrat trahi pour les technologies
   d'assistance).
2. `aria-label`/`aria-labelledby` sur tout élément interactif sans texte
   visible (icône seule, bouton fermer) : jamais un bouton muet pour un
   lecteur d'écran.
3. `aria-live` (`polite`/`assertive`) sur les zones de contenu dynamique qui
   doivent être annoncées (notification, erreur de formulaire apparue après
   soumission) : sinon changement invisible pour qui n'utilise pas les yeux.
4. `aria-expanded`/`aria-selected`/`aria-current` posés sur les composants
   qui en ont l'équivalent visuel (accordéon, onglet, item actif) : l'état
   visuel doit avoir un équivalent exposé.

### 3. Contraste et perception visuelle
1. Contraste texte/fond ≥ 4.5:1 (texte normal) ou 3:1 (texte large ≥ 18px
   gras/24px) : niveau WCAG AA, vérifié sur les couleurs réelles du design
   system, pas approximé à l'œil.
2. L'information n'est jamais portée uniquement par la couleur (ex. rouge =
   erreur) : toujours doublée d'un texte, icône ou motif.
3. Contenu redimensionnable jusqu'à 200% (zoom navigateur) sans perte de
   contenu ni de fonctionnalité : pas de largeur figée en `px` qui casse au
   zoom.

### 4. Formulaires : le point le plus souvent cassé
1. Chaque champ a un `<label>` associé (`for`/`id` ou wrapping), jamais un
   placeholder seul en guise de label : le placeholder disparaît à la saisie.
2. Message d'erreur associé au champ via `aria-describedby`, annoncé au
   moment où il apparaît (pas seulement affiché visuellement).
3. Champs requis marqués via `required`/`aria-required`, pas seulement par un
   astérisque visuel sans équivalent exposé.

## Sortie / checkpoint
Les quatre sections passées en revue sur le diff touché ; pour un audit plus
large d'une page/site déjà en prod (pas seulement le diff en cours), voir
l'agent `accessibility-auditor`.

## Garde-fous
- Ne pas confondre conformité WCAG et expérience réelle : un audit outillé
  (axe-core, Lighthouse) ne remplace pas un test clavier/lecteur d'écran
  manuel sur les parcours critiques.
- Pas d'ARIA ajouté par réflexe "pour faire propre" : seulement quand le HTML
  natif ne suffit pas (voir règle d'or section 2).
- Cette brique n'a pas encore de vécu de production Xefi dédié : à confronter
  au premier vrai audit a11y réel, pas à traiter comme doctrine éprouvée.

## Origine
Sourcé sur WCAG 2.2 (niveau AA, critères de succès repris), MDN
(sémantique HTML, ARIA authoring practices), W3C ARIA APG (patterns
modale/accordéon/onglet). Mécanismes réécrits en checklist actionnable, pas de
texte copié. Recherche de marché, pas de retour de production interne à ce
stade : même statut que `seo`.
